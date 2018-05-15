# -*- coding:utf-8 -*-

__author__ = 'gjw'
__date__ = '2018/5/13 20:16'
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer
from contextlib import contextmanager
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 数据库回滚,当上方的数据库操作失败会影响后面的数据库操作，建议进行回滚
            db.session.rollback()
            raise e


# 改写filter_by方法，加入status=1的校验
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        # 判断是否传入status
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # 传入字典时，需要对字典进行解包，加入**
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 基础模型，不会创建该表
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 将form中与model相同名字的字段，放入model中
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)


    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None