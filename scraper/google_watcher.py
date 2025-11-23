import os
import requests

# ✅ Optimized natural-language search terms for CloudBees and DevOps
QUERIES = [
    # Frustration / Problems
    'site:reddit.com jenkins OR cloudbees upgrade issues OR plugin problems',
    
    # Praise / Success stories
    'site:linkedin.com "ci/cd success" OR cloudbees experience OR stable pipeline',
    
    # Platform comparisons
    'site:medium.com cloudbees vs gitlab OR github actions vs jenkins',
    
    # Migration stories
    'site:reddit.com moved to harness OR migrated from jenkins OR ci/cd migration',

    # Metrics & Analytics
    'site:linkedin.com dora metrics OR platform analytics OR flow metrics',
    
    # DevOps trends and tooling reviews
    'site:youtube.com devops tooling OR internal dev platform reviews'
]

SERPER_URL = "https://google.serper.dev/search"

def fetch_google_results(top_n=5):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("🚨 SERPER_API_KEY is not set. Add it to GitHub Secrets to enable Google search.")

    results = []
    headers = {"X-API-KEY": api_key}

    for query in QUERIES:
        print(f"\n🔎 Searching (new, recent-only): {query}")

        payload = {
            "q": query,
            "gl": "us",
            "num": 10,
            "tbs": "qdr:w"   # 🔥 Past week only
        }

        resp = requests.post(SERPER_URL, json=payload, headers=headers)
        
        try:
            data = resp.json()
        except Exception as e:
            print("⚠️ Failed to parse JSON from Serper response.")
            continue

        organic = data.get("organic", [])
        if not organic:
            print("⚠️ No results found.")
            continue

        for item in organic[:top_n]:
            title = item.get("title", "No title")
            link = item.get("link", "")
            snippet = item.get("snippet", "")

            print(f"📌 Found (recent): {title} ({link})")

            results.append({
                "source": "Google Search",
                "title": title,
                "link": link,
                "summary": snippet[:300]
            })

    print(f"\n✅ Total recent Google results fetched: {len(results)}")
    return results
