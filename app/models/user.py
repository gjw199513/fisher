# -*- coding:utf-8 -*-
from app import login_manager

__author__ = 'gjw'
__date__ = '2018/5/13 20:16'

from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 继承UserMixin可以实现flask_login需要的函数
class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    # 属性读取
    @property
    def password(self):
        return self._password

    # 属性赋值
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 校验密码
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # flask-login需要知道用户唯一标示的函数，使用该插件必须创建
    # 如果非id实现唯一标示，需要重新写该方法
    # def get_id(self):
    #     return self.id


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
