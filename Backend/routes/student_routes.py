from flask import Blueprint, render_template, request, redirect, session

from database.db_connection import cursor, db

student_bp = Blueprint("student_bp", __name__)


# ==============================
# HOME PAGE
# ==============================

@student_bp.route("/")
def home():
    return render_template("index.html")


# ==============================
# STUDENT REGISTER
# ==============================

@student_bp.route("/student-register", methods=["GET", "POST"])
def student_register():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        department = request.form["department"]
        year = request.form["year"]

        # Check existing email
        check_query = "SELECT * FROM students WHERE email=%s"

        cursor.execute(check_query, (email,))

        existing_student = cursor.fetchone()

        if existing_student:

            message = "Email already exists"

            return render_template(
                "student_register.html",
                message=message
            )

        # Insert student
        insert_query = """
        INSERT INTO students(name, email, password, phone, department_id, year) 
        VALUES(%s,%s,%s,%s,%s,%s)"""

        cursor.execute(
            insert_query,
            (name, email, password, phone, department, year)
        )

        db.commit()

        return redirect("/student-login")

    return render_template(
        "student_register.html",
        message=message
    )


# ==============================
# STUDENT LOGIN
# ==============================

@student_bp.route("/student-login", methods=["GET", "POST"])
def student_login():

    message = ""

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        query = """
        SELECT * FROM students
        WHERE email=%s AND password=%s
        """

        cursor.execute(query, (email, password))

        student = cursor.fetchone()

        if student:

            session["student"] = student["name"]
            session["student_email"] = student["email"]

            return redirect("/student-dashboard")

        else:

            message = "Invalid Email or Password"

    return render_template(
        "student_login.html",
        message=message
    )


# ==============================
# STUDENT DASHBOARD
# ==============================

@student_bp.route("/student-dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/student-login")

    student_email = session["student_email"]

    # Fetch Student Details
    query = """
    SELECT *
    FROM students
    WHERE email=%s
    """

    cursor.execute(query, (student_email,))

    student = cursor.fetchone()

    # Fetch Events
    cursor.execute("""
        SELECT *
        FROM events
        ORDER BY event_date ASC
    """)

    events = cursor.fetchall()

    # Fetch Notices
    cursor.execute("""
        SELECT *
        FROM notices
        ORDER BY notice_id DESC
    """)

    notices = cursor.fetchall()

    return render_template(

        "student_dashboard.html",

        student=student,

        events=events,

        notices=notices
    )

# ==============================
# LOGOUT
# ==============================

@student_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")