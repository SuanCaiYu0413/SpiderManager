from flask import Flask,render_template,request,session
from flask.views import MethodView
from forms.forms import AddForm,UpdateForm
import restful
import config
from models import CMSUser,HostList
from exts import db
from flask_wtf import CSRFProtect
from decorators import login_required
from host_requests import connect_host,scrapyd_connerct


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CSRFProtect(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/deploy/')
@login_required
def deploy():
    return render_template('deploy.html')


@app.route('/log/')
@login_required
def log():
    return render_template('log.html')


@app.route('/pmanage/')
@login_required
def pmanage():
    host_list = HostList.query.all()
    return render_template('project_manage.html',host_list=host_list)


@app.route('/daemonstatus/', methods=['POST'])
@login_required
def daemonstatus():
    ip_address = request.form.get('ip_address')
    port_num = request.form.get('port_num')
    req = connect_host(ip_address,port_num,10)
    if req.get('status') == 'ok':
        return restful.success()
    else:
        return restful.unauth_error(message='连接失败')



@app.route('/pdelete/',methods=['POST'])
@login_required
def pdelete():
    host_id = request.form.get("host_id")
    if not host_id:
        return restful.params_error('请传入项目id！')
    host = HostList.query.get(host_id)
    if not host:
        return restful.params_error(message='没有这个项目！')

    db.session.delete(host)
    db.session.commit()
    return restful.success()


@app.route('/pcreate/',methods=['POST'])
@login_required
def pcreate():
    form = AddForm(request.form)
    if form.validate():
        host_name = request.form.get('host_name')
        ip_address = request.form.get('ip_address')
        port_num = request.form.get('port_num')
        host_list = HostList(host_name=host_name,ip_address=ip_address,port_num=port_num)

        db.session.add(host_list)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@app.route('/pupdate/',methods=['POST'])
@login_required
def pupdate():
    form = UpdateForm(request.form)
    if form.validate():
        host_id = request.form.get('host_id')
        host_name = request.form.get('host_name')
        ip_address = request.form.get('ip_address')
        port_num = request.form.get('port_num')
        host = HostList.query.get(host_id)
        if host:
            host.host_name = host_name
            host.ip_address = ip_address
            host.port_num = port_num
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个主机！')
    else:
        return restful.params_error(message=form.get_error())


@app.route('/psucedule/<id>')
@login_required
def psucedule(id):
    if id:
        host = HostList.query.get(id)
    return render_template('sucedule.html',host=host)


@app.route('/lprojects/', methods=['POST'])
@login_required
def lprojects():
    host_id = request.form.get('host_id')

    if host_id:
        host = HostList.query.get(host_id)
        ip_address = host.ip_address
        port_num = host.port_num
        scrapyd = scrapyd_connerct(ip_address, port_num)
        projects = scrapyd.list_projects()
        all_spiders = []
        if projects:
            for project in projects:
                list_spiders = scrapyd.list_jobs(project)
                all_spiders.append(list_spiders)
        projects_infos = [all_spiders,projects]
        return restful.restful_result(code=200,data=projects_infos,message='success')
    else:
        return restful.unauth_error(message='连接失败')



class Login(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        user = CMSUser.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session[config.CMS_USER_ID] = user.id
            return render_template('spider_base.html')
        else:
            return self.get()



app.add_url_rule('/login/',view_func=Login.as_view('login'))




if __name__ == '__main__':
    app.run(port=9000)
