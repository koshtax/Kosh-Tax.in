from fpdf import FPDF
import datetime

def generate_form16(data, output_filename="Final_Form16.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # --- Header Section ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, txt="FORM NO. 16", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 6, txt="[See rule 31(1)(a)]", ln=True, align='C')
    pdf.cell(190, 6, txt="Certificate under section 203 of the Income-tax Act, 1961 for tax deducted at source on Salary", ln=True, align='C')
    
    pdf.line(10, 35, 200, 35)
    
    # --- Employer & Employee Details ---
    pdf.set_font("Arial", 'B', 9)
    pdf.set_y(40)
    pdf.cell(95, 6, txt="Name and Address of the Employer:", ln=False)
    pdf.cell(95, 6, txt="Name and Designation of the Employee:", ln=True)
    
    pdf.set_font("Arial", '', 9)
    # Automatically using DDO mapped data
    employer_address = data.get('employer_name_address', 'K.B. +2 High School, Arki, Khunti')
    pdf.multi_cell(95, 5, txt=employer_address)
    
    pdf.set_xy(105, 46)
    employee_info = f"{data.get('emp_name', 'Employee Name')}\nDesignation: {data.get('designation', 'Clerk (Lipik)')}"
    pdf.multi_cell(95, 5, txt=employee_info)
    
    pdf.line(10, 65, 200, 65)
    
    # --- PAN & TAN Details ---
    pdf.set_font("Arial", 'B', 9)
    pdf.set_y(70)
    pdf.cell(65, 6, txt="PAN of the Deductor:", ln=False)
    pdf.cell(65, 6, txt="TAN of the Deductor:", ln=False)
    pdf.cell(60, 6, txt="PAN of the Employee:", ln=True)
    
    pdf.set_font("Arial", '', 9)
    pdf.cell(65, 6, txt=data.get('emp_pan', 'NOT PROVIDED'), ln=False)
    pdf.cell(65, 6, txt=data.get('tan', 'NOT PROVIDED'), ln=False)
    pdf.cell(60, 6, txt=data.get('employee_pan', 'NOT PROVIDED'), ln=True)
    
    pdf.line(10, 85, 200, 85)
    
    # --- Financial Computation (Part B) ---
    pdf.set_font("Arial", 'B', 11)
    pdf.set_y(90)
    pdf.cell(190, 8, txt="PART B - Details of Salary Paid and any other income", ln=True)
    
    pdf.set_font("Arial", '', 10)
    gross_salary = data.get('gross_salary', 0)
    standard_deduction = 75000
    net_taxable = max(0, gross_salary - standard_deduction)
    tax_payable = data.get('tax_payable', 0)
    
    pdf.cell(140, 8, txt="1. Gross Salary (Basic + DA + HRA + Medical)", ln=False)
    pdf.cell(50, 8, txt=f"Rs. {gross_salary:,}", ln=True, align='R')
    
    pdf.cell(140, 8, txt="2. Standard Deduction u/s 16(ia)", ln=False)
    pdf.cell(50, 8, txt=f"Rs. {standard_deduction:,}", ln=True, align='R')
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(140, 8, txt="3. Total Taxable Income", ln=False)
    pdf.cell(50, 8, txt=f"Rs. {net_taxable:,}", ln=True, align='R')
    
    pdf.cell(140, 10, txt="4. Net Tax Payable (Under New Regime)", ln=False)
    pdf.set_text_color(200, 0, 0) # Red color for final tax
    pdf.cell(50, 10, txt=f"Rs. {tax_payable:,}", ln=True, align='R')
    
    # --- Footer ---
    pdf.set_y(-30)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Generated on {datetime.date.today()} via Kosh-Tax System", align='C')
    
    pdf.output(output_filename)
    return output_filename
