from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for

from app.extensions import bcrypt, bootstrap, db, login_manager
from config import Config


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    bootstrap.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Authentication required.", "errors": {}}), 401
        return redirect(url_for("auth.login"))

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    from app.routes.admin_routes import admin_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.api_auth_routes import api_auth_bp
    from app.routes.api_booking_routes import api_booking_bp
    from app.routes.api_event_routes import api_event_bp
    from app.routes.api_organizer_routes import api_organizer_bp
    from app.routes.event_routes import event_bp
    from app.routes.organizer_routes import organizer_bp
    from app.routes.participant_routes import participant_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(api_event_bp)
    app.register_blueprint(api_booking_bp)
    app.register_blueprint(api_organizer_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(participant_bp)
    app.register_blueprint(organizer_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    return app
