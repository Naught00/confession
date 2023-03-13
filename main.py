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
    posts = con.execute("select * from posts order by id desc limit 20;")
    posts = posts.fetchall()

    i = 0
    for _ in posts:
        replies = con.execute("SELECT * FROM replies WHERE post_id=?", (posts[i][0],))
        replies = replies.fetchall()
        posts[i] += (len(replies),)
        print("post count", posts[i][4])
        i += 1


    for post in posts:
        print("post count", post[4])

    print(posts[0][3])
    print(posts)
    print(posts[1][3])
    print(posts[2][3])

    return render_template('index.html', next_page=next_page, posts=posts)

@app.route('/page/<index>')
def index_amount(index):
    back_button = True

    con = get_db()

    index = int(index)
    next_page = index + 20
    previous_page = index - 20
    print("PREVIOUS PAGE:", previous_page)

    posts = con.execute("select * from posts order by id desc limit ?;", (next_page,))
    posts = posts.fetchall()
    posts = posts[index:]


    return render_template('index.html', next_page=next_page, posts=posts, back_button=back_button, previous_page=previous_page)

@app.route('/post/<post_id>')
def post(post_id):
    con = get_db()

    posts = con.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    replies = con.execute("SELECT * FROM replies WHERE post_id=?", (post_id,))
    replies_to_replies = con.execute("SELECT * FROM replies_to_replies WHERE post_id=?", (post_id,))

    posts = posts.fetchone()

    replies = replies.fetchall()
    replies_to_replies = replies_to_replies.fetchall()
    print(replies_to_replies)
    replies.reverse()

    if posts == None:
        return "<h1> Page Not Found!</h1> Invalid Confession ID"

    if replies == None:
        return render_template('post.html', post=posts)
    elif replies_to_replies == None:
        return render_template('post.html', post=posts, replies=replies)

    print("REPLIES", replies)
    return render_template('post.html', post=posts, replies=replies, replies_to_replies=replies_to_replies)

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

@app.route('/reply', methods=['POST'])
def reply():
    db = get_db()

    text = request.form['text']
    post_id = request.form['post_id']

    print(type(text))
    if len(text) > 20000:
        return "Post too big!"

    db.execute("INSERT INTO replies (post_id, reply) VALUES(?, ?)", 
               (post_id, text))

    db.commit()

    return redirect(f"/post/{post_id}")

@app.route('/reply-to-comment', methods=['POST'])
def reply_to_comment():
    db = get_db()

    text = request.form['text']
    post_id = request.form['post_id']
    reply_id = request.form['reply_id']

    print(type(text))
    if len(text) > 20000:
        return "Post too big!"

    db.execute("INSERT INTO replies_to_replies (post_id, reply_id, reply) VALUES(?, ?, ?)", 
               (post_id, reply_id, text))

    db.commit()

    return redirect(f"/post/{post_id}")
