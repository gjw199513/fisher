# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 14:42'

from flask import Flask
from app.models.book import db


def create_app():
    app = Flask(__name__)
    # 放入参数为模块路径
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
