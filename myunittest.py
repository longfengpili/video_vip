'''
@Author: longfengpili
@Date: 2019-09-18 07:53:49
@LastEditTime: 2019-09-18 13:49:33
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

    def test_iqiyi(self):
        search = '废柴'
        iqy = Iqiyi(headers=headers2, search=search)
        episodes = iqy.get_search()
        print(episodes)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTest(tasktest('test_iqiyi'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
