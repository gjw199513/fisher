# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 17:37'

from flask import Flask, current_app

app = Flask(__name__)

# 应用上下文 对象 Flask
# 请求上下文 对象 Request
# Flask AppContext
# Request RequestContext

"""
    当离线应用、单元测试时，需要手动将上下文入栈
"""
# 将AppContext入栈
ctx = app.app_context()
ctx.push()
a = current_app
d = current_app.config['DEBUG']
ctx.pop()

# with语句改写
with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']


# 文件读写
try:
    f = open(r'D:\t.txt')
    print(f.read())
finally:
    f.close()

# with改写
with open(r'') as f:
    print(f.read())

# with语句使用场景：实现了上下文协议对象使用with
# 上下文管理器
# 实现了__enter__ __exit__ 就是实现了上下文协议
# 上下文表达式必须返回上下文管理器
