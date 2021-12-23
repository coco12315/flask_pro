# coding=utf-8
from flask import Flask, redirect, url_for, request, render_template, flash, make_response, session
from flask_login import login_required, logout_user, current_user, login_user
import functools
from flask_sqlalchemy import SQLAlchemy
import os
from flask_pro.views import admin_view
from module import LoginForm, RegisterForm, Book, Author, redirect_back, Admin
from flask_pro import db


@admin_view.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('登录状态:', session)
        data = {'sn': '123456700001', 'itemcode': '130000000001', 'addr': 'XiLi', 'name': 'board', 'num': 5}
        return render_template('admin/detail.html', form=data)
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.pwd.data
        remember = form.remember.data
        admin = Admin.query.filter_by(username=username).first()
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


@admin_view.route('/register', methods=['GET', 'POST'])
def register():
    print('session:', session)
    # <SecureCookieSession {'_fresh': True,
    # '_id': '3fe1c1dd0da49adcfa872d5843c30d044aaa30a69215be437eab6fc550f65465fd3004487b27852d148cd24072eeb39a0eb3c6
    # bda41279ba078160e33b810bea',
    # '_user_id': '3', 'csrf_token': '03e9900a1a74117057f492069c9153b92a21f235'}>
    print('cookies:', request.cookies)
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('admin/register.html', form=form)
    else:
        form = RegisterForm()
        if form.validate():
            print('用户提交数据通过格式验证，提交的值为：', form.data)
            name = form.data['name']
            pwd = form.data['pwd']
            admin = Admin.query.filter_by(username=name).first()
            if admin:
                flash('账号已存在')
                print('账号已存在')
            else:
                try:
                    user = Admin(username=name)
                    user.set_password(pwd)
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print('服务器写入失败:', e)
                    db.session.rollback()
                else:
                    flash('注册成功')
                    print('注册成功')
        else:
            print(form.errors)
        return render_template('admin/register.html', form=form)


@login_required
@admin_view.route('/detail', methods=['GET', 'POST'])
def detail():
    data = {'sn': '123456700001', 'itemcode': '130000000001', 'addr': 'XiLi', 'name': 'board', 'num': 5}
    return render_template('admin/detail.html', form=data)


@admin_view.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logout success')
    # return redirect_back()
    return render_template('admin/logout.html')


@admin_view.before_request
def be_request():
    print('admin_view before_request')


@admin_view.after_request
def af_request(response):
    print('admin_view after_request', response)
    return response


if __name__ == '__main__':
    from flask import Flask
    import os
    from module import LoginForm, Book, Author
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")  # 默认从instance文件夹中加载配置
    db.init_app(app)
    app.app_context().push()
    try:
        print('init db')
        db.drop_all()
        db.create_all()
    except Exception as e:
        print('数据库操作失败：', e)
    try:
        author1 = Author(author_name='航航', phone=111)
        author2 = Author(author_name='娟娟', phone=222)
        author3 = Author(author_name='科科', phone=333)
        db.session.add_all([author1, author2, author3])
        db.session.commit()
    except Exception as e:
        print('数据库操作失败：', e)
        db.session.rollback()
    try:
        book1 = Book(book_name='python入门', author_id=1)
        book2 = Book(book_name='python中级', author_id=1)
        book3 = Book(book_name='python高级', author_id=3)
        book4 = Book(book_name='mysql上', author_id=1)
        book5 = Book(book_name='mysql中', author_id=3)
        book6 = Book(book_name='mysql下', author_id=2)
        db.session.add_all([book1, book2, book3, book4, book5, book6])
        db.session.commit()
    except Exception as e:
        print('数据库操作失败：', e)
        db.session.rollback()
    x = Book.query.all()
    print('=-=', x)
