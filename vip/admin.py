'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-09-17 08:10:08
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


@admin.route('show/', methods=['GET'])
def show():
    # print(request.headers)
    url = request.args.get('url')
    source = request.args.get('source')
    main = request.args.get('main')
    main = main if main else url
    print(f'==================url: {url}, main:{main}, source:{source}')
    if re.search('www\..*?\.com', url):
        title, all_episode = get_videolist(main,source)
        print(all_episode)
        return render_template('admin/show.html', title=title, all_episode=all_episode, video_url=url)
    else:
        
        return redirect(url_for('admin.search',search=url, source=source))

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
            url_ = video.a['href'].strip()
            if 'iqiyi.com/v_' in url_:
                url = re.subn('.*?www', 'http://www', url, 1)[0]
                episode['main'] = url
                episode['url'] = vip_pass(url_, source)
                episode['title'] = video.a.string.strip()
                try:
                    episode['num'] = re.findall('第(\d+)集', video.a.string.strip())[0]
                else:
                    episode['num'] = 0
                episode['source'] = source
                all_episode.append(episode)
        
    return title, all_episode


def vip_pass(url, source):
    for id, api in enumerate(work_url):
        if id == int(source):
            u = api + url
            return u


@admin.route('search/?search=<search>', methods=['GET'])
def search(search):
    url = request.args.get('url')
    source = request.args.get('source')
    if url:
        return redirect(url_for('admin.show', url=url, source=source))
    else:
        url = f'https://so.iqiyi.com/so/q_{search}?'
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
                if url.endswith('search'): #后面考虑 暂时去掉
                    search['title'] = title
                    search['url'] = url
                    search['source'] = source
                    search_results.append(search)
            except:
                pass
        return render_template('admin/search.html', title=searchtitle, all_episode=search_results)


@admin.route('video/', methods=['GET'])
def video():
    # print(request.headers)
    url = request.args.get('url')
    source = request.args.get('source')
    if re.search('www\..*?\.com', url):
        return render_template('admin/video.html', video_url=url)
    else:
        print(url, source)
        return redirect(url_for('admin.search', search=url, source=source))
