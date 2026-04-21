import requests
from config import TIKTOK_ACCESS_TOKEN

BASE_URL = "https://open.tiktokapis.com/v2"


def upload(video_path, title, hashtags):
    """
    Upload a video to TikTok via the Content Posting API.
    Requires approved API access from developers.tiktok.com.
    """
    # Step 1: Initialise upload
    resp = requests.post(
        f"{BASE_URL}/post/video/init/",
        headers={
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={
            "post_info": {
                "title": f"{title} {hashtags}"[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": _file_size(video_path),
                "chunk_size": _file_size(video_path),
                "total_chunk_count": 1,
            },
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    publish_id = data["publish_id"]
    upload_url = data["upload_url"]

    # Step 2: Upload file
    with open(video_path, "rb") as f:
        video_bytes = f.read()

    upload_resp = requests.put(
        upload_url,
        headers={
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes 0-{len(video_bytes)-1}/{len(video_bytes)}",
        },
        data=video_bytes,
        timeout=120,
    )
    upload_resp.raise_for_status()

    print(f"TikTok video published: {publish_id}")
    return publish_id


def _file_size(path):
    import os
    return os.path.getsize(path)
