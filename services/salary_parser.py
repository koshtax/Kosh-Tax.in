import fitz  # PyMuPDF
import re
from typing import Dict, Any, Optional

class SalarySlipParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.extracted_text = ""
        self.confidence_scores = {}

    def extract_raw_text(self) -> str:
        """PDF se text extract karta hai."""
        try:
            doc = fitz.open(self.pdf_path)
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            self.extracted_text = text
            return text
        except Exception as e:
            return ""

    def parse_components(self) -> Dict[str, Any]:
        """Salary components aur employee identity regex patterns se parse karta hai."""
        if not self.extracted_text:
            self.extract_raw_text()

        components = {
            "pan": self._extract_pan(),
            "employee_name": self._extract_field(r"(?:Name|Employee\s*Name)\s*[:\-]?\s*([A-Za-z\s\.]+)", default="Review required"),
            "designation": self._extract_field(r"(?:Designation|Post)\s*[:\-]?\s*([A-Za-z0-9\+\s]+)", default="Clerk / Teacher"),
            "office_name": self._extract_field(r"(?:School|Office|Department)\s*[:\-]?\s*([A-Za-z0-9\+\s\,\.\-]+)", default=""),
            "basic_pay": self._extract_amount(r"(?:Basic\s*Pay|मूल\s*वेतन|Basic)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "da": self._extract_amount(r"(?:DA|Dearness\s*Allowance|महंगाई\s*भत्ता)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "hra": self._extract_amount(r"(?:HRA|House\s*Rent\s*Allowance|मकान\s*किराया)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "medical": self._extract_amount(r"(?:Medical|चिकित्सा)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "gpf": self._extract_amount(r"(?:GPF|भविष्य\s*निधि)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "nps": self._extract_amount(r"(?:NPS|PRAN)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "ptax": self._extract_amount(r"(?:PTAX|Professional\s*Tax|व्यवसाय\s*कर)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "gis": self._extract_amount(r"(?:GIS|समूह\s*बीमा)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "tds": self._extract_amount(r"(?:TDS|Income\s*Tax|आयकर)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "gross_salary": self._extract_amount(r"(?:Gross\s*Salary|कुल\s*वेतन|सकल\s*योग)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
            "net_salary": self._extract_amount(r"(?:Net\s*Salary|शुद्ध\s*भुगतान)\s*[:\-]?\s*(?:Rs\.?|₹)?\s*([\d,]+(?:\.\d{2})?)"),
        }

        return components

    def _extract_pan(self) -> Optional[str]:
        match = re.search(r"\b([A-Z]{5}[0-9]{4}[A-Z]{1})\b", self.extracted_text)
        return match.group(1) if match else "PAN Not Detected"

    def _extract_field(self, pattern: str, default: str = "") -> str:
        match = re.search(pattern, self.extracted_text, re.IGNORECASE)
        if match:
            val = match.group(1).split("\n")[0].strip()
            return val if len(val) > 2 else default
        return default

    def _extract_amount(self, pattern: str) -> float:
        match = re.search(pattern, self.extracted_text, re.IGNORECASE)
        if match:
            clean_str = match.group(1).replace(",", "").strip()
            try:
                return float(clean_str)
            except ValueError:
                return 0.0
        return 0.0

    def validate_arrear_trap(self, extracted_basic: float, expected_matrix_basic: float) -> Dict[str, Any]:
        """
        Pay Matrix + History validation:
        ₹70,800 jaise combined arrear amounts ko normal monthly basic nahi maanta.
        """
        # Agar basic pay 1.4 guna ya usse zyada detect hoti hai normal matrix basic se
        if expected_matrix_basic > 0 and extracted_basic > (expected_matrix_basic * 1.35):
            return {
                "status": "ARREAR_DETECTED",
                "extracted_value": extracted_basic,
                "retained_basic": expected_matrix_basic,
                "warning": (
                    f"Warning: Extracted Basic Pay (₹{extracted_basic:,.2f}) appears to include combined "
                    f"arrears or double salary. Retained monthly basic validated against Pay Matrix: ₹{expected_matrix_basic:,.2f}."
                )
            }

        return {
            "status": "VERIFIED",
            "extracted_value": extracted_basic,
            "retained_basic": extracted_basic,
            "warning": None
        }
