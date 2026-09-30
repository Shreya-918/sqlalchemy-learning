# SQLAlchemy Level 1- Engine , Base , Session and CRUD
# ============================================================
# LEVEL 1 - SQLALCHEMY FUNDAMENTALS
#
# Topics:
# 1. Engine
# 2. Base
# 3. mapped_column
# 4. Session
# 5. create_all
# 6. CRUD
#
# Database:
# SQLALchemy.db
# ============================================================
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import create_engine, String, Integer, select

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker
)

# ============================================================
# 1. ENGINE
# ============================================================
#it creates the connection configuration between your python application and database
DATABASE_URL = "sqlite:///./SQLALchemy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ============================================================
# 2. BASE
# ============================================================
#DeclarativeBase is provided by SQLAlchemy. It is the base class for your database models.
class Base(DeclarativeBase):
    pass


# ============================================================
# 3. MODEL / TABLE
# ============================================================

class Employee(Base):

    __tablename__ = "level1_employees"

    employee_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    employee_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    salary: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


# ============================================================
# 4. CREATE TABLE
# ============================================================
#create those tables in database
Base.metadata.create_all(bind=engine)


# ============================================================
# 5. SESSION
# ============================================================
#A Session is basically your working connection with the database through SQLAlchemy ORM.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ============================================================
# 6. FASTAPI
# ============================================================

app = FastAPI(
    title="SQLAlchemy Level 1"
)


# ============================================================
# 7. DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ============================================================
# CREATE
# ============================================================

@app.post("/employees")
def create_employee(
    employee_name: str,
    salary: int,
    db: Session = Depends(get_db)
):

    employee = Employee(
        employee_name=employee_name,
        salary=salary
    )

    db.add(employee)
#"I want to insert this object into the database."
    db.commit()
#ORM converts the object into SQL roughly 
    db.refresh(employee)
#refresh() gets the latest database values back into the Python object.

    return {
        "message": "Employee created successfully",
        "employee_id": employee.employee_id,
        "employee_name": employee.employee_name,
        "salary": employee.salary
    }


# ============================================================
# READ - ALL
# ============================================================

@app.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):

    statement = select(Employee)

    employees = db.scalars(statement).all()

    return [
        {
            "employee_id": employee.employee_id,
            "employee_name": employee.employee_name,
            "salary": employee.salary
        }
        for employee in employees
    ]


# ============================================================
# READ - ONE
# ============================================================

@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.get(
        Employee,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "employee_id": employee.employee_id,
        "employee_name": employee.employee_name,
        "salary": employee.salary
    }


# ============================================================
# UPDATE
# ============================================================

@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_name: str,
    salary: int,
    db: Session = Depends(get_db)
):

    employee = db.get(
        Employee,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.employee_name = employee_name

    employee.salary = salary

    db.commit()

    db.refresh(employee)

    return {
        "message": "Employee updated successfully",
        "employee_id": employee.employee_id,
        "employee_name": employee.employee_name,
        "salary": employee.salary
    }


# ============================================================
# DELETE
# ============================================================

@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = db.get(
        Employee,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)

    db.commit()

    return {
        "message": "Employee deleted successfully"
    }


# ============================================================
# EXTRA PRACTICE:
# ADD MULTIPLE EMPLOYEES
# ============================================================

@app.post("/employees/bulk")
def create_multiple_employees(
    db: Session = Depends(get_db)
):

    employees = [

        Employee(
            employee_name="Shreya",
            salary=60000
        ),

        Employee(
            employee_name="Rahul",
            salary=50000
        ),

        Employee(
            employee_name="Priya",
            salary=45000
        ),

        Employee(
            employee_name="Amit",
            salary=70000
        ),

        Employee(
            employee_name="Sneha",
            salary=55000
        )
    ]

    db.add_all(employees)

    db.commit()

    return {
        "message": "Multiple employees inserted successfully"
    }

