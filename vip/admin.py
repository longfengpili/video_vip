'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-09-11 21:45:41
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
from config import headers1, headers2
from api_urls import work_url, notwork_url

admin = Blueprint('admin',__name__)


@admin.route('/')
@admin.route('/index')
def index():
    return render_template('admin/index.html')


@admin.route('search/', methods=['GET'])
def search():
    # print(request.headers)
    url = request.args.get('url')
    source = request.args.get('source')
    if re.search('www\..*?\.com', url):
        # print(url)
        title, all_episode = get_videolist(url,source)
        return render_template('admin/search.html', title=title, all_episode=all_episode)
    else:
        print(f"40{url_for('admin.search_video',search=url, source=source)}")
        return redirect(url_for('admin.search_video',search=url, source=source))

def get_videolist(url, source=3):
    req = requests.get(url, headers=headers1)
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


@admin.route('search_video/?search=<search>', methods=['GET'])
def search_video(search):
    print(request.args)
    url = request.args.get('url')
    source = request.args.get('source')
    if url:
        print(f'76='*10)
        return redirect(url_for('admin.search', url=url, source=source))
    else:
        url = f'https://so.iqiyi.com/so/q_{search}?source=input&sr=1006493155769'
        req = requests.get(url, headers=headers2)
        html = req.text
        soup = BeautifulSoup(html)
        searchtitle = soup.title
        result_title = soup.find_all('h3', class_="result_title")
        # print(searchtitle)
        search_results = []
        for result in result_title:
            search = {}
            try:
                title = result.a['title']
                url = result.a['href']
                if url.endswith('search'):
                    search['title'] = title
                    search['url'] = url
                    search['source'] = source
                    search_results.append(search)
            except:
                pass
        return render_template('admin/search_video.html', title=searchtitle, all_episode=search_results)
