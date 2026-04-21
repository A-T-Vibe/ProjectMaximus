import pickle
import requests
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from database.db import get_conn, insert_stats
from config import META_ACCESS_TOKEN

TOKEN_FILE = "youtube_token.pkl"
BASE_META = "https://graph.facebook.com/v19.0"


def collect_all():
    print("Collecting YouTube stats...")
    _collect_youtube()
    print("Collecting Instagram stats...")
    _collect_instagram()
    print("Stats collection complete.")


def _collect_youtube():
    if not _youtube_token_exists():
        return

    creds = None
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds)
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, platform_post_id FROM posts WHERE platform='youtube' AND platform_post_id IS NOT NULL"
    ).fetchall()
    conn.close()

    if not rows:
        return

    video_ids = [r["platform_post_id"] for r in rows]
    id_to_post = {r["platform_post_id"]: r["id"] for r in rows}

    resp = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids),
    ).execute()

    for item in resp.get("items", []):
        vid_id = item["id"]
        stats = item.get("statistics", {})
        insert_stats(
            post_id=id_to_post[vid_id],
            views=int(stats.get("viewCount", 0)),
            likes=int(stats.get("likeCount", 0)),
            comments=int(stats.get("commentCount", 0)),
            shares=0,
        )


def _collect_instagram():
    if not META_ACCESS_TOKEN:
        return

    conn = get_conn()
    rows = conn.execute(
        "SELECT id, platform_post_id FROM posts WHERE platform='instagram' AND platform_post_id IS NOT NULL"
    ).fetchall()
    conn.close()

    for row in rows:
        resp = requests.get(
            f"{BASE_META}/{row['platform_post_id']}/insights",
            params={
                "metric": "plays,likes,comments,shares",
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=30,
        )
        if resp.status_code != 200:
            continue

        metrics = {m["name"]: m["values"][0]["value"] for m in resp.json().get("data", [])}
        insert_stats(
            post_id=row["id"],
            views=metrics.get("plays", 0),
            likes=metrics.get("likes", 0),
            comments=metrics.get("comments", 0),
            shares=metrics.get("shares", 0),
        )


def _youtube_token_exists():
    import os
    return os.path.exists(TOKEN_FILE)
