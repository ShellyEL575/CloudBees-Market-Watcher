import os
import serpapi
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
    client = serpapi.Client(api_key=api_key)
    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching: {query}")
        params = {
            "q": query,
            "engine": "google",
            "location": "United States",
            "hl": "en",
            "gl": "us",
            "num": 10
        }
        results = client.search(params)
        for result in results.get("organic_results", []):
            title = result.get("title")
            link = result.get("link")
            if title and link:
                all_results.append({
                    "title": title,
                    "link": link,
                    "source": "Google",
                    "category": "💬 Social Buzz",
                    "timestamp": datetime.utcnow().isoformat()
                })
    return all_results
