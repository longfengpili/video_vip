'''
@Author: longfengpili
@Date: 2019-09-18 07:53:49
@LastEditTime: 2019-09-19 07:58:55
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import unittest
from vip.video.iqiyi import Iqiyi
from config import headers1, headers2


class tasktest(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print(f'tearDown...')

    def test_iqiyi_search(self):
        search = '蝙蝠侠'
        iqy = Iqiyi(headers=headers2, search=search)
        episodes = iqy.get_search()
        print(episodes)

    def test_iqiyi_video(self):
        video_url = 'http://www.iqiyi.com/lib/m_212716614.html?src=search'
        iqy = Iqiyi(headers=headers1)
        soup = iqy.get_video(video_url)
        print(soup)
        with open('./test.csv', 'w', encoding='utf-8') as f:
            f.write(str(soup))

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTest(tasktest('test_iqiyi_video'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
