import os
import requests

QUERIES = [
    'site:reddit.com/r/devops cloudbees OR cicd OR jenkins',
    'site:linkedin.com/company cloudbees OR platformengineering OR devops',
    'site:medium.com cloudbees OR jenkins pipeline OR internal developer platform',
    'site:youtube.com devops platform cloudbees'
]

def fetch_google_results(top_n=5):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("Missing SERPER_API_KEY.")
        return []

    results = []
    for query in QUERIES:
        print(f"🔎 Searching: {query}")
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key},
            json={"q": query}
        )
        data = resp.json()
        for item in data.get("organic", [])[:top_n]:
            results.append({
                "source": "Google Search",
                "title": item.get("title", "No title"),
                "link": item.get("link", "#"),
                "summary": item.get("snippet", "")[:300]
            })

    print(f"✅ Fetched {len(results)} total Google results.")
    return results

