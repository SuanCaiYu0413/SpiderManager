# @Time    : 2018/6/14 15:43
# @Author  : SuanCaiYu
# @File    : config
# @Software: PyCharm

import os

USER_ID = '*thwv8tthqxpzCCbHiOdP9J@%vPY6iLh'
# 程序运行目录
basedir = os.path.abspath(os.path.dirname(__file__))
# egg文件存放目录
eggdir = '%s/source/egg/' % basedir

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/source/database/sm.db'.format(basedir)
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = os.urandom(24)

# DEBUG = True
# TEMPLATES_AUTO_RELOAD = True
