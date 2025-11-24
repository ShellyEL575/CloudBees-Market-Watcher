# exec_summary.py
from datetime import datetime
from llm_helpers import extract_insights_batch_linked

def generate_exec_summary(posts, curated_sources):
    """
    Full executive summary generator:
    - Extract insights using LLM (batched + evidence linked)
    - Produce a clean exec-ready summary
    - Include curated source deck
    """

    date = datetime.utcnow().strftime("%Y-%m-%d")

    # ---- STEP 1: Extract insights with evidence linking ----
    print("🧠 Extracting executive insights...")
    insights_md = extract_insights_batch_linked(posts)  # returns markdown with sources attached

    # ---- STEP 2: Format source deck ----
    source_md = "\n".join([
        f"- [{title}]({url})"
        for title, url in curated_sources
    ])

    # ---- STEP 3: Combine everything ----
    return f"""
# 🚨 CloudBees Market Watch — Executive Brief ({date})

## 🔥 Key Market Signals
Below are the most important strategic signals detected in the last 24h.

{insights_md}

---

## 📚 Source Deck for PMs & PMMs
Use these to validate insights and explore deeper.

{source_md}

---
Generated automatically by CloudBees Market Watch Agent.
"""
