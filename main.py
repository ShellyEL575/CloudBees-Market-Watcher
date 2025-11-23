from scraper.competitor import fetch_competitor_posts
from scraper.hn import fetch_hn_posts
from scraper.google_watcher import fetch_google_results
from summarizer import generate_summary
from datetime import datetime
import os

def save_markdown(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    posts = (
        fetch_competitor_posts() +
        fetch_hn_posts() +
        fetch_google_results()
    )

    summary = generate_summary(posts)

    print("\n===== 📄 Market Watch Summary =====\n")
    print(summary)
    print("\n===== ✅ End of Summary =====\n")

    os.makedirs("reports", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    save_markdown(summary, f"reports/{today}.md")

if __name__ == "__main__":
    main()
