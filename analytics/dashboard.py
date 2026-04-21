from flask import Flask, render_template_string
from database.db import get_recent_posts, get_credits_used, get_conn
from config import KLING_MONTHLY_CREDIT_LIMIT, HAILUO_MONTHLY_CREDIT_LIMIT, PIKA_MONTHLY_CREDIT_LIMIT

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>ProjectMaximus Dashboard</title>
  <style>
    body { font-family: sans-serif; max-width: 1100px; margin: 40px auto; padding: 0 20px; background: #0f0f0f; color: #eee; }
    h1 { color: #ff4d4d; }
    h2 { color: #aaa; border-bottom: 1px solid #333; padding-bottom: 8px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
    th { background: #1a1a1a; padding: 10px; text-align: left; color: #ff4d4d; }
    td { padding: 10px; border-bottom: 1px solid #222; }
    tr:hover td { background: #1a1a1a; }
    .credits { display: flex; gap: 20px; margin-bottom: 30px; }
    .credit-card { background: #1a1a1a; padding: 16px 24px; border-radius: 8px; min-width: 160px; }
    .credit-card h3 { margin: 0 0 8px; font-size: 14px; color: #aaa; }
    .credit-card .number { font-size: 28px; font-weight: bold; color: #ff4d4d; }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    .published { background: #1a3a1a; color: #4caf50; }
    .failed { background: #3a1a1a; color: #f44336; }
    .pending { background: #2a2a1a; color: #ff9800; }
  </style>
</head>
<body>
  <h1>ProjectMaximus</h1>

  <h2>Generator Credits Remaining This Month</h2>
  <div class="credits">
    {% for g in generators %}
    <div class="credit-card">
      <h3>{{ g.name | title }}</h3>
      <div class="number">{{ g.remaining }}</div>
      <div style="font-size:12px;color:#666">/ {{ g.limit }} free</div>
    </div>
    {% endfor %}
  </div>

  <h2>Recent Posts</h2>
  <table>
    <tr>
      <th>Platform</th><th>Status</th><th>Posted</th><th>Views</th><th>Likes</th><th>Generator</th><th>Prompt</th>
    </tr>
    {% for post in posts %}
    <tr>
      <td>{{ post.platform | title }}</td>
      <td><span class="badge {{ post.status }}">{{ post.status }}</span></td>
      <td>{{ post.posted_at or '—' }}</td>
      <td>{{ post.views or 0 }}</td>
      <td>{{ post.likes or 0 }}</td>
      <td>{{ post.generator_used }}</td>
      <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="{{ post.prompt }}">{{ post.prompt[:80] }}...</td>
    </tr>
    {% endfor %}
  </table>

  <h2>Top Performing Videos</h2>
  <table>
    <tr><th>Prompt</th><th>Platform</th><th>Views</th><th>Likes</th></tr>
    {% for post in top_posts %}
    <tr>
      <td style="max-width:400px">{{ post.prompt[:100] }}</td>
      <td>{{ post.platform | title }}</td>
      <td>{{ post.views or 0 }}</td>
      <td>{{ post.likes or 0 }}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
"""


@app.route("/")
def index():
    posts = get_recent_posts(limit=50)
    top_posts = sorted(posts, key=lambda p: p["views"] or 0, reverse=True)[:10]

    generators = [
        {"name": "Kling",   "remaining": KLING_MONTHLY_CREDIT_LIMIT   - get_credits_used("kling")["credits_used"],  "limit": KLING_MONTHLY_CREDIT_LIMIT},
        {"name": "Hailuo",  "remaining": HAILUO_MONTHLY_CREDIT_LIMIT  - get_credits_used("hailuo")["credits_used"], "limit": HAILUO_MONTHLY_CREDIT_LIMIT},
        {"name": "Pika",    "remaining": PIKA_MONTHLY_CREDIT_LIMIT    - get_credits_used("pika")["credits_used"],   "limit": PIKA_MONTHLY_CREDIT_LIMIT},
    ]

    return render_template_string(HTML, posts=posts, top_posts=top_posts, generators=generators)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
