import os


class Config:
    """base config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root@127.0.0.1/sqlorm')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False