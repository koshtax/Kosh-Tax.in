from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import (
    EmployeeProfile,
    EmployeeFYRecord,
    TANMaster,
    SalaryMonthlyLedger,
)


class EmployeeRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_pan(self, pan: str):
        pan = pan.strip().upper()

        return self.session.scalar(
            select(EmployeeProfile)
            .where(EmployeeProfile.pan == pan)
        )

    def create(self, employee: EmployeeProfile):
        self.session.add(employee)
        self.session.flush()
        return employee

    def get_fy_record(
        self,
        employee_id: int,
        financial_year: str,
    ):
        return self.session.scalar(
            select(EmployeeFYRecord)
            .where(
                EmployeeFYRecord.employee_id == employee_id,
                EmployeeFYRecord.financial_year == financial_year,
            )
        )


class TANRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_tan(self, tan: str):
        tan = tan.strip().upper()

        return self.session.scalar(
            select(TANMaster)
            .where(TANMaster.tan == tan)
        )


class LedgerRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_month(
        self,
        employee_fy_id: int,
        month: int,
        year: int,
    ):
        return self.session.scalar(
            select(SalaryMonthlyLedger)
            .where(
                SalaryMonthlyLedger.employee_fy_id
                == employee_fy_id,
                SalaryMonthlyLedger.salary_month
                == month,
                SalaryMonthlyLedger.salary_year
                == year,
            )
        )
