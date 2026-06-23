from flask import Flask
from flask_cors import CORS

from src.config.settings import Settings
from src.database.connection import init_app as init_db_connection
from src.database.schema import initialize_database
from src.middlewares.error_handler import register_error_handlers
from src.views.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    CORS(app)

    init_db_connection(app)
    register_error_handlers(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        initialize_database()

    return app

