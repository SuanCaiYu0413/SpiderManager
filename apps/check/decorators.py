# @Time    : 2018/6/14 15:58
# @Author  : SuanCaiYu
# @File    : decorators
# @Software: PyCharm

from flask import session, redirect, url_for
from utils.result import *
from functools import wraps
import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('client.login'))

    return inner


def api_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.USER_ID in session:
            return func(*args, **kwargs)
        else:
            return Result.get_result(respCode=ResponseCode.auth_error, data={})

    return inner
