# backend/agents/underwriting_agent.py
"""
Underwriting logic:
- Fetch credit score & pre_approved_limit from customer dict
- Rules:
  1. credit_score < 700 => reject
  2. amount <= pre_approved_limit => approve instantly
  3. amount <= 2 * pre_approved_limit => require salary slip; then approve only if EMI <= 50% salary
  4. amount > 2 * pre_approved_limit => reject
- EMI calculation: monthly_interest_rate = annual_rate/12; EMI formula or simple heuristic for prototype
"""

def monthly_emi(amount: float, annual_rate_percent: float, months: int) -> float:
    # Standard EMI formula
    r = annual_rate_percent / 100 / 12
    if r == 0:
        return amount / months
    emi = amount * r * (1 + r) ** months / ((1 + r) ** months - 1)
    return emi

def evaluate_loan(customer: dict, requested_amount: int, tenure_months: int, interest_rate: float, salary_slip_submitted: bool=False, salary: int=None):
    score = customer.get("credit_score", 0)
    limit = customer.get("pre_approved_limit", 0)

    # Step A: credit score check
    if score < 700:
        return {"status": "rejected", "reason": "Credit score below threshold (<700)."}

    # Step B: amount checks
    if requested_amount <= limit:
        # Instant approval
        emi = monthly_emi(requested_amount, interest_rate, tenure_months)
        return {"status": "approved", "mode": "instant", "emi": emi}
    elif requested_amount <= 2 * limit:
        # Need salary verification
        if not salary_slip_submitted:
            return {"status": "action_required", "next_action": "request_salary_slip"}
        # If slip present, require salary for eligibility check
        if salary is None:
            return {"status": "rejected", "reason": "Salary information missing despite slip."}
        emi = monthly_emi(requested_amount, interest_rate, tenure_months)
        if emi <= 0.5 * salary:
            return {"status": "approved", "mode": "after_salary_verification", "emi": emi}
        else:
            return {"status": "rejected", "reason": "EMI > 50% of salary."}
    else:
        return {"status": "rejected", "reason": "Requested amount exceeds 2× pre-approved limit."}
