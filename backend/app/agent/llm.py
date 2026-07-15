import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm() -> BaseChatModel:
    groq_api_key = os.getenv("GROQ_API_KEY")
    print(groq_api_key)
    if not groq_api_key or groq_api_key == "YOUR_GROQ_API_KEY_HERE":
        print("[WARNING] GROQ_API_KEY not found. Using high-fidelity Mock LLM for demo purposes.")
        return MockCRMLLM()
    
    try:
        # Use llama-3.3-70b-versatile since gemma2-9b-it is decommissioned by Groq
        return ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=groq_api_key,
            temperature=0.1
        )
    except Exception as e:
        print(f"[ERROR] Failed to initialize ChatGroq: {e}. Falling back to Mock LLM.")
        return MockCRMLLM()

# High-fidelity mock LLM that can parse sentences, recommend compliance issues, and act as a tool caller
from typing import List, Optional, Union, Any, Dict
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
import json
import re

class MockCRMLLM(BaseChatModel):
    def bind_tools(self, tools: List[Any], **kwargs: Any) -> 'MockCRMLLM':
        return self

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Simple heuristic response generation based on message keywords
        # to simulate LangGraph tool calls and conversational responses.
        
        # 1. Gather conversation context
        user_msg = ""
        for m in reversed(messages):
            if m.type == "user":
                user_msg = m.content
                break
                
        hcp_id_context = 1  # default to Jenkins
        
        # Look for references to Dr. Chen or Dr. Vance or Dr. Jenkins
        if "chen" in user_msg.lower():
            hcp_id_context = 2
        elif "vance" in user_msg.lower():
            hcp_id_context = 3
        elif "jenkins" in user_msg.lower() or "sarah" in user_msg.lower():
            hcp_id_context = 1

        response_content = ""
        tool_calls = []

        # Analyze keywords in user message to determine tool calls
        lower_msg = user_msg.lower()
        
        # --- TOOL CALL SIMULATIONS ---
        # A. Log interaction
        if "log" in lower_msg and ("interaction" in lower_msg or "meeting" in lower_msg or "call" in lower_msg or "discussed" in lower_msg):
            # Parse possible fields from natural language
            channel = "In-Person"
            if "video" in lower_msg or "zoom" in lower_msg or "teams" in lower_msg:
                channel = "Video Call"
            elif "email" in lower_msg:
                channel = "Email"
            elif "phone" in lower_msg or "call" in lower_msg:
                channel = "Phone"
                
            # Date
            date = "2026-07-13" # Today
            if "yesterday" in lower_msg:
                date = "2026-07-12"
            
            # Sentiment
            sentiment = "Positive"
            if "angry" in lower_msg or "upset" in lower_msg or "refused" in lower_msg:
                sentiment = "Negative"
            elif "hesitant" in lower_msg or "busy" in lower_msg:
                sentiment = "Neutral"

            # Topics and Products
            topics = ["General Discussion"]
            if "zyntra" in lower_msg:
                topics = ["Zyntra", "Diabetes", "Efficacy"]
            elif "cardioguard" in lower_msg:
                topics = ["CardioGuard", "Hypertension", "Safety"]
            elif "oncoshield" in lower_msg:
                topics = ["OncoShield", "Oncology", "Indication"]

            # Summarization
            summary = f"Discussion with HCP regarding pharmaceutical products. Discussed: {', '.join(topics)}."
            if "zyntra" in lower_msg:
                summary = "Logged meeting regarding Zyntra efficacy. HCP showed positive interest in cardiovascular clinical data."
            elif "cardioguard" in lower_msg:
                summary = "Virtual meeting about CardioGuard side effects. Discussed potential drug-drug interactions and dosage."
            
            # Compliance Check simulation within Log Interaction
            compliance_status = "Compliant"
            compliance_notes = "Checked for compliance: Compliant with PhRMA guidelines. No off-label claims or inducements identified."
            
            if "gift" in lower_msg or "tickets" in lower_msg or "hawaii" in lower_msg or "lunch" in lower_msg or "dinner" in lower_msg or "pay for" in lower_msg:
                compliance_status = "Non-Compliant"
                compliance_notes = "WARNING: PhRMA code violation detected. Offering individual meals, travel, or gifts to HCPs is strictly prohibited."
            
            # Mocking Tool call for logging
            tool_calls.append({
                "name": "log_interaction",
                "args": {
                    "hcp_id": hcp_id_context,
                    "date": date,
                    "channel": channel,
                    "transcript": user_msg,
                    "summary": summary,
                    "discussion_topics": ", ".join(topics),
                    "follow_up_date": "2026-07-20",
                    "compliance_status": compliance_status,
                    "compliance_notes": compliance_notes,
                    "sentiment": sentiment,
                    "next_steps": "Send follow-up resources as requested."
                },
                "id": "call_log_1"
            })
            
            response_content = "I will proceed to log this interaction details. Let me check compliance first..."

        # B. Compliance check
        elif "comply" in lower_msg or "compliance" in lower_msg or "check" in lower_msg and ("gift" in lower_msg or "hawaii" in lower_msg or "pay" in lower_msg or "off-label" in lower_msg):
            tool_calls.append({
                "name": "analyze_compliance",
                "args": {
                    "transcript": user_msg,
                    "discussion_topics": ["Compliance Review"]
                },
                "id": "call_comp_1"
            })
            response_content = "Let me run a compliance check on this conversation content."

        # C. Get HCP Profile
        elif "profile" in lower_msg or "hcp" in lower_msg or "doctor" in lower_msg or "details" in lower_msg:
            tool_calls.append({
                "name": "get_hcp_profile",
                "args": {
                    "hcp_id": hcp_id_context
                },
                "id": "call_profile_1"
            })
            response_content = "Retrieving the profile and history for the requested HCP."

        # D. Generate follow-up
        elif "follow up" in lower_msg or "email" in lower_msg or "task" in lower_msg:
            tool_calls.append({
                "name": "generate_follow_up",
                "args": {
                    "hcp_id": hcp_id_context,
                    "notes": user_msg
                },
                "id": "call_follow_1"
            })
            response_content = "Creating follow-up tasks and generating a draft email template."

        # E. Edit interaction
        elif "edit" in lower_msg or "update" in lower_msg or "change" in lower_msg:
            # Try to parse interaction ID
            int_id = 1
            match = re.search(r'interaction\s*(\d+)', lower_msg)
            if match:
                int_id = int(match.group(1))
            
            tool_calls.append({
                "name": "edit_interaction",
                "args": {
                    "interaction_id": int_id,
                    "updates": {"summary": "Updated interaction summary via AI agent voice instructions."}
                },
                "id": "call_edit_1"
            })
            response_content = f"Updating the interaction record ID {int_id} as requested."

        # Conversational Response if no tool matches
        else:
            if hcp_id_context == 1:
                hcp_name = "Dr. Sarah Jenkins"
            elif hcp_id_context == 2:
                hcp_name = "Dr. Robert Chen"
            else:
                hcp_name = "Dr. Elizabeth Vance"
                
            response_content = (
                f"Hello! I am your AI CRM Assistant. I am focused on assisting you with **{hcp_name}**.\n\n"
                "I can help you with:\n"
                "1. **Logging Interactions**: 'Log an in-person meeting with Dr. Jenkins today discussing Zyntra.'\n"
                "2. **HCP Profile Queries**: 'Show profile for Dr. Chen.'\n"
                "3. **Compliance Checking**: 'Is it compliant if we pay for a doctor's lunch?'\n"
                "4. **Follow-ups & Emails**: 'Generate follow up email for Dr. Vance.'\n"
                "5. **Updating Entries**: 'Update interaction 2 summary.'"
            )

        ai_msg = AIMessage(content=response_content)
        if tool_calls:
            ai_msg.additional_kwargs = {"tool_calls": tool_calls}
            
        generation = ChatGeneration(message=ai_msg)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock_crm_llm"
