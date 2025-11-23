# 🛠️ CloudBees Market Watch Agent

A lightweight DevOps market-intelligence agent that scrapes public sources, extracts trends and sentiment, and generates clean Markdown reports.  
Designed for **VS Code**, **GitHub Actions**, and **absolute reliability** in unattended daily runs.

This repo uses the **latest simplified + hardened architecture**, including:

- **Scraping sources:** Hacker News, competitor blogs, Google Search via **Serper.dev**
- **No Reddit**, **no LinkedIn**, **no SerpAPI**
- **Two-phase pipeline:**  
  `scrape_only.py` → `summarize_only.py`
- **HTML-cleaned + truncated summaries** (fast + clean GPT prompts)
- **Safe trend classifier**
- **Dedupe + retry-hardened scrapers**
- **Consistent Markdown reporting**

---

## 📦 Project Structure

CloudBees-Market-Watcher/
├── scrape_only.py # Collects posts → data/posts.json
├── summarize_only.py # Summaries + insights → reports/YYYY-MM-DD.md
├── summarizer.py # GPT summarization + insight extraction
├── utils.py # Grouping + Markdown report writer
├── main.py # (Optional) combined pipeline for local runs
├── scraper/
│ ├── competitor.py # Hardened RSS competitor scraper (HTML-safe)
│ ├── google_watcher.py # Serper.dev search, deduped + retried
│ ├── hn.py # Hacker News RSS + HTML cleanup
│ ├── trend_classifier.py # Keyword-based trend tagging
│ ├── competitors.yaml # Feed list
│ ├── hn.yaml # Feed list
│ └── reddit.yaml # (Unused — historical)
└── data/
└── reports/

yaml
Copy code

---

## 🚀 What the Agent Does

### 1. Scrapes:

- **Hacker News** (filtered CI/CD/DevOps topics)
- **Competitor blogs** (GitHub/GitLab/CircleCI/Harness/etc.)
- **Google Search** (Serper.dev) using targeted queries:
  - Jenkins upgrade issues
  - CloudBees vs GitHub/GitLab
  - Migration patterns (Jenkins → Harness)
  - DORA metrics / flow metrics
  - Internal Developer Platform (IDP) ecosystem
  - DevOps tooling reviews

### 2. Cleans & normalizes into structured JSON

Each item includes:

```json
{
  "title": "...",
  "url": "...",
  "summary": "clean text...",
  "source": "Google | Competitors | HackerNews",
  "type": "🚀 Product Updates | 💬 Social Buzz | 📈 Trends",
  "is_trend": true/false
}
All summaries are:

HTML-stripped

Truncated to ~300 chars

Safe for GPT input

3. Summarizes into Markdown
Organized into:

🚀 Product Updates

💬 Social Buzz

📈 Trends

🧠 Insights (AI-generated)

Key Trends

Pain Points

Opportunities for CloudBees

Market Sentiment Indicators

4. Outputs a daily report:
css
Copy code
reports/YYYY-MM-DD.md
🧪 Local Setup
1. Install dependencies
bash
Copy code
pip install -r requirements.txt
2. Add environment variables
In .env or shell:

bash
Copy code
export SERPER_API_KEY=<your-serper-dev-key>
export OPENAI_API_KEY=<your-openai-key>
3. Run manually
bash
Copy code
python scrape_only.py
python summarize_only.py
(Optional) Use combined runner:
bash
Copy code
python main.py
🧠 Architecture Notes
Why HTML cleanup?
Competitor RSS feeds often embed full blog HTML.
We now clean all HTML + truncate long summaries →
Cleaner reports + faster + cheaper GPT calls.

Why dedupe?
Google can repeat the same result across multiple queries.
We now dedupe globally per run.

Why two phases?
Scrape failures shouldn’t block summarization.
Artifacts allow debugging raw scraped data.

Trend classifier
Simple keyword-based classifier covering:

GitOps

Platform Engineering

Internal Developer Platforms (IDP)

AI-in-DevOps

Supply chain / SBOM

DORA/Flow metrics

Migration/modernization

Extend in scraper/trend_classifier.py.

📤 GitHub Actions Automation
The workflow:

Checks out repo

Installs dependencies

Runs scrape_only.py

Uploads data/posts.json for debugging

Runs summarize_only.py

Uploads final report

Secrets required:

nginx
Copy code
SERPER_API_KEY
OPENAI_API_KEY
Schedule example:

yaml
Copy code
schedule:
  - cron: "0 9 * * *"
🧩 Future Improvements
Slack/Teams notifications

Notion/Supabase sync

Weekly trend deltas

ML-based sentiment scoring

Auto-tagging of topics

🤝 Contributions
PRs welcome—especially:

New blog feeds

Better trend rules

New search queries

Report formatting improvements

If you want help extending CI, adding alerts, or plugging into databases, just ask! 🚀

yaml
Copy code

---

# 🎉 README is done  
If you want:  
✅ a badge for GHA status  
✅ auto-commit reports back to the repo  
✅ Slack notifications  
✅ or a cleaner TOC

Just tell me!
