# 🛠️ Better Scraper – CloudBees Market Watch Agent

A Python-based GitHub Actions agent that scrapes competitor blogs, Reddit, Hacker News, and Google Search (Reddit, LinkedIn, Medium, YouTube) to generate **daily market watch reports** in Markdown — tailored for PMs, PMMs, DevOps, and Platform teams at CloudBees.

---

## 📦 Project Structure

Better_scraper/
├── main.py # Entrypoint - runs all scrapers and summarizer
├── requirements.txt # Python dependencies
├── summarizer.py # GPT-4o summarization logic
├── reports/ # Output folder for daily markdown reports
├── scraper/
│ ├── init.py
│ ├── competitor.py # Competitor blog scraper
│ ├── reddit.py # (optional) Reddit RSS fallback
│ ├── hn.py # Hacker News RSS parser
│ ├── google_watcher.py # Google Search → Reddit, LinkedIn, Medium, YouTube
│ ├── competitors.yaml
│ ├── reddit.yaml
│ └── hn.yaml
└── .github/
└── workflows/
└── market_watch.yml # GitHub Actions automation

yaml
Copy code

---

## 🚀 What It Does

- 📰 Scrapes competitor changelogs and blog feeds (`competitors.yaml`)
- 🔎 Uses Serper.dev to Google-search for:
  - Reddit DevOps struggles/wins
  - LinkedIn user sentiment posts
  - Medium tutorials and trends
  - YouTube platform reviews
- 💬 Groups insights into:
  - 🚀 Product Updates
  - 💬 Social Buzz
  - 📈 Trends
- 🧠 Summarizes everything with OpenAI GPT-4o
- 🗂️ Saves a daily markdown report to `reports/YYYY-MM-DD.md`
- 🧪 Prints results directly in GitHub Action logs
- 📤 Uploads the report as a GitHub Actions artifact

---

## 🧪 Setup Instructions

### 1. Clone and install:

```bash
git clone https://github.com/your-username/Better_scraper.git
cd Better_scraper
pip install -r requirements.txt
2. API Keys
Add these as GitHub → Settings → Secrets:

OPENAI_API_KEY

SERPER_API_KEY (get free key at https://serper.dev)

3. Run it manually or via GitHub Actions:
bash
Copy code
python main.py
Or push to GitHub and let the action run on schedule.

⏰ GitHub Action
Workflow file: .github/workflows/market_watch.yml
Runs daily at 09:00 UTC or on demand.

Action Output:
✅ Search logs and links are printed

✅ Summary shown in the log

✅ Report saved to reports/ and uploaded

📄 Sample Markdown Report
markdown
Copy code
# Market Watch Report – 2025-11-22

## 🚀 Product Updates
- [GitHub Blog: Git 2.52 Released](...)

## 💬 Social Buzz
- [Reddit: "Plugin hell" discussion](...)
- [LinkedIn: Jenkins migration story](...)

## 📈 Trends
- AI in CI/CD
- Security metrics
- Release orchestration
🤖 Next Features
 Add sentiment scores (Positive/Negative/Neutral)

 Sync summaries to Notion or Supabase

 Weekly delta reports

 Trend graphs

🧠 Built for CloudBees Strategy Teams
Helps PMMs, DevSecOps, and platform leads stay on top of:

Industry sentiment

DevOps tech shifts

Migration patterns

Customer pain points

No doomscrolling required.

yaml
Copied

---

Once pasted into GitHub, just commit the change and push. Let me know if you want a on
