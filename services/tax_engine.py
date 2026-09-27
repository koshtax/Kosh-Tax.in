from decimal import Decimal, ROUND_HALF_UP

class TaxEngine:
    def __init__(self):
        self.standard_deduction = Decimal("75000.00")
        self.rebate_limit = Decimal("1200000.00") # FY 2025-26 New Tax Regime threshold
        self.cess_rate = Decimal("0.04")

    def round_currency(self, amount: Decimal) -> Decimal:
        return amount.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)

    def calculate_tax(self, gross_salary: Decimal, actual_tds_paid: Decimal) -> dict:
        gross_salary = Decimal(str(gross_salary))
        actual_tds_paid = Decimal(str(actual_tds_paid))

        taxable_income = max(Decimal("0.00"), gross_salary - self.standard_deduction)
        
        # Round to nearest 10 as per Income Tax Act section 288A
        taxable_income = Decimal(round(float(taxable_income) / 10.0) * 10)

        # FY 2025-26 New Slabs as seen in tds1.pdf[cite: 11]
        slab1_tax = Decimal("0.00") # 4L - 8L @ 5%
        slab2_tax = Decimal("0.00") # 8L - 12L @ 10%
        slab3_tax = Decimal("0.00") # 12L - 16L @ 15%
        slab4_tax = Decimal("0.00") # 16L - 20L @ 20%
        slab5_tax = Decimal("0.00") # 20L - 24L @ 25%
        slab6_tax = Decimal("0.00") # Above 24L @ 30%

        if taxable_income > Decimal("400000.00"):
            amount = min(taxable_income, Decimal("800000.00")) - Decimal("400000.00")
            slab1_tax = amount * Decimal("0.05")

        if taxable_income > Decimal("800000.00"):
            amount = min(taxable_income, Decimal("1200000.00")) - Decimal("800000.00")
            slab2_tax = amount * Decimal("0.10")

        if taxable_income > Decimal("1200000.00"):
            amount = min(taxable_income, Decimal("1600000.00")) - Decimal("1200000.00")
            slab3_tax = amount * Decimal("0.15")

        if taxable_income > Decimal("1600000.00"):
            amount = min(taxable_income, Decimal("2000000.00")) - Decimal("1600000.00")
            slab4_tax = amount * Decimal("0.20")

        tax_before_rebate = slab1_tax + slab2_tax + slab3_tax + slab4_tax + slab5_tax + slab6_tax

        # Section 87A Relief Logic[cite: 11]
        rebate_87a = Decimal("0.00")
        if taxable_income <= self.rebate_limit:
            rebate_87a = tax_before_rebate

        tax_after_rebate = max(Decimal("0.00"), tax_before_rebate - rebate_87a)
        cess_amount = self.round_currency(tax_after_rebate * self.cess_rate)
        total_tax = tax_after_rebate + cess_amount

        # February Balancing TDS (Remaining tax to be deducted)[cite: 10]
        balance_tds = total_tax - actual_tds_paid

        return {
            "gross_salary": float(gross_salary),
            "standard_deduction": float(self.standard_deduction),
            "taxable_income": float(taxable_income),
            "tax_slab_1": float(slab1_tax),
            "tax_slab_2": float(slab2_tax),
            "tax_slab_3": float(slab3_tax),
            "tax_before_rebate": float(tax_before_rebate),
            "rebate_87a": float(rebate_87a),
            "tax_after_rebate": float(tax_after_rebate),
            "cess_amount": float(cess_amount),
            "total_tax": float(total_tax),
            "actual_tds": float(actual_tds_paid),
            "balance_tds": float(balance_tds)
        }
