'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime: 2019-09-18 07:58:04
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from config import headers1


class Iqiyi(GetResponseBase):
    def __init__(self, url, headers):
        super(Iqiyi, self).__init__(url, headers)

    def get_html_from_iqiyi(self):
        soup = self.main_base()
        return soup



    
