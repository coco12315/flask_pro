# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_pro import db
from sqlalchemy import func
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, url_for, redirect


class LoginForm(FlaskForm):
    # 用户名
    name = StringField(
        label='用户名',
        validators=[
            DataRequired(message='用户名不能为空.'),
            # Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ]
    )
    # 密码
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired(message='密码不能为空.'),
            # Length(min=8, message='用户名长度必须大于%(min)d'),
            # Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z0-9$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')

        ]
    )
    remember = BooleanField(label='记住密码')


class RegisterForm(FlaskForm):
    # 用户名
    name = StringField(
        label='用户名',
        validators=[
            DataRequired(message='用户名不能为空.'),
            # Length(min=6, max=18, message='用户名长度必须大于%(min)d且小于%(max)d')
        ]
    )
    # 密码
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired(message='密码不能为空.'),
            # Length(min=8, message='用户名长度必须大于%(min)d'),
            # Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z0-9$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')

        ]
    )
    # 确认密码
    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired(message='密码不能为空.'),
            # Length(min=8, message='用户名长度必须大于%(min)d'),
            # Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z0-9$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
            EqualTo('pwd', message='两次密码不一致')
        ]
    )
    # 手机号
    phone = StringField(
        label='手机号',
        validators=[
            DataRequired(message='手机号不能为空.'),
            # Length(min=8, message='用户名长度必须大于%(min)d'),
            # Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z0-9$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ]
    )
    # 邮箱
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired(message='邮箱不能为空.'),
            # Length(min=8, message='用户名长度必须大于%(min)d'),
            # Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z0-9$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ]
    )


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.VARCHAR(20), nullable=False, unique=True)
    email = db.Column(db.VARCHAR(30), nullable=True)
    phone = db.Column(db.CHAR(11))
    books = db.relationship('Book')

    def __repr__(self):
        return '{}({!r},{})'.format(__class__.__name__, self.author_name, self.id)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.VARCHAR(20), nullable=False, unique=True)
    create_time = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete='CASCADE'))

    def __repr__(self):
        return '{}({!r},{!r})'.format(__class__.__name__, self.book_name, self.author_id)


def redirect_back(default='home', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))
