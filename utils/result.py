# @Time    : 2018/6/15 17:45
# @Author  : SuanCaiYu
# @File    : result
# @Software: PyCharm
from flask import jsonify


class Result(object):

    @staticmethod
    def get_result(respCode, data):
        return jsonify({'code': respCode[0], 'msg': respCode[1], 'data': data})


class ResponseCode():
    success = (200, '请求成功')
    auth_error = (201, '身份验证错误')
    args_error = (202, '参数错误')
