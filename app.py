import streamlit as st
import time

# 1. Page Configuration (Keep your existing CSS & Theme setup)
st.set_page_config(page_title="Kosh-Tax | Secure Form 16 Portal", page_icon="🔒", layout="wide")

# Initialize Session State for Wizard Steps
if 'step' not in st.session_state:
    st.session_state.step = 1

# ... [Keep your existing CSS and Sidebar Code Here] ...
menu = "📄 Generate Form 16" # Dummy placeholder for context

if menu == "📄 Generate Form 16":
    st.markdown("<div class='security-banner'>🔒 CONNECTION IS SECURE & ENCRYPTED.</div>", unsafe_allow_html=True)
    st.title("Automated Form 16 Wizard")
    
    # Progress Bar
    progress_text = ["1. Upload", "2. Employee Details", "3. Employer Details", "4. Salary Details", "5. Payment"]
    st.progress(st.session_state.step / 5, text=progress_text[st.session_state.step - 1])
    
    uploaded_file = st.file_uploader("Upload Salary Slip (PDF Only)", type=["pdf"])

    if uploaded_file is not None:
        
        # ==========================================
        # STEP 1: Basic Extraction Preview
        # ==========================================
        if st.session_state.step == 1:
            with st.spinner("Extracting primary data..."):
                time.sleep(1)
            
            st.success("✅ Document processed.")
            st.subheader("Extracted Primary Details")
            
            st.text_input("Full Name", value="Nitin Chandraushaa Mallick", disabled=True)
            st.text_input("PAN Number", value="ABCDE1234F", disabled=True)
            st.text_input("Latest Basic Pay (7th CPC)", value="₹ 49,000", disabled=True)
            
            if st.button("Next: Employee Details"):
                st.session_state.step = 2
                st.rerun()

        # ==========================================
        # STEP 2: Employee Details (Auto-fill & Manual)
        # ==========================================
        elif st.session_state.step == 2:
            st.subheader("Employee Details")
            
            st.markdown("**Auto-Filled from Records:**")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Full Name", value="Nitin Chandraushaa Mallick", disabled=True)
                st.text_input("PAN Number", value="ABCDE1234F", disabled=True)
            with c2:
                st.text_input("Employee Designation", value="Clerk (Lipik)")
                st.text_input("GPF/CPS/PRAN Number", value="1100XXXXXX")
            
            st.markdown("**Manual Entry Required:**")
            st.text_input("Office / School Name & Address", value="Utkramit +2 High School, Tubil")
            st.text_input("District", value="Khunti")
            
            c3, c4 = st.columns(2)
            with c3:
                st.text_input("Mobile Number")
            with c4:
                st.text_input("Email ID")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back"):
                    st.session_state.step = 1
                    st.rerun()
            with col2:
                if st.button("Next: Employer Details"):
                    st.session_state.step = 3
                    st.rerun()

        # ==========================================
        # STEP 3: Employer Details (TAN Logic)
        # ==========================================
        elif st.session_state.step == 3:
            st.subheader("Employer Details")
            
            tan_input = st.text_input("Enter Employer TAN Number", placeholder="e.g. RANC12345E")
            
            # Simulated DB Logic
            db_tan = "RANC12345E"
            is_fetched = (tan_input.upper() == db_tan)
            
            if tan_input and not is_fetched:
                st.warning("TAN not found in Database. Please enter details manually.")
            elif is_fetched:
                st.success("✅ Employer Details Auto-Fetched from Database!")

            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Employer PAN", value="AAALE0000X" if is_fetched else "")
                st.text_input("DDO Officer Name", value="Rajesh Kumar" if is_fetched else "")
            with c2:
                st.text_area("Name & Address of Employer", value="K.B. +2 High School, Arki" if is_fetched else "", height=68)
                st.text_input("DDO Father/Mother Name", value="S. Kumar" if is_fetched else "")
                
            st.text_input("Designation", value="Disbursing & Drawing Officer", disabled=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back"):
                    st.session_state.step = 2
                    st.rerun()
            with col2:
                if st.button("Next: Salary Details"):
                    st.session_state.step = 4
                    st.rerun()

        # ==========================================
        # STEP 4: Salary Details
        # ==========================================
        elif st.session_state.step == 4:
            st.subheader("Salary & Tax Computation")
            st.write("Review the calculated tax based on your inputs.")
            
            st.info("Gross Income: ₹5,91,000 | Net Tax: ₹0") # Dummy display
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back"):
                    st.session_state.step = 3
                    st.rerun()
            with col2:
                if st.button("Proceed to Payment Gateway"):
                    st.session_state.step = 5
                    st.rerun()

        # ==========================================
        # STEP 5 & 6: Payment & Download
        # ==========================================
        elif st.session_state.step == 5:
            st.subheader("Secure Payment Gateway")
            st.markdown("""
            <div style='text-align:center; padding: 20px; border: 1px solid #ddd; border-radius: 8px;'>
                <h3>Scan QR to Pay ₹99</h3>
                <img src='https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg' width='150'>
                <p>Upon successful payment, your PDF will unlock instantly.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back"):
                    st.session_state.step = 4
                    st.rerun()
            with col2:
                # Simulated successful payment download
                st.download_button(label="Download Form 16 PDF", data="Dummy PDF Content", file_name="Form16.pdf", mime="application/pdf")
