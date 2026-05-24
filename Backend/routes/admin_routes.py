from flask import Blueprint, render_template, request, redirect, session

from database.db_connection import cursor, db

admin_bp = Blueprint("admin_bp", __name__)


# ==============================
# ADMIN REGISTER
# ==============================

@admin_bp.route("/admin-register", methods=["GET", "POST"])
def admin_register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Check existing admin
        check_query = """
        SELECT * FROM admin
        WHERE username=%s
        """

        cursor.execute(check_query, (username,))

        existing_admin = cursor.fetchone()

        if existing_admin:

            message = "Admin already exists"

            return render_template(
                "admin_register.html",
                message=message
            )

        # Insert admin
        insert_query = """
        INSERT INTO admin(username, password)
        VALUES(%s,%s)
        """

        cursor.execute(
            insert_query,
            (username, password)
        )

        db.commit()

        return redirect("/admin-login")

    return render_template(
        "admin_register.html",
        message=message
    )


# ==============================
# ADMIN LOGIN
# ==============================

@admin_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        query = """
        SELECT * FROM admin
        WHERE username=%s AND password=%s
        """

        cursor.execute(query, (username, password))

        admin = cursor.fetchone()

        if admin:

            session["admin"] = admin["username"]

            return redirect("/admin-dashboard")

        else:

            message = "Invalid Username or Password"

    return render_template(
        "admin_login.html",
        message=message
    )


# ==============================
# ADMIN DASHBOARD
# ==============================

@admin_bp.route("/admin-dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin-login")

    # Total Students
    cursor.execute(
        "SELECT COUNT(*) AS total_students FROM students"
    )
    students = cursor.fetchone()

    # Total Events
    cursor.execute(
        "SELECT COUNT(*) AS total_events FROM events"
    )
    events = cursor.fetchone()

    # Total Departments
    cursor.execute(
        "SELECT COUNT(*) AS total_departments FROM departments"
    )
    departments = cursor.fetchone()

    # Fetch Feedbacks with Student Names
    cursor.execute("""

        SELECT
            feedback.feedback_id,
            feedback.message,
            feedback.submitted_at,
            students.name

        FROM feedback

        JOIN students
        ON feedback.student_id = students.student_id

        ORDER BY feedback.feedback_id DESC

    """)

    feedbacks = cursor.fetchall()

    return render_template(

        "admin_dashboard.html",

        total_students=students["total_students"],

        total_events=events["total_events"],

        total_departments=departments["total_departments"],

        feedbacks=feedbacks,

        admin_name=session["admin"]
    )