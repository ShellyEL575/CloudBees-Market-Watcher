# exec_summary.py (FINAL)
from datetime import datetime

def generate_exec_summary(insights, curated_sources):
    """
    Clean executive-ready summary.
    insights: LLM-generated markdown section
    curated_sources: list of (title, url)
    """
    date = datetime.utcnow().strftime("%Y-%m-%d")

    source_md = "\n".join(
        [f"- [{title}]({url})" for title, url in curated_sources]
    )

    return f"""
# 🚨 CloudBees Market Watch — Executive Brief ({date})

## 🔥 Key Market Signals
The most important strategic signals detected in the last 24 hours:

{insights}

---

## 📚 Source Deck for PMs & PMMs
Validate insights and explore deeper:

{source_md}

---
Generated automatically by CloudBees Market Watch Agent.
"""
