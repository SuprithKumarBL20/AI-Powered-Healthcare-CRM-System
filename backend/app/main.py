from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import os
import json

from .database import get_db, engine, Base
from .models import HCP, Interaction, Product, FollowUp, ComplianceFlag
from .schemas import (
    HCPSchema, ProductSchema, InteractionSchema, InteractionCreate,
    InteractionUpdate, FollowUpSchema, FollowUpUpdate, ChatRequest, ChatResponse, ChatMessage
)
from .agent.graph import app_graph
from .agent.tools import analyze_compliance
from .seed import seed_db

# Initialize database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP API", version="1.0.0")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Pre-seed if HCP table is empty
    db = next(get_db())
    try:
        if db.query(HCP).count() == 0:
            print("Database is empty. Seeding initial data...")
            seed_db()
    finally:
        db.close()

@app.post("/api/init-db")
def reseed_database():
    try:
        seed_db()
        return {"status": "Success", "message": "Database reseeded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed database: {str(e)}")

# --- HCP ENDPOINTS ---
@app.get("/api/hcps", response_model=List[HCPSchema])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).all()

@app.get("/api/hcps/{hcp_id}", response_model=HCPSchema)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp

# --- PRODUCT ENDPOINTS ---
@app.get("/api/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# --- INTERACTION ENDPOINTS ---
@app.get("/api/interactions", response_model=List[InteractionSchema])
def get_interactions(db: Session = Depends(get_db)):
    # Order by date descending, then id descending
    return db.query(Interaction).order_by(Interaction.date.desc(), Interaction.id.desc()).all()

@app.post("/api/interactions", response_model=InteractionSchema)
def create_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == data.hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
        
    # Check compliance using analyze_compliance helper
    topics = [t.strip() for t in data.discussion_topics.split(",") if t.strip()] if data.discussion_topics else []
    comp_result_str = analyze_compliance.invoke({
        "transcript": data.transcript or "",
        "discussion_topics": topics
    })
    comp_result = json.loads(comp_result_str)
    
    compliance_status = comp_result.get("compliance_status", "Compliant")
    compliance_notes = comp_result.get("recommendation", "")
    
    interaction = Interaction(
        hcp_id=data.hcp_id,
        rep_id=data.rep_id,
        date=data.date,
        channel=data.channel,
        transcript=data.transcript,
        summary=data.summary or f"Discussion with {hcp.name} on {data.discussion_topics}",
        discussion_topics=data.discussion_topics,
        follow_up_date=data.follow_up_date,
        compliance_status=compliance_status,
        compliance_notes=compliance_notes,
        sentiment=data.sentiment,
        next_steps=data.next_steps
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    
    # Save compliance flags in DB if non-compliant
    for flag_data in comp_result.get("flags", []):
        flag = ComplianceFlag(
            interaction_id=interaction.id,
            flagged_text=flag_data.get("flagged_text"),
            rule_matched=flag_data.get("rule"),
            severity=flag_data.get("severity"),
            description=flag_data.get("description")
        )
        db.add(flag)
    db.commit()
    db.refresh(interaction)

    # Automatically create a pending follow-up task if follow_up_date is provided
    if data.follow_up_date:
        follow_up = FollowUp(
            hcp_id=data.hcp_id,
            interaction_id=interaction.id,
            title=f"Follow-up: {data.discussion_topics or 'General'}",
            description=f"Action item: {data.next_steps or 'Send resources discussed'}",
            due_date=data.follow_up_date,
            status="Pending",
            recommended_email=f"Dear {hcp.name},\n\nThank you for our meeting on {data.date}. As discussed, I am following up on {data.discussion_topics}.\n\nBest regards,\nSales Representative"
        )
        db.add(follow_up)
        db.commit()
        
    return interaction

@app.put("/api/interactions/{int_id}", response_model=InteractionSchema)
def update_interaction(int_id: int, updates: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == int_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
        
    # Apply updates
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interaction, key, value)
        
    # Re-evaluate compliance if transcript or topics changed
    if "transcript" in update_data or "discussion_topics" in update_data:
        topics = [t.strip() for t in interaction.discussion_topics.split(",") if t.strip()] if interaction.discussion_topics else []
        comp_result_str = analyze_compliance.invoke({
            "transcript": interaction.transcript or "",
            "discussion_topics": topics
        })
        comp_result = json.loads(comp_result_str)
        
        interaction.compliance_status = comp_result.get("compliance_status", "Compliant")
        interaction.compliance_notes = comp_result.get("recommendation", "")
        
        # Clear old flags
        db.query(ComplianceFlag).filter(ComplianceFlag.interaction_id == interaction.id).delete()
        
        # Write new flags
        for flag_data in comp_result.get("flags", []):
            flag = ComplianceFlag(
                interaction_id=interaction.id,
                flagged_text=flag_data.get("flagged_text"),
                rule_matched=flag_data.get("rule"),
                severity=flag_data.get("severity"),
                description=flag_data.get("description")
            )
            db.add(flag)
            
    db.commit()
    db.refresh(interaction)
    return interaction

@app.delete("/api/interactions/{int_id}")
def delete_interaction(int_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == int_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    db.delete(interaction)
    db.commit()
    return {"status": "Success", "message": f"Interaction {int_id} deleted."}

# --- FOLLOW-UP ENDPOINTS ---
@app.get("/api/follow-ups", response_model=List[FollowUpSchema])
def get_follow_ups(db: Session = Depends(get_db)):
    return db.query(FollowUp).all()

@app.put("/api/follow-ups/{f_id}", response_model=FollowUpSchema)
def update_follow_up(f_id: int, updates: FollowUpUpdate, db: Session = Depends(get_db)):
    follow_up = db.query(FollowUp).filter(FollowUp.id == f_id).first()
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow up not found")
    
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(follow_up, key, value)
        
    db.commit()
    db.refresh(follow_up)
    return follow_up

# --- CHAT & AGENT ENDPOINTS ---
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    # Convert incoming ChatMessage to LangChain format
    langchain_messages = []
    
    # Prepend a system message to guide the CRM Agent
    system_prompt = (
        "You are an AI-First CRM assistant helping a life sciences field representative "
        "log and manage interactions with Healthcare Professionals (HCPs).\n"
        "You have access to 5 specific tools to help manage CRM activities:\n"
        "1. get_hcp_profile: Use this to fetch HCP info, history, and preferences.\n"
        "2. log_interaction: Use this when the user requests to log a completed meeting or interaction.\n"
        "3. edit_interaction: Use this to update a specific logged interaction by ID.\n"
        "4. analyze_compliance: Use this to check meeting transcripts or drafts for PhRMA guideline violations.\n"
        "5. generate_follow_up: Use this to create follow-up tasks and write draft follow-up emails.\n\n"
        "When the user describes an interaction in chat, you should extract details and call `log_interaction` "
        "or help them verify compliance. If they request profiles or changes, invoke the correct tools."
    )
    langchain_messages.append(SystemMessage(content=system_prompt))
    
    for msg in request.messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            langchain_messages.append(AIMessage(content=msg.content))
            
    # Initial state
    state = {
        "messages": langchain_messages,
        "hcp_id": request.hcp_id,
        "extracted_state": {},
        "compliance_check": {},
        "recommendations": []
    }
    
    try:
        # Run the LangGraph
        result = app_graph.invoke(state)
        
        # Get last message content
        response_msg = result["messages"][-1].content
        
        return ChatResponse(
            response=response_msg,
            extracted_state=result.get("extracted_state"),
            compliance_check=result.get("compliance_check"),
            recommendations=result.get("recommendations")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent graph: {str(e)}")
