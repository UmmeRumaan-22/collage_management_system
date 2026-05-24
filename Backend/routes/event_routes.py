from flask import Blueprint, render_template, request, redirect, session

from database.db_connection import cursor, db

event_bp = Blueprint("event_bp", __name__)


# ==============================
# EVENTS PAGE
# ==============================

@event_bp.route("/events")
def events():

    if "student" not in session and "admin" not in session:
        return redirect("/")

    cursor.execute("SELECT * FROM events ORDER BY event_date ASC")

    all_events = cursor.fetchall()

    return render_template(
        "events.html",
        events=all_events
    )


# ==============================
# ADD EVENT (ADMIN ONLY)
# ==============================

@event_bp.route("/add-event", methods=["GET", "POST"])
def add_event():

    if "admin" not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]
        venue = request.form["venue"]
        description = request.form["description"]
        department_id = request.form["department_id"]

        query = """
        INSERT INTO events
        (
            event_name,
            event_date,
            event_time,
            venue,
            description,
            department_id
        )
        VALUES(%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                event_name,
                event_date,
                event_time,
                venue,
                description,
                department_id
            )
        )

        db.commit()

        return redirect("/events")

    return render_template("add_event.html")


# ==============================
# NOTICES PAGE
# ==============================

@event_bp.route("/notices")
def notices():

    if "student" not in session and "admin" not in session:
        return redirect("/")

    # Fetch notices from database
    cursor.execute("""
        SELECT * FROM notices
        ORDER BY notice_id DESC
    """)

    all_notices = cursor.fetchall()

    return render_template(
        "notices.html",
        notices=all_notices
    )


# ==============================
# ADD NOTICE (ADMIN ONLY)
# ==============================

@event_bp.route("/add-notice", methods=["GET", "POST"])
def add_notice():

    if "admin" not in session:
        return redirect("/admin-login")

    if request.method == "POST":

        title = request.form["title"]
        message = request.form["message"]

        query = """
        INSERT INTO notices(title, message)
        VALUES(%s,%s)
        """

        cursor.execute(query, (title, message))

        db.commit()

        return redirect("/notices")

    return render_template("add_notice.html")