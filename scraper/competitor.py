# scraper/competitor.py

import feedparser
import yaml
import requests
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import re

# Suppress XML parsed as HTML warnings from BeautifulSoup
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def clean_feed_content(content):
    """Sanitize malformed XML using built‑in HTML parser."""
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)


def extract_link_from_summary(summary):
    """Fallback: extract article URL from summary HTML if <link> is missing."""
    match = re.search(r'href="(https?://[^"]+)"', summary)
    return match.group(1) if match else ""


def fetch_competitor_updates():
    """Load competitor RSS feeds and extract posts safely."""
    with open("scraper/competitors.yaml") as f:
        urls = yaml.safe_load(f)

    posts = []
    brand_stats = {}

    for brand, feed_urls in urls.items():
        total_entries = 0

        for url in feed_urls:
            try:
                response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                response.encoding = "utf-8"
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
                title = entry.get("title")
                if not title:
                    title = entry.get("id") or entry.get("summary", "")[:80]  # fallback title

                link = entry.get("link") or extract_link_from_summary(entry.get("summary", ""))
                if not link:
                    print(f"⚠️ Skipping entry with missing link in {brand}: {entry}")
                    continue

                posts.append({
                    "source": brand,
                    "title": title,
                    "url": link,
                    "summary": entry.get("summary", ""),
                    "type": "🚀 Product Updates",
                })

        brand_stats[brand] = total_entries

    # Summary report
    print(f"\n✅ Competitor scraper pulled {len(posts)} posts from {len(urls)} brands.")
    for brand, count in brand_stats.items():
        print(f"   - {brand}: {count} posts")
        if count == 0:
            print(f"⚠️ No posts found for {brand}. Check feed URL or source availability.")

    return posts
