import os
import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SQLITE_DB", "analytics.db")

SCHEMA = '''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    post_id TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT,
    created_at TEXT NOT NULL,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    followers INTEGER DEFAULT 0,
    url TEXT,
    sentiment REAL,
    engagement_rate REAL,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author);
'''

@contextmanager
def get_conn():
    new_db = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        if new_db:
            conn.executescript(SCHEMA)
            conn.commit()
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        conn.commit()

def bulk_insert_posts(rows):
    with get_conn() as conn:
        conn.executemany(
            '''INSERT INTO posts
            (platform, post_id, author, content, created_at, likes, comments, shares, views, followers, url, sentiment, engagement_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            rows
        )
        conn.commit()

def query_one(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.fetchone()

def query_all(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.fetchall()
