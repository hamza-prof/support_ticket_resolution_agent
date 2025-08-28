# agent/nodes/escalation.py
import csv
from pathlib import Path

ESCALATION_FILE = Path("data/escalation_log.csv")

ESCALATION_FILE.parent.mkdir(parents=True, exist_ok=True)
if not ESCALATION_FILE.exists():
    with open(ESCALATION_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "Description", "Draft", "Feedback", "Escalation_Reason"])

def log_escalation(state):
    # Determine escalation reason
    current_attempt = state.get("attempt", 1)
    escalation_reason = f"Max attempts ({current_attempt}) reached without approval"
    
    # Log the escalation
    with open(ESCALATION_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            state['subject'],
            state['description'],
            state.get('draft', 'N/A'),
            state.get('review_feedback', 'N/A'),
            escalation_reason
        ])
    
    # Update state to indicate escalation and provide final response
    return {
        **state, 
        "escalated": True,
        "final_response": f"Ticket requires human review. Escalated after {current_attempt} attempts. Reason: {escalation_reason}"
    }
