import sqlite3
import os
from datetime import datetime
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            generator_used TEXT NOT NULL,
            file_path TEXT NOT NULL,
            duration INTEGER,
            created_at TEXT DEFAULT (datetime('now')),
            status TEXT DEFAULT 'ready'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            platform_post_id TEXT,
            posted_at TEXT,
            scheduled_time TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (video_id) REFERENCES videos(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            collected_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (post_id) REFERENCES posts(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS generator_credits (
            generator TEXT PRIMARY KEY,
            credits_used INTEGER DEFAULT 0,
            credits_reset_date TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_video(prompt, generator_used, file_path, duration=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO videos (prompt, generator_used, file_path, duration) VALUES (?, ?, ?, ?)",
        (prompt, generator_used, file_path, duration)
    )
    video_id = c.lastrowid
    conn.commit()
    conn.close()
    return video_id


def insert_post(video_id, platform, scheduled_time=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (video_id, platform, scheduled_time) VALUES (?, ?, ?)",
        (video_id, platform, scheduled_time)
    )
    post_id = c.lastrowid
    conn.commit()
    conn.close()
    return post_id


def update_post_published(post_id, platform_post_id):
    conn = get_conn()
    conn.execute(
        "UPDATE posts SET platform_post_id=?, posted_at=datetime('now'), status='published' WHERE id=?",
        (platform_post_id, post_id)
    )
    conn.commit()
    conn.close()


def update_post_failed(post_id, reason=""):
    conn = get_conn()
    conn.execute(
        "UPDATE posts SET status='failed' WHERE id=?",
        (post_id,)
    )
    conn.commit()
    conn.close()


def insert_stats(post_id, views, likes, comments, shares):
    conn = get_conn()
    conn.execute(
        "INSERT INTO stats (post_id, views, likes, comments, shares) VALUES (?, ?, ?, ?, ?)",
        (post_id, views, likes, comments, shares)
    )
    conn.commit()
    conn.close()


def get_credits_used(generator):
    conn = get_conn()
    row = conn.execute(
        "SELECT credits_used, credits_reset_date FROM generator_credits WHERE generator=?",
        (generator,)
    ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"credits_used": 0, "credits_reset_date": None}


def increment_credits(generator, amount=1):
    conn = get_conn()
    conn.execute("""
        INSERT INTO generator_credits (generator, credits_used, credits_reset_date)
        VALUES (?, ?, date('now', 'start of month', '+1 month'))
        ON CONFLICT(generator) DO UPDATE SET credits_used = credits_used + ?
    """, (generator, amount, amount))
    conn.commit()
    conn.close()


def reset_credits_if_new_month(generator):
    conn = get_conn()
    row = conn.execute(
        "SELECT credits_reset_date FROM generator_credits WHERE generator=?",
        (generator,)
    ).fetchone()
    if row and row["credits_reset_date"]:
        reset_date = datetime.strptime(row["credits_reset_date"], "%Y-%m-%d")
        if datetime.now() >= reset_date:
            conn.execute(
                "UPDATE generator_credits SET credits_used=0, credits_reset_date=date('now', 'start of month', '+1 month') WHERE generator=?",
                (generator,)
            )
            conn.commit()
    conn.close()


def get_recent_posts(limit=50):
    conn = get_conn()
    rows = conn.execute("""
        SELECT p.id, p.platform, p.status, p.posted_at,
               v.prompt, v.generator_used,
               MAX(s.views) as views, MAX(s.likes) as likes
        FROM posts p
        JOIN videos v ON p.video_id = v.id
        LEFT JOIN stats s ON s.post_id = p.id
        GROUP BY p.id
        ORDER BY p.posted_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
