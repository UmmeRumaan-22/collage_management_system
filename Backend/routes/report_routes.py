from flask import Blueprint, render_template
from database.db_connection import cursor

report_bp = Blueprint("report_bp", __name__)

@report_bp.route("/reports")
def reports():

    cursor.execute("SELECT COUNT(*) AS total_students FROM students")
    students = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_events FROM events")
    events = cursor.fetchone()

    return render_template(
        "reports.html",
        students=students,
        events=events
    )