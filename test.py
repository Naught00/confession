import sqlite3

con = sqlite3.connect("test.db")
posts = con.execute("SELECT * FROM posts ")

print(posts.fetchall())
for i in range(100):
    con.execute("INSERT INTO posts (title, text, timestamp, last_reply_timestamp) VALUES(?, ?, ?, ?)", 
               (i, i, i, i))
con.commit()
con.close()


#max_poll = con.execute("SELECT MAX(id) from polls;")
#max_poll = con.execute("select * from polls")
#max_poll = max_poll.fetchall()
#print(max_poll[0][0])

