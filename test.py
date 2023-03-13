import sqlite3

con = sqlite3.connect("conf.db")
posts = con.execute("SELECT * FROM posts ")

print(posts.fetchall())
for i in range(50):
    con.execute("INSERT INTO posts (title, text) VALUES(?, ?)", 
               (i, i))
con.commit()
con.close()

