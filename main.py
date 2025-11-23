from scraper.competitor import fetch_competitor_posts
from scraper.reddit import fetch_reddit_posts
from scraper.hn import fetch_hn_posts
from summarizer import generate_summary
from datetime import datetime
import os

def save_markdown(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    all_posts = (
        fetch_competitor_posts() +
        fetch_reddit_posts() +
        fetch_hn_posts()
    )
    summary = generate_summary(all_posts)
    os.makedirs("reports", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    save_markdown(summary, f"reports/{today}.md")

if __name__ == "__main__":
    main()
