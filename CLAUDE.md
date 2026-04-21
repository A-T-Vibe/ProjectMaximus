# ProjectMaximus

## Project Overview
Fully automated viral video channel. Generates short satisfying/ASMR-style videos using free AI tiers and posts to YouTube Shorts, Instagram Reels, Facebook Reels, and TikTok at peak UK commuter times (8AM, 4PM, 6PM). Tracks analytics via a local web dashboard.

## Architecture
```
Windows Task Scheduler → main.py
├── generators/     rotate across Kling / Hailuo (MiniMax) / Pika free tiers
├── content/        prompt library + FFmpeg video processing
├── platforms/      YouTube / Instagram / TikTok posting
├── analytics/      stats collection + Flask dashboard (localhost:5000)
└── database/       SQLite (projectmaximus.db)
```

## Prerequisites (install before running)
- **Python 3.11+** — python.org/downloads
- **FFmpeg** — ffmpeg.org/download.html → add to PATH
- **Python packages** — `pip install -r requirements.txt`

## Setup Steps
1. Copy `.env.example` to `.env` and fill in API keys
2. Place YouTube `client_secret.json` in project root
3. Run `python main.py --generate-only` to test generation
4. Run `python main.py --post --platform youtube --dry-run` to test YouTube auth
5. Run `python scheduler/windows_tasks.py` (as Administrator) to register scheduled tasks

## Common Commands
```bash
# Test video generation only
python main.py --generate-only

# Post to all platforms
python main.py --post

# Post to one platform
python main.py --post --platform youtube

# Test without actually posting
python main.py --post --dry-run

# Pull analytics stats
python main.py --collect-stats

# Launch dashboard at localhost:5000
python main.py --dashboard

# Register Windows scheduled tasks
python scheduler/windows_tasks.py

# Remove scheduled tasks
python scheduler/windows_tasks.py --remove
```

## Video Generation (Free Tiers)
| Service | Free Credits/Month | Sign Up |
|---|---|---|
| Kling AI | ~166 | klingai.com |
| Hailuo (MiniMax) | ~100 | hailuoai.video / platform.minimaxi.com |
| Pika | ~150 | pika.art |

## Platform API Setup
| Platform | API | Status |
|---|---|---|
| YouTube Shorts | YouTube Data API v3 (Google Cloud Console) | Phase 1 |
| Instagram Reels | Meta Graph API (developers.facebook.com) | Phase 2 |
| Facebook Reels | Meta Graph API (same app as Instagram) | Phase 2 |
| TikTok | Content Posting API (developers.tiktok.com) | Phase 2 — needs approval |

## Credentials Email
projectmaximus@amtierney.co.uk

## Repository
- **GitHub:** https://github.com/A-T-Vibe/ProjectMaximus
- Auto-backup: Stop hook commits and pushes changes after each Claude session

## Change Log
| Date | Change |
|------|--------|
| 2026-04-21 | Project initialised, CLAUDE.md created, GitHub repo set up |
| 2026-04-21 | Full application built: generators, platforms, analytics, scheduler |
