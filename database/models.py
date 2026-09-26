from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


# ============================================================
# USERS
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="USER",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    employee_fy_records = relationship(
        "EmployeeFYRecord",
        back_populates="created_by_user",
    )


# ============================================================
# USER SESSIONS
# ============================================================

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_token_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )


# ============================================================
# EMPLOYEE
# ============================================================

class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    pan: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
    )

    designation: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    department: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    office_name: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    employee_code: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    mobile: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    fy_records = relationship(
        "EmployeeFYRecord",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


# ============================================================
# PAY MATRIX
# ============================================================

class PayMatrixVersion(Base):
    __tablename__ = "pay_matrix_versions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    version_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    cells = relationship(
        "PayMatrixCell",
        back_populates="matrix_version",
        cascade="all, delete-orphan",
    )


class PayMatrixCell(Base):
    __tablename__ = "pay_matrix_cells"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    matrix_version_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pay_matrix_versions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    pay_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    cell_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    basic_pay: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    matrix_version = relationship(
        "PayMatrixVersion",
        back_populates="cells",
    )

    __table_args__ = (
        UniqueConstraint(
            "matrix_version_id",
            "pay_level",
            "cell_number",
            name="uq_matrix_level_cell",
        ),
    )


# ============================================================
# TAX RULES
# ============================================================

class TaxRuleVersion(Base):
    __tablename__ = "tax_rule_versions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    assessment_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    tax_year: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    regime: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NEW",
    )

    standard_deduction: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    rebate_income_limit: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    rebate_max_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    cess_rate: Mapped[Decimal] = mapped_column(
        Numeric(8, 5),
        nullable=False,
    )

    surcharge_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    version_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    slabs = relationship(
        "TaxSlab",
        back_populates="tax_rule",
        cascade="all, delete-orphan",
    )


class TaxSlab(Base):
    __tablename__ = "tax_slabs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tax_rule_version_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tax_rule_versions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    lower_limit: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    upper_limit: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    tax_rate: Mapped[Decimal] = mapped_column(
        Numeric(8, 5),
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    tax_rule = relationship(
        "TaxRuleVersion",
        back_populates="slabs",
    )


# ============================================================
# SALARY COMPONENTS
# ============================================================

class SalaryComponent(Base):
    __tablename__ = "salary_components"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    component_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    component_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    taxable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    deduction: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class SalaryComponentRule(Base):
    __tablename__ = "salary_component_rules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    component_id: Mapped[int] = mapped_column(
        ForeignKey(
            "salary_components.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    calculation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    percentage: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 5),
        nullable=True,
    )

    fixed_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    base_component_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    formula: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# INCREMENT RULES
# ============================================================

class IncrementRule(Base):
    __tablename__ = "increment_rules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    increment_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    increment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    pay_matrix_based: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    matrix_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pay_matrix_versions.id"),
        nullable=True,
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    effective_to: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# EMPLOYEE FY
# ============================================================

class EmployeeFYRecord(Base):
    __tablename__ = "employee_fy_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    assessment_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    tax_year: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    tax_regime: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NEW",
    )

    tax_rule_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tax_rule_versions.id"),
        nullable=True,
    )

    pay_matrix_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pay_matrix_versions.id"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DRAFT",
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    employee = relationship(
        "EmployeeProfile",
        back_populates="fy_records",
    )

    created_by_user = relationship(
        "User",
        back_populates="employee_fy_records",
    )

    salary_slips = relationship(
        "SalarySlip",
        back_populates="employee_fy",
        cascade="all, delete-orphan",
    )

    ledger = relationship(
        "SalaryMonthlyLedger",
        back_populates="employee_fy",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "financial_year",
            name="uq_employee_fy",
        ),
    )


# ============================================================
# SALARY SLIPS
# ============================================================

class SalarySlip(Base):
    __tablename__ = "salary_slips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    stored_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    file_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    salary_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    salary_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    extraction_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UPLOADED",
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    employee_fy = relationship(
        "EmployeeFYRecord",
        back_populates="salary_slips",
    )

    extraction_results = relationship(
        "SalaryExtractionResult",
        back_populates="salary_slip",
        cascade="all, delete-orphan",
    )


class SalaryExtractionResult(Base):
    __tablename__ = "salary_extraction_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    salary_slip_id: Mapped[int] = mapped_column(
        ForeignKey(
            "salary_slips.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    extracted_value: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    normalized_value: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    confidence: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(6, 5),
        nullable=True,
    )

    source_page: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    source_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    extraction_method: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    validation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    salary_slip = relationship(
        "SalarySlip",
        back_populates="extraction_results",
    )


# ============================================================
# MONTHLY LEDGER
# ============================================================

