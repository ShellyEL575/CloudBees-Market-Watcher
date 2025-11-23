# 🛠️ CloudBees Market Watch Agent

A lightweight, VS Code–friendly DevOps market‑intelligence agent. It scrapes public sources, extracts trends and sentiment, and generates daily Markdown reports.

This repo now reflects the **latest simplified architecture**:

* **Scraping sources:** Hacker News, competitor blogs, Google Search via **Serper.dev**
* **No Reddit**, **no LinkedIn**, **no SerpAPI**
* **Two‑phase workflow:** scrape → summarize
* **Safe trend classification**
* **Clean Markdown reporting**

---

## 📦 Project Structure

```
CloudBees-Market-Watcher/
├── scrape_only.py          # Collects all posts into data/posts.json
├── summarize_only.py       # Generates summaries + insights
├── summarizer.py           # GPT-based summarization + insight extraction
├── utils.py                # Grouping and report writer
├── scraper/
│   ├── competitor.py       # RSS competitor feeds
│   ├── google_watcher.py   # Serper.dev search → recent/postive signals
│   ├── hn.py               # Hacker News RSS
│   ├── trend_classifier.py # Regex-based trend matching
│   ├── competitors.yaml    # Feed list
│   ├── hn.yaml             # Feed list
│   └── reddit.yaml         # (unused)
└── data/
└── reports/
```

---

## 🚀 What the Agent Does

### 1. Scrapes:

* **Hacker News** (filtered feeds)
* **Competitor blogs/changelogs**
* **Google Search results** via **Serper.dev** using targeted queries:

  * CloudBees vs GitHub/GitLab
  * Jenkins upgrade issues
  * DORA metrics
  * Internal Developer Platforms
  * Migration patterns (Jenkins → Harness, etc.)

### 2. Normalizes all posts into structured JSON

Each item contains:

```
{
  title,
  url,
  summary,
  source,
  type (Product Update / Social Buzz / Trend),
  is_trend: true/false
}
```

### 3. Summarizes into human‑readable Markdown

* Product Updates
* Social Buzz
* Trends
* Insights (pain points, sentiment, opportunities)

### 4. Outputs a daily report at:

```
reports/YYYY-MM-DD.md
```

---

## 🧪 Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add required environment variables

This agent now uses **Serper.dev** (NOT SerpAPI).

GitHub Actions → Settings → Secrets → Actions:

```
SERPER_API_KEY=<your-serper-dev-key>
OPENAI_API_KEY=<your-openai-key>
```

### 3. Run manually

```bash
python scrape_only.py
python summarize_only.py
```

---

## 🧠 Notes on Architecture

### Why no Reddit/LinkedIn?

* We shifted to **Google → Reddit/LinkedIn/Medium/YouTube** discovery using Serper.
* No direct scraping reduces breakage and TOS issues.

### Why two phases?

* Cloud/CI runs can fail mid‑scrape; separating summarization keeps reports deterministic.

### Trend classifier

Uses keyword hits from:

* GitOps
* Platform Engineering / IDP
* DORA/Flow Metrics
* K8s, DevSecOps, AI-in‑DevOps

You can extend this in `scraper/trend_classifier.py`.

---

## 📤 GitHub Actions Automation

The Action runs:

1. `python scrape_only.py`
2. Saves `data/posts.json`
3. `python summarize_only.py`
4. Uploads report artifact

A scheduled workflow (e.g., daily UTC) is recommended.

---

## 🧩 Next Improvements

* Sentiment scoring per post
* Notion/Supabase sync
* Weekly delta comparison
* Auto-deduping Google organic results

---

## 🤝 Contributions

PRs welcome—especially additional feed sources or report enhancements.

If you want help wiring CI, adding Slack notifications, or expanding trend logic, just ask! 🚀
