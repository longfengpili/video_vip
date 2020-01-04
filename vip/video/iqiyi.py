'''
@Author: longfengpili
@Date: 2019-09-18 07:39:03
@LastEditTime : 2020-01-04 12:25:51
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from .get_html import GetResponseBase
from bs4 import BeautifulSoup
import re
from api_urls import api_urls
import json
import datetime

import logging
from logging import config
config.fileConfig('vip_log.conf')
iqylogger = logging.getLogger('iqy')

class Iqiyi(GetResponseBase):
    def __init__(self, headers, api_id, search=None):
        self.search = search
        self.api_id = api_id
        self.url = f'https://so.iqiyi.com/so/q_{search}'
        self.headers = headers
        super(Iqiyi, self).__init__(self.url, self.headers)

    def get_html_from_iqiyi(self):
        soup = self.get_response_soup()
        # with open('./test.csv', 'w' ,encoding='utf-8') as f:
        #     f.write(str(soup))
        return soup

    def get_search(self, first=False):
        soup = self.get_html_from_iqiyi()
        title = soup.title
        while not title or '404' in title.string:
            soup = self.get_html_from_iqiyi()
            title = soup.title
        title = title.string
        results = soup.find_all('h3', class_="qy-search-result-tit")
        search_results = []
        for result in results:
            search_result = {}
            if 'title' in str(result.a):
                search_result['src'] = self.url
                search_result['api_id'] = self.api_id
                search_result['title'] = result.a['title']
                search_result['url'] = result.a['href']
                if search_result not in search_results and '<em' in str(result):
                    iqylogger.info(search_result)
                    search_results.append(search_result)
                if first:
                    break
        return title, search_results
    
    def url_api(self, url, api_id=None):
        if not api_id:
            api_id = self.api_id
        for id, api in enumerate(api_urls):
            if id == int(api_id):
                url_api = api + url
                return url_api

    def iqiyi_api(self, video_url, source_id, album_list, p_status=True):
        episodes = []
        if not source_id or not album_list:
            return episodes

        for date in album_list:
            url = f'http://pcw-api.iqiyi.com/album/source/svlistinfo?sourceid={source_id}&timelist={date}&callback=window.Q.__callbacks__.cbejn72o'
            iqylogger.info(url)
            response = self.get_response_soup(headers=self.headers, url=url)
            if response and '请求失败,请重试' not in str(response):
                # print(response)
                response = re.search('cbejn72o\((.*?)\);}catch', str(response)).group(1)
                response_json = json.loads(response)
                try:
                    results = response_json['data'].get(date)
                except Exception as e:
                    iqylogger.error(f'pcw-api error :{response_json}')
                    results = []
                for result in results:
                    episode = {}
                    episode['src'] = video_url
                    episode['api_id'] = self.api_id
                    episode['title'] = result['shortTitle']
                    url = result['playUrl']
                    episode['url'] = self.url_api(url, self.api_id)
                    if 'iqiyi.com' in episode['url'] and episode not in episodes:
                        if p_status:
                            # iqylogger.info(episode)
                            pass
                        episodes.insert(0, episode)
        return episodes

    def get_video_variety(self, video_url, soup, p_status):
        scripts = soup.head.find_all('script')
        script = ''.join([script.string.replace('\n', '').replace(' ', '') for script in scripts if script.string])
        ids = re.findall('albumId:"(.*?)",tvId:"(.*?)",sourceId:(.*?),', script)
        if ids:
            album_id, tv_id, source_id = ids[0]
        else:
            source_id = 0
        # iqylogger.info(source_id)
           
        album_list = soup.find_all('li', attrs={'data-tab-title':'widget-tab-1'})
        if album_list:
            album_list = [i['data-year'] for i in album_list if 'data-year' in str(i) and i['data-year'] != 'all']
        else:
            try:
                date_upload = soup.head.find_all('meta', attrs={'itemprop': 'uploadDate'})[0]['content'][:4]
                date_published = soup.head.find_all('meta', attrs={'itemprop': 'datePublished'})[0]['content'][:4]
                album_list = [str(year) for year in range(int(date_upload), int(date_published)+1, 1)]
            except:
                album_list = []
        # iqylogger.info(f'source_id: {source_id}, album_list: {album_list}')

        episodes = self.iqiyi_api(video_url, source_id, album_list, p_status=True)
                      
        return episodes

    def get_video(self, video_url, p_status):
        k = 0
        episodes = []
        soup = self.get_response_soup(url=video_url)
        title = soup.head.title if soup and soup.find_all('head') else soup.title
        while (not title or '404' in title.string) and k <= 5:
            soup = self.get_response_soup(url=video_url)
            title = soup.head.title if soup and soup.find_all('head') else soup.title
            k += 1
        with open('./test.csv', 'w' ,encoding='utf-8') as f:
            f.write(str(soup))
        title = title.string
        if 'playpage-barrage-list' in str(soup) or not re.search('iqiyi', video_url): #根据是否有弹幕列表判断是否是内页或者非iqiyi视频
            episode = {}
            episode['src'] = video_url
            episode['api_id'] = self.api_id
            episode['title'] = title
            episode['url'] = self.url_api(video_url)
            episodes.append(episode)            
        else:
            # iqylogger.info(title)
            if '综艺' in title:
                results = soup.find_all('a', class_="stageNum")
                episodes = self.get_video_variety(video_url, soup, p_status)
            elif '电影' in title:
                results = soup.find_all('a', class_="albumPlayBtn") #电影
            elif '电视剧' in title:
                results = soup.find_all('a', class_="plotNum") #电视剧
                episodes = self.get_video_variety(video_url, soup, p_status)
            else:
                results = [{'title': title, 'href': video_url}]
                episodes = self.get_video_variety(video_url, soup, p_status)
            if not episodes:
                for result in results:
                    # iqylogger.info(result)
                    episode = {}
                    episode['src'] = video_url
                    episode['api_id'] = self.api_id
                    episode['title'] = result['title'] if 'title' in result else result.string if result.string else title
                    url = re.subn('.*?www', 'http://www', result['href'], 1)[0]
                    episode['url'] = self.url_api(url)
                    if 'iqiyi.com' in episode['url'] and episode not in episodes:
                        # iqylogger.info(episode)
                        episodes.append(episode)
        iqylogger.info(title)
        iqylogger.info(episodes)
        return title, episodes

    def get_video_info(self, url=None):
        if not url:
            url = self.search
        response = self.get_response_soup(headers=self.headers, url=url)
        title = response.title.string
        url = self.url_api(url)
        return title, url







