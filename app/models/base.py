# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/13 20:16'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import SmallInteger, Column, Integer

db = SQLAlchemy()


class Base(db.Model):
    # 基础模型，不会创建该表
    __abstract__ = True
    # create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    # 将form中与model相同名字的字段，放入model中
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)