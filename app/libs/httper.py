# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/5/12 10:14'

import requests


class HTTP:
    # 静态方法
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)

        # if+return处理特例的思想来简化代码
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
        # if r.status_code == 200:
        #     if return_json:
        #         # 返回json格式
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ''