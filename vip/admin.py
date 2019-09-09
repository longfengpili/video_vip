'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-09-09 07:51:27
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
from config import headers
from api_urls import work_url, notwork_url

admin = Blueprint('admin',__name__)

@admin.route('/index')
def index():
    return render_template('admin/index.html')

@admin.route('search/', methods=['GET'])
def search():
    # print(request.headers)
    url = request.args.get('url')
    source = request.args.get('source')
    title, all_episode = get_videolist(url,source)
    # return redirect(url_for('admin.index', title=title, all_episode=all_episode))
    return render_template('admin/search.html', title=title, all_episode=all_episode)

def get_videolist(url, source=3):
    req = requests.get(url, headers=headers)
    html = req.text
    soup = BeautifulSoup(html)
    title = soup.title
    videos = soup.find_all('p', class_="site-piclist_info_title")
    all_episode = []
    for video in videos:
        episode = {}
        if 'sub1' in video.a['rseat']:
            url = video.a['href'].strip()
            if 'iqiyi.com/v_' in url:
                url = re.subn('.*?www', 'http://www', url, 1)[0]
                episode['url'] = vip_pass(url, source)
                episode['title'] = video.a.string.strip()
                print(f"[{episode['title']}]{episode['url']}")
                all_episode.append(episode)
    return title, all_episode


def vip_pass(url, source):
    for id, api in enumerate(work_url):
        if id == int(source):
            u = api + url
            return u


    
