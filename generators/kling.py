import os
import time
import requests
from config import KLING_API_KEY, VIDEOS_DIR

BASE_URL = "https://api.klingai.com/v1"
GENERATOR_NAME = "kling"


def generate(prompt, duration=10, aspect_ratio="9:16"):
    """
    Submit a video generation task to Kling AI and poll until complete.
    Returns local file path of the downloaded video.
    """
    headers = {
        "Authorization": f"Bearer {KLING_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "kling-v1",
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "cfg_scale": 0.5,
    }

    resp = requests.post(f"{BASE_URL}/videos/text2video", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    task_id = resp.json()["data"]["task_id"]

    return _poll_and_download(task_id, headers)


def _poll_and_download(task_id, headers, max_wait=300):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        resp = requests.get(f"{BASE_URL}/videos/text2video/{task_id}", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("task_status")

        if status == "succeed":
            video_url = data["task_result"]["videos"][0]["url"]
            return _download(video_url, task_id)
        elif status == "failed":
            raise RuntimeError(f"Kling generation failed: {data.get('task_status_msg')}")

        time.sleep(10)

    raise TimeoutError(f"Kling task {task_id} did not complete within {max_wait}s")


def _download(url, task_id):
    output_path = os.path.join(VIDEOS_DIR, f"kling_{task_id}.mp4")
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def credits_cost():
    return 1
