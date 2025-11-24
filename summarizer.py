# summarizer.py — with LLM-based evidence linking
from openai import OpenAI
import os

client = OpenAI()

# ---------------------------------------------------------
# 1. Generate simple summaries (unchanged)
# ---------------------------------------------------------
def generate_summary(posts):
    if not posts:
        return "No updates found.\n"

    lines = []
    for post in posts:
        title = post.get("title", "Untitled")
        summary = post.get("summary", "").strip()
        url = post.get("url") or post.get("link") or ""
        lines.append(f"- [{title}]({url}) — {summary}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------
# 2. Extract structured insights (4 sections)
# ---------------------------------------------------------
def extract_insights_from_social(posts):
    """
    Returns a DICT with 4 arrays:
    {
        "Key Trends": [...],
        "Pain Points": [...],
        "Opportunities for CloudBees": [...],
        "Indicators of DevOps Market Sentiment": [...]
    }
    """

    text_blob = "\n".join([
        f"Title: {p.get('title')}\nSummary: {p.get('summary')}"
        for p in posts
    ])

    prompt = f"""
You are an expert DevOps market analyst.

Extract insights into **four structured lists**. 
Return ONLY a pure JSON object with four keys:

"Key Trends": [],
"Pain Points": [],
"Opportunities for CloudBees": [],
"Indicators of DevOps Market Sentiment": []

Rules:
- Each item should be a short, clear bullet (sentence fragment is fine).
- DO NOT include any markdown, no bullets, no headings. Pure JSON only.
- Do NOT include sources. Only insights.
- Keep each insight concise and high value.

TEXT:
{text_blob}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    # Parse JSON safely
    raw = response.choices[0].message.content

    import json
    try:
        insights = json.loads(raw)
    except:
        # fallback: wrap in braces and retry
        cleaned = raw.strip()
        if not cleaned.startswith("{"):
            cleaned = "{" + cleaned
        if not cleaned.endswith("}"):
            cleaned = cleaned + "}"
        insights = json.loads(cleaned)

    return insights


# ---------------------------------------------------------
# 3. LLM-based evidence linking
# ---------------------------------------------------------
def link_sources_to_insights(insight_list, posts):
    """
    For a list of insights, return:
    {
      "insight text": [ {title, url}, {title, url} ... ],
      ...
    }
    """

    # Build a compact list of sources for the model
    all_sources = [
        {
            "title": p.get("title", "Untitled"),
            "url": p.get("url") or p.get("link") or ""
        }
        for p in posts
        if p.get("url") or p.get("link")
    ]

    source_blob = "\n".join(
        f"- {s['title']} ({s['url']})"
        for s in all_sources
    )

    results = {}

    for insight in insight_list:
        prompt = f"""
You are an assistant that links insights to supporting evidence.

Insight:
"{insight}"

Here are all available sources:
{source_blob}

Task:
Return ONLY a pure JSON array of supporting sources, each formatted as:
{{
  "title": "...",
  "url": "..."
}}

Rules:
- Choose the **3–6 most relevant** sources.
- Base relevance on title similarity and topical alignment.
- If no meaningful match, return an empty array [].
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )

        raw = response.choices[0].message.content.strip()

        import json
        try:
            parsed = json.loads(raw)
        except:
            parsed = []

        results[insight] = parsed

    return results


# ---------------------------------------------------------
# 4. Format “Insights + Supporting Sources” as Markdown
# ---------------------------------------------------------
def format_insights_with_sources(insights_dict, linked_sources_dict):
    """
    Return a clean markdown section like:

    ### Key Trends
    - Insight
      - [source title](url)
      - [another source](url)
    """

    output = []

    for section, insight_list in insights_dict.items():
        output.append(f"### {section}")

        if not insight_list:
            output.append("_No insights found._\n")
            continue

        for insight in insight_list:
            output.append(f"- **{insight}**")

            links = linked_sources_dict.get(insight, [])
            if links:
                for s in links:
                    output.append(f"  - [{s['title']}]({s['url']})")
            else:
                output.append("  - _No supporting sources detected_")

        output.append("")  # spacing

    return "\n".join(output)
