from langchain_core.tools import tool
from typing import List, Dict, Any, Optional
import json
from ..database import SessionLocal
from ..models import HCP, Interaction, Product, FollowUp, ComplianceFlag

@tool
def get_hcp_profile(hcp_id: Any) -> str:
    """Retrieve HCP profile details, including specialty, clinic, next best action, and historical interactions."""
    db = SessionLocal()
    try:
        try:
            hcp_id = int(hcp_id)
        except (ValueError, TypeError):
            return f"Error: Invalid HCP ID format: {hcp_id}."
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return f"Error: HCP with ID {hcp_id} not found."
        
        # Fetch historical interactions
        interactions = db.query(Interaction).filter(Interaction.hcp_id == hcp_id).order_by(Interaction.date.desc()).all()
        past_interactions_data = []
        for i in interactions:
            past_interactions_data.append({
                "id": i.id,
                "date": i.date,
                "channel": i.channel,
                "summary": i.summary,
                "compliance_status": i.compliance_status
            })
            
        profile = {
            "id": hcp.id,
            "name": hcp.name,
            "specialty": hcp.specialty,
            "hospital": hcp.hospital,
            "preferred_channel": hcp.preferred_channel,
            "next_best_action": hcp.next_best_action,
            "notes": hcp.notes,
            "past_interactions": past_interactions_data
        }
        return json.dumps(profile, indent=2)
    except Exception as e:
        return f"Error retrieving HCP profile: {str(e)}"
    finally:
        db.close()


