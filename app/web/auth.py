from flask import render_template, request, redirect, url_for, flash

from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import login_user, logout_user

__author__ = '七月'


@web.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    # 当为POST请求进行校验
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        # db.session.commit()
        # 重定向到login视图函数
        return redirect(url_for('web.login'))

    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 持续的cookie
            login_user(user, remember=True)
            # 获取页面参数
            next = request.args.get('next')
            # 防止重定向攻击
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == "POST":
        pass
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
