# -*- coding:utf-8 -*-
import json

from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo

__author__ = 'gjw'
__date__ = '2018/5/12 12:15'
from flask import jsonify, request, flash, render_template
from app.forms.book import SearchForm

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web


@web.route('/book/search')
def search():
    """
        q:普通关键字 isbn
        page：start count
    :return:
    """
    # request获取查询参数
    # request必须处在flask的上下文环境中才可以获得参数
    # q = request.args['q']
    # page = request.args['page']

    form = SearchForm(request.args)
    books = BookCollection()

    # 判断数据是否校验通过
    if form.validate():
        # 将flask中request不可变的字典转换为可变字典
        # a = request.args.to_dict()

        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # dict序列化
        # return json.dumps(result), 200, {'content-type': 'application/json'}
        # return jsonify(books)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取出书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 判断当前用户是否登录
    # 根据用户的需求改变状态
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    # 所有赠送者信息
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    # 所有索要者信息
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wished=has_in_wishes)
