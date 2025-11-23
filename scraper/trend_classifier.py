import re

def classify_trends(posts):
    trends = []
    keywords = [
        "gitops", "dora metrics", "platform engineering", "internal developer platform",
        "kubernetes", "k8s", "devsecops", "copilot", "chaos engineering",
        "ai in devops", "resilience", "supply chain", "idp", "mlops", "observability"
    ]

    pattern = re.compile("|".join(re.escape(k) for k in keywords), re.IGNORECASE)

    for post in posts:
        text = f"{post.get('title', '')} {post.get('summary', '')}"
        if pattern.search(text):
            post["type"] = "📈 Trends"
            trends.append(post)

    return trends
