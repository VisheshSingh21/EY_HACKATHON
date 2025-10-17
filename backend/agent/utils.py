# backend/agents/utils.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # backend/

def load_json(filename: str):
    path = BASE_DIR / "data" / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_customer_by_id(customer_id: int):
    customers = load_json("customers.json")
    for c in customers:
        if c["id"] == customer_id:
            return c
    return None
