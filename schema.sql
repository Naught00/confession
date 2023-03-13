CREATE TABLE posts (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	text TEXT NOT NULL,
	pic TEXT, 
);

CREATE TABLE replies (
	id INTEGER PRIMARY KEY,
	post_id INTEGER,
	reply TEXT 
);


CREATE TABLE replies_to_replies (
	id INTEGER PRIMARY KEY,
	post_id INTEGER,
	reply_id INTEGER,
	reply TEXT 
);
