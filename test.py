import sqlite3

con = sqlite3.connect("conf.db")
#posts = con.execute("SELECT * FROM posts ")
#
#print(posts.fetchall())
#for i in range(50):
#    con.execute("INSERT INTO posts (title, text) VALUES(?, ?)", 
#               (i, i))
#con.commit()
#con.close()


max_poll = con.execute("SELECT MAX(id) from polls;")
max_poll = con.execute("select * from polls")
max_poll = max_poll.fetchall()
print(max_poll[0][0])

