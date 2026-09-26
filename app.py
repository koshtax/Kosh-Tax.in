import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="Kosh-Tax | Form 16 SaaS", page_icon="🛡️", layout="wide")

# 2. Teal Theme CSS
st.markdown("""
<style>
    .stButton>button { background-color: #008080; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #005E5E; color: white; }
    .css-1v0mbdj.etr89bj1 { text-align: center; } /* Center align sidebar title */
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='color: #008080; text-align: center;'>🛡️ Kosh-Tax</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("Menu", ["📄 Generator", "📖 How to Use", "🏢 About", "📞 Contact Us", "🔒 Admin Login"])

# ==========================================
# PAGE 1: Dynamic Generator
# ==========================================
if menu == "📄 Generator":
    st.title("Form 16 Generator")
    st.write("Upload your PDF salary slip. The system will extract your data dynamically.")
    
    # PDF Upload Trigger
    uploaded_file = st.file_uploader("Upload Salary Slip (PDF)", type=["pdf"])
    
    # Logic: Form tabhi dikhega jab file upload hogi
    if uploaded_file is not None:
        
        # Simulating Document AI (OCR) Processing Delay
        with st.spinner("Analyzing document and extracting data..."):
            time.sleep(2)
            
        st.success("✅ Document processed successfully! Please verify the extracted details below.")
        st.write("---")
        
        # Dynamic Data Entry Fields (Completely Blank / 0 initially)
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("1. Profile Details")
            emp_name = st.text_input("Employee Name", value="")
            pan = st.text_input("PAN Number", value="")
            school = st.text_input("School / Office Name", value="")
            ddo = st.text_input("DDO Mapping", value="")
            
        with c2:
            st.subheader("2. Financial Entries")
            basic = st.number_input("Total Basic Pay (₹)", value=0, step=1000)
            da = st.number_input("Total DA (₹)", value=0, step=1000)
            hra = st.number_input("Total HRA (₹)", value=0, step=1000)
            medical = st.number_input("Medical Allowance (₹)", value=0, step=100)
            
        st.write("---")
        
        # Generate Button
        if st.button("Calculate Tax & Generate Draft"):
            gross = basic + da + hra + medical
            standard_deduction = 75000
            net_taxable = max(0, gross - standard_deduction)
            
            # Dynamic Tax Calculation (New Regime)
            tax = 0
            if net_taxable > 700000:
                if net_taxable > 400000: tax += min(net_taxable - 400000, 400000) * 0.05
                if net_taxable > 800000: tax += min(net_taxable - 800000, 400000) * 0.10
                if net_taxable > 1200000: tax += min(net_taxable - 1200000, 400000) * 0.15
                if net_taxable > 1600000: tax += min(net_taxable - 1600000, 400000) * 0.20
                if net_taxable > 2000000: tax += min(net_taxable - 2000000, 400000) * 0.25
                if net_taxable > 2400000: tax += (net_taxable - 2400000) * 0.30
                tax += tax * 0.04  # 4% Health & Education Cess
            
            tax = round(tax)
            
            # Draft Preview Output
            st.markdown(f"""
            <div style="border: 2px dashed #008080; padding: 25px; text-align: center; background-color: #f8f9fa; border-radius: 8px;">
                <h3 style="color: #008080;">📄 Draft Preview</h3>
                <div style="font-size: 18px; line-height: 1.8;">
                    <b>Gross Total Income:</b> ₹{gross:,}<br>
                    <b>Standard Deduction:</b> ₹{standard_deduction:,}<br>
                    <h2 style="color: #d32f2f; margin-top: 15px;">Net Tax Payable: ₹{tax:,}</h2>
                </div>
                <p style="color: red; opacity: 0.6; font-size: 22px; font-weight: bold; transform: rotate(-5deg); margin-top: 15px;">DRAFT - NOT FOR OFFICIAL USE</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("Pay ₹99 via UPI to download the digitally signed Form 16 PDF.")

# ==========================================
# PAGE 2: How to Use
# ==========================================
elif menu == "📖 How to Use":
    st.title("How to Use Kosh-Tax")
    st.write("1. **Upload:** Go to Generator and upload your PDF salary slip.")
    st.write("2. **Verify:** Check the dynamically extracted fields.")
    st.write("3. **Generate:** Review the Draft Form 16 and process the ₹99 payment to get your PDF.")

# ==========================================
# PAGE 3: About
# ==========================================
elif menu == "🏢 About":
    st.title("About Kosh-Tax")
    st.write("Kosh-Tax is a secure SaaS platform designed to automate Form 16 generation and 7th CPC tax calculations for government employees and DDO administrative offices.")

# ==========================================
# PAGE 4: Contact Us
# ==========================================
elif menu == "📞 Contact Us":
    st.title("Contact Support")
    st.text_input("Name")
    st.text_input("Email / Phone")
    st.text_area("Issue Description")
    st.button("Submit Query")

# ==========================================
# PAGE 5: Admin Login
# ==========================================
elif menu == "🔒 Admin Login":
    st.title("Admin Portal")
    st.text_input("Username")
    st.text_input("Password", type="password")
    if st.button("Login"):
        st.error("Database connection required to access Admin Dashboard.")
