import os

from flask import Flask, render_template

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), )

app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db

db.init_app(app)

from . import auth

app.register_blueprint(auth.bp)

from . import search

app.register_blueprint(search.bp)

from . import myfav

app.register_blueprint(myfav.bp)

from . import myshow

app.register_blueprint(myshow.bp)


@app.route('/')
def index():
    return 'hello, world'


@app.route('/about', methods=('GET',))
def about():
    """About page"""
    return render_template('about.html')

@app.route('/error', methods=('GET',))
def error():
    """Error occurance page"""
    return render_template('error.html')
