# @Time    : 2018/6/14 16:00
# @Author  : SuanCaiYu
# @File    : models
# @Software: PyCharm
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(50), nullable=False)
    _password = db.Column(db.VARCHAR(320), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self._password = generate_password_hash(password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result



class HostList(db.Model):
    __tablename__ = 'host_list'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    host_name = db.Column(db.String(50),nullable=False)
    ip_address = db.Column(db.String(50),nullable=False)
    port_num = db.Column(db.String(50),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    user = db.Column(db.VARCHAR(50), nullable=True)
    pwd = db.Column(db.VARCHAR(50), nullable=True)