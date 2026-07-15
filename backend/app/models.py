from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)
    hospital = Column(String(200))
    email = Column(String(100))
    phone = Column(String(20))
    preferred_channel = Column(String(50))
    next_best_action = Column(String(500))
    notes = Column(Text)

    interactions = relationship("Interaction", back_populates="hcp", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="hcp", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    therapeutic_class = Column(String(100))
    indications = Column(Text)
    contraindications = Column(Text)
    key_benefits = Column(Text)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id", ondelete="CASCADE"), nullable=False)
    rep_id = Column(String(50), default="REP-001")
    date = Column(String(50), nullable=False)  # Stored as YYYY-MM-DD
    channel = Column(String(50))  # In-Person, Video, Email, Phone
    summary = Column(Text)
    transcript = Column(Text)
    discussion_topics = Column(Text)  # JSON-encoded array or comma-separated list of topics/products
    follow_up_date = Column(String(50))
    compliance_status = Column(String(50))  # Compliant, Non-Compliant, Flagged
    compliance_notes = Column(Text)
    sentiment = Column(String(50))  # Positive, Neutral, Negative
    next_steps = Column(Text)

    hcp = relationship("HCP", back_populates="interactions")
    compliance_flags = relationship("ComplianceFlag", back_populates="interaction", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="interaction")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id", ondelete="SET NULL"), nullable=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    due_date = Column(String(50))
    status = Column(String(50), default="Pending")  # Pending, Completed, Cancelled
    recommended_email = Column(Text)

    hcp = relationship("HCP", back_populates="follow_ups")
    interaction = relationship("Interaction", back_populates="follow_ups")


class ComplianceFlag(Base):
    __tablename__ = "compliance_flags"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id", ondelete="CASCADE"), nullable=False)
    flagged_text = Column(Text)
    rule_matched = Column(String(200))
    severity = Column(String(50))  # High, Medium, Low
    description = Column(Text)

    interaction = relationship("Interaction", back_populates="compliance_flags")
