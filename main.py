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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DATABASE = 'conf.db'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def index():
    con = get_db()
    next_page = 20
    posts = con.execute("SELECT * FROM posts WHERE id < 21")
    posts = posts.fetchall()
    print(posts[0][3])
    print(posts)
    print(posts[1][3])
    print(posts[2][3])

    return render_template('index.html', next_page=next_page, posts=posts)

@app.route('/page/<index>')
def index_amount(index):
    con = get_db()
    next_page = int(index) + 20

    posts = con.execute("SELECT * FROM posts WHERE id BETWEEN ? AND ?", (next_page, index))
    posts = posts.fetchall()
    print(posts)

    return render_template('index.html', next_page=next_page)

@app.route('/post/<post_id>')
def post(post_id):
    con = get_db()

    posts = con.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    posts = posts.fetchone()

    if posts == None:
        return "<h1> Page Not Found!</h1> Invalid Confession ID"

    return render_template('post.html', post=posts)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        file = request.files['file']
        if file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print("here")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db = get_db()
                db.execute("INSERT INTO posts (title, text, pic) VALUES(?, ?, ?)", 
                           (title, text, filename))

                db.commit()

                return redirect('/')

        db.execute("INSERT INTO posts (title, text) VALUES(?, ?)", 
                   (title, text))

        db.commit()

        return redirect('/')




    return render_template('submit.html')

@app.route('/about')
def about():
    return render_template('about.html')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
