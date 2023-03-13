CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        pic TEXT
, timestamp integer, poll_id integer);
CREATE TABLE replies (
        id INTEGER PRIMARY KEY,
        post_id INTEGER,
        reply TEXT
, timestamp integer);
CREATE TABLE replies_to_replies (
        id INTEGER PRIMARY KEY,
        post_id INTEGER,
        reply_id INTEGER,
        reply TEXT
, timestamp integer);
CREATE TABLE polls (
        id INTEGER PRIMARY KEY,
        title text,
        option1 text,
        option2 text,
        option1p integer,
        option2p integer
);
