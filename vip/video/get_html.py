'''
@Author: longfengpili
@Date: 2019-09-18 07:28:59
@LastEditTime: 2019-09-19 07:33:09
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class GetResponseBase(object):
    
    def __init__(self, url, headers, params=None):
        self.url = url
        self.headers = headers
        self.params = params
        self.html = None

    def get_html(self, url=None):
        if not url:
            url = self.url
        req = requests.get(url=url, headers=self.headers, params=self.params)
        self.html = req.text
        return self.html

    def soup_html(self):
        soup = BeautifulSoup(self.html, "lxml")
        return soup

    def main_base(self, url=None):
        self.get_html(url=url)
        soup = self.soup_html()
        return soup
    
