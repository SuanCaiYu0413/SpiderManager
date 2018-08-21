# @Time    : 2018/6/14 16:12
# @Author  : SuanCaiYu
# @File    : views
# @Software: PyCharm

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask.views import MethodView
import config
from ..check.decorators import login_required
from ..models.models import HostList, ProjectList, Users
from flask import jsonify
from exts import db
from scrapyd_requests import *
import copy
import os
import time
import re
import shutil

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
    return render_template('host-list.html', host_list=host_list, counts=counts)


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
            return jsonify({'code': 200, 'message': '上传成功！'})
        else:
            return jsonify({'code': 200, 'message': '获取文件失败！'})


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
        return render_template('host-update.html', host_info=host)

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


# 项目管理模块
class Upload_Project(MethodView):
    decorators = [login_required]

    def get(self):
        # 查询数据展示
        try:
            root_dir = "E:\manage\SpiderManager\source\project"
            project_list = os.listdir(root_dir)
            for project in project_list:
                flag = ProjectList.query.filter_by(project_name=project).count()
                if not flag:
                    # 项目名称
                    # 项目加入时间
                    path = os.path.join(root_dir, project)
                    join_time_handle_one = os.path.getmtime(path)
                    join_time_handle_two = time.localtime(join_time_handle_one)
                    join_time = time.strftime("%Y-%m-%d %H:%M:%S", join_time_handle_two)
                    # 项目状态
                    status = "已上传"
                    project_list = ProjectList(project_name=project, join_time=join_time, status=status)
                    db.session.add(project_list)
                    db.session.commit()
            project_list = ProjectList.query.all()
        except Exception as e:
            return render_template("404.html"), 404
        return render_template("upload-project.html", project_list=project_list)

    def post(self):
        f = request.files
        try:
            root_dir = "E:\manage\SpiderManager\source\project"
            obj = f.to_dict()[""]
            relative_path = obj.filename.replace(r"/", "\\")
            path_handle = os.path.join(root_dir, relative_path)
            path = re.search(r"(.*)\\.*$", path_handle).group(1)
            if not os.path.exists(path):
                os.makedirs(path)
                with open(r"E:\manage\SpiderManager\source\project\{}".format(relative_path), "wb") as f:
                    f.write(obj.read())
            else:
                with open(r"E:\manage\SpiderManager\source\project\{}".format(relative_path), "wb") as f:
                    f.write(obj.read())
            return jsonify({"code": 200, "message": "上传成功"})
        except Exception as e:
            return jsonify({"code": 404, "message": "上传失败"})


class Del_Project(MethodView):
    decorators = [login_required]

    def post(self):
        try:
            name = request.form.get("name")
            path = "E:\manage\SpiderManager\source\project\{}".format(name)
            shutil.rmtree(path)
            root_dir = "E:\manage\SpiderManager\source\project"
            project_list = os.listdir(root_dir)
            flag = ProjectList.query.filter_by(project_name=name).first()
            if name not in project_list and flag:
                # session占用
                db.session.query(ProjectList).filter_by(project_name=name).delete()
                db.session.commit()
                return jsonify({"code": 200, "message": "删除成功!"})
        except Exception as e:
            return jsonify({"code": 404, "message": "删除失败"})


class Deploy_Project(MethodView):
    decorators = [login_required]

    def get(self):
        host_list = HostList.query.all()
        counts = len(host_list)
        project = request.args.get("project")
        return render_template('deploy-project.html', host_list=host_list, counts=counts, project=project)

    def post(self):
        try:
            host_list = request.form.get("host_list")
            if host_list:
                for host in host_list:
                    with open(r"E:\manage\SpiderManager\source\project\{}\scrapy.cfg".format(name), "a+") as f:
                        f.seek(0, 0)
                        deploy = "\n" + "\n" + "[deploy:{}]".format(host) + "\n" + "url=" + "http://{}:6800/".format(
                            ip) + "\n" + "project={}".format(name)
                        f.write(deploy)
            else:
                return jsonify({"code": 404, "message": "还未添加任何主机"})
            # 部署成功检测
            return jsonify({"code": 200, "message": "部署成功", "ip": "0.0.0.0"})
        except Exception as e:
            return jsonify({"message": "部署失败"})


class Deploy_Detail(MethodView):
    decorators = [login_required]

    def get(self):
        host_id = request.args.get("id")
        host = db.session.query(HostList).filter_by(id=host_id).first()
        project = request.args.get("project")
        return render_template("deploy-detail.html", host=host, project=project)

    def post(self):
        pass
        # os.chdir("E:\\Myproject\\SpiderManager-master\\source\\project\\{}".format(name))
        # os.system("scrapyd-deploy {} -v {}".format(host, version))


bp.add_url_rule('/login', view_func=Login.as_view('login'))
bp.add_url_rule('/hadd', view_func=Host_add.as_view('hadd'))
bp.add_url_rule('/hupdate', view_func=Host_update.as_view('hupdate'))
bp.add_url_rule('/upload_project', view_func=Upload_Project.as_view('upload_project'))
bp.add_url_rule('/del_project', view_func=Del_Project.as_view('del_project'))
bp.add_url_rule('/deploy_project', view_func=Deploy_Project.as_view('deploy_project'))
bp.add_url_rule('/deploy_detail', view_func=Deploy_Detail.as_view('deploy_detail'))
