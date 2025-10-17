# backend/main.py
from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI(title="Loan Chatbot API")

# ---------------------------
# Loan Request Model
# ---------------------------
class LoanRequest(BaseModel):
    name: str
    loan_type: str
    amount: float
    tenure: int
    income: float
    credit_score: int

# ---------------------------
# Loan Inquiry Endpoint
# ---------------------------
@app.post("/api/loan_inquiry")
def loan_inquiry(request: LoanRequest):
    if request.credit_score < 600:
        return {"status": "rejected", "message": "Low credit score, loan not approved"}

    interest_rate = {
        "Personal Loan": 12,
        "Home Loan": 8,
        "Car Loan": 10,
        "Education Loan": 9,
        "Business Loan": 14
    }.get(request.loan_type, 10)

    emi = (request.amount * (1 + interest_rate / 100)) / request.tenure
    return {
        "status": "approved",
        "message": f"Loan approved for {request.name}!",
        "interest_rate": interest_rate,
        "emi": round(emi, 2)
    }

# ---------------------------
# Root Route (optional)
# ---------------------------
@app.get("/")
def root():
    return {"message": "Welcome to Loan Chatbot API"}
