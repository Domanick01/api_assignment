from fastapi import APIRouter, HTTPException
from models import Student
from database import get_connection

router = APIRouter()


def _validate_student(student: Student) -> None:
    if not student.name or not student.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if not student.major or not student.major.strip():
        raise HTTPException(status_code=400, detail="Major is required")
    if student.gpa < 0.0 or student.gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")
    if student.enrollment_year < 1000 or student.enrollment_year > 9999:
        raise HTTPException(status_code=400, detail="Enrollment year must be a 4-digit year")


@router.get("/students")
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    students = [dict(row) for row in rows]
    conn.close()
    return {"students": students, "count": len(students)}


@router.get("/students/by-major")
def get_students_by_major(major: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE major = ?", (major,))
    rows = cursor.fetchall()
    students = [dict(row) for row in rows]
    conn.close()
    return {"students": students, "count": len(students), "major": major}


@router.get("/students/by-gpa")
def get_students_by_gpa(min_gpa: float):
    if min_gpa < 0.0 or min_gpa > 4.0:
        raise HTTPException(status_code=400, detail="GPA must be between 0.0 and 4.0")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE gpa >= ?", (min_gpa,))
    rows = cursor.fetchall()
    students = [dict(row) for row in rows]
    conn.close()
    return {"students": students, "count": len(students), "min_gpa": min_gpa}


@router.get("/students/{student_id}")
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return dict(row)


@router.post("/students", status_code=201)
def create_student(student: Student):
    _validate_student(student)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, major, gpa, enrollment_year) VALUES (?, ?, ?, ?, ?)",
        (student.name.strip(), student.email, student.major.strip(), student.gpa, student.enrollment_year),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM students WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)


@router.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    _validate_student(student)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    existing = cursor.fetchone()
    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")

    cursor.execute(
        "UPDATE students SET name = ?, email = ?, major = ?, gpa = ?, enrollment_year = ? WHERE id = ?",
        (student.name.strip(), student.email, student.major.strip(), student.gpa, student.enrollment_year, student_id),
    )
    conn.commit()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)


@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
    return {"message": "Student deleted successfully"}