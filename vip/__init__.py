'''
@Author: longfengpili
@Date: 2019-09-08 13:55:55
@LastEditTime: 2019-09-08 14:07:38
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__all__ = ['db', 'login_manager']

from flask import Flask, url_for, request, redirect, render_template
app = Flask(__name__)
app.config.from_object('config')



from vip import models
from vip import views
