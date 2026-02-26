# Student Management API

A RESTful API built with FastAPI and SQLite to manage student records.  
The API supports full CRUD operations and filtering by major and GPA threshold.  
All data is stored in a persistent SQLite database.

---

## Features

- Create, read, update, and delete students
- Filter students by major
- Filter students by minimum GPA
- Input validation (GPA range, required fields, valid email)
- Proper HTTP status codes (200, 201, 400, 404)
- Persistent data storage

---

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### GET /students  
Returns all students.

### GET /students/{student_id}  
Returns a specific student by ID.  
Returns 404 if not found.

### POST /students  
Creates a new student.  
Returns 201 Created.

### PUT /students/{student_id}  
Updates an existing student.  
Returns 404 if the student does not exist.

### DELETE /students/{student_id}  
Deletes a student.  
Returns 404 if the student does not exist.

### GET /students/by-major?major=Computer Science  
Returns students matching the exact major.

### GET /students/by-gpa?min_gpa=3.5  
Returns students with GPA greater than or equal to the given value.  
Returns 400 if GPA is outside 0.0–4.0.

---

## Validation Rules

- Name must not be empty
- Major must not be empty
- GPA must be between 0.0 and 4.0
- Enrollment year must be a 4-digit year
- Email must be a valid email format

Invalid input returns a 400 Bad Request response.  
If a student ID does not exist, a 404 Not Found response is returned.

---

## Testing

1. Start the server.
2. Open `http://127.0.0.1:8000/docs`
3. Use the interactive interface to test each endpoint.
4. Restart the server to confirm that data persists.

---

## Notes

- The SQLite database file (`students.db`) is created automatically.
- The database file and virtual environment are excluded from version control.
- All route logic is implemented in `routes.py`.