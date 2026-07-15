import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")

# Automatically create the MySQL database if it doesn't exist yet
if DATABASE_URL.startswith("mysql"):
    try:
        import pymysql
        # Clean URL schema for urlparse (e.g. mysql+pymysql -> mysql)
        clean_url = DATABASE_URL
        if "mysql+pymysql://" in DATABASE_URL:
            clean_url = DATABASE_URL.replace("mysql+pymysql://", "mysql://")
            
        parsed = urlparse(clean_url)
        db_name = parsed.path.lstrip("/")
        
        # Decode URL-encoded characters in username and password
        user = unquote(parsed.username) if parsed.username else "root"
        password = unquote(parsed.password) if parsed.password else ""
        
        # Connect to MySQL server without database context
        connection = pymysql.connect(
            host=parsed.hostname or "127.0.0.1",
            port=parsed.port or 3306,
            user=user,
            password=password,
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            connection.commit()
            print(f"[Database] Checked/Created MySQL database '{db_name}' successfully.")
        finally:
            connection.close()
    except Exception as e:
        print(f"[Database Warning] Failed to pre-create MySQL database: {e}")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
