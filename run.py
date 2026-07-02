import os
from pathlib import Path

from app import create_app
from app.extensions import db
import app.models


app = create_app()
need = True


def rebuild_database() -> None:
    database_path = Path(app.instance_path) / "music_event.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    if database_path.exists():
        try:
            database_path.unlink()
        except PermissionError:
            pass
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    if need is True and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        rebuild_database()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=not need)
