import yaml
import feedparser

def fetch_reddit_posts():
    with open("scraper/reddit.yaml", "r") as f:
        feeds = yaml.safe_load(f)
    results = []
    for subreddit in feeds:
        parsed = feedparser.parse(subreddit["url"])
        for entry in parsed.entries[:5]:
            results.append({
                "source": subreddit["name"],
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")[:200]
            })
    return results
