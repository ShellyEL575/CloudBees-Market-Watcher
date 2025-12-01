import feedparser
import yaml
import requests
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import re
import time
from datetime import datetime, timedelta

# Suppress XML parsed as HTML warnings from BeautifulSoup
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

RECENT_DAYS = 30  # only keep posts from the last 30 days
CUTOFF_DATE = datetime.utcnow() - timedelta(days=RECENT_DAYS)

def clean_feed_content(content):
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)

def extract_link_from_summary(summary):
    match = re.search(r'href="(https?://[^\"]+)"', summary)
    return match.group(1) if match else ""

def classify_post(title, summary):
    title_summary = f"{title} {summary}".lower()
    if any(kw in title_summary for kw in ["security", "vulnerability", "breach", "attack", "malware", "cve"]):
        return "🛡️ Security Alert"
    if any(kw in title_summary for kw in ["launch", "update", "release", "improvement", "feature", "announcement"]):
        return "🚀 Product Updates"
    if any(kw in title_summary for kw in ["case study", "customer", "story"]):
        return "👥 Customer Story"
    if any(kw in title_summary for kw in ["event", "webinar", "conference"]):
        return "📅 Event"
    return "📰 General"

def fetch_competitor_updates():
    with open("scraper/competitors.yaml") as f:
        urls = yaml.safe_load(f)

    posts = []
    brand_stats = {}
    type_stats = {}

    for brand, feed_urls in urls.items():
        total_entries = 0
        for url in feed_urls:
            try:
                response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                response.encoding = 'utf-8'
                cleaned_content = clean_feed_content(response.text)
                feed = feedparser.parse(cleaned_content)
            except Exception as e:
                print(f"❌ Exception while fetching {brand} feed: {url} - {e}")
                continue

            if feed.bozo:
                print(f"❌ Feed parse error for {brand}: {url} (Error: {feed.bozo_exception})")
                continue

            entry_count = len(feed.entries)
            total_entries += entry_count

            for entry in feed.entries:
                title = entry.get("title") or entry.get("summary", "")[:100]
                link = (
                    entry.get("link")
                    or extract_link_from_summary(entry.get("summary", ""))
                    or entry.get("id")
                    or entry.get("href", "")
                )
                if not title or not link:
                    print(f"⚠️ Skipping entry missing title or link in {brand}: {entry}")
                    continue

                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    dt = datetime.fromtimestamp(time.mktime(published))
                else:
                    dt = datetime.utcnow()
                    print(f"⚠️ Missing timestamp for post '{title}' — using current time.")

                if dt < CUTOFF_DATE:
                    print(f"🕒 Skipping old post from {dt.date()}: {title}")
                    continue

                content_type = classify_post(title, entry.get("summary", ""))
                posts.append({
                    "source": brand,
                    "title": title,
                    "url": link,
                    "summary": entry.get("summary", ""),
                    "type": content_type,
                    "timestamp": dt.isoformat()
                })
                print(f"📦 Post added: {{'source': '{brand}', 'title': '{title}', 'url': '{link}', 'type': '{content_type}'}}")
                type_stats[content_type] = type_stats.get(content_type, 0) + 1

        brand_stats[brand] = total_entries

    print(f"\n✅ Competitor scraper pulled {len(posts)} posts from {len(urls)} brands.")
    for brand, count in brand_stats.items():
        print(f"   - {brand}: {count} posts")
        if count == 0:
            print(f"⚠️ No posts found for {brand}. Check feed URL or source availability.")

    print("\n📊 Content Type Breakdown:")
    for ctype, count in type_stats.items():
        print(f"   - {ctype}: {count} posts")

    return posts
