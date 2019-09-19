'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime: 2019-09-19 08:04:37
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from config import headers1
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
        # with open('./test.csv', 'w', encoding='utf-8') as f:
        #     f.write(str(soup))
        title = soup.title
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
        title = soup.head.title.string
        if '综艺' in title:
            results = soup.find_all('a', class_="recoAlbumTit-link") #综艺
        elif '电影' in title:
            results = soup.find_all('a', class_="albumPlayBtn") #电影
        elif '电视剧' in title:
            # return soup
            results = soup.find_all('a', class_="plotNum") #电视剧
        episodes = []
        for result in results:
            episode = {}
            episode['title'] = result['title']
            episode['title_s'] = result.string
            episode['url'] = result['href']
            if 'iqiyi.com' in episode['url']:
                episodes.append(episode)
        return title, episodes







