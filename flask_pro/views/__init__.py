# coding=utf-8
from flask import Blueprint

user_view = Blueprint('user', __name__, url_prefix='/user')
admin_view = Blueprint('admin', __name__, url_prefix='/admin')
