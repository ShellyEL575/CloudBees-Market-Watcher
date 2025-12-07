import os
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup  # added for summary cleanup

API_URL = "https://google.serper.dev/search"

SEARCH_QUERIES = [
    # 🧱 Legacy CI/CD + Migration Signals
    'jenkins plugin compatibility issues OR jenkins upgrade friction',
    'migrated from jenkins OR moved to github actions OR ci/cd migration',
    'cloudbees migration OR migrated to cloudbees experience',
    'jenkins vs github actions OR gitlab vs cloudbees OR ci/cd tool comparisons',
    'github actions vs jenkins 2026 OR jenkins vs harness OR devops platform comparison',

    # 🚀 Platform Engineering / Internal Developer Platforms
    '"internal developer platform" OR IDP OR platform engineering reviews',
    'enterprise developer platform adoption OR idp team success',
    'cloudbees platform vs backstage OR internal platform tools ci/cd',

    # 🔐 DevSecOps + Compliance Trends
    'devsecops in ci/cd OR pipeline security best practices',
    'policy as code devops OR compliance pipelines enterprise',
    'secure ci/cd implementation OR infrastructure as code security tools',

    # 🧠 AI in DevOps / AIOps Signals
    'ai-assisted devops tools OR ai-enhanced pipelines OR devops automation AI',
    'ai for build optimization OR ci/cd performance tuning with ai',
    'aiops case studies 2026 OR ai tools for dev workflows',

    # 📊 Observability / Monitoring / FinOps
    'observability pipelines OR full stack observability devops',
    'finops best practices ci/cd OR cloud cost optimization pipelines',
    'monitoring platform reviews OR logs metrics traces devops',

    # ⚙️ Cloud Native / Kubernetes / GitOps
    'gitops pipelines OR gitops vs traditional ci/cd OR flux argo case study',
    'kubernetes ci/cd patterns OR cloud native deployment workflows',
    'serverless ci/cd 2026 OR modern cloud deployment pipeline',

    # 🧪 Tooling + Dev Experience
    'new ci/cd tools 2026 OR devops tooling landscape',
    'modern devops stack OR emerging ci/cd platforms',
    'developer experience feedback OR internal tools for dev productivity',

    # 🧭 Strategic Insights + Market Positioning
    'ci/cd enterprise tool ROI OR devops platform total cost of ownership',
    'which ci/cd platform to choose OR 2026 ci/cd buyer guide',
    'top devops platforms gartner OR ci/cd vendor comparison reviews',

    # 💬 Community/Practitioner Signals
    'reddit devops pain points OR ci/cd tool complaints 2026',
    'stackoverflow ci/cd migration issues OR internal dev tooling questions',
    'devops linkedin post OR platform engineering success story',
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
            "tbs": "qdr:w"  # Filter: past week only
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

            # Clean summary of any HTML tags
            clean_summary = BeautifulSoup(snippet, "html.parser").get_text()

            print(f"📌 Found: {title} ({url})")

            all_posts.append({
                "title": title,
                "url": url,
                "summary": clean_summary,
                "source": "Google",
                "type": "💬 Social Buzz",
                "timestamp": datetime.utcnow().isoformat(),
            })

    print(f"\n✅ Google posts collected: {len(all_posts)}")
    return all_posts
