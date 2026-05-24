from flask import Blueprint, render_template, request, redirect, session

from database.db_connection import cursor, db

feedback_bp = Blueprint("feedback_bp", __name__)


# ==============================
# FEEDBACK PAGE
# ==============================

@feedback_bp.route("/feedback", methods=["GET", "POST"])
def feedback():

    # Student must login
    if "student" not in session:
        return redirect("/student-login")

    if request.method == "POST":

        message = request.form["message"]

        student_email = session["student_email"]

        # Get student id
        cursor.execute(
            """
            SELECT student_id
            FROM students
            WHERE email=%s
            """,
            (student_email,)
        )

        student = cursor.fetchone()

        # Insert feedback
        query = """
        INSERT INTO feedback(student_id, message)
        VALUES(%s,%s)
        """

        cursor.execute(
            query,
            (
                student["student_id"],
                message
            )
        )

        db.commit()

        return redirect("/student-dashboard")

    return render_template("feedback.html")


# ==============================
# ADMIN VIEW FEEDBACKS
# ==============================

@feedback_bp.route("/view-feedbacks")
def view_feedbacks():

    # Only admin can access
    if "admin" not in session:
        return redirect("/admin-login")

    query = """

    SELECT

        feedback.feedback_id,
        feedback.message,
        feedback.submitted_at,
        students.name

    FROM feedback

    JOIN students
    ON feedback.student_id = students.student_id

    ORDER BY feedback.feedback_id DESC

    """

    cursor.execute(query)

    feedbacks = cursor.fetchall()

    return render_template(
        "view_feedbacks.html",
        feedbacks=feedbacks
    )