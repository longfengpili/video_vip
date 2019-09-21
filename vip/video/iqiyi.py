'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime: 2019-09-21 19:35:58
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from bs4 import BeautifulSoup
import re
from api_urls import api_urls
import json


class Iqiyi(GetResponseBase):
    def __init__(self, headers, api_id, search=None):
        self.search = search
        self.api_id = api_id
        self.url = f'https://so.iqiyi.com/so/q_{search}'
        super(Iqiyi, self).__init__(self.url, headers)

    def get_html_from_iqiyi(self):
        soup = self.get_response_soup()
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
                search_result['api_id'] = self.api_id
                search_result['title'] = result.a['title']
                search_result['url'] = result.a['href']
                if search_result not in search_results:
                    search_results.append(search_result)
        return title, search_results
    
    def url_api(self, url, api_id):
        for id, api in enumerate(api_urls):
            if id == int(api_id):
                url_api = api + url
                return url_api

    def get_video_variety(self, video_url, soup, p_status):
        source_id = soup.find_all('span', class_="effect-score")
        if source_id:
            source_id = source_id[0]['data-score-tvid']
        album_list = soup.find_all('li', attrs={'data-tab-title':'widget-tab-1'})
        if album_list:
            album_list = [i['data-year'] for i in album_list if i['data-year'] != 'all']

        episodes = []
        if source_id and album_list:
            for date in album_list:
                # print(date)
                url = f'http://pcw-api.iqiyi.com/album/source/svlistinfo?sourceid={source_id}&timelist={date}&callback=window.Q.__callbacks__.cbejn72o'
                headers= {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
                }
                response = self.get_response_soup(headers=headers, url=url)
                if response:
                    response = re.search('cbejn72o\((.*?)\);}catch', str(response)).group(1)
                    response_json = json.loads(response)
                    results = response_json['data'].get(date)
                    for result in results:
                        episode = {}
                        episode['src'] = video_url
                        episode['api_id'] = self.api_id
                        episode['title'] = result['name']
                        url = result['playUrl']
                        episode['url'] = self.url_api(url, self.api_id)
                        if 'iqiyi.com' in episode['url'] and episode not in episodes:
                            if p_status:
                                print(episode)
                            episodes.insert(0, episode)
        return episodes

    def get_video(self, video_url, p_status):
        k = 0
        episodes = []
        soup = self.get_response_soup(url=video_url)
        title = soup.head.title
        while (not title or '404' in title.string) and k <= 5:
            soup = self.get_response_soup(url=video_url)
            title = soup.head.title
            k += 1
        # with open('./test.csv', 'w' ,encoding='utf-8') as f:
        #     f.write(str(soup))
        title = title.string
        if '综艺' in title:
            results = soup.find_all('a', class_="stageNum")
            episodes = self.get_video_variety(video_url, soup, p_status)
        elif '电影' in title:
            results = soup.find_all('a', class_="albumPlayBtn") #电影
        elif '电视剧' in title:
            results = soup.find_all('a', class_="plotNum") #电视剧
        if not episodes:
            for result in results:
                episode = {}
                episode['src'] = video_url
                episode['api_id'] = self.api_id
                episode['title'] = result['title']
                # episode['title_s'] = result.string.strip()
                url = re.subn('.*?www', 'http://www', result['href'], 1)[0]
                episode['url'] = self.url_api(url, self.api_id)
                if 'iqiyi.com' in episode['url'] and episode not in episodes:
                    episodes.append(episode)
        return title, episodes







