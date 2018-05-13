# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/13 20:16'
from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)