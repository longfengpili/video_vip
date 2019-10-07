'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-10-08 07:36:32
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

admin = Blueprint('admin',__name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html', api_count=list(range(len(api_urls))))

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
    print(f'【url】: {url}, 【src】:{src}, 【api_id】:{api_id}')
    if url and re.search('www\..*?\.com', url):
        iqy = Iqiyi(headers=headers_video, api_id=api_id)
        title_, episodes = iqy.get_video(src, p_status)
        title = title if title else title_
        if url == src: #首次search 不显示
            url = None
        return render_template('admin/show.html', title=title, episodes=episodes, video_url=url, api_count=list(range(len(api_urls))))
    else:
        return redirect(url_for('admin.search', search=search, api_id=api_id, api_count=list(range(len(api_urls)))))

@admin.route('search/', methods=['GET'])
def search():
    search = request.args.get('search')
    api_id = request.args.get('api_id')
    if re.search('www\..*?\.com', search):
        iqy = Iqiyi(headers_agent, api_id=api_id, search=search)
        title, url = iqy.get_video_info()
        return render_template('admin/show.html', title=title, video_url=url, api_count=list(range(len(api_urls))))
    else:
        iqy = Iqiyi(headers_search, api_id=api_id, search=search)
        title, search_results = iqy.get_search()
        return render_template('admin/search.html', title=title, all_episode=search_results, api_count=list(range(len(api_urls))))


