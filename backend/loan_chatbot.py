from fastapi import APIRouter # type: ignore
from pydantic import BaseModel # type: ignore

router = APIRouter()

LOAN_TYPES = {
    "Personal Loan": 12,
    "Home Loan": 8,
    "Car Loan": 10,
    "Education Loan": 9,
    "Business Loan": 14
}

class LoanRequest(BaseModel):
    name: str
    loan_type: str
    amount: float
    tenure: int
    income: float
    credit_score: int

def check_eligibility(income, credit_score, amount):
    if credit_score < 600:
        return False, "Credit score too low for loan"
    if income < 15000 and amount > 500000:
        return False, "Income too low for requested loan amount"
    return True, "Eligible"

def calculate_emi(amount, tenure, rate):
    r = rate / (12 * 100)
    n = tenure * 12
    emi = (amount * r * (1 + r)**n) / ((1 + r)**n - 1)
    return round(emi, 2)

@router.post("/api/loan_inquiry")
def loan_inquiry(data: LoanRequest):
    eligible, msg = check_eligibility(data.income, data.credit_score, data.amount)
    if not eligible:
        return {"status": "rejected", "message": msg}
    
    interest_rate = LOAN_TYPES.get(data.loan_type, 12)
    emi = calculate_emi(data.amount, data.tenure, interest_rate)
    
    return {
        "status": "approved",
        "loan_type": data.loan_type,
        "amount": data.amount,
        "tenure": data.tenure,
        "interest_rate": interest_rate,
        "emi": emi,
        "message": f"Your loan is approved! Monthly EMI: ₹{emi}"
    }

