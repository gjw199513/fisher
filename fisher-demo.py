# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/11 23:47'

from flask import Flask

# from config import DEBUG

app = Flask(__name__)
# 放入参数为模块路径
app.config.from_object('config')


@app.route('/hello/')
def hello():
    # 视图函数中返回Response对象
    return "hello,gjw"


# 使用基于类视图需要该种方式注册
# app.add_url_rule("/hello/", view_func=hello)


# 主入口函数可以保证放入生产环境中不会执行下面flask内置的服务器
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
