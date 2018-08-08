# @Time    : 2018/6/14 16:12
# @Author  : SuanCaiYu
# @File    : views
# @Software: PyCharm

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask.views import MethodView
import config
from ..check.decorators import login_required
from ..models.models import *
from flask import jsonify
from exts import db
from scrapyd_requests import *
import copy
import os

bp = Blueprint("client", __name__, url_prefix='/client')


@bp.route('/index')
@login_required
def index():
    return render_template('index.html', username=session.get('UserName'))


@bp.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', username=session.get('UserName'))


@bp.route('/projects')
@login_required
def projects():
    return render_template('project-list.html')


@bp.route('/hlist')
@login_required
def hlist():
    host_list = HostList.query.all()
    counts = len(host_list)
    return render_template('host-list.html', host_list=host_list,counts = counts)


@bp.route('/test')
@login_required
def test():
    items = []
    item = {}
    host_list = HostList.query.all()
    for host in host_list:
        item['status'] = '正在连接'
        item['id'] = host.id
        item['host_name'] = host.host_name
        item['port_num'] = host.port_num
        item['ip_address'] = host.ip_address
        item['create_time'] = host.create_time
        items.append(copy.deepcopy(item))

    return jsonify({'host_list': items})


@bp.route('/dhost', methods=['POST'])
@login_required
def dhost():
    host_id = request.form.get("host_id")
    if not host_id:
        return jsonify({'code': 404, 'message': '请传入ID'})
    host = HostList.query.get(host_id)
    if not host:
        return jsonify({'code': 404, 'message': '没有这条数据'})

    db.session.delete(host)
    db.session.commit()
    return jsonify({'code': 200, 'message': '删除成功'})


@bp.route('/daemonstatus', methods=['POST'])
@login_required
def daemonstatus():
    ip_address = request.form.get('ip_address')
    port_num = request.form.get('port_num')
    req = connect_host(ip_address, port_num, 10)
    if req.get('status') == 'ok':
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 404, 'status': 'error'})


class Upload_Project(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('upload-project.html')

    def post(self):
        f = request.files['file']
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(base_path, 'utils')
        file_name = f.filename

        if f:
            f.save(r'C:\Users\Administrator\Desktop\上传文件\{}'.format(file_name))
            return jsonify({'code': 200,'message':'上传成功！'})
        else:
            return jsonify({'code': 200,'message':'获取文件失败！'})


class Host_add(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('host-add.html')

    def post(self):
        host_name = request.form.get('host_name')
        ip_address = request.form.get('ip_address')
        port_num = request.form.get('port_num')
        host_list = HostList(host_name=host_name, ip_address=ip_address, port_num=port_num)

        db.session.add(host_list)
        db.session.commit()
        return jsonify({'code': 200})

class Host_update(MethodView):
    decorators = [login_required]

    def get(self):
        host_id = request.args.get('id')
        if not host_id:
            return jsonify({'code': 404, 'message': '请传入ID'})
        host = HostList.query.get(host_id)
        return render_template('host-update.html',host_info=host)

    def post(self):
        host_name = request.form.get('host_name')
        ip_address = request.form.get('ip_address')
        port_num = request.form.get('port_num')
        host_id = request.form.get('host_id')
        host_info = HostList.query.get(host_id)

        if host_info:
            host_info.host_name = host_name
            host_info.ip_address = ip_address
            host_info.port_num = port_num

            db.session.commit()
            return jsonify({'code': 200})
        else:
            return jsonify({'code': 404})


class Login(MethodView):

    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['UserName'] = user.username
            session[config.USER_ID] = user.id
            return redirect(url_for('client.index'))
        else:
            return self.get()


bp.add_url_rule('/login', view_func=Login.as_view('login'))
bp.add_url_rule('/hadd', view_func=Host_add.as_view('hadd'))
bp.add_url_rule('/hupdate', view_func=Host_update.as_view('hupdate'))
bp.add_url_rule('/upload_project', view_func=Upload_Project.as_view('upload_project'))
