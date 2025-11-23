import yaml
import feedparser

KEYWORDS = [
    "devops", "ci", "cd", "cicd", "pipeline", "platform",
    "deployment", "cloudbees", "jenkins", "gitlab", "github",
    "harness", "security", "compliance", "automation"
]

def score_post(title, summary):
    text = f"{title.lower()} {summary.lower()}"
    return sum(kw in text for kw in KEYWORDS)

def fetch_reddit_posts(top_n=5):
    with open("scraper/reddit.yaml", "r") as f:
        feeds = yaml.safe_load(f)

    scored_posts = []

    for subreddit in feeds:
        parsed = feedparser.parse(subreddit["url"])
        for entry in parsed.entries:
            title = entry.title
            summary = entry.get("summary", "")
            score = score_post(title, summary)

            if score == 0:
                continue  # Skip irrelevant posts

            scored_posts.append({
                "source": subreddit["name"],
                "title": title,
                "link": entry.link,
                "summary": summary[:200],
                "score": score
            })

    # Sort by score (high to low) and return top N
    sorted_posts = sorted(scored_posts, key=lambda x: x["score"], reverse=True)
    return sorted_posts[:top_n]