@tool
def log_interaction(
    hcp_id: Any,
    date: str,
    channel: str,
    transcript: str,
    summary: str,
    discussion_topics: str,
    follow_up_date: Optional[str] = None,
    compliance_status: Optional[str] = "Compliant",
    compliance_notes: Optional[str] = None,
    sentiment: Optional[str] = "Neutral",
    next_steps: Optional[str] = None
) -> str:
    """Log a new interaction with an HCP, summarizing details and conducting automated compliance checking."""
    db = SessionLocal()
    try:
        try:
            hcp_id = int(hcp_id)
        except (ValueError, TypeError):
            return f"Error: Invalid HCP ID format: {hcp_id}."
        # Verify HCP exists
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return f"Error: HCP with ID {hcp_id} not found."
            
        # Create interaction
        interaction = Interaction(
            hcp_id=hcp_id,
            rep_id="REP-001",
            date=date,
            channel=channel,
            transcript=transcript,
            summary=summary,
            discussion_topics=discussion_topics,
            follow_up_date=follow_up_date,
            compliance_status=compliance_status,
            compliance_notes=compliance_notes,
            sentiment=sentiment,
            next_steps=next_steps
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        
        # Look for compliance violations and create flags if applicable
        # We perform keyword-based analysis
        text_to_check = (transcript or "") + " " + (summary or "")
        text_lower = text_to_check.lower()
        
        violations = []
        if "hawaii" in text_lower or "travel" in text_lower or "flight" in text_lower or "lodging" in text_lower:
            violations.append(ComplianceFlag(
                interaction_id=interaction.id,
                flagged_text=transcript,
                rule_matched="PhRMA Code - Non-educational items / Individual Entertainment & Travel",
                severity="High",
                description="Offering travel sponsorship or recreational event coverage (e.g., Hawaii trips) is strictly forbidden under the PhRMA guidelines."
            ))
            compliance_status = "Non-Compliant"
            compliance_notes = "WARNING: PhRMA violation flagged regarding travel/entertainment sponsorships."
            
        if "gift" in text_lower or "cash" in text_lower or "check" in text_lower:
            violations.append(ComplianceFlag(
                interaction_id=interaction.id,
                flagged_text=transcript,
                rule_matched="PhRMA Code - Prohibition of Cash and Non-Educational Gifts",
                severity="High",
                description="Offering personal gifts, cash, or items of value (recreational items) to HCPs violates the PhRMA Code."
            ))
            compliance_status = "Non-Compliant"
            compliance_notes = "WARNING: Compliance flag regarding gifts/financial incentives."

        if "weight loss" in text_lower or "obesity" in text_lower:
            # If discussing Zyntra (which is Endocrinology/Diabetes) for weight loss (which might be off-label)
            if "zyntra" in text_lower:
                violations.append(ComplianceFlag(
                    interaction_id=interaction.id,
                    flagged_text=transcript,
                    rule_matched="PhRMA Code - Off-Label Promotion",
                    severity="Medium",
                    description="Zyntra is FDA approved solely for Type 2 Diabetes glycemic control. Suggesting or discussing Zyntra for weight loss or obesity management constitutes off-label promotion."
                ))
                compliance_status = "Flagged"
                compliance_notes = "Warning: Contains discussion of Zyntra for off-label indications (obesity/weight loss)."

        if violations:
            for flag in violations:
                db.add(flag)
            interaction.compliance_status = compliance_status
            interaction.compliance_notes = compliance_notes
            db.commit()
            db.refresh(interaction)

        # Create auto follow-up task if follow_up_date is set
        if follow_up_date:
            follow_up = FollowUp(
                hcp_id=hcp_id,
                interaction_id=interaction.id,
                title=f"Follow-up: {discussion_topics}",
                description=f"Action item: {next_steps or 'Contact doctor regarding discussed topics'}",
                due_date=follow_up_date,
                status="Pending",
                recommended_email=f"Dear {hcp.name},\n\nThank you for taking the time to speak with me on {date}. As discussed, I am following up on {discussion_topics}. Please find the clinical details attached.\n\nBest regards,\nMedical Representative"
            )
            db.add(follow_up)
            db.commit()

        # Update HCP next best action
        if next_steps:
            hcp.next_best_action = next_steps
            db.commit()

        return json.dumps({
            "status": "Success",
            "message": f"Interaction logged successfully with ID {interaction.id}.",
            "interaction_id": interaction.id,
            "compliance_status": interaction.compliance_status,
            "compliance_notes": interaction.compliance_notes
        }, indent=2)
        
    except Exception as e:
        db.rollback()
        return f"Error logging interaction: {str(e)}"
    finally:
        db.close()


@tool
def edit_interaction(interaction_id: Any, updates: Dict[str, Any]) -> str:
    """Modify details of a logged interaction (such as summary, follow-up, topics, next steps)."""
    db = SessionLocal()
    try:
        try:
            interaction_id = int(interaction_id)
        except (ValueError, TypeError):
            return f"Error: Invalid Interaction ID format: {interaction_id}."
        interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        if not interaction:
            return f"Error: Interaction with ID {interaction_id} not found."
            
        # Apply updates
        for key, value in updates.items():
            if hasattr(interaction, key):
                setattr(interaction, key, value)
        
        # Recheck compliance if transcript or summary was updated
        if "transcript" in updates or "summary" in updates:
            text_to_check = (interaction.transcript or "") + " " + (interaction.summary or "")
            text_lower = text_to_check.lower()
            
            # Clear old compliance flags
            db.query(ComplianceFlag).filter(ComplianceFlag.interaction_id == interaction.id).delete()
            
            violations = []
            compliance_status = "Compliant"
            compliance_notes = "Checked for compliance: Compliant with PhRMA guidelines."
            
            if "hawaii" in text_lower or "travel" in text_lower or "flight" in text_lower or "lodging" in text_lower:
                violations.append(ComplianceFlag(
                    interaction_id=interaction.id,
                    flagged_text=interaction.transcript,
                    rule_matched="PhRMA Code - Non-educational items / Individual Entertainment & Travel",
                    severity="High",
                    description="Offering travel sponsorship or recreational event coverage is forbidden."
                ))
                compliance_status = "Non-Compliant"
                compliance_notes = "WARNING: PhRMA violation flagged regarding travel/entertainment sponsorships."
                
            if "gift" in text_lower or "cash" in text_lower:
                violations.append(ComplianceFlag(
                    interaction_id=interaction.id,
                    flagged_text=interaction.transcript,
                    rule_matched="PhRMA Code - Prohibition of Cash and Non-Educational Gifts",
                    severity="High",
                    description="Offering personal gifts or cash violates PhRMA Code."
                ))
                compliance_status = "Non-Compliant"
                compliance_notes = "WARNING: Compliance flag regarding gifts."
                
            if "weight loss" in text_lower or "obesity" in text_lower:
                if "zyntra" in text_lower:
                    violations.append(ComplianceFlag(
                        interaction_id=interaction.id,
                        flagged_text=interaction.transcript,
                        rule_matched="PhRMA Code - Off-Label Promotion",
                        severity="Medium",
                        description="Discussing Zyntra for off-label indications (obesity/weight loss)."
                    ))
                    compliance_status = "Flagged"
                    compliance_notes = "Warning: Contains discussion of Zyntra for off-label indications."
            
            if violations:
                for flag in violations:
                    db.add(flag)
                interaction.compliance_status = compliance_status
                interaction.compliance_notes = compliance_notes
            else:
                interaction.compliance_status = compliance_status
                interaction.compliance_notes = compliance_notes

        db.commit()
        return json.dumps({
            "status": "Success",
            "message": f"Interaction ID {interaction_id} updated successfully.",
            "compliance_status": interaction.compliance_status,
            "compliance_notes": interaction.compliance_notes
        }, indent=2)
        
    except Exception as e:
        db.rollback()
        return f"Error editing interaction: {str(e)}"
    finally:
        db.close()


@tool
def analyze_compliance(transcript: str, discussion_topics: List[str]) -> str:
    """Pre-run check to evaluate interaction text against PhRMA compliance guidelines."""
    text_lower = (transcript or "").lower()
    topics_lower = [t.lower() for t in discussion_topics]
    
    flags = []
    status = "Compliant"
    
    # 1. Travel/Recreation check
    if any(k in text_lower for k in ["hawaii", "travel", "flight", "ticket", "hotel", "lodging", "resort"]):
        flags.append({
            "rule": "PhRMA Code - Non-educational items / Individual Entertainment & Travel",
            "severity": "High",
            "flagged_text": transcript,
            "description": "Sponsorship of travel, lodging, or registration fees for individuals to attend scientific conferences is strictly prohibited under the PhRMA guidelines."
        })
        status = "Non-Compliant"
        
    # 2. Gifts/Meals check
    if any(k in text_lower for k in ["gift", "cash", "payment", "fee", "compensation", "dinner"]):
        # Note: Modest meals are allowed during presentations, but general cash or personal gifts are not.
        if "cash" in text_lower or "gift" in text_lower or "pay" in text_lower:
            flags.append({
                "rule": "PhRMA Code - Prohibition of Cash and Non-Educational Gifts",
                "severity": "High",
                "flagged_text": transcript,
                "description": "Providing personal gifts (recreational items, cash, gift certificates, flowers, etc.) to healthcare professionals is forbidden."
            })
            status = "Non-Compliant"
            
    # 3. Off-label check
    if "zyntra" in text_lower or "zyntra" in topics_lower:
        if "weight loss" in text_lower or "obesity" in text_lower or "slimming" in text_lower:
            flags.append({
                "rule": "PhRMA Code - Off-Label Promotion",
                "severity": "Medium",
                "flagged_text": "Discussion of Zyntra for weight loss/obesity",
                "description": "Zyntra is FDA-approved only for Type 2 Diabetes. Promoting or presenting efficacy curves for weight loss constitutes off-label promotion."
            })
            status = "Flagged"

    report = {
        "compliance_status": status,
        "flags": flags,
        "recommendation": "Maintain discussions focused strictly on FDA-approved package insert details." if status == "Compliant" else "Modify the offer or discussion topic to ensure PhRMA guideline compliance before logging."
    }
    return json.dumps(report, indent=2)


@tool
def generate_follow_up(hcp_id: Any, notes: str) -> str:
    """Generate recommended follow-up tasks and draft personalized follow-up emails based on interaction details."""
    db = SessionLocal()
    try:
        try:
            hcp_id = int(hcp_id)
        except (ValueError, TypeError):
            return f"Error: Invalid HCP ID format: {hcp_id}."
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if not hcp:
            return f"Error: HCP with ID {hcp_id} not found."
            
        notes_lower = notes.lower()
        
        # Decide title and email content based on notes
        title = "Follow-up discussion"
        subject = "Follow-up from our meeting"
        body = "It was a pleasure meeting with you. Please let me know if you need any further clinical details."
        
        if "zyntra" in notes_lower:
            title = "Send Zyntra clinical trials brochure"
            subject = "Clinical Study Brochure - Zyntra"
            body = (
                f"Dear {hcp.name},\n\n"
                "Thank you for speaking with me today. As requested, I've attached the clinical brochure "
                "for Zyntra, highlighting the cardiovascular safety outcomes and HbA1c reduction curves "
                "we discussed during our meeting.\n\n"
                "Please let me know if you would like to schedule a brief follow-up call to go over the data in detail.\n\n"
                "Warm regards,\nMedical Representative"
            )
        elif "cardioguard" in notes_lower:
            title = "Schedule discussion on CardioGuard safety profile"
            subject = "Safety Profile Presentation - CardioGuard"
            body = (
                f"Dear {hcp.name},\n\n"
                "Thank you for the virtual meeting today. I have attached the latest safety profiles "
                "for CardioGuard, including the drug-drug interaction tables we talked about.\n\n"
                "I will follow up next week to see if you have any questions or would like to schedule "
                "a quick review.\n\n"
                "Best regards,\nMedical Representative"
            )
        elif "oncoshield" in notes_lower:
            title = "Email OncoShield safety brochure"
            subject = "OncoShield Efficacy and Safety Brochure"
            body = (
                f"Dear {hcp.name},\n\n"
                "As requested in our conversation today, I am sharing the OncoShield scientific publication "
                "outlining the 40% recurrence risk reduction in postmenopausal women with early breast cancer.\n\n"
                "Feel free to reach out if you require any additional materials.\n\n"
                "Sincerely,\nMedical Representative"
            )
            
        follow_up_data = {
            "hcp_id": hcp_id,
            "title": title,
            "description": f"AI-suggested follow-up based on discussion: {notes[:80]}...",
            "due_date": "2026-07-20",
            "recommended_email": f"Subject: {subject}\n\n{body}"
        }
        
        return json.dumps(follow_up_data, indent=2)
    except Exception as e:
        return f"Error generating follow up: {str(e)}"
    finally:
        db.close()
