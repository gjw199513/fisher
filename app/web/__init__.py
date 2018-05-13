# -*- coding:utf-8 -*-
from flask import Blueprint

__author__ = 'gjw'
__date__ = '2018/5/12 14:46'

# 实例化蓝图
web = Blueprint('web', __name__)

from app.web import book
