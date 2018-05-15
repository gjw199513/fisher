# -*- coding:utf-8 -*-
from app.spider.yushu_book import YuShuBook

__author__ = 'gjw'
__date__ = '2018/5/14 12:19'
from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    # 获得用户的所有礼物
    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)
        ).all()
        return wishes

    # 得到各个书籍的心愿数量
    @classmethod
    def get_gifts_counts(cls, isbn_list):
        # 根据传入的一组isbn，到wish表中计算出某个礼物的wish心愿数量
        # filter_by接收关键字参数，filter接收条件表达式
        # 当跨表或者复杂的查询，使用db.session.query较好
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            # 查看是否在isbn列表中
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    # 得到礼物下面的书籍
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
