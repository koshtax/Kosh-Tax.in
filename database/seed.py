from database.database import SessionLocal
from database.models import SalaryComponent


COMPONENTS = [
    ("BASIC", "Basic Pay", "EARNING", True, False),
    ("DA", "Dearness Allowance", "EARNING", True, False),
    ("HRA", "House Rent Allowance", "EARNING", True, False),
    ("TA", "Transport Allowance", "EARNING", True, False),
    ("MEDICAL", "Medical", "EARNING", True, False),
    ("ARREAR", "Arrear", "EARNING", True, False),
    ("OTHER_ALLOWANCE", "Other Allowance", "EARNING", True, False),

    ("NPS", "NPS", "DEDUCTION", False, True),
    ("GPF", "GPF", "DEDUCTION", False, True),
    ("GIS", "GIS", "DEDUCTION", False, True),
    ("PTAX", "Professional Tax", "DEDUCTION", False, True),
    ("TDS", "TDS", "DEDUCTION", False, True),
    ("OTHER_DEDUCTION", "Other Deduction", "DEDUCTION", False, True),
]


def seed_components():

    db = SessionLocal()

    try:
        for code, name, category, taxable, deduction in COMPONENTS:

            exists = db.query(
                SalaryComponent
            ).filter(
                SalaryComponent.component_code == code
            ).first()

            if exists:
                continue

            db.add(
                SalaryComponent(
                    component_code=code,
                    component_name=name,
                    category=category,
                    taxable=taxable,
                    deduction=deduction,
                )
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_components()
    print("Seed complete.")
