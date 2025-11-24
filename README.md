🛠️ CloudBees Market Watch Agent

A lightweight DevOps intelligence agent that scrapes public sources, extracts insights, links every insight to its evidence, and generates daily Markdown reports.

Designed for PMs, PMMs, competitive intelligence, engineering leadership, and analysts who need clear signals and traceability — not a mountain of raw data.

This repo now uses:

Serper.dev Google Search

Hacker News RSS

Competitor RSS feeds

LLM-based Insight Extraction

LLM-based Evidence Linking (Option A)

GitHub Actions automation with auto-commit

A clean, Teams-ready summary format

No Reddit.
No LinkedIn.
No HTML noise.
No raw GPT responses in the summary.

📦 Project Structure
CloudBees-Market-Watcher/
├── scrape_only.py          # Scrapes all sources → data/posts.json
├── summarize_only.py       # Summaries, insights, evidence linking, reporting
├── summarizer.py           # GPT logic: summaries, insights, evidence linking
├── utils.py                # Grouping, report writer, sources writer
├── scraper/
│   ├── competitor.py       # Competitor RSS feeds (YAML configured)
│   ├── google_watcher.py   # Serper.dev Google Search scraper
│   ├── hn.py               # HackerNews RSS scraper
│   ├── trend_classifier.py # Lightweight keyword-based trend tags
│   ├── competitors.yaml    # Feed list
│   └── hn.yaml             # Feed list
├── data/                   # Raw scraped data
└── reports/                # Final daily reports
└── sources/                # Evidence sources for verification

🚀 What the Agent Does
1. Scrapes Market & Ecosystem Data

From:

Hacker News (filtered feeds)

Competitor blogs (GitLab, CircleCI, Harness, Atlassian, CloudBees, etc.)

Google Search via Serper.dev

Jenkins upgrade issues

CloudBees vs GitHub/GitLab

CI/CD migration patterns (Jenkins → Harness, etc.)

DORA & Flow metrics

IDP / DevOps tooling

Platform engineering trends

2. Normalizes Everything into Structured JSON

Each post becomes:

{
  "title": "",
  "url": "",
  "summary": "",
  "source": "",
  "type": "Product Update | Social Buzz | Trend",
  "is_trend": true/false
}

3. Extracts Insights Using GPT-4o-mini

Key Trends

Pain Points

Opportunities for CloudBees

Market Sentiment Signals

4. NEW: LLM Evidence Linking

Each insight is paired with 3–6 relevant supporting URLs:

### Key Trends
- Shift toward agentic AI
  - [GitLab Duo Agent Platform](…)
  - [Azure DevOps – Agentic AI](…)
  - [Harness Knowledge Agent](…)


This creates full traceability for PMs, PMMs, CI teams, and executives.

5. Generates Two Markdown Artifacts
reports/YYYY-MM-DD.md          → Teams-ready summary with evidence
sources/YYYY-MM-DD-sources.md  → Clean list of all sources


Both are auto-committed back into the repo.

🧪 Local Setup
1. Install dependencies
pip install -r requirements.txt

2. Set your environment variables
SERPER_API_KEY=<your-serper-key>
OPENAI_API_KEY=<your-openai-key>

3. Run the pipeline manually
python scrape_only.py
python summarize_only.py


Outputs:

data/posts.json

reports/<date>.md

sources/<date>-sources.md

📤 GitHub Actions Automation (with Auto-Commit)

The workflow:

Runs daily (or on-demand)

Scrapes → data/posts.json

Summarizes + insight extraction + evidence linking

Generates:

/reports/YYYY-MM-DD.md

/sources/YYYY-MM-DD-sources.md

Uploads artifacts

Auto-commits new reports back into the repo

Avoids infinite loops (reports & sources do not trigger new runs)

The complete workflow file lives at:

.github/workflows/market-watch.yml

🧠 How Insight Extraction Works
The LLM performs three tasks:
1️⃣ Summarization

Your post groups become bulleted summaries.

2️⃣ Insight Extraction

The LLM returns this JSON structure:

{
  "Key Trends": [],
  "Pain Points": [],
  "Opportunities for CloudBees": [],
  "Indicators of DevOps Market Sentiment": []
}

3️⃣ Evidence Linking (NEW)

For every insight, the model maps the most relevant URLs from the scraped dataset.

Users get:

Meaningful insights

Trustworthy traceability

Links for deeper research

🧩 How to Edit the LLM Prompt

All prompt editing lives in:

summarizer.py


You can modify:

Tone

Depth

Audience

Section names

Structure

Output format

If you want help tuning prompts for:

Executives

PMs

PMMs

Competitive intelligence

Engineering leadership

Just ask!

🔮 Next Improvements

“Delta Mode” → what changed since yesterday

Team Slack notifications

Notion / Confluence sync

Confidence scoring per insight

Heatmaps of noisy vs high-value sources

De-duplication for Google Search results

🤝 Contributions & Feedback

PRs welcome — especially:

New feed sources

Better trend rules

Improved insight prompts

UI integrations (Slack, Teams, Notion)

If you want help expanding this agent into a fully production competitive intelligence system, just ask!
