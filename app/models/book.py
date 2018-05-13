# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 16:54'
from sqlalchemy import Column, Integer, String
from app.models.base import db, Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))  # 精装或平装
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))  # 出版日期
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))  # 书籍简介
    image = Column(String(50))
