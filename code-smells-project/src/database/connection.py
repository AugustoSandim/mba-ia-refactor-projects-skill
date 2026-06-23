import sqlite3
from flask import g, current_app


def get_db():
    if "db_connection" not in g:
        connection = sqlite3.connect(current_app.config["DB_PATH"])
        connection.row_factory = sqlite3.Row
        g.db_connection = connection
    return g.db_connection


def close_db(_error=None):
    connection = g.pop("db_connection", None)
    if connection is not None:
        connection.close()


def init_app(app):
    app.teardown_appcontext(close_db)