class SalaryMonthlyLedger(Base):
    __tablename__ = "salary_monthly_ledger"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    salary_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    salary_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    basic_pay: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    gross_salary: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    total_deductions: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    net_salary: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    actual_tds: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    projected_tds: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    is_actual: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_projected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING",
    )

    projection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    source_salary_slip_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("salary_slips.id"),
        nullable=True,
    )

    verified_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    employee_fy = relationship(
        "EmployeeFYRecord",
        back_populates="ledger",
    )

    components = relationship(
        "SalaryLedgerComponent",
        back_populates="ledger",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_fy_id",
            "salary_month",
            "salary_year",
            name="uq_employee_salary_month",
        ),
    )


# ============================================================
# LEDGER COMPONENTS
# ============================================================

class SalaryLedgerComponent(Base):
    __tablename__ = "salary_ledger_components"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    ledger_id: Mapped[int] = mapped_column(
        ForeignKey(
            "salary_monthly_ledger.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    component_id: Mapped[int] = mapped_column(
        ForeignKey(
            "salary_components.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    percentage: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 5),
        nullable=True,
    )

    calculation_base: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_reference: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    ledger = relationship(
        "SalaryMonthlyLedger",
        back_populates="components",
    )

    component = relationship(
        "SalaryComponent",
    )


# ============================================================
# PROJECTION LOG
# ============================================================

class SalaryProjectionLog(Base):
    __tablename__ = "salary_projection_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    target_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    target_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    previous_basic: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    previous_pay_level: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    previous_cell: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    projected_basic: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    projected_pay_level: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    projected_cell: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    pay_matrix_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pay_matrix_versions.id"),
        nullable=True,
    )

    increment_rule_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("increment_rules.id"),
        nullable=True,
    )

    reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    input_snapshot: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    output_snapshot: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    accepted_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    accepted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# TAN / DDO MASTER
# ============================================================

class TANMaster(Base):
    __tablename__ = "tan_masters"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tan: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
    )

    officer_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    father_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    designation: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    capacity: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    office_name: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    office_address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    office_pan: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
    )

    mobile: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class TANMasterHistory(Base):
    __tablename__ = "tan_master_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    tan_master_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tan_masters.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    tan: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    officer_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    father_name: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    designation: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    capacity: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    office_name: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    office_address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    office_pan: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
    )

    snapshot_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    changed_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    change_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class EmployeeEmployerLink(Base):
    __tablename__ = "employee_employer_links"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    tan_master_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tan_masters.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    linked_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    linked_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )


# ============================================================
# FORM 16
# ============================================================

class Form16Record(Base):
    __tablename__ = "form16_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    previous_record_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("form16_records.id"),
        nullable=True,
    )

    employee_name_snapshot: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    employee_pan_snapshot: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    tan_snapshot: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    officer_name_snapshot: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    officer_father_name_snapshot: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    officer_designation_snapshot: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    capacity_snapshot: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    employer_name_snapshot: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    employer_address_snapshot: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    financial_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    assessment_year: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
    )

    tax_year: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    tax_rule_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tax_rule_versions.id"),
        nullable=True,
    )

    pay_matrix_version_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("pay_matrix_versions.id"),
        nullable=True,
    )

    gross_salary: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    standard_deduction: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    taxable_income: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    tax_before_rebate: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    rebate: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    surcharge: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    cess: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    total_tax: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    actual_tds: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    balance_tds: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    pdf_path: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    pdf_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )

    generation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DRAFT",
    )

    generation_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_fy_id",
            "version_number",
            name="uq_form16_version",
        ),
    )


class Form16GenerationLog(Base):
    __tablename__ = "form16_generation_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    form16_record_id: Mapped[int] = mapped_column(
        ForeignKey(
            "form16_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )


# ============================================================
# PAYMENTS
# ============================================================

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employee_fy_records.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    form16_record_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "form16_records.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
    )

    upi_id_snapshot: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    payee_name_snapshot: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    utr: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING_PAYMENT",
        index=True,
    )

    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    rejected_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    approved_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    rejection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    admin_remarks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    payment_reference: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    payment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "payments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    old_status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    new_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    remarks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# DOWNLOAD TOKENS
# ============================================================

class DownloadToken(Base):
    __tablename__ = "download_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    form16_record_id: Mapped[int] = mapped_column(
        ForeignKey(
            "form16_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    payment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("payments.id"),
        nullable=True,
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message_masked: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    external_message_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# EMAIL LOGS
# ============================================================

class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    employee_fy_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("employee_fy_records.id"),
        nullable=True,
    )

    form16_record_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("form16_records.id"),
        nullable=True,
    )

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    attachment_path: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    sent_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# ADMIN SETTINGS
# ============================================================

class AdminSetting(Base):
    __tablename__ = "admin_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    setting_key: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    setting_value: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    value_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    is_secret: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# AUDIT
# ============================================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    old_data: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    new_data: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# ============================================================
# SCHEMA MIGRATIONS
# ============================================================

class SchemaMigration(Base):
    __tablename__ = "schema_migrations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    migration_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        unique=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    checksum: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
    )

    applied_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
