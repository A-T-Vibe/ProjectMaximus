"""
ProjectMaximus — main orchestrator.

Usage:
  python main.py --post                         # generate + post to all platforms
  python main.py --post --platform youtube      # post to one platform only
  python main.py --generate-only               # generate video, skip posting
  python main.py --collect-stats               # pull analytics from APIs
  python main.py --dashboard                   # launch web dashboard
  python main.py --post --dry-run              # full flow without actually posting
"""
import argparse
import os
import sys

from database.db import init_db, insert_video, insert_post, update_post_published, update_post_failed
from generators import generate_video
from content.prompts import get_random_prompt
from content.processor import process_video


PLATFORMS = ["youtube", "instagram", "tiktok"]


def run_post(platform_filter=None, dry_run=False):
    init_db()

    prompt_data = get_random_prompt()
    prompt = prompt_data["prompt"]
    hashtags = prompt_data["hashtags"]
    audio_file = prompt_data["audio_file"]
    category = prompt_data["category"]

    print(f"Category: {category}")
    print(f"Prompt: {prompt}")

    print("Generating video...")
    generator_name, raw_path = generate_video(prompt)
    print(f"Generated: {raw_path}")

    output_filename = os.path.basename(raw_path).replace(".mp4", "_processed.mp4")
    print("Processing video...")
    processed_path = process_video(raw_path, audio_file, output_filename)
    print(f"Processed: {processed_path}")

    video_id = insert_video(prompt, generator_name, processed_path)

    title = f"Oddly Satisfying {category.replace('_', ' ').title()}"

    targets = PLATFORMS if platform_filter is None else [platform_filter]

    for platform in targets:
        post_id = insert_post(video_id, platform)
        if dry_run:
            print(f"[DRY RUN] Would post to {platform}")
            continue
        try:
            platform_post_id = _post_to(platform, processed_path, title, hashtags)
            update_post_published(post_id, platform_post_id)
            print(f"Posted to {platform}: {platform_post_id}")
        except NotImplementedError as e:
            print(f"Skipping {platform}: {e}")
            update_post_failed(post_id)
        except Exception as e:
            print(f"Failed to post to {platform}: {e}")
            update_post_failed(post_id)


def _post_to(platform, video_path, title, hashtags):
    if platform == "youtube":
        from platforms.youtube import upload
        return upload(video_path, title, f"Satisfying video. {hashtags}", hashtags)
    elif platform == "instagram":
        from platforms.instagram import upload
        return upload(video_path, title, hashtags)
    elif platform == "tiktok":
        from platforms.tiktok import upload
        return upload(video_path, title, hashtags)
    else:
        raise ValueError(f"Unknown platform: {platform}")


def run_collect_stats():
    init_db()
    from analytics.collector import collect_all
    collect_all()


def run_dashboard():
    from analytics.dashboard import app
    print("Dashboard running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ProjectMaximus orchestrator")
    parser.add_argument("--post", action="store_true", help="Generate and post a video")
    parser.add_argument("--generate-only", action="store_true", help="Generate video only, no posting")
    parser.add_argument("--collect-stats", action="store_true", help="Collect analytics from APIs")
    parser.add_argument("--dashboard", action="store_true", help="Launch web dashboard")
    parser.add_argument("--platform", type=str, help="Limit posting to one platform")
    parser.add_argument("--dry-run", action="store_true", help="Skip actual API posting")
    args = parser.parse_args()

    if args.post or args.generate_only:
        run_post(
            platform_filter=args.platform,
            dry_run=args.dry_run or args.generate_only,
        )
    elif args.collect_stats:
        run_collect_stats()
    elif args.dashboard:
        run_dashboard()
    else:
        parser.print_help()
