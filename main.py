from flask import Flask
from flask import render_template
from flask import g
from flask import  flash, request, redirect, url_for
from flask import send_from_directory, make_response
from flask import session
import sqlite3
from werkzeug.utils import secure_filename
import os
import time
from datetime import datetime
import json
import requests

UPLOAD_FOLDER = '/home/naught/prj/conf/static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
DATABASE = 'conf.db'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = b''

@app.route('/')
def index():
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    print(stamp)

    con = get_db()
    next_page = 20
    posts = con.execute("select * from posts order by id desc limit 20;")
    posts = posts.fetchall()
    print(posts)

    i = 0
    for _ in posts:
        replies = con.execute("SELECT * FROM replies WHERE post_id=?", (posts[i][0],))
        replies = replies.fetchall()
        posts[i] += (len(replies),)
        print("post count", posts[i][6])
        i += 1


    for post in posts:
        print("post count", post[6])


    return render_template('index.html', next_page=next_page, posts=posts, now=now, stamp=stamp)

@app.route('/page/<index>')
def index_amount(index):
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    print(stamp)
    back_button = True

    con = get_db()

    index = int(index)
    next_page = index + 20
    previous_page = index - 20
    print("PREVIOUS PAGE:", previous_page)

    posts = con.execute("select * from posts order by id desc limit ?;", (next_page,))
    posts = posts.fetchall()
    posts = posts[index:]


    return render_template('index.html', next_page=next_page, posts=posts, back_button=back_button, previous_page=previous_page, now=now, stamp=stamp)

@app.route('/post/<post_id>')
def post(post_id):
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    con = get_db()

    posts = con.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    replies = con.execute("SELECT * FROM replies WHERE post_id=?", (post_id,))
    replies_to_replies = con.execute("SELECT * FROM replies_to_replies WHERE post_id=?", (post_id,))

    posts = posts.fetchone()
    print("POSTS:", posts[5])

    # If we have a poll
    poll = None
    if posts[5]:
        poll_id = posts[5]
        poll = con.execute("SELECT * FROM polls WHERE id=?", (poll_id,))
        poll = poll.fetchone()

    replies = replies.fetchall()
    replies_to_replies = replies_to_replies.fetchall()
    print(replies_to_replies)
    replies.reverse()

    if posts == None:
        return "<h1> Page Not Found!</h1> Invalid Confession ID"

    if replies == None:
        return render_template('post.html', post=posts, now=now, stamp=stamp, poll=poll)

    if replies_to_replies == None:
        return render_template('post.html', post=posts, replies=replies, now=now, stamp=stamp, poll=poll)

    print("REPLIES", replies)
    return render_template('post.html', post=posts, replies=replies, replies_to_replies=replies_to_replies, now=now, stamp=stamp, poll=poll)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    timestamp = int(time.time())

    db = get_db()
    if request.method == 'POST':
        token = request.form['g-recaptcha-response']

        params = {
           'secret': '',
           'response': token
        }

        resp_json = requests.post('https://www.google.com/recaptcha/api/siteverify', params)
        resp = resp_json.json()

        print(resp['success'])
        if resp['success'] != True:
            return "<h1> Robot Detected! </h1>"


        title = request.form['title']
        text = request.form['text']

        link = False
        if request.form['is_link'] == '1':
            link = True

        poll_id = 0
        poll = False
        if request.form['boolean'] == 'true':
            poll = True
            poll_title = request.form['poll_title']
            poll_option1 = request.form['poll_option1']
            poll_option2 = request.form['poll_option2']
            db.execute("INSERT INTO polls (title, option1, option2, option1p, option2p) VALUES(?, ?, ?, ?, ?)", (poll_title, poll_option1, poll_option2, 0, 0))

            max_poll = db.execute("SELECT MAX(id) from polls;")
            max_poll = max_poll.fetchall()
            print(max_poll)
            if max_poll == None:
                poll_id = 1
            else:
                poll_id = max_poll[0][0]

        file = request.files['file']
        if file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db = get_db()


                if poll:
                    db.execute("INSERT INTO posts (title, text, pic, timestamp, poll_id, is_link) VALUES(?, ?, ?, ?, ?, ?)", (title, text, filename, timestamp, poll_id, link))
                else:
                    db.execute("INSERT INTO posts (title, text, pic, timestamp, is_link) VALUES(?, ?, ?, ?, ?)", (title, text, filename, timestamp, link))

                db.commit()

                return redirect('/')

        if poll:
            db.execute("INSERT INTO posts (title, text, timestamp, poll_id, is_link) VALUES(?, ?, ?, ?)", (title, text, timestamp, poll_id, link))
        else:
            db.execute("INSERT INTO posts (title, text, timestamp, is_link) VALUES(?, ?, ?, ?)", (title, text, timestamp, link))

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
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    text = request.form['text']
    post_id = request.form['post_id']

    print(type(text))
    if len(text) > 20000:
        return "Post too big!"

    db.execute("INSERT INTO replies (post_id, reply, timestamp) VALUES(?, ?, ?)", 
               (post_id, text, now))

    db.commit()

    return redirect(f"/post/{post_id}")

@app.route('/reply-to-comment', methods=['POST'])
def reply_to_comment():
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    text = request.form['text']
    post_id = request.form['post_id']
    reply_id = request.form['reply_id']

    print(type(text))
    if len(text) > 20000:
        return "Post too big!"

    db.execute("INSERT INTO replies_to_replies (post_id, reply_id, reply, timestamp) VALUES(?, ?, ?, ?)", 
               (post_id, reply_id, text, now))

    db.commit()

    return redirect(f"/post/{post_id}")


@app.route('/vote', methods=['POST'])
def vote():
    now = int(time.time())
    print(now)
    stamp = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    vote = request.form['vote']
    post_id = request.form['post_id']
    poll_id = request.form['poll_id']

    if poll_id in session:
        flash("You Can Only Vote Once!")
        return post(post_id)

    print(vote)

    option = None
    if vote == 'Vote 1':
        db.execute("UPDATE polls SET option1p = option1p + 1 where id=?", (poll_id,))
    else:
        db.execute("UPDATE polls SET option2p = option2p + 1 where id=?", (poll_id,))

    session[poll_id] = "voted"
    db.commit()
    db.close()
    return redirect(f"/post/{post_id}")

