# @Time    : 2018/6/14 16:12
# @Author  : SuanCaiYu
# @File    : views
# @Software: PyCharm

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask.views import MethodView
import config
from apps.check.decorators import login_required
from apps.models.models import *

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
    return render_template('host-list.html')


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
