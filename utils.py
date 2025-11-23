# utils.py

def group_posts_by_topic(all_posts):
    """
    Groups posts into categories: Product Updates, Social Buzz, Trends
    all_posts: list of dicts each with keys 'source', 'title', 'link', 'summary'
    Returns a dict: { "🚀 Product Updates": [...], "💬 Social Buzz": [...], "📈 Trends": [...] }
    """
    grouped = {
        "🚀 Product Updates": [],
        "💬 Social Buzz": [],
        "📈 Trends": []
    }

    for post in all_posts:
        url = post.get("link", "").lower()
        source = post.get("source", "").lower()

        if any(domain in url for domain in ["reddit.com", "linkedin.com", "youtube.com", "medium.com"]):
            grouped["💬 Social Buzz"].append(post)
        elif source == "google search" and any(domain in url for domain in ["reddit.com", "linkedin.com", "youtube.com", "medium.com"]):
            grouped["💬 Social Buzz"].append(post)
        elif "blog" in source or "changelog" in source or "devops" in source:
            grouped["🚀 Product Updates"].append(post)
        else:
            grouped["📈 Trends"].append(post)

    return grouped
