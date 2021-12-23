# coding=utf-8
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect  # 导入csrf保护
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from instance.settings import BASE_DIR
import os

bootstrap = Bootstrap()
moment = Moment()
login_manage = LoginManager()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()
login_manage.login_view = 'admin.login'
login_manage.login_message = '请先登录'


@login_manage.user_loader
def load_user(user_id):
    from module import Admin
    user = Admin.query.get(int(user_id))
    print('user:', user)
    return user


def register_logging(app):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(BASE_DIR, 'logs/flaskmes.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    # if not app.debug:
    app.logger.addHandler(file_handler)


def create():
    """
    创建flask实例
    """
    # template_folder='templates', static_folder='static', static_url_path='/static'
    app = Flask(__name__, instance_relative_config=True)
    import os
    app.config.from_pyfile("settings.py")  # 默认从instance文件夹中加载配置app.instance_path
    # app.config.from_object(Config)  # 从类中加载配置
    register_logging(app)
    db.init_app(app)   # db = Sqlalchemy(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    csrf.init_app(app)
    login_manage.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    from flask_pro.views.user import user_view
    from flask_pro.views.admin import admin_view
    app.register_blueprint(admin_view)
    app.register_blueprint(user_view)
    # app.app_context().push()
    app.logger.info('Flask Start')
    return app
