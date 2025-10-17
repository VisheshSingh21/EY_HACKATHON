# backend/agents/master_agent.py
from .utils import get_customer_by_id
from .sales_agent import handle_sales_conversation
from .verification_agent import verify_customer_kyc
from .underwriting_agent import evaluate_loan, monthly_emi
from .sanction_agent import generate_sanction_letter

def master_agent_run(customer_id: int, requested_amount: int, tenure_months: int, salary_slip_submitted: bool=False, salary: int=None):
    """
    Orchestration steps:
    1. Load customer
    2. Sales -> get interest rate proposal
    3. Verification -> check KYC
    4. Underwriting -> evaluate loan using rules
       - If underwriting requests salary slip, the frontend should upload & call back with slip flag + salary
    5. If approved -> generate sanction letter (PDF) and return path
    """

    # 1. Load customer
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "reason": "Customer not found."}

    # 2. Sales agent
    sale = handle_sales_conversation(customer, requested_amount, tenure_months)
    interest_rate = sale["proposal"]["interest_rate"]

    # 3. Verification agent
    ver = verify_customer_kyc(customer_id)
    if ver.get("status") != "verified":
        return {"status": "rejected", "reason": "KYC verification failed."}

    # 4. Underwriting agent
    underwriting_result = evaluate_loan(customer, requested_amount, tenure_months, interest_rate, salary_slip_submitted, salary)
    if underwriting_result["status"] == "action_required" and underwriting_result.get("next_action") == "request_salary_slip":
        # Ask frontend to request salary slip from user
        return {"status": "action_required", "next_action": "request_salary_slip", "message": "Please upload salary slip for further processing."}
    if underwriting_result["status"] == "rejected":
        return {"status": "rejected", "reason": underwriting_result["reason"]}

    # If approved
    emi = underwriting_result.get("emi", monthly_emi(requested_amount, interest_rate, tenure_months))
    pdf_path = generate_sanction_letter(customer["name"], customer_id, requested_amount, interest_rate, tenure_months, emi)

    response = {
        "status": "approved",
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "approved_amount": requested_amount,
        "interest_rate": interest_rate,
        "tenure_months": tenure_months,
        "emi": emi,
        "sanction_letter_path": pdf_path
    }
    return response
