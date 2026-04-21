import os
import time
import requests
from config import PIKA_API_KEY, VIDEOS_DIR

BASE_URL = "https://api.pika.art/v1"
GENERATOR_NAME = "pika"


def generate(prompt, duration=8, aspect_ratio="9:16"):
    """
    Submit a video generation task to Pika and poll until complete.
    Returns local file path of the downloaded video.
    """
    headers = {
        "Authorization": f"Bearer {PIKA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "promptText": prompt,
        "options": {
            "aspectRatio": aspect_ratio,
            "frameRate": 24,
            "duration": duration,
        },
    }

    resp = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    task_id = resp.json()["data"]["id"]

    return _poll_and_download(task_id, headers)


def _poll_and_download(task_id, headers, max_wait=300):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        resp = requests.get(f"{BASE_URL}/generate/{task_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("status")

        if status == "finished":
            video_url = data["video"]["url"]
            return _download(video_url, task_id)
        elif status == "failed":
            raise RuntimeError(f"Pika generation failed for task {task_id}")

        time.sleep(10)

    raise TimeoutError(f"Pika task {task_id} did not complete within {max_wait}s")


def _download(url, task_id):
    output_path = os.path.join(VIDEOS_DIR, f"pika_{task_id}.mp4")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def credits_cost():
    return 1
