# scraper/google_watcher.py (HARDENED VERSION)

import os
import time
import requests
from datetime import datetime

API_URL = "https://google.serper.dev/search"

SEARCH_QUERIES = [
    'jenkins OR cloudbees upgrade issues OR plugin problems',
    '"ci/cd success" OR cloudbees experience OR stable pipeline',
    'cloudbees vs gitlab OR github actions vs jenkins',
    'moved to harness OR migrated from jenkins OR ci/cd migration',
    'dora metrics OR platform analytics OR flow metrics',
    'devops tooling OR internal dev platform reviews',
]


# --------------------------
# Helper: Retry Wrapper
# --------------------------
def safe_post(url, headers, payload, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            resp.raise_for_status()
            return resp.json()

        except Exception as e:
            print(f"❌ Serper request failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("⚠️ Giving up on this query.")
                return None


# --------------------------
# Main Fetcher
# --------------------------
def fetch_google_results():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    all_posts = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching (Serper): {query}")

        payload = {
            "q": query,
            "num": 10,
            "gl": "us",
            "hl": "en",
            "autocorrect": True,
            "type": "search",
        }

        data = safe_post(API_URL, headers, payload)

        if not data:
            continue

        organic = data.get("organic", [])
        if not organic:
            print("⚠️ No organic results returned.")
            continue

        for result in organic:
            title = result.get("title")
            url = result.get("link")
            snippet = result.get("snippet", "")

            # Required fields
            if not title or not url:
                continue

            # Dedupe URLs across all queries
            if url in seen_urls:
                continue
            seen_urls.add(url)

            print(f"📌 Found: {title} ({url})")

            all_posts.append({
                "title": title,
                "url": url,
                "summary": snippet,
                "source": "Google",
                "type": "💬 Social Buzz",
                "timestamp": datetime.utcnow().isoformat(),
            })

    print(f"\n✅ Google posts collected: {len(all_posts)}")
    return all_posts
