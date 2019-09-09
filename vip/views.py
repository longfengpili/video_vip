'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-09-08 17:13:56
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

from vip import app
from .admin import admin


app.register_blueprint(admin,url_prefix='/')