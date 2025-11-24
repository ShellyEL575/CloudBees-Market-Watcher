# summarizer.py — Batch Evidence Linking Version
from openai import OpenAI
import json

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
# 2. Extract structured insights (JSON with 4 sections)
# ---------------------------------------------------------
def extract_insights_from_social(posts):
    """
    Returns structured JSON:
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

Extract insights into four structured JSON lists.

Return ONLY valid JSON with this structure:

{{
  "Key Trends": [],
  "Pain Points": [],
  "Opportunities for CloudBees": [],
  "Indicators of DevOps Market Sentiment": []
}}

Rules:
- No markdown
- No bullet characters
- Short, high-value insights only
- Do NOT include sources
- Pure JSON output only

TEXT:
{text_blob}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    try:
        insights = json.loads(raw)
    except:
        cleaned = raw.strip()
        if not cleaned.startswith("{"):
            cleaned = "{" + cleaned
        if not cleaned.endswith("}"):
            cleaned = cleaned + "}"
        insights = json.loads(cleaned)

    return insights


# ---------------------------------------------------------
# 3. BATCH evidence linking (1 GPT call per category)
# ---------------------------------------------------------
def batch_link_sources(insights_dict, posts):
    """
    Returns:
    {
        "Key Trends": { insight: [ {title,url}, ... ] },
        "Pain Points": { ... },
        ...
    }
    """

    # Build compact list of available sources
    all_sources = [
        {
            "title": p.get("title", "Untitled"),
            "url": p.get("url") or p.get("link") or ""
        }
        for p in posts
        if p.get("url") or p.get("link")
    ]

    source_blob = "\n".join(
        f"- {s['title']} ({s['url']})" for s in all_sources
    )

    # For each category, one GPT call
    linked = {}

    for category, insight_list in insights_dict.items():

        if not insight_list:
            linked[category] = {}
            continue

        insights_blob = "\n".join([f"- {i}" for i in insight_list])

        prompt = f"""
You are an AI assistant linking insights to supporting evidence.

INSIGHTS:
{insights_blob}

SOURCES:
{source_blob}

Task:
Return a JSON object mapping *each insight* to an array of 3–6 relevant sources.

Format:
{{
  "insight text": [
    {{ "title": "...", "url": "..." }},
    ...
  ],
  ...
}}

Rules:
- Only JSON, no markdown
- If no relevant match, return empty array []
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
        except:
            parsed = {}

        linked[category] = parsed

    return linked


# ---------------------------------------------------------
# 4. Convert insights + evidence → Markdown
# ---------------------------------------------------------
def format_insights_with_sources(insights_dict, linked_sources):
    """
    Final markdown for the report.
    """

    output = []

    for category, insight_list in insights_dict.items():
        output.append(f"### {category}")

        if not insight_list:
            output.append("_No insights found._\n")
            continue

        for insight in insight_list:
            output.append(f"- **{insight}**")

            matches = (linked_sources
                       .get(category, {})
                       .get(insight, []))

            if matches:
                for s in matches:
                    output.append(f"  - [{s['title']}]({s['url']})")
            else:
                output.append("  - _No supporting sources detected_")

        output.append("")  # spacing

    return "\n".join(output)
