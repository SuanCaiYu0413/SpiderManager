# @Time    : 2018/6/14 16:29
# @Author  : SuanCaiYu
# @File    : hooks
# @Software: PyCharm

from .views import bp
import config
from apps.models.models import Users
from flask import session, g


@bp.before_request
def before_request():
    if config.USER_ID in session:
        user_id = session.get(config.USER_ID)
        user = Users.query.get(user_id)
        if user:
            g.cms_user = user
