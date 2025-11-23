# scraper/google_watcher.py

import os
import requests
from datetime import datetime

SEARCH_QUERIES = [
    'jenkins OR cloudbees upgrade issues OR plugin problems',
    '"ci/cd success" OR cloudbees experience OR stable pipeline',
    'cloudbees vs gitlab OR github actions vs jenkins',
    'moved to harness OR migrated from jenkins OR ci/cd migration',
    'dora metrics OR platform analytics OR flow metrics',
    'devops tooling OR internal dev platform reviews',
]

def fetch_google_results():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    all_results = []
    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching (new, recent-only): {query}")
        payload = {
            "q": query,
            "num": 10,
            "gl": "us",
            "hl": "en",
            "autocorrect": True,
            "type": "search"
        }
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        data = response.json()
        for result in data.get("organic", []):
            title = result.get("title")
            link = result.get("link")
            if title and link:
                print(f"📌 Found (recent): {title} ({link})")
                all_results.append({
                    "title": title,
                    "url": link,
                    "source": "Google",
                    "type": "💬 Social Buzz",
                    "timestamp": datetime.utcnow().isoformat()
                })

    print(f"\n✅ Google posts: {len(all_results)}")
    return all_results
