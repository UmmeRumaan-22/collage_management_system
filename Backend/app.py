from flask import Flask

from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.event_routes import event_bp
from routes.attendance_routes import attendance_bp
from routes.feedback_routes import feedback_bp
from routes.report_routes import report_bp

app = Flask(

    __name__,

    template_folder="../frontend/templates",

    static_folder="../frontend/static"
)

app.secret_key = "secretkey"

# Register Blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)
app.register_blueprint(event_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(report_bp)

if __name__ == "__main__":
    app.run(debug=True)