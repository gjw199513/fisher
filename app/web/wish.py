from app.view_models.trade import MyTrades

__author__ = 'gjw'
__date__ = '2018/5/13 20:16'

from flask import current_app, flash, redirect, url_for, render_template

from app.models.base import db


from flask_login import login_required, current_user

from app.models.wish import Wish
from . import web


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gifts_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            # 获得当前用户的id
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash("这本书已添加至您的赠送清单或已存在与您的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
