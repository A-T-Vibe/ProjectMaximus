import os
import time
import requests
from config import HAILUO_API_KEY, HAILUO_GROUP_ID, VIDEOS_DIR

BASE_URL = "https://api.minimaxi.chat/v1"
GENERATOR_NAME = "hailuo"


def generate(prompt, duration=6):
    """
    Submit a video generation task to Hailuo (MiniMax) and poll until complete.
    Returns local file path of the downloaded video.
    """
    headers = {
        "Authorization": f"Bearer {HAILUO_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "video-01",
        "prompt": prompt,
    }

    resp = requests.post(
        f"{BASE_URL}/video_generation",
        json=payload,
        headers=headers,
        params={"GroupId": HAILUO_GROUP_ID},
        timeout=30,
    )
    resp.raise_for_status()
    task_id = resp.json()["task_id"]

    return _poll_and_download(task_id, headers)


def _poll_and_download(task_id, headers, max_wait=300):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        resp = requests.get(
            f"{BASE_URL}/query/video_generation",
            headers=headers,
            params={"task_id": task_id, "GroupId": HAILUO_GROUP_ID},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")

        if status == "Success":
            video_url = data["file_id"]
            return _download_by_file_id(video_url, headers, task_id)
        elif status == "Fail":
            raise RuntimeError(f"Hailuo generation failed for task {task_id}")

        time.sleep(10)

    raise TimeoutError(f"Hailuo task {task_id} did not complete within {max_wait}s")


def _download_by_file_id(file_id, headers, task_id):
    resp = requests.get(
        f"{BASE_URL}/files/retrieve",
        headers=headers,
        params={"file_id": file_id, "GroupId": HAILUO_GROUP_ID},
        timeout=30,
    )
    resp.raise_for_status()
    download_url = resp.json()["file"]["download_url"]

    output_path = os.path.join(VIDEOS_DIR, f"hailuo_{task_id}.mp4")
    video_resp = requests.get(download_url, stream=True, timeout=60)
    video_resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in video_resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


def credits_cost():
    return 1
