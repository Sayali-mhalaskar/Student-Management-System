from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

app = FastAPI()


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PostgreSQL connection
# connection = psycopg2.connect(
#     host=os.getenv("DB_HOST"),
#     database=os.getenv("DB_DATABASE"),
#     port=os.getenv("DB_PORT"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     sslmode="require"
# )

connection = psycopg2.connect(

'postgresql://neondb_owner:npg_qQxI58PSmnJM@ep-crimson-silence-b343stkm-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
# Create cursor
cursor = connection.cursor()


# Pydantic model for Student
class Student(BaseModel):
    id: int
    name: str
    course: str


# Pydantic model for PATCH
class StudentUpdate(BaseModel):
    id: int | None = None
    name: str | None = None
    course: str | None = None


# --------------------------------------------------
# GET ALL STUDENTS
# --------------------------------------------------

@app.get("/students")
def get_all_students():

    try:
        cursor.execute("SELECT id, name, course FROM students")
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({
                "id": row[0],
                "name": row[1],
                "course": row[2]
            })

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# GET SINGLE STUDENT
# --------------------------------------------------

@app.get("/students/{id}")
def get_single_student(id: int):

    try:
        cursor.execute(
            "SELECT id, name, course FROM students WHERE id=%s",
            (id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "id": row[0],
            "name": row[1],
            "course": row[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# CREATE STUDENT
# --------------------------------------------------

@app.post("/students", status_code=201)
def create_student_record(student: Student):

    try:
        cursor.execute(
            """
            INSERT INTO students (id, name, course)
            VALUES (%s, %s, %s)
            """,
            (
                student.id,
                student.name,
                student.course
            )
        )

        connection.commit()

        return {
            "message": "Student record created successfully",
            "student": student
        }

    except psycopg2.IntegrityError:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail="Student with this ID already exists"
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# UPDATE COMPLETE STUDENT
# --------------------------------------------------

@app.put("/students/{id}")
def update_student_record(id: int, student: Student):

    try:
        cursor.execute(
            """
            UPDATE students
            SET id=%s, name=%s, course=%s
            WHERE id=%s
            """,
            (
                student.id,
                student.name,
                student.course,
                id
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "message": "Student record updated successfully"
        }

    except HTTPException:
        raise

    except psycopg2.IntegrityError:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail="Student with this ID already exists"
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# PARTIAL UPDATE STUDENT
# --------------------------------------------------

@app.patch("/students/{id}")
def update_student_partial_record(
    id: int,
    student: StudentUpdate
):

    try:

        # Check whether student exists
        cursor.execute(
            "SELECT id FROM students WHERE id=%s",
            (id,)
        )

        existing_student = cursor.fetchone()

        if existing_student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )


        # Update only provided fields
        if student.name is not None:

            cursor.execute(
                """
                UPDATE students
                SET name=%s
                WHERE id=%s
                """,
                (student.name, id)
            )


        if student.course is not None:

            cursor.execute(
                """
                UPDATE students
                SET course=%s
                WHERE id=%s
                """,
                (student.course, id)
            )


        if student.id is not None:

            cursor.execute(
                """
                UPDATE students
                SET id=%s
                WHERE id=%s
                """,
                (student.id, id)
            )


        connection.commit()

        return {
            "message": "Partial student record updated successfully"
        }

    except HTTPException:
        raise

    except psycopg2.IntegrityError:

        connection.rollback()

        raise HTTPException(
            status_code=400,
            detail="Student with this ID already exists"
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------

@app.delete("/students/{id}")
def delete_student_record(id: int):

    try:

        cursor.execute(
            "DELETE FROM students WHERE id=%s",
            (id,)
        )

        if cursor.rowcount == 0:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "message": "Student record deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )