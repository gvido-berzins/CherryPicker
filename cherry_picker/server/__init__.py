from pathlib import Path

from flask import Flask

MODULE_PATH = Path(__file__).parent
CONFIG_PATH = MODULE_PATH / "config.py"


def create_app(config_filename: Path = CONFIG_PATH) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from cherry_picker.server.views import home

    app.register_blueprint(home)
    return app
