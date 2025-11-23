import yaml
import feedparser

def fetch_hn_posts():
    with open("scraper/hn.yaml", "r") as f:
        feeds = yaml.safe_load(f)
    results = []
    for feed in feeds:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:5]:
            results.append({
                "source": feed["name"],
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")[:200]
            })
    return results
