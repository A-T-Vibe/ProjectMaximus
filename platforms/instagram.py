import time
import requests
from config import META_ACCESS_TOKEN, META_INSTAGRAM_ACCOUNT_ID

BASE_URL = "https://graph.facebook.com/v19.0"


def upload(video_path, caption, hashtags):
    """
    Upload a Reel to Instagram via Meta Graph API.
    Uses the two-step container + publish flow.
    Returns the media ID of the published post.
    """
    full_caption = f"{caption}\n\n{hashtags}"

    # Step 1: Create container
    resp = requests.post(
        f"{BASE_URL}/{META_INSTAGRAM_ACCOUNT_ID}/media",
        data={
            "media_type": "REELS",
            "video_url": _upload_to_accessible_url(video_path),
            "caption": full_caption,
            "access_token": META_ACCESS_TOKEN,
        },
        timeout=60,
    )
    resp.raise_for_status()
    container_id = resp.json()["id"]

    # Step 2: Wait for container to be ready
    _wait_for_container(container_id)

    # Step 3: Publish
    resp = requests.post(
        f"{BASE_URL}/{META_INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": META_ACCESS_TOKEN,
        },
        timeout=30,
    )
    resp.raise_for_status()
    media_id = resp.json()["id"]
    print(f"Instagram Reel published: {media_id}")
    return media_id


def _wait_for_container(container_id, max_wait=120):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        resp = requests.get(
            f"{BASE_URL}/{container_id}",
            params={
                "fields": "status_code,status",
                "access_token": META_ACCESS_TOKEN,
            },
            timeout=30,
        )
        resp.raise_for_status()
        status = resp.json().get("status_code")
        if status == "FINISHED":
            return
        elif status == "ERROR":
            raise RuntimeError(f"Instagram container failed: {resp.json()}")
        time.sleep(10)
    raise TimeoutError("Instagram container did not become ready in time")


def _upload_to_accessible_url(video_path):
    """
    Instagram requires a publicly accessible video URL.
    For now, raise a NotImplementedError — this will be replaced
    with a file hosting step (e.g. upload to a temporary CDN or
    self-hosted endpoint) once the server is configured.
    """
    raise NotImplementedError(
        "Instagram requires a public video URL. "
        "Set up a file hosting step (e.g. upload to your server's public directory) "
        "and return the URL here."
    )
