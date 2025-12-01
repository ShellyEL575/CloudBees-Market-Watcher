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
    # Sanitize malformed XML using built-in HTML parser
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)

def extract_link_from_summary(summary):
    match = re.search(r'href="(https?://[^"]+)"', summary)
    return match.group(1) if match else ""

def classify_post_type(title, summary):
    combined = f"{title} {summary}".lower()
    if any(kw in combined for kw in ["release", "update", "announcing", "launched", " v", "version"]):
        return "🚀 Product Updates"
    if any(kw in combined for kw in ["security", "vulnerability", "cve", "supply chain"]):
        return "🛡️ Security Alert"
    if any(kw in combined for kw in ["how we", "lessons learned", "our take", "what we think"]):
        return "📢 Thought Leadership"
    if any(kw in combined for kw in ["case study", "customer", "success story", "migrated"]):
        return "📈 Case Study"
    if any(kw in combined for kw in ["tutorial", "how to", "benchmark", "demo"]):
        return "🧰 Technical Guide"
    return "🧵 Miscellaneous"

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
                title = entry.get("title", "").strip()
                link = entry.get("link") or extract_link_from_summary(entry.get("summary", ""))

                if not title or title.startswith("http"):
                    raw_summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()
                    title = raw_summary.strip().split(".")[0][:100].strip()
                    print(f"🔧 Using fallback title: {title[:60]}...")

                if not title or not link:
                    print(f"⚠️ Skipping entry missing title or link in {brand}: {entry}")
                    continue

                summary = entry.get("summary", "")
                post_type = classify_post_type(title, summary)
                type_stats[post_type] = type_stats.get(post_type, 0) + 1

                post = {
                    "source": brand,
                    "title": title,
                    "url": link,
                    "summary": summary,
                    "type": post_type
                }
                posts.append(post)
                print(f"📦 Post added: {post}")

        brand_stats[brand] = total_entries

    print(f"\n✅ Competitor scraper pulled {len(posts)} posts from {len(urls)} brands.")
    for brand, count in brand_stats.items():
        print(f"   - {brand}: {count} posts")
        if count == 0:
            print(f"⚠️ No posts found for {brand}. Check feed URL or source availability.")

    print("\n📊 Post Type Breakdown:")
    for t, count in type_stats.items():
        print(f"   - {t}: {count} posts")

    return posts
