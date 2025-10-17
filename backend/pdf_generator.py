from fastapi import APIRouter # type: ignore
from fastapi.responses import StreamingResponse # type: ignore
from fpdf import FPDF # type: ignore
from io import BytesIO

router = APIRouter()

@router.post("/api/generate_pdf")
def generate_pdf(name: str, loan_type: str, amount: float, tenure: int, interest_rate: float, emi: float):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt="Loan Approval Letter", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"""
Name: {name}
Loan Type: {loan_type}
Loan Amount: ₹{amount}
Tenure: {tenure} years
Interest Rate: {interest_rate}%
EMI: ₹{emi}

Congratulations! Your loan has been approved.
    """)
    
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    
    return StreamingResponse(pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=loan_approval_{name}.pdf"})
