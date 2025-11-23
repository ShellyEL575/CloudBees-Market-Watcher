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
                continue

            post = {
                "source": subreddit["name"],
                "title": title,
                "link": entry.link,
                "summary": summary[:200],
                "score": score
            }
            scored_posts.append(post)

    # Log to GitHub Actions
    print("\n===== 🧪 Reddit Scored Posts =====")
    for post in sorted(scored_posts, key=lambda x: x["score"], reverse=True):
        print(f"{post['score']} - {post['title']} ({post['link']})")

    return sorted(scored_posts, key=lambda x: x["score"], reverse=True)[:top_n]
