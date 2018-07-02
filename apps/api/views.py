# @Time    : 2018/6/14 15:57
# @Author  : SuanCaiYu
# @File    : views
# @Software: PyCharm

from flask import Blueprint
from flask_restful import request, Api, Resource
from apps.check.decorators import api_required
from apps.models.models import *
from utils.tools import get_eggfile_count, del_eggfile
from utils.result import *

bp = Blueprint("api", __name__, url_prefix='/api')

api = Api(bp)


class BaseInfo(Resource):
    @api_required
    def get(self):
        clients = Clients.query.all()
        peoject, count = get_eggfile_count()
        return Result.get_result(ResponseCode.success, {'client_count': len(clients), 'eggfile_count': count})


class EggFile(Resource):
    @api_required
    def get(self):
        files, count = get_eggfile_count()
        return Result.get_result(ResponseCode.success, {'files': files, 'count': count})

    @api_required
    def delete(self):
        args = request.values
        filename = args.get('filename')
        if filename:
            del_result = del_eggfile(filename)
            return Result.get_result(ResponseCode.success, del_result)
        else:
            return Result.get_result(ResponseCode.args_error, 0)


api.add_resource(BaseInfo, '/baseinfo')
api.add_resource(EggFile, '/projects')
