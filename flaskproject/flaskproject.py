from flask import Flask,url_for,redirect,render_template
import config


app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def hello_world():
    return redirect(url_for('login'))

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/moban/')
def moban():
    info={
        'age': 18,
        'name': None
    }
    return render_template('login.html',**info)

if __name__ == '__main__':
    app.run()
