'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime : 2020-01-04 10:10:03
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
import datetime, time
import re
import os
import random
import requests
from bs4 import BeautifulSoup
from config import headers_video, headers_search, headers_agent
from api_urls import api_urls
from .video import Iqiyi

import logging
from logging import config
config.fileConfig('vip_log.conf')
flask_logger = logging.getLogger('flask')

admin = Blueprint('admin',__name__)


def get_api_count():
    return list(map(str, range(len(api_urls))))

@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', api_count=get_api_count())

def get_video_url_before_after(video_url, episodes=None):
    videos = {}
    video_url_before = None
    video_url_after = None
    if not episodes:
        videos['current'] = video_url
        return videos
    for ix, episode in enumerate(episodes):
        url = episode.get('url')
        if url == video_url:
            videos['current'] = video_url
            if ix > 0:
                video_url_before = episodes[ix-1]
                video_url_before = url_for('admin.show', url=video_url_before.get('url'), api_id=video_url_before.get('api_id'), 
                                                    src=video_url_before.get('src'), title=video_url_before.get('title'))
                videos['before'] = video_url_before
            if ix < len(episodes)-1:
                video_url_after = episodes[ix+1]
                video_url_after = url_for('admin.show', url=video_url_after.get('url'), api_id=video_url_after.get('api_id'), 
                                                    src=video_url_after.get('src'), title=video_url_after.get('title'))
                videos['after'] = video_url_after
    return videos

@admin.route('show/', methods=['GET'])
def show():
    # print(request.headers)
    url = request.args.get('url')
    p_status = False if url and 'api' in url else True #是否打印
    title = request.args.get('title')
    src = request.args.get('src')
    api_id = request.args.get('api_id')
    search = request.args.get('search')
    src = src if src else url
    flask_logger.info(f'【search】: {search}, 【url】: {url}, 【src】:{src}, 【api_id】:{api_id}')
    if url:
        iqy = Iqiyi(headers=headers_video, api_id=api_id)
        title_, episodes = iqy.get_video(src, p_status)
        title = title if title else title_
        if url == src: #首次search 不显示
            url = None
        videos = get_video_url_before_after(url, episodes)
        return render_template('admin/show.html', src=src, title=title, episodes=episodes, videos=videos, api_id=api_id, api_count=get_api_count())
    else:
        return redirect(url_for('admin.search', src=search, search=search, api_id=api_id, api_count=get_api_count()))

@admin.route('search/', methods=['GET'])
def search():
    search = request.args.get('search')
    api_id = request.args.get('api_id')
    # src = request.args.get('src')
    # print(search)
    if re.search('^http.*?\.com', search):
        iqy = Iqiyi(headers_agent, api_id=api_id, search=search)
        title, url = iqy.get_video_info()
        videos = get_video_url_before_after(url)
        flask_logger.info(videos)
        return render_template('admin/show.html', src=search, title=title, videos=videos, api_id=api_id, api_count=get_api_count())
    else:
        iqy = Iqiyi(headers_search, api_id=api_id, search=search)
        title, search_results = iqy.get_search()
        return render_template('admin/search.html', src=search, title=title, all_episode=search_results, api_id=api_id, api_count=get_api_count())


