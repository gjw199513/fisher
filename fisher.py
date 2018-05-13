# -*- coding:utf-8 -*-


from app import create_app

__author__ = 'gjw'
__date__ = '2018/5/11 23:47'


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], threaded=True)
