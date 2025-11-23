import os
from serpapi import GoogleSearch
from datetime import datetime, timedelta

SEARCH_QUERIES = [
    'jenkins OR cloudbees upgrade issues OR plugin problems',
    '"ci/cd success" OR cloudbees experience OR stable pipeline',
    'cloudbees vs gitlab OR github actions vs jenkins',
    'moved to harness OR migrated from jenkins OR ci/cd migration',
    'dora metrics OR platform analytics OR flow metrics',
    'devops tooling OR internal dev platform reviews',
]

def fetch_google_posts():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment")

    all_results = []
    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching (new, recent-only): site:reddit.com {query}")
        search = GoogleSearch({
            "q": f"site:reddit.com {query}",
            "location": "United States",
            "hl": "en",
            "gl": "us",
            "num": 10,
            "api_key": api_key
        })

        results = search.get_dict()
        if "organic_results" in results:
            for result in results["organic_results"]:
                title = result.get("title")
                link = result.get("link")
                if title and link:
                    print(f"📌 Found (recent): {title} ({link})")
                    all_results.append({
                        "title": title,
                        "link": link,
                        "source": "Google",
                        "category": "💬 Social Buzz",
                        "timestamp": datetime.utcnow().isoformat()
                    })

    return all_results
