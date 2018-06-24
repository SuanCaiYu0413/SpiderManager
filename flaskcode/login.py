from flask import Flask,render_template,request,jsonify
import config
from flask.views import MethodView
from flask_bootstrap import Bootstrap
from config import db


app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():
    content=[]
    cur = db.cursor()
    sql = "select city from city_list"
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        city = row[0]
        content.append(city)

    content = content
    return render_template('select.html',content=content)

@app.route('/select/')
def select():
    select_key = request.args.get('select_key')
    return jsonify({'result':select_key})

class Login(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'yc' and password =='111111':
            return render_template('select.html')
        else:
            return self.get()

app.add_url_rule('/login/',view_func=Login.as_view('login'))


if __name__ == '__main__':
    app.run()




