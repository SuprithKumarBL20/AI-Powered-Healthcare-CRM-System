from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import HCP, Product, Interaction, FollowUp, ComplianceFlag

def seed_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing data to avoid duplicates
        db.query(ComplianceFlag).delete()
        db.query(FollowUp).delete()
        db.query(Interaction).delete()
        db.query(HCP).delete()
        db.query(Product).delete()
        
        # Add Products
        zyntra = Product(
            name="Zyntra",
            therapeutic_class="Endocrinology/Diabetes",
            indications="Treatment of Type 2 Diabetes Mellitus in adults to improve glycemic control.",
            contraindications="Type 1 Diabetes, Diabetic Ketoacidosis, Hypersensitivity to active ingredients.",
            key_benefits="Reduces HbA1c effectively, promotes cardiovascular risk reduction, supports moderate weight loss."
        )
        cardioguard = Product(
            name="CardioGuard",
            therapeutic_class="Cardiology/Hypertension",
            indications="Management of essential hypertension in adults and reduction of cardiovascular events.",
            contraindications="Severe bradycardia, cardiogenic shock, second or third-degree AV block.",
            key_benefits="Lowers systolic and diastolic blood pressure, decreases cardiac workload, reduces stroke risk."
        )
        oncoshield = Product(
            name="OncoShield",
            therapeutic_class="Oncology/Breast Cancer",
            indications="Adjuvant treatment of postmenopausal women with hormone receptor-positive early breast cancer.",
            contraindications="Pregnancy, lactation, pre-menopausal endocrine status.",
            key_benefits="Inhibits tumor aromatase activity, reduces recurrence risk by 40% compared to standard adjuvant therapy."
        )
        
        db.add_all([zyntra, cardioguard, oncoshield])
        db.commit()

        # Add HCPs
        jenkins = HCP(
            name="Dr. Sarah Jenkins",
            specialty="Endocrinology",
            hospital="Metro Health Endocrinology Clinic",
            email="sjenkins@metrohealth.org",
            phone="555-0192",
            preferred_channel="In-Person",
            next_best_action="Deliver clinical trials overview sheet for Zyntra.",
            notes="Prefers morning meetings on Tuesdays. Highly analytical; requires peer-reviewed publications."
        )
        chen = HCP(
            name="Dr. Robert Chen",
            specialty="Cardiology",
            hospital="St. Jude Heart Center",
            email="rchen@stjudeheart.org",
            phone="555-0143",
            preferred_channel="Video Call",
            next_best_action="Discuss CardioGuard side effects and safety profile.",
            notes="Very tech-savvy, prefers video calls. Busy on Mondays/Thursdays. Interested in drug-drug interactions."
        )
        vance = HCP(
            name="Dr. Elizabeth Vance",
            specialty="Oncology",
            hospital="City Cancer Institute",
            email="evance@citycancer.org",
            phone="555-0187",
            preferred_channel="Email",
            next_best_action="Email OncoShield safety brochure.",
            notes="Extremely busy. Primary channel is Email. Only schedules physical meetings for major multi-center trial reviews."
        )
        
        db.add_all([jenkins, chen, vance])
        db.commit()

        # Add initial interaction (past)
        past_interaction = Interaction(
            hcp_id=jenkins.id,
            rep_id="REP-001",
            date="2026-06-15",
            channel="In-Person",
            summary="Initial presentation of Zyntra. Dr. Jenkins requested efficacy data comparing Zyntra to standard therapies.",
            transcript="Meeting started at 9:00 AM. Rep presented Zyntra's mechanism of action. Dr. Jenkins was receptive but asked for specific HbA1c reduction curves. Promised to deliver study brochures.",
            discussion_topics="Zyntra, Efficacy Comparison",
            follow_up_date="2026-06-22",
            compliance_status="Compliant",
            compliance_notes="Checked for off-label discussion: None. Efficacy claims match package insert.",
            sentiment="Positive",
            next_steps="Send HbA1c efficacy brochures."
        )
        db.add(past_interaction)
        db.commit()

        # Add a compliance flag to showcase the system
        flagged_interaction = Interaction(
            hcp_id=chen.id,
            rep_id="REP-001",
            date="2026-07-02",
            channel="Video Call",
            summary="Discussion about CardioGuard. Dr. Chen asked if we could provide tickets to a medical conference in Hawaii. Rep agreed to check.",
            transcript="Rep: Hi Dr. Chen, let's talk about CardioGuard. Chen: I'm interested in using it more. By the way, are you sponsoring delegates for the Cardiology Summit in Hawaii next month? Rep: I think we can arrange that and cover travel. Let me get that sorted for you.",
            discussion_topics="CardioGuard, Event Sponsorship",
            follow_up_date="2026-07-10",
            compliance_status="Non-Compliant",
            compliance_notes="PhRMA guidelines prohibit providing individual travel, lodging, or conference registration sponsorships for HCPs.",
            sentiment="Neutral",
            next_steps="Correct the travel offer to remain compliant."
        )
        db.add(flagged_interaction)
        db.commit()

        flag = ComplianceFlag(
            interaction_id=flagged_interaction.id,
            flagged_text="Rep: I think we can arrange that and cover travel. Let me get that sorted for you.",
            rule_matched="PhRMA Code - Non-educational items / Individual Entertainment & Travel",
            severity="High",
            description="Offering to pay for travel and lodging to a conference in Hawaii violates the PhRMA code on interactions with healthcare professionals, which prohibits recreational and personal expenses sponsorship."
        )
        db.add(flag)
        
        # Add a follow-up for Jenkins
        follow_up = FollowUp(
            hcp_id=jenkins.id,
            interaction_id=past_interaction.id,
            title="Deliver study brochure",
            description="Email the clinical study brochures showing HbA1c reduction curves.",
            due_date="2026-06-22",
            status="Completed",
            recommended_email="Dear Dr. Jenkins, It was great speaking with you on June 15th. As promised, I have attached the clinical trial brochures for Zyntra showing its superior HbA1c reduction curves. Let me know if you have any questions. Best, Rep."
        )
        db.add(follow_up)
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
