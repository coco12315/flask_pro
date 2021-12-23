# coding=utf-8
from flask import Flask, redirect, url_for, request, render_template, flash, make_response, session
from wtforms import widgets, validators, Form, simple
from flask_login import login_required, login_user, current_user
import functools
from flask_sqlalchemy import SQLAlchemy
import os
from flask_pro.views import user_view
from module import LoginForm, RegisterForm, Admin


@user_view.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('登录状态')
        data = {'sn': '123456700001', 'itemcode': '130000000001', 'addr': 'XiLi', 'name': 'board', 'num': 5}
        return render_template('admin/detail.html', form=data)
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.pwd.data
        remember = form.remember.data
        admin = Admin.query.filter_by(username=username).first()
        print('admin:', admin)
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                print('Welcome back.')
                data = {'sn': '123456700001', 'itemcode': '130000000001', 'addr': 'XiLi', 'name': 'board', 'num': 5}
                return render_template('admin/detail.html', form=data)
            flash('Invalid username or password.', 'warning')
            print('Invalid username or password.')
        else:
            flash('No account.', 'warning')
            print('No account.')
    return render_template('admin/login.html', form=form)


@user_view.before_request
def be_request():
    print('user_view before_request')


@user_view.after_request
def af_request(response):
    print('user_view after_request', response)
    return response
