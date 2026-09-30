#============================================================
# LEVEL 4-SQL queries involving multiple tables and calculations.
#
# JOIN
#OUTER JOIN
#GROUP BY
#HAVING
#COUNT
#AVG
#SUM
#MIN
#MAX
# Database:
# SQLALchemy.db
# ============================================================


from fastapi import FastAPI, Depends
from sqlalchemy import (
    create_engine,
    String,
    Integer,
    ForeignKey,
    select,
    func
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker
)


# =====================================================
# 1. DATABASE
# =====================================================

DATABASE_URL="sqlite:///./SQLALchemey.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_smae_thread":False}
)

# =====================================================
# 2. BASE
# =====================================================

class Base(DeclarativeBase):
    pass

# =====================================================
# 3. DEPARTMENT
# =====================================================

class Department(Base):

    __tablename__ = "level4_departments"

    department_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

# =====================================================
# 4. EMPLOYEE
# =====================================================

class Employee(Base):

    __tablename__ = "level4_employees"

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

    department_id: Mapped[int] = mapped_column(
        ForeignKey("level4_departments.department_id"),
        nullable=False
    )
# =====================================================
# 5. CREATE TABLES
# =====================================================

Base.metadata.create_all(bind=engine)

# =====================================================
# 6. SESSION
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =====================================================
# 7. FASTAPI
# =====================================================

app = FastAPI(title="SQLAlchemy Level 4")


# =====================================================
# INSERT SAMPLE DATA
# =====================================================

@app.post("/insert-data")
def insert_data(db: Session = Depends(get_db)):

    departments = [
        Department(
            department_name="IT"
        ),
        Department(
            department_name="HR"
        ),
        Department(
            department_name="Finance"
        )
    ]

    db.add_all(departments)
    db.commit()

    employees = [

        Employee(
            employee_name="Shreya",
            salary=60000,
            department_id=1
        ),

        Employee(
            employee_name="Rahul",
            salary=50000,
            department_id=1
        ),

        Employee(
            employee_name="Priya",
            salary=45000,
            department_id=2
        ),

        Employee(
            employee_name="Amit",
            salary=70000,
            department_id=3
        ),

        Employee(
            employee_name="Sneha",
            salary=55000,
            department_id=2
        )
    ]

    db.add_all(employees)
    db.commit()

    return {
        "message": "Data inserted successfully"
    }


# =====================================================
# 1. INNER JOIN
# =====================================================

@app.get("/join")
def inner_join(db: Session = Depends(get_db)):

    statement = (
        select(
            Employee.employee_name,
            Employee.salary,
            Department.department_name
        )
        .join(
            Department,
            Employee.department_id == Department.department_id
        )
    )

    result = db.execute(statement).all()

    return [
        {
            "employee_name": row.employee_name,
            "salary": row.salary,
            "department": row.department_name
        }
        for row in result
    ]


# =====================================================
# 2. OUTER JOIN
# =====================================================

@app.get("/outer-join")
def outer_join(db: Session = Depends(get_db)):

    statement = (
        select(
            Department.department_name,
            Employee.employee_name
        )
        .outerjoin(
            Employee,
            Department.department_id == Employee.department_id
        )
    )

    result = db.execute(statement).all()

    return [
        {
            "department": row.department_name,
            "employee": row.employee_name
        }
        for row in result
    ]


# =====================================================
# 3. COUNT
# =====================================================

@app.get("/employee-count")
def employee_count(db: Session = Depends(get_db)):

    statement = select(
        func.count(Employee.employee_id)
    )

    count = db.scalar(statement)

    return {
        "employee_count": count
    }


# =====================================================
# 4. GROUP BY + COUNT
# =====================================================

@app.get("/employees-by-department")
def employees_by_department(
    db: Session = Depends(get_db)
):

    statement = (
        select(
            Employee.department_id,
            func.count(Employee.employee_id)
        )
        .group_by(Employee.department_id)
    )

    result = db.execute(statement).all()

    return [
        {
            "department_id": row[0],
            "employee_count": row[1]
        }
        for row in result
    ]


# =====================================================
# 5. SUM
# =====================================================

@app.get("/total-salary")
def total_salary(db: Session = Depends(get_db)):

    statement = select(
        func.sum(Employee.salary)
    )

    total = db.scalar(statement)

    return {
        "total_salary": total
    }


# =====================================================
# 6. AVG
# =====================================================

@app.get("/average-salary")
def average_salary(db: Session = Depends(get_db)):

    statement = select(
        func.avg(Employee.salary)
    )

    average = db.scalar(statement)

    return {
        "average_salary": average
    }


# =====================================================
# 7. MIN
# =====================================================

@app.get("/minimum-salary")
def minimum_salary(db: Session = Depends(get_db)):

    statement = select(
        func.min(Employee.salary)
    )

    minimum = db.scalar(statement)

    return {
        "minimum_salary": minimum
    }


# =====================================================
# 8. MAX
# =====================================================

@app.get("/maximum-salary")
def maximum_salary(db: Session = Depends(get_db)):

    statement = select(
        func.max(Employee.salary)
    )

    maximum = db.scalar(statement)

    return {
        "maximum_salary": maximum
    }


# =====================================================
# 9. GROUP BY + AVG
# =====================================================

@app.get("/average-by-department")
def average_by_department(
    db: Session = Depends(get_db)
):

    statement = (
        select(
            Employee.department_id,
            func.avg(Employee.salary)
        )
        .group_by(Employee.department_id)
    )

    result = db.execute(statement).all()

    return [
        {
            "department_id": row[0],
            "average_salary": row[1]
        }
        for row in result
    ]


# =====================================================
# 10. GROUP BY + HAVING
# =====================================================

@app.get("/departments-high-average")
def departments_high_average(
    db: Session = Depends(get_db)
):

    statement = (
        select(
            Employee.department_id,
            func.avg(Employee.salary).label("average_salary")
        )
        .group_by(Employee.department_id)
        .having(
            func.avg(Employee.salary) > 50000
        )
    )

    result = db.execute(statement).all()

    return [
        {
            "department_id": row.department_id,
            "average_salary": row.average_salary
        }
        for row in result
    ]
