from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


__author__ = 'gjw'
__date__ = '2018/5/13 20:16'


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
