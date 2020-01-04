'''
@Author: longfengpili
@Date: 2019-09-18 07:28:59
@LastEditTime : 2020-01-04 11:40:55
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

    def get_html(self, headers=None, url=None):
        if not url:
            url = self.url
        if not headers:
            headers = self.headers
        req = requests.get(url=url, headers=headers, params=self.params)
        self.html = req.text
        return self.html

    def soup_html(self):
        soup = BeautifulSoup(self.html, "lxml")
        return soup

    def get_response_soup(self, headers=None, url=None):
        self.get_html(headers=headers, url=url)
        soup = self.soup_html()
        with open('./test.csv', 'w' ,encoding='utf-8') as f:
            f.write(self.html)
        return soup
    
