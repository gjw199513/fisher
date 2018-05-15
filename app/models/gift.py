# -*- coding:utf-8 -*-
from flask import current_app

from app.spider.yushu_book import YuShuBook
from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

__author__ = 'gjw'
__date__ = '2018/5/13 20:16'


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    # 获得用户的所有礼物
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)
        ).all()
        return gifts

    # 得到各个书籍的心愿数量
    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn，到wish表中计算出某个礼物的wish心愿数量
        # filter_by接收关键字参数，filter接收条件表达式
        # 当跨表或者复杂的查询，使用db.session.query较好
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            # 查看是否在isbn列表中
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn':w[1]} for w in count_list]
        return count_list

    # 得到礼物下面的书籍
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 对象代表一个具体的礼物
    # 类代表礼物这个事物,不是具体的“一个”
    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
