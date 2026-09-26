import streamlit as st

# 1. Global Page Configuration
st.set_page_config(page_title="Kosh-Tax | Trusted Form 16 SaaS", page_icon="🛡️", layout="wide")

# 2. Professional Teal Theme CSS
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --teal-main: #008080;
        --teal-dark: #005E5E;
        --slate: #2F4F4F;
        --light-bg: #F4F7F6;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: var(--teal-main);
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--teal-dark);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Headers & Text */
    h1, h2, h3 { color: var(--slate); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Draft Watermark Box */
    .draft-box {
        border: 2px dashed var(--teal-main);
        padding: 2rem;
        text-align: center;
        background-color: white;
        border-radius: 8px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .watermark {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: 3rem;
        font-weight: 900;
        color: rgba(255,0,0,0.08);
        white-space: nowrap;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #008080;'>🛡️ Kosh-Tax</h2>", unsafe_allow_html=True)
    st.caption("<div style='text-align: center; margin-bottom: 20px;'>Govt. Employee Tax Portal</div>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation Menu",
        ["📄 Form 16 Generator", "📖 How to Use", "🏢 About Kosh-Tax", "📞 Contact Support", "🔒 Admin Login"]
    )
    
    st.divider()
    st.info("💡 **Secure Portal**\n256-bit Encryption applied for all tax document processing.")

# ==========================================
# PAGE 1: Main Form 16 Generator
# ==========================================
if page == "📄 Form 16 Generator":
    st.title("Automated Form 16 Generator")
    st.markdown("Upload your salary slip to instantly extract data, calculate 7th CPC tax, and generate your Form 16.")
    
    # Options
    col1, col2 = st.columns([3, 1])
    with col2:
        clerk_mode = st.toggle("Enable Clerk / Bulk Mode")
    
    st.divider()
    
    # Step 1: Upload
    st.subheader("Step 1: Upload Document")
    uploaded_file = st.file_uploader("Drag & Drop Dec/Jan Salary Slip (PDF, JPG, PNG)", type=["pdf", "png", "jpg"])
    
    # Step 2: Verification (Simulated as open for UI demo)
    st.subheader("Step 2: Verify Extracted Data")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Employee & DDO Profile**")
        emp_name = st.text_input("Full Name", value="Nitin C. Mallick" if not clerk_mode else "")
        pan = st.text_input("PAN Number", value="ABCDE1234F" if not clerk_mode else "")
        school = st.text_input("School / Office Name", value="Utkramit +2 High School, Tubil")
        ddo = st.text_input("DDO Mapping", value="K.B. +2 High School, Arki")
    
    with c2:
        st.markdown("**Financial Ledger (FY 2025-26)**")
        basic = st.number_input("Gross Basic Pay (₹)", value=591000)
        da = st.number_input("Gross DA (₹)", value=338860)
        hra = st.number_input("Gross HRA (₹)", value=59100)
        medical = st.number_input("Medical / Other (₹)", value=6000)

    # Step 3: Draft Generation
    if st.button("Generate Secure Draft"):
        gross = basic + da + hra + medical
        standard_deduction = 75000
        net_taxable = max(0, gross - standard_deduction)
        
        # Simple dummy tax for UI preview
        tax = 40083 if net_taxable > 700000 else 0 
        
        st.success("✅ Data verified successfully. Please review your draft below.")
        
        st.markdown(f"""
        <div class="draft-box">
            <div class="watermark">DRAFT - NOT FOR OFFICIAL USE</div>
            <h3 style="color: #2F4F4F; margin-bottom: 20px;">Tax Computation Summary</h3>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0;">
                <span><b>Gross Total Income:</b></span> <span>₹{gross:,}</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0;">
                <span><b>Standard Deduction (Sec 16):</b></span> <span>₹{standard_deduction:,}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 15px 0; margin-top: 10px;">
                <span style="font-size: 1.2rem; color: #008080;"><b>Net Tax Payable (New Regime):</b></span> 
                <span style="font-size: 1.3rem; color: #d32f2f; font-weight: bold;">₹{tax:,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.info("🔒 **Next Step:** Pay the ₹99 processing fee via UPI to instantly download your digitally signed PDF.")

# ==========================================
# PAGE 2: How to Use
# ==========================================
elif page == "📖 How to Use":
    st.title("How Kosh-Tax Works")
    st.markdown("Generating your official Form 16 is now a matter of minutes. Follow these simple steps:")
    
    st.markdown("""
    ### 1. Upload Your Salary Slip
    Upload your December or January salary slip. Our AI (Optical Character Recognition) will automatically extract your Basic Pay, DA, HRA, and employer details.
    
    ### 2. Verify Data & Auto-Fill
    Check the extracted numbers on the screen. If you are a returning user, your PAN and DDO details will auto-fill from our secure vault. You can edit any field manually if needed.
    
    ### 3. Review the Draft
    A comprehensive Draft Form 16 will be generated instantly. Verify your tax liability and gross income before making any payment.
    
    ### 4. One-Click Payment & Download
    Pay a nominal processing fee of ₹99 via UPI. Once approved, your official Form 16 PDF (ready for ITR filing) will be downloaded. All your past PDFs are securely stored in your FY-wise Vault.
    """)

# ==========================================
# PAGE 3: About Us
# ==========================================
elif page == "🏢 About Kosh-Tax":
    st.title("About Kosh-Tax")
    st.subheader("Empowering Government Employees with Smart Tax Solutions")
    
    st.markdown("""
    Kosh-Tax was built with a single mission: to eliminate the administrative headache of tax season for government employees, specifically school teachers and clerks.
    
    We understand the complexities of 7th CPC increments, DA arrear logic, and state-specific treasury mappings. Our platform is designed to be a reliable digital assistant for individual employees and DDO administrative offices alike.
    
    **Why Trust Kosh-Tax?**
    * **100% Accuracy:** Powered by advanced AI extraction and precise New Tax Regime algorithms.
    * **Data Privacy:** Your financial data is not shared with third-party advertisers. 
    * **Built for the Ground Reality:** Features like 'Clerk Mode' and 'DDO Default Mapping' prove our system is built for the actual workflow of administrative offices.
    """)

# ==========================================
# PAGE 4: Contact Support
# ==========================================
elif page == "📞 Contact Support":
    st.title("Contact Support")
    st.markdown("Facing issues with an UTR approval or data extraction? We are here to help.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Name")
        st.text_input("Registered Email / Phone")
        st.text_area("Describe your issue")
        st.button("Submit Query")
    
    with c2:
        st.markdown("""
        ### Support Desk
        **Email:** support@koshtax.in  
        **Working Hours:** 10:00 AM - 06:00 PM (Mon-Sat)
        
        *Note: UTR approvals usually take less than 5 minutes during working hours.*
        """)

# ==========================================
# PAGE 5: Admin Login
# ==========================================
elif page == "🔒 Admin Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #008080;'>Admin Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Authorized Personnel Only</p>", unsafe_allow_html=True)
        
        with st.form("admin_login"):
            st.text_input("Admin Username")
            st.text_input("Password", type="password")
            submitted = st.form_submit_button("Access Dashboard")
            
            if submitted:
                st.error("Authentication Server Offline. Database connection required.")
        
        st.caption("Dashboard capabilities include Live UTR Approvals, VIP Whitelist management, and FY Data Collections.")
