# backend/agents/verification_agent.py
from .utils import load_json

def verify_customer_kyc(customer_id: int):
    crm = load_json("crm_data.json")
    for rec in crm:
        if rec["id"] == customer_id:
            # in real world we'd verify phone, address, etc.
            return {"status": "verified", "phone": rec["phone"], "address": rec["address"]}
    return {"status": "failed", "reason": "KYC record not found"}
