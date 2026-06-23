import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    DB_PATH = os.getenv("DB_PATH", "loja.db")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin-dev-token")

