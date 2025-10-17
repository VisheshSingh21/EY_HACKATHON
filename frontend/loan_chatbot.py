import streamlit as st # type: ignore
import requests # type: ignore

st.title("AI Loan Chatbot")

LOAN_TYPES = ["Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Business Loan"]

with st.form(key="loan_form"):
    name = st.text_input("Your Name")
    loan_type = st.selectbox("Loan Type", LOAN_TYPES)
    amount = st.number_input("Loan Amount", min_value=1000)
    tenure = st.number_input("Tenure (years)", min_value=1)
    income = st.number_input("Monthly Income", min_value=0)
    credit_score = st.number_input("Your Credit Score", min_value=300, max_value=900)
    submit = st.form_submit_button("Check Eligibility")

if submit:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/loan_inquiry",
            json={
                "name": name,
                "loan_type": loan_type,
                "amount": amount,
                "tenure": tenure,
                "income": income,
                "credit_score": credit_score
            }
        ).json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Make sure FastAPI server is running.")
        st.stop()

    st.write("Backend response:", response)

    st.write(response.get("message", response.get("detail", "No message returned")))


    if response["status"] == "approved":
        try:
            pdf_response = requests.post(
                "http://127.0.0.1:8000/api/generate_pdf",
                params={
                    "name": name,
                    "loan_type": loan_type,
                    "amount": amount,
                    "tenure": tenure,
                    "interest_rate": response["interest_rate"],
                    "emi": response["emi"]
                },
                stream=True
            )
            st.download_button(
                label="Download Loan Approval PDF",
                data=pdf_response.content,
                file_name=f"loan_approval_{name}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to download PDF: {e}")
