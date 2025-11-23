import os
import requests

# Sentiment-driven queries for CloudBees, Jenkins, CI/CD user feedback
QUERIES = [
    # Pain points
    'site:reddit.com "plugin hell" OR "jenkinsfile confusion" OR "cannot upgrade jenkins"',
    'site:linkedin.com/in "stuck with jenkins" OR "ci/cd is slow" OR "security scan problems"',
    
    # Praise & success
    'site:reddit.com "jenkins saved us" OR "automated deployments working great" OR "devops win"',
    'site:medium.com "favorite jenkins plugin" OR "ci/cd finally stable" OR "love cloudbees"',

    # Uncertainty/questions
    'site:linkedin.com "how to scale ci/cd" OR "migrate from jenkins" OR "what is dora metrics"',
    'site:medium.com "release orchestration strategy" OR "flaky pipeline" OR "compare cloudbees"',

    # Competitor comparisons
    'site:reddit.com "cloudbees vs gitlab" OR "switched to harness" OR "jenkins vs github actions"',
    'site:youtube.com "ci/cd platform showdown" OR "internal developer platform reviews"'
]

def fetch_google_results(top_n=5):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("🚨 SERPER_API_KEY is not set. Add it to GitHub Secrets to enable Google search.")

    results = []
    for query in QUERIES:
        print(f"\n🔎 Searching: {query}")
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key},
            json={"q": query}
        )
        data = resp.json()

        for item in data.get("organic", [])[:top_n]:
            title = item.get("title", "No title")
            link = item.get("link", "#")
            snippet = item.get("snippet", "")

            print(f"📌 Found: {title} ({link})")

            results.append({
                "source": "Google Search",
                "title": title,
                "link": link,
                "summary": snippet[:300]
            })

    print(f"\n✅ Total Google results fetched: {len(results)}")
    return results
