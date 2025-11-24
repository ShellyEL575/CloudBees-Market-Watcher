# exec_summary.py
from datetime import datetime

def generate_exec_summary(insights_markdown, curated_sources):
    """
    Create an executive-ready summary.
    insights_markdown = final insights block from LLM (already markdown)
    curated_sources = list of (title, url) tuples
    """
    date = datetime.utcnow().strftime("%Y-%m-%d")

    # Render sources into markdown bullets
    source_md = "\n".join([f"- [{title}]({url})" for title, url in curated_sources])

    return f"""
# 🚨 CloudBees Market Watch — Executive Brief ({date})

## 🔥 Key Market Signals
Below are the most important strategic signals detected in the last 24h.

{insights_markdown}

---

## 📚 Source Deck for PMs & PMMs
Use these to validate insights and explore deeper.

{source_md}

---
Generated automatically by CloudBees Market Watch Agent.
"""
