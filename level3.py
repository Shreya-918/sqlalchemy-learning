#============================================================
# LEVEL 3 -Relationships
#
# Topics:
# 1. ForeignKey
# 2. relationship()
# 3. back_populates
# 4. One-to-Many
# 5. One-to-One
# 6. Many-to-Many
# Database:
# SQLALchemy.db
# ============================================================
from fastapi import FastAPI, Depends
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker,
    relationship
)
# =====================================================
# 1. DATABASE
# =====================================================

DATABASE_URL="sqlite:///./SQLALchemy.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

# =====================================================
# 2. BASE
# =====================================================


class Base(DeclarativeBase):
    pass

# =====================================================
# 3. DEPARTMENT MODEL
# =====================================================

class Department(Base):
    __table__="level3_departments"

    department_id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True
    )

    department_name:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )

     # One Department → Many Employees
    employees:Mapped[list["Employee"]]=relationship(
           "Employee",
           back_populates="departments"

    )

 
# =====================================================
# 4. EMPLOYEE MODEL
# =====================================================
class Employee(Base):
    __table__="level3_employees"

    employee_id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True
    )  

    employee_name:Mapped[str]=mapped_column(
        String,
        nullable=False
    )

    salary:Mapped[int]=mapped_column(
        Integer,
        nullable=False
    )

      # Foreign Key
    department_id:Mapped[int]=mapped_column(
        ForeignKey("level3_departments.department_id")
    )
    # Many Employees → One Department
    department:Mapped["Department"]=relationship(
        "Department",
        back_populates="employees"
    )

# =====================================================
# 5. ONE-TO-ONE: EMPLOYEE PROFILE
# =====================================================

class EmployeeProfile(Base):

    __tablename__ = "level3_employee_profiles"

    profile_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("level3_employees.employee_id"),
        unique=True
    )

    employee: Mapped["Employee"] = relationship(
        "Employee"
    )

# =====================================================
# 6. PROJECT MODEL
# =====================================================

class Project(Base):

    __tablename__ = "level3_projects"

    project_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        secondary="level3_employee_projects"
    )


# =====================================================
# 7. MANY-TO-MANY ASSOCIATION TABLE
# =====================================================

class EmployeeProject(Base):

    __tablename__ = "level3_employee_projects"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("level3_employees.employee_id"),
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("level3_projects.project_id"),
        primary_key=True
    )


# =====================================================
# 8. CREATE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# 9. SESSION
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =====================================================
# 10. DATABASE DEPENDENCY
# =====================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================================
# 11. FASTAPI
# =====================================================

app = FastAPI(title="SQLAlchemy Level 3")
