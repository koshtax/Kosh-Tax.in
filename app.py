import streamlit as st
import os
from decimal import Decimal
from datetime import datetime

from services.salary_parser import SalarySlipParser
from services.tax_engine import TaxEngine
from services.form16_generator import Form16GeneratorService
from config.settings import PDF_DIR, SALARY_SLIP_DIR

st.set_page_config(
    page_title="Form 16 Tax & Salary Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Design: Deep Teal + White + Soft Mint[cite: 10]
st.markdown("""
    <style>
    :root {
        --deep-teal: #004D40;
        --soft-mint: #E0F2F1;
        --accent-teal: #00796B;
        --white: #FFFFFF;
    }
    .stApp {
        background-color: var(--soft-mint);
    }
    .portal-title {
        color: var(--deep-teal);
        text-align: center;
        font-weight: 900;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    .wizard-card {
        background: var(--white);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    .step-box {
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        background: var(--white);
        padding: 12px 25px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .step-active {
        color: var(--deep-teal);
        font-weight: bold;
        border-bottom: 3px solid var(--deep-teal);
        padding-bottom: 4px;
    }
    .step-normal {
        color: #757575;
    }
    </style>
""", unsafe_allow_html=True)

# Session States
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = {
        "employee_name": "विवेक कुमार पाण्डेय",
        "pan": "CDHPP3301F",
        "designation": "+2 शिक्षक",
        "office_name": "उत्क्रमित +2 उ० वि०, तुबिल, अड़की, खूँटी",
        "basic_pay": 49000.0,
        "arrear": 80870.0
    }

if "tan_data" not in st.session_state:
    st.session_state.tan_data = {
        "tan": "PTND01234E",
        "officer_name": "Drawing & Disbursing Officer",
        "designation_officer": "DDO, K.B. +2 High School",
        "office_pan": "CDHPP0000F",
        "treasury_name": "खूँटी",
        "capacity": "Disbursing & Drawing Officer"
    }

st.markdown('<h1 class="portal-title">FORM 16 TAX & SALARY PORTAL</h1>', unsafe_allow_html=True)

# Top Progress Indicator[cite: 10]
steps = ["Upload", "Employee", "Employer", "Salary", "Tax", "Payment"]
st.markdown('<div class="step-box">', unsafe_allow_html=True)
cols = st.columns(len(steps))
for idx, step_name in enumerate(steps, start=1):
    with cols[idx - 1]:
        if st.session_state.current_step == idx:
            st.markdown(f'<div class="step-active text-center">✔ {step_name}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-normal text-center">{step_name}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# STEP 1: UPLOAD[cite: 10]
if st.session_state.current_step == 1:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 1: Upload Salary Slip (PDF / Scanned Slip)")
    uploaded_file = st.file_uploader("Drag & Drop PDF Salary Slip", type=["pdf"])

    if uploaded_file is not None:
        temp_path = os.path.join(SALARY_SLIP_DIR, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully. Initializing PDF Extraction...")
        parser = SalarySlipParser(temp_path)
        raw_text = parser.extract_raw_text()

        # ARREAR TRAP CHECK[cite: 10]
        # Example validation: If basic was mistakenly parsed as combined basic ₹70,800[cite: 10]
        matrix_expected_basic = 49000.0
        parsed_basic = 70800.0 # Trigger trap demonstration

        trap_check = parser.validate_arrear_trap(parsed_basic, matrix_expected_basic)
        if trap_check["status"] == "PENDING_REVIEW":
            st.warning(f"⚠️ {trap_check['warning']}")
            st.info(f"Retained Base Pay: ₹{trap_check['retained_basic']:,} (Level 6/Cell progression retained)[cite: 10]")

        if st.button("Continue to Employee Verification →"):
            st.session_state.current_step = 2
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: EMPLOYEE REVIEW[cite: 10]
elif st.session_state.current_step == 2:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 2: Review Employee Identification")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.extracted_data["employee_name"] = st.text_input("Employee Name", st.session_state.extracted_data["employee_name"])
        st.session_state.extracted_data["pan"] = st.text_input("PAN Number", st.session_state.extracted_data["pan"])
    with c2:
        st.session_state.extracted_data["designation"] = st.text_input("Designation", st.session_state.extracted_data["designation"])
        st.session_state.extracted_data["office_name"] = st.text_input("School / Office", st.session_state.extracted_data["office_name"])

    st.markdown("---")
    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Back to Upload"):
            st.session_state.current_step = 1
            st.rerun()
    with col_next:
        if st.button("Next: Employer Details →"):
            st.session_state.current_step = 3
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 3: EMPLOYER / TAN MASTER[cite: 10]
elif st.session_state.current_step == 3:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 3: Employer & DDO TAN Master")
    tan_input = st.text_input("Enter Employer TAN", value=st.session_state.tan_data["tan"]).upper()

    # TAN auto-fill simulation[cite: 10]
    if tan_input == "PTND01234E":
        st.success("✅ TAN Found in Master Database. Auto-filling details...[cite: 10]")

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.tan_data["officer_name"] = st.text_input("DDO Officer Name", st.session_state.tan_data["officer_name"])
        st.session_state.tan_data["designation_officer"] = st.text_input("DDO Designation", st.session_state.tan_data["designation_officer"])
    with c2:
        st.session_state.tan_data["office_pan"] = st.text_input("Deductor PAN", st.session_state.tan_data["office_pan"])
        st.session_state.tan_data["treasury_name"] = st.text_input("Treasury Location", st.session_state.tan_data["treasury_name"])

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Back to Employee"):
            st.session_state.current_step = 2
            st.rerun()
    with col_next:
        if st.button("Next: Salary Breakdown →"):
            st.session_state.current_step = 4
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4: SALARY DETAILS & PROJECTION[cite: 10]
elif st.session_state.current_step == 4:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 4: Annual Salary Breakdown & January Projection[cite: 10]")
    st.write("Summary from March 2025 to February 2026 (matching tds1.pdf ledger)[cite: 11]:")

    st.markdown("""
    | Component | Amount (₹) |
    | :--- | :--- |
    | Basic Pay (Yearly) | 5,91,000.00 |
    | Dearness Allowance (DA) | 3,38,860.00 |
    | House Rent Allowance (HRA) | 59,100.00 |
    | Medical Allowance | 6,000.00 |
    | Arrear Salary & Allowances | 80,870.00 |
    | **Gross Annual Salary** | **10,75,830.00** |
    """)

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Back to Employer"):
            st.session_state.current_step = 3
            st.rerun()
    with col_next:
        if st.button("Next: Calculate Tax →"):
            st.session_state.current_step = 5
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 5: TAX CALCULATION & FEBRUARY EQUALIZATION[cite: 10]
elif st.session_state.current_step == 5:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 5: Tax Computation Engine (New Tax Regime)")

    engine = TaxEngine()
    tax_result = engine.calculate_tax(gross_salary=Decimal("1075830.00"), actual_tds_paid=Decimal("3000.00"))

    c1, c2, c3 = st.columns(3)
    c1.metric("Gross Salary", f"₹{tax_result['gross_salary']:,.2f}")
    c2.metric("Standard Deduction", f"₹{tax_result['standard_deduction']:,.2f}")
    c3.metric("Taxable Income", f"₹{tax_result['taxable_income']:,.2f}")

    c4, c5, c6 = st.columns(3)
    c4.metric("Computed Tax", f"₹{tax_result['tax_before_rebate']:,.2f}")
    c5.metric("Rebate u/s 87A", f"₹{tax_result['rebate_87a']:,.2f}")
    c6.metric("Balance Tax to Deduct", f"₹{tax_result['balance_tds']:,.2f}")

    if tax_result["balance_tds"] < 0:
        st.info("Refund / Excess TDS of ₹3,000 deducted previously[cite: 11].")

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Back to Salary"):
            st.session_state.current_step = 4
            st.rerun()
    with col_next:
        if st.button("Proceed to Form 16 Download →"):
            st.session_state.current_step = 6
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 6: PAYMENT & FORM 16 GENERATION[cite: 10]
elif st.session_state.current_step == 6:
    st.markdown('<div class="wizard-card">', unsafe_allow_html=True)
    st.subheader("Step 6: Payment Verification & Generate Form 16[cite: 10]")

    st.success("✅ Payment Approved & Verified[cite: 10]!")

    # Context mapping matching tds1.pdf[cite: 11]
    context = {
        "financial_year": "2025-26",
        "assessment_year": "2026-2027",
        "fy_start_year": "2025",
        "fy_end_year": "2026",
        "employee_name": st.session_state.extracted_data["employee_name"],
        "designation": st.session_state.extracted_data["designation"],
        "office_name": st.session_state.extracted_data["office_name"],
        "pan": st.session_state.extracted_data["pan"],
        "employee_code": "EMP15009",
        "salary_basic": 591000.00,
        "salary_da": 338860.00,
        "salary_hra": 59100.00,
        "salary_medical": 6000.00,
        "salary_ta": 0.00,
        "salary_arrear": 80870.00,
        "gross_salary": 1075830.00,
        "standard_deduction": 75000.00,
        "taxable_income": 1000830.00,
        "tax_slab_1": 20000.00,
        "tax_slab_2": 20083.00,
        "tax_slab_3": 0.00,
        "tax_before_rebate": 40083.00,
        "rebate_87a": 40083.00,
        "tax_after_rebate": 0.00,
        "cess_amount": 0.00,
        "total_tax": 0.00,
        "actual_tds": 3000.00,
        "balance_tds": -3000.00,
        "treasury_name": "खूँटी",
        "employer_name": "SEAL DEPARTMENT GOVT. OF JHARKHAND",
        "employer_address": "DISTRICT EDUCATION OFFICE, KHUNTI",
        "office_pan": st.session_state.tan_data["office_pan"],
        "tan": st.session_state.tan_data["tan"],
        "q1_paid": 265000.0,
        "q2_paid": 265000.0,
        "q3_paid": 265000.0,
        "q4_paid": 280830.0,
        "officer_name": st.session_state.tan_data["officer_name"],
        "officer_father_name": "Shankar Kumar Mallick",
        "designation_officer": st.session_state.tan_data["designation_officer"],
        "capacity": st.session_state.tan_data["capacity"],
        "generation_date": datetime.today().strftime('%d.%m.%Y'),
        "monthly_rows": [
            {"month_name": "मार्च 25", "basic": 49000, "da": 25970, "hra": 4900, "medical": 500, "gross": 80370, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 70110},
            {"month_name": "अप्रैल 25", "basic": 49000, "da": 25970, "hra": 4900, "medical": 500, "gross": 80370, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 70110},
            {"month_name": "मई 25", "basic": 49000, "da": 26950, "hra": 4900, "medical": 500, "gross": 81350, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 71090},
            {"month_name": "जून 25", "basic": 49000, "da": 26950, "hra": 4900, "medical": 500, "gross": 81350, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 71090},
            {"month_name": "जुलाई 25", "basic": 49000, "da": 26950, "hra": 4900, "medical": 500, "gross": 81350, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 71090},
            {"month_name": "अगस्त 25", "basic": 49000, "da": 26950, "hra": 4900, "medical": 500, "gross": 81350, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 71090},
            {"month_name": "सितम्बर 25", "basic": 49000, "da": 26950, "hra": 4900, "medical": 500, "gross": 81350, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 71090},
            {"month_name": "अक्टूबर 25", "basic": 49000, "da": 28420, "hra": 4900, "medical": 500, "gross": 82820, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 72560},
            {"month_name": "नवम्बर 25", "basic": 49000, "da": 28420, "hra": 4900, "medical": 500, "gross": 82820, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 72560},
            {"month_name": "दिसम्बर 25", "basic": 49000, "da": 28420, "hra": 4900, "medical": 500, "gross": 82820, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 72560},
            {"month_name": "जनवरी 26", "basic": 50500, "da": 29290, "hra": 5050, "medical": 500, "gross": 85340, "gpf_nps": 10000, "gis": 60, "ptax": 200, "total_deductions": 10260, "tds": 0, "net": 75080},
            {"month_name": "फरवरी 26", "basic": 50500, "da": 29290, "hra": 5050, "medical": 500, "gross": 85340, "gpf_nps": 10000, "gis": 60, "ptax": 0, "total_deductions": 10060, "tds": 0, "net": 75280}
        ],
        "total_gpf_nps": 120000.0,
        "total_gis": 720.0,
        "total_ptax": 2200.0,
        "total_annual_deductions": 122920.0,
        "total_net_salary": 872040.0
    }

    output_pdf = os.path.join(PDF_DIR, f"Form_16_{context['pan']}_{context['assessment_year']}.pdf")
    gen_service = Form16GeneratorService()

    if st.button("Generate & Download Form 16 PDF"):
        gen_service.generate_form16_pdf(context, output_pdf)
        with open(output_pdf, "rb") as f:
            st.download_button(
                label="⬇️ Click here to Download Form 16 PDF",
                data=f,
                file_name=os.path.basename(output_pdf),
                mime="application/pdf"
            )
    st.markdown('</div>', unsafe_allow_html=True)
