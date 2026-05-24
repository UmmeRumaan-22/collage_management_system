from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from database.db_connection import cursor, db

attendance_bp = Blueprint(
    "attendance_bp",
    __name__
)

# =========================================
# STUDENT ATTENDANCE
# =========================================

@attendance_bp.route(
    "/attendance",
    methods=["GET", "POST"]
)
def attendance():

    # Student login required
    if "student" not in session:
        return redirect("/student-login")

    student_email = session["student_email"]

    # Fetch student
    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE email=%s
        """,
        (student_email,)
    )

    student = cursor.fetchone()

    # Submit attendance
    if request.method == "POST":

        status = request.form["status"]

        # Prevent duplicate attendance
        cursor.execute(
            """
            SELECT *
            FROM attendance

            WHERE student_id=%s
            AND attendance_date=CURDATE()
            """,
            (student["student_id"],)
        )

        existing = cursor.fetchone()

        if not existing:

            query = """
            INSERT INTO attendance
            (
                student_id,
                status,
                attendance_date
            )
            VALUES(%s,%s,CURDATE())
            """

            cursor.execute(
                query,
                (
                    student["student_id"],
                    status
                )
            )

            db.commit()

    # Fetch attendance records
    cursor.execute(
        """
        SELECT *
        FROM attendance

        WHERE student_id=%s

        ORDER BY attendance_id DESC
        """,
        (student["student_id"],)
    )

    attendance_records = cursor.fetchall()

    return render_template(
        "attendance.html",

        attendance_records=attendance_records
    )


# =========================================
# ADMIN MANAGE ATTENDANCE
# =========================================

@attendance_bp.route("/manage-attendance")
def manage_attendance():

    # ADMIN login required
    if "admin" not in session:
        return redirect("/admin-login")

    query = """

    SELECT

        attendance.attendance_id,
        attendance.status,
        attendance.attendance_date,

        students.name,
        students.email

    FROM attendance

    JOIN students

    ON attendance.student_id = students.student_id

    ORDER BY attendance.attendance_id DESC

    """

    cursor.execute(query)

    records = cursor.fetchall()

    return render_template(
        "manage_attendance.html",
        records=records
    )


# =========================================
# UPDATE ATTENDANCE
# =========================================

@attendance_bp.route(
    "/update-attendance/<int:id>",
    methods=["POST"]
)
def update_attendance(id):

    # Only admin
    if "admin" not in session:
        return redirect("/admin-login")

    status = request.form["status"]

    query = """
    UPDATE attendance

    SET status=%s

    WHERE attendance_id=%s
    """

    cursor.execute(
        query,
        (
            status,
            id
        )
    )

    db.commit()

    return redirect("/manage-attendance")