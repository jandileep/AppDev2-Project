import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DB_DIR = os.path.join(basedir, "/db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///ticket_database.sqlite3"
    DEBUG = True
    JWT_SECRET_KEY = 'super-secret' # Change this to your own secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CORS_HEADERS = 'Content-Type' 
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"
    SMPTP_SERVER_HOST = "localhost"
    SMPTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "example@mail.com"
    SENDER_PASSWORD = ""

    




class ProjectDevelopmentConfig(Config):
    SQLALCHEMY_DB_DIR = os.path.join(basedir, "/db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLALCHEMY_DB_DIR, "ticket_database.sqlite3")
    JWT_SECRET_KEY = 'super-secret' # Change this to your own secret key
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CORS_HEADERS = 'Content-Type' 
    
    DEBUG = False