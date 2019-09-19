'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime: 2019-09-19 13:58:17
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from bs4 import BeautifulSoup
import re


class Iqiyi(GetResponseBase):
    def __init__(self, headers, search=None):
        self.search = search
        self.url = f'https://so.iqiyi.com/so/q_{search}'
        super(Iqiyi, self).__init__(self.url, headers)

    def get_html_from_iqiyi(self):
        soup = self.main_base()
        return soup

    def get_search(self):
        soup = self.get_html_from_iqiyi()
        title = soup.title
        while not title or '404' in title.string:
            print(title)
            soup = self.get_html_from_iqiyi()
            title = soup.title
        title = title.string
        results = soup.find_all('h3', class_="result_title")
        search_results = []
        for result in results:
            search_result = {}
            if 'title' in str(result.a):
                search_result['src'] = self.url
                search_result['title'] = result.a['title']
                search_result['url'] = result.a['href']
                print(result.a['title'], result.a['href'])
                search_results.append(search_result)
        return title, search_results

    def get_video(self, video_url):
        soup = self.main_base(video_url)
        title = soup.head.title
        while not title:
            print(title)
            soup = self.main_base(video_url)
            title = soup.head.title
        title = title.string
        if '综艺' in title:
            results = soup.find_all('a', class_="stageNum")  # 综艺 #未解决第二页
        elif '电影' in title:
            results = soup.find_all('a', class_="albumPlayBtn") #电影
        elif '电视剧' in title:
            results = soup.find_all('a', class_="plotNum") #电视剧
        episodes = []
        for result in results:
            episode = {}
            episode['title'] = result['title']
            episode['title_s'] = result.string.strip()
            episode['url'] = re.subn('.*?www', 'http://www', result['href'], 1)[0]
            print(episode)
            if 'iqiyi.com' in episode['url']:
                episodes.append(episode)
        return title, episodes







