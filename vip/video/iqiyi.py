'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime: 2019-09-18 13:51:50
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from config import headers1
from bs4 import BeautifulSoup
import re


class Iqiyi(GetResponseBase):
    def __init__(self, headers, search):
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
        episodes = []
        for result in results:
            episode = {}
            if 'title' in str(result.a) and self.search in result.a['title']:
                episode['src'] = self.url
                episode['title'] = result.a['title']
                episode['url'] = result.a['href']
                episodes.append(episode)
        return title, episodes




        # print(videos)
        # all_episode = []
        # for video in videos:
        #     print(video)
        #     episode = {}
        #     if 'sub1' in video.a['rseat']:
        #         url_single = video.a['href'].strip()
        #         if 'iqiyi.com/v_' in url_single:
        #             url_single = re.subn('.*?www', 'http://www', url_single, 1)[0]
        #             episode['src'] = self.url
        #             episode['url'] = url_single
        #             episode['title'] = video.a.string.strip()
        #             try:
        #                 episode['num'] = re.findall('第(\d+)集', video.a.string.strip())[0]
        #             except:
        #                 episode['num'] = 0
        #             all_episode.append(episode)
        # return title, all_episode

