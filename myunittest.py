'''
@Author: longfengpili
@Date: 2019-09-18 07:53:49
@LastEditTime: 2019-09-19 13:56:55
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import unittest
from vip.video.iqiyi import Iqiyi
from config import headers_video, headers_search


class tasktest(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print(f'tearDown...')

    def test_iqiyi_search(self):
        search = '坑王'
        iqy = Iqiyi(headers=headers_search, search=search)
        episodes = iqy.get_search()
        print(episodes)

    def test_iqiyi_video(self):
        video_url = 'http://www.iqiyi.com/a_19rrh3kj85.html'
        iqy = Iqiyi(headers=headers_video)
        soup = iqy.get_video(video_url)
        print(soup)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTest(tasktest('test_iqiyi_video'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
