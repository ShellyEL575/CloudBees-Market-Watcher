import yaml
import feedparser

def fetch_competitor_posts():
    with open("scraper/competitors.yaml", "r") as f:
        feeds = yaml.safe_load(f)
    results = []
    for site in feeds:
        parsed = feedparser.parse(site["url"])
        for entry in parsed.entries[:5]:
            results.append({
                "source": site["name"],
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")[:200]
            })
    return results
