DEBUG = True
import pymysql

#BOOTSTRAP_SERVE_LOCAL = True
#SECRET_KEY = os.urandom(24)

DIALECT ='mysql'
DRIVER = 'pymysql'
USERNAME ='root'
PASSWORD ='123qwe'
HOST='127.0.0.1'
PORT='3306'
DATABASE='flask'

DB_URL ='{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URL

SQLALCHEMY_TRACK_MODIFICATIONS=False


db= pymysql.connect(host='127.0.0.1',user='root',
    password='123qwe',db='flask',port=3306,charset='utf8')