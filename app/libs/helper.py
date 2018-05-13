# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 10:00'


def is_isbn_or_key(word):
    """
        判断是否为isbn关键字
    :param word:
    :return:
    """
    # isbn isbn13 13个0到9的数字组成
    # isbn10 10个0到9数字组成，含有一些‘-’
    isbn_or_key = 'key'
    # isdigit()函数判断是否全为数字
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'

    # 判断是否符合isbn10规范：存在-，除去-外为10位纯数字
    short_q = word.replace('-', '')
    if '-' in word and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key