# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 14:42'

from flask import Flask
from flask_login import LoginManager
from app.models.book import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    # 放入参数为模块路径
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    login_manager.init_app(app)
    # flask-login回到登录视图函数
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    db.init_app(app)
    # db.create_all(app=app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
