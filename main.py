from flask import Flask
from flask import render_template
from flask import g
from flask import  flash, request, redirect, url_for
from flask import send_from_directory, make_response
from flask import session
import os
import sqlite3
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/naught/prj/conf/static/images/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DATABASE = 'conf.db'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post.html')
