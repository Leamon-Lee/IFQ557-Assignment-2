from flask import Flask

from app.extensions import bcrypt, bootstrap, db, login_manager
from config import Config


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    from app.routes.admin_routes import admin_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.organizer_routes import organizer_bp
    from app.routes.participant_routes import participant_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(participant_bp)
    app.register_blueprint(organizer_bp)
    app.register_blueprint(admin_bp)

    return app
