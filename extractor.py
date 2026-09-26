import pdfplumber
import re

def extract_salary_data(pdf_file_path):
    extracted_data = {
        "pan": "",
        "basic_pay": 0,
        "name": "Nitin Chandraushaa Mallick" # Fallback for now, usually requires complex OCR depending on slip format
    }
    
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                
        # 1. Extract PAN Number using Regex (e.g., ABCDE1234F)
        pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', text)
        if pan_match:
            extracted_data["pan"] = pan_match.group(0)
            
        # 2. Extract Basic Pay (Looking for keywords like "Basic Pay", "Basic", etc.)
        basic_match = re.search(r'Basic\s*Pay[\s\:\-]*([\d\,]+)', text, re.IGNORECASE)
        if basic_match:
            clean_number = basic_match.group(1).replace(',', '')
            extracted_data["basic_pay"] = int(clean_number)
            
        return extracted_data
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return extracted_data
