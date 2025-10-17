# backend/agents/sales_agent.py
"""
Sales Agent:
- Receives customer profile and requested amount/tenure
- Proposes rate & next step
- Returns a compact response dict
"""

def handle_sales_conversation(customer: dict, requested_amount: int, tenure_months: int):
    # Simple business rule for interest:
    # If within pre-approved limit — lower rate; otherwise higher.
    limit = customer.get("pre_approved_limit", 0)
    if requested_amount <= limit:
        interest_rate = 11.5  # lower, promotional
    else:
        interest_rate = 13.5  # higher if above pre-approved
    message = (
        f"Proposed loan ₹{requested_amount} for {tenure_months} months at {interest_rate}% p.a."
    )
    return {
        "status": "ok",
        "proposal": {
            "amount": requested_amount,
            "tenure_months": tenure_months,
            "interest_rate": interest_rate,
            "message": message
        },
        "next": "verification"
    }
