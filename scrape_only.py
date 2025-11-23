import os
from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.dev_blogs import fetch_blog_posts
from scraper.trend_classifier import classify_trends

# Aggregate all sources
posts = []
posts.extend(fetch_hn_stories())
posts.extend(fetch_blog_posts())
posts.extend(fetch_competitor_updates())

# Classify trends
trend_posts = classify_trends(posts)
posts.extend(trend_posts)

# Save to file for summarization
import json
from datetime import datetime
from pathlib import Path

Path("data").mkdir(exist_ok=True)
outfile = f"data/{datetime.now().strftime('%Y-%m-%d')}.json"
with open(outfile, "w") as f:
    json.dump(posts, f, indent=2)

print(f"✅ Collected {len(posts)} posts and saved to {outfile}")
