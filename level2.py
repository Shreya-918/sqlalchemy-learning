#============================================================
# LEVEL 2 -Querying & Filtering
#
# Topics:
# 1. select()
# 2. where
# 3. order_by()
# 4. limit()
# 5. offset()
# 6. Filtering with conditions
# 7.Combining conditions
# Database:
# SQLALchemy.db
# ============================================================
from fastapi import FastAPI,Depends
from sqlalchemy import create_engine,String,Integer,select
from sqlalchemy.orm import(
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    sessionmaker
)

# -----------------------------
# 1. DATABASE
# -----------------------------

DATABASE_URL = "sqlite:///./SQLALchemy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# -----------------------------
# 2. BASE
# -----------------------------

class Base(DeclarativeBase):
    pass

# -----------------------------
# 3. MODEL
# -----------------------------

class Employee(Base):

    __tablename__ = "level2_employees"

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
# -----------------------------
# 4. CREATE TABLE
# -----------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------
# 5. SESSION
# -----------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# -----------------------------
# 6. DATABASE DEPENDENCY
# -----------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# -----------------------------
# 7. FASTAPI
# -----------------------------

app = FastAPI(title="SQLAlchemy Level 2")

# =====================================================
# INSERT SAMPLE DATA
# =====================================================

@app.post("/employees")
def create_employees(db: Session = Depends(get_db)):

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
        "message": "Employees inserted successfully"
    }


# =====================================================
# 1. SELECT
# =====================================================

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):

    statement = select(Employee)

    employees = db.scalars(statement).all()

    return employees
# =====================================================
# 2. WHERE
# =====================================================

@app.get("/employees/high-salary")
def high_salary(db: Session = Depends(get_db)):

    statement = select(Employee).where(
        Employee.salary > 55000
    )

    employees = db.scalars(statement).all()

    return employees

# =====================================================
# 3. ORDER BY - ASCENDING
# =====================================================
@app.get("/employees/salary-low-to-high")
def salary_low_to_high(db:Session=Depends(get_db)):
    statement=select(Employee).order_by(
        Employee.salary
    )

    employees=db.scalars(statement).all()

    return employees

# =====================================================
# 4. ORDER BY - DESCENDING
# =====================================================
@app.get("/employees/salary-high-to-low")
def salary_high_to_low(db:Session=Depends(get_db)):
    statement=select(Employee).order_by(
       Employee.salary.desc()
    )

    employees=db.scalars(statement).all

    return employees

# =====================================================
# 5. LIMIT
# =====================================================
@app.get("/employees/top-3")
def top_three(db:Session=Depends(get_db)):
    statement=(
        select(Employee)
        .order_by(Employee.salary.desc())
        .limit(3)
    )

    employees=db.scalars(statement).all

    return employees

# =====================================================
# 6. OFFSET
# =====================================================

@app.get("/employees/skip-2")
def skip_two(db: Session = Depends(get_db)):

    statement = (
        select(Employee)
        .order_by(Employee.employee_id)
        .offset(2)
    )

    employees = db.scalars(statement).all()

    return employees


# =====================================================
# 7. LIMIT + OFFSET
# =====================================================

@app.get("/employees/page")
def pagination(db: Session = Depends(get_db)):

    statement = (
        select(Employee)
        .order_by(Employee.employee_id)
        .offset(2)
        .limit(2)
    )

    employees = db.scalars(statement).all()

    return employees
# =====================================================
# 8. MULTIPLE CONDITIONS
# =====================================================

@app.get("/employees/filter")
def filter_employees(db: Session = Depends(get_db)):

    statement = select(Employee).where(
        Employee.salary >= 50000,
        Employee.salary <= 60000
    )

    employees = db.scalars(statement).all()

    return employees
