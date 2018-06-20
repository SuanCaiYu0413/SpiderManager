# @Time    : 2018/6/14 15:43
# @Author  : SuanCaiYu
# @File    : main
# @Software: PyCharm

from flask import Flask, redirect, url_for, session
import config
from flask_wtf import CSRFProtect
from exts import db

from apps.client import bp as client_bp

from apps.api import bp as api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(client_bp)
    app.register_blueprint(api_bp)
    db.init_app(app)
    CSRFProtect(app)

    @app.route('/')
    def start():
        return redirect(url_for('client.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
