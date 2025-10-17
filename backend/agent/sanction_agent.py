# backend/agents/sanction_agent.py
from fpdf import FPDF # pyright: ignore[reportMissingModuleSource]
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1] / "sanction_letters"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_sanction_letter(customer_name: str, customer_id: int, amount: int, interest_rate: float, tenure_months: int, emi: float):
    # Create a simple PDF using FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Tata Capital - Sanction Letter", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(0, 8, f"Customer Name: {customer_name}", ln=True)
    pdf.cell(0, 8, f"Customer ID: {customer_id}", ln=True)
    pdf.cell(0, 8, f"Loan Amount: ₹{amount}", ln=True)
    pdf.cell(0, 8, f"Interest Rate: {interest_rate}% per annum", ln=True)
    pdf.cell(0, 8, f"Tenure: {tenure_months} months", ln=True)
    pdf.cell(0, 8, f"Estimated EMI: ₹{emi:.2f} per month", ln=True)
    pdf.ln(8)
    pdf.multi_cell(0, 7, "Terms & Conditions: This is a mock sanction letter generated for demonstration within the project. Final sanction will be subject to verification and formal agreements.")
    filename = OUT_DIR / f"sanction_{customer_id}_{customer_name.replace(' ', '_')}.pdf"
    pdf.output(str(filename))
    return str(filename)
