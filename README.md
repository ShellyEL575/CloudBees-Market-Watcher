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

