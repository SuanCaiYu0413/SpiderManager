# @Time    : 2018/6/14 17:07
# @Author  : SuanCaiYu
# @File    : manage
# @Software: PyCharm
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config
from exts import db
import apps.models.models as cms_models

User = cms_models.Users
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_cms_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


if __name__ == '__main__':
    manager.run()
