# coding=utf-8
import os
DEBUG = True
SECRET_KEY = 'q1w2e3r4'
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC_PATH = os.path.join(BASE_DIR, 'flask_pro', 'static')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root@127.0.0.1/sqlorm')
SQLALCHEMY_TRACK_MODIFICATIONS = False
USER_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
DEBUG_TB_INTERCEPT_REDIRECTS = False
