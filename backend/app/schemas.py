from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    therapeutic_class: Optional[str] = None
    indications: Optional[str] = None
    contraindications: Optional[str] = None
    key_benefits: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int

    class Config:
        from_attributes = True


class HCPBase(BaseModel):
    name: str
    specialty: str
    hospital: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    preferred_channel: Optional[str] = None
    next_best_action: Optional[str] = None
    notes: Optional[str] = None

class HCPCreate(HCPBase):
    pass

class HCPSchema(HCPBase):
    id: int

    class Config:
        from_attributes = True


class ComplianceFlagBase(BaseModel):
    flagged_text: str
    rule_matched: str
    severity: str
    description: str

class ComplianceFlagCreate(ComplianceFlagBase):
    pass

class ComplianceFlagSchema(ComplianceFlagBase):
    id: int
    interaction_id: int

    class Config:
        from_attributes = True


class FollowUpBase(BaseModel):
    hcp_id: int
    interaction_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: str = "Pending"
    recommended_email: Optional[str] = None

class FollowUpCreate(FollowUpBase):
    pass

class FollowUpUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    recommended_email: Optional[str] = None

class FollowUpSchema(FollowUpBase):
    id: int

    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    hcp_id: int
    rep_id: str = "REP-001"
    date: str
    channel: str
    summary: Optional[str] = None
    transcript: Optional[str] = None
    discussion_topics: Optional[str] = None
    follow_up_date: Optional[str] = None
    compliance_status: Optional[str] = "Compliant"
    compliance_notes: Optional[str] = None
    sentiment: Optional[str] = "Neutral"
    next_steps: Optional[str] = None

class InteractionCreate(InteractionBase):
    pass

class InteractionUpdate(BaseModel):
    date: Optional[str] = None
    channel: Optional[str] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None
    discussion_topics: Optional[str] = None
    follow_up_date: Optional[str] = None
    compliance_status: Optional[str] = None
    compliance_notes: Optional[str] = None
    sentiment: Optional[str] = None
    next_steps: Optional[str] = None

class InteractionSchema(InteractionBase):
    id: int
    compliance_flags: List[ComplianceFlagSchema] = []
    follow_ups: List[FollowUpSchema] = []

    class Config:
        from_attributes = True


# Chat Interface schemas
class ChatMessage(BaseModel):
    role: str  # user, assistant, system, tool
    content: str
    id: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    hcp_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    extracted_state: Optional[dict] = None  # Live-sync extracted parameters for UI
    compliance_check: Optional[dict] = None
    recommendations: Optional[List[dict]] = None
