# -*- coding:utf-8 -*-
from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish

__author__ = 'gjw'
__date__ = '2018/5/13 20:16'

from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.spider.yushu_book import YuShuBook


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

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送者和索要者

        # 该本图书既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


# flask-login将id编号转化为模型
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
