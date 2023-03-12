CREATE TABLE posts (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	text TEXT NOT NULL,
	pic TEXT, 
);

CREATE TABLE replies (
	id INTEGER KEY,
	reply TEXT 
);


