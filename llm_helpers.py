# llm_helpers.py
import re
from openai import OpenAI

client = OpenAI()

# -----------------------------
# HTML STRIPPER + NORMALIZER
# -----------------------------
def clean_text(raw: str) -> str:
    if not raw:
        return ""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", raw)
    # Replace multiple spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()
    # Limit size for LLM
    return text[:1200]


# -----------------------------
# SUMMARIZE POSTS INTO BULLETS
# -----------------------------
def summarize_posts(posts):
    if not posts:
        return "No updates found.\n"

    lines = []
    for p in posts:
        title = p.get("title", "Untitled").strip()
        summary_raw = p.get("summary") or p.get("description") or ""
        summary = clean_text(summary_raw)
        url = p.get("url") or p.get("link") or ""

        lines.append(f"- [{title}]({url}) — {summary}")

    return "\n".join(lines) + "\n"


# -----------------------------
# GPT INSIGHTS (1 call)
# -----------------------------
def extract_insights(posts):
    if not posts:
        return "_No social buzz detected._"

    corpus = "\n".join(
        f"- {clean_text(p.get('title',''))}: {clean_text(p.get('summary',''))}"
        for p in posts
    )

    prompt = f"""
You are a DevOps market research analyst.

Analyze the following posts and extract **insights only**, NOT summaries.

Return Markdown in the following structure:

### Key Trends
- bullets

### Pain Points
- bullets

### Opportunities for CloudBees
- bullets

### Indicators of DevOps Market Sentiment
- bullets

CORPUS:
{corpus}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -----------------------------
# BATCH EVIDENCE LINKING
# -----------------------------
def link_insights_to_sources(insights_md, posts):
    """
    For each bullet in insights, find the top 2 most relevant sources.
    Batched for speed.
    """

    bullets = [
        b.strip("- ").strip()
        for b in insights_md.split("\n")
        if b.startswith("- ")
    ]

    if not bullets:
        return insights_md

    # Prepare batch payload
    items = []
    for b in bullets:
        items.append({
            "type": "insight",
            "insight": b,
            "sources": [
                {
                    "title": p.get("title", ""),
                    "summary": clean_text(p.get("summary", "")),
                    "url": p.get("url") or p.get("link") or "",
                }
                for p in posts
            ]
        })

    prompt = f"""
Match each insight to the 1–2 most relevant sources.

Return the result in this format:

- Insight text
  - 🔗 Source: Title (URL)
  - 🔗 Source: Title (URL)

ONLY return this structured markdown.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You create attribution mappings."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": str(items)}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
