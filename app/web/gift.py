from flask import current_app, flash, redirect, url_for

from app.models.base import db
from app.models.gift import Gift
from . import web
from flask_login import login_required, current_user
__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    return 'My Gifts'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # 获得当前用户的id
            gift.uid = current_user.id
            # 当前用户增加0.5个鱼豆
            # current_user.beans += 0.5
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     # 数据库回滚,当上方的数据库操作失败会影响后面的数据库操作，建议进行回滚
        #     db.session.rollback()
        #     raise e
    else:
        flash("这本书已添加至您的赠送清单或已存在与您的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



