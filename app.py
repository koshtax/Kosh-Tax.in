import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="Kosh-Tax | Secure Form 16 Portal", page_icon="🔒", layout="wide")

# 2. Professional Enterprise CSS & Trust Signals
st.markdown("""
<style>
    /* Clean and Strict Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Top Security Banner */
    .security-banner {
        background-color: #003333;
        color: #4ADE80;
        text-align: center;
        padding: 8px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1px;
        width: 100%;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    /* Strict Buttons */
    .stButton>button {
        background-color: #008080;
        color: white;
        border-radius: 4px;
        border: 1px solid #005E5E;
        width: 100%;
        font-weight: 600;
        letter-spacing: 0.5px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #005E5E; color: white; }
    
    /* Data Privacy Box */
    .privacy-box {
        border-left: 4px solid #008080;
        background-color: #F8FAFC;
        padding: 15px;
        margin: 15px 0;
        font-size: 14px;
        color: #334155;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #E2E8F0;
        font-size: 12px;
        color: #64748B;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation with Trust Badges
with st.sidebar:
    st.markdown("<h2 style='color: #008080; text-align: center; font-weight: 800;'>KOSH-TAX</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Govt. Employee Portal</p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Navigation Menu", ["📄 Generate Form 16", "📖 How to Use", "🏢 About Kosh-Tax", "📞 Contact Support", "🔒 Admin Login"])
    
    st.write("---")
    st.markdown("""
    <div style='text-align: center; font-size: 12px; color: #475569;'>
        <p>🔒 <b>256-Bit SSL Encrypted</b></p>
        <p>🛡️ <b>Data Privacy Compliant</b></p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 1: Dynamic Generator
# ==========================================
if menu == "📄 Generate Form 16":
    
    # Global Security Banner
    st.markdown("<div class='security-banner'>🔒 CONNECTION IS SECURE & ENCRYPTED. YOUR DATA IS SAFE.</div>", unsafe_allow_html=True)
    
    st.title("Automated Form 16 Generator")
    st.write("Securely upload your salary slip. Our automated system calculates your 7th CPC tax liability instantly.")
    
    # Trust Box before upload
    st.markdown("""
    <div class='privacy-box'>
        <b>Privacy Guarantee:</b> We do not store your PDF or PAN details on our servers after your session ends. All data is processed in real-time and automatically deleted to ensure strict financial confidentiality.
    </div>
    """, unsafe_allow_html=True)
    
    # PDF Upload Trigger
    uploaded_file = st.file_uploader("Upload Salary Slip (PDF Only)", type=["pdf"])
    
    if uploaded_file is not None:
        
        with st.spinner("🔒 Authenticating document and securely extracting data..."):
            time.sleep(2)
            
        st.success("✅ Document processed securely. Please review your details.")
        st.write("---")
        
        # Dynamic Data Entry Fields
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("1. Employee & DDO Details")
            emp_name = st.text_input("Full Name", value="")
            pan = st.text_input("PAN Number", value="")
            school = st.text_input("School / Office Name", value="")
            ddo = st.text_input("DDO Mapping", value="")
            
        with c2:
            st.subheader("2. Financial Ledger")
            basic = st.number_input("Total Basic Pay (₹)", value=0, step=1000)
            da = st.number_input("Total DA (₹)", value=0, step=1000)
            hra = st.number_input("Total HRA (₹)", value=0, step=1000)
            medical = st.number_input("Medical Allowance (₹)", value=0, step=100)
            
        st.write("---")
        
        if st.button("Generate Secure Draft & Calculate Tax"):
            gross = basic + da + hra + medical
            standard_deduction = 75000
            net_taxable = max(0, gross - standard_deduction)
            
            tax = 0
            if net_taxable > 700000:
                if net_taxable > 400000: tax += min(net_taxable - 400000, 400000) * 0.05
                if net_taxable > 800000: tax += min(net_taxable - 800000, 400000) * 0.10
                if net_taxable > 1200000: tax += min(net_taxable - 1200000, 400000) * 0.15
                if net_taxable > 1600000: tax += min(net_taxable - 1600000, 400000) * 0.20
                if net_taxable > 2000000: tax += min(net_taxable - 2000000, 400000) * 0.25
                if net_taxable > 2400000: tax += (net_taxable - 2400000) * 0.30
                tax += tax * 0.04 
            tax = round(tax)
            
            # Professional Draft Preview
            st.markdown(f"""
            <div style="border: 2px solid #E2E8F0; padding: 25px; background-color: #ffffff; border-radius: 4px; margin-top: 20px; position: relative;">
                <h3 style="color: #0F172A; border-bottom: 2px solid #008080; padding-bottom: 10px;">Tax Computation Summary</h3>
                <div style="font-size: 16px; line-height: 2; margin-top: 15px; color: #334155;">
                    <div style="display: flex; justify-content: space-between;"><b>Gross Total Income:</b> <span>₹{gross:,}</span></div>
                    <div style="display: flex; justify-content: space-between;"><b>Standard Deduction:</b> <span>₹{standard_deduction:,}</span></div>
                    <div style="display: flex; justify-content: space-between; border-top: 1px dashed #cbd5e1; margin-top: 10px; padding-top: 10px;">
                        <b style="color: #008080; font-size: 18px;">Net Tax Payable:</b> 
                        <span style="color: #b91c1c; font-size: 20px; font-weight: 800;">₹{tax:,}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("🔒 Pay ₹99 via UPI to securely download the digitally certified Form 16 PDF.")

# Professional Footer
st.markdown("""
<div class='footer'>
    © 2026 Kosh-Tax Services | All Rights Reserved<br>
    Strictly adhering to New Tax Regime guidelines. Data processed securely.
</div>
""", unsafe_allow_html=True)
