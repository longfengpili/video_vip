'''
@Author: longfengpili
@Date: 2019-09-18 07:53:49
@LastEditTime: 2019-11-14 18:11:55
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from vip.video.iqiyi import Iqiyi
from config import headers_video, headers_search, headers_agent



def write(string):
    with open('./test.csv', 'w' ,encoding='utf-8') as f:
        f.write(str(string))

def test_iqiyi_search():
    search = '废柴'
    iqy = Iqiyi(headers=headers_search, search=search, api_id=0)
    episodes = iqy.get_search()
    print(episodes)

def test_iqiyi_video():
    video_url = 'http://www.iqiyi.com/a_19rri0mxfp.html' #'https://www.iqiyi.com/a_19rrhzs3ed.html'
    iqy = Iqiyi(headers=headers_search, api_id=0)
    soup = iqy.get_video(video_url, p_status=True)
    # print(soup)

def test_iqiyi_more():
    search = '废柴'
    iqy = Iqiyi(headers=headers_search, search=search, api_id=0)
    episodes = iqy.get_search()
    # print(episodes[1])
    for episode in episodes[1]:
        video_url = episode['url']
        iqy = Iqiyi(headers=headers_video, api_id=0)
        soup = iqy.get_video(video_url, p_status=True)
        print(soup)

def test_iqiyi_get_video_info():
    url = 'https://www.iqiyi.com/v_19rsbmrh9g.html'
    iqy = Iqiyi(headers=headers_agent, search=url, api_id=0)
    response = iqy.get_video_info()
    write(response)
    
    # print(episodes[1])
    # for episode in episodes[1]:
    #     video_url = episode['url']
    #     iqy = Iqiyi(headers=headers_video, api_id=0)
    #     soup = iqy.get_video(video_url)
    #     print(soup)
