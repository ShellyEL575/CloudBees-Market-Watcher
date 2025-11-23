# scraper/google_watcher.py

import os
from serpapi import GoogleSearch
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

    all_results = []
    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching (new, recent-only): site:google.com {query}")
        search = GoogleSearch({
            "q": query,
            "engine": "google",
            "location": "United States",
            "hl": "en",
            "gl": "us",
            "num": 10,
            "api_key": api_key
        })
        results = search.get_dict()
        for result in results.get("organic_results", []):
            title = result.get("title")
            link = result.get("link")
            if not title or not link:
                print(f"⚠️ Skipping entry with missing title or link: {result}")
                continue
            all_results.append({
                "title": title,
                "url": link,
                "summary": result.get("snippet", ""),
                "source": "Google",
                "type": "💬 Social Buzz",
                "timestamp": datetime.utcnow().isoformat()
            })
    return all_results
