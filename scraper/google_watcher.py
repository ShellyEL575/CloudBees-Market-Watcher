import os
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup  # added for summary cleanup

API_URL = "https://google.serper.dev/search"

# ✅ Release Orchestration Market Intel — Serper Search Queries
RELEASE_ORCH_QUERIES = [
    # 🧠 Problem / Pain Signals (what hurts)
    '"release coordination" pain OR "release coordination" bottleneck',
    '"release process" is manual OR "release process" spreadsheet OR "release checklist" spreadsheet',
    '"release train" delays OR "release train" bottleneck',
    '"release management" war room OR "release" war room OR "release weekend" fire drill',
    '"change approvals" slow OR "approval gates" bottleneck OR "change management" slows releases',
    '"multiple pipelines" release coordination OR "multi tool" CI/CD release process',
    '"hardening sprint" why OR "release hardening" time',
    '"hotfix" release process pain OR "emergency release" approvals',

    # 🧪 Category / Solution Language (what people call it)
    '"release orchestration" platform OR "release orchestration tool"',
    '"release management" platform OR "enterprise release management"',
    '"pipeline orchestration" OR "orchestrate pipelines" OR "orchestrating CI/CD"',
    '"deployment orchestration" platform OR "deployment orchestrator"',
    '"value stream orchestration" OR "value stream management" orchestration',
    '"release automation" enterprise OR "release automation platform"',

    # ⚙️ Multi-tool / complex environments (CloudBees sweet spot)
    '"orchestrate" Jenkins and GitHub Actions OR "orchestrate" Jenkins GitLab',
    '"multi tool" CI/CD orchestration OR "toolchain orchestration"',
    '"standardize CI/CD" across teams OR "govern CI/CD" across enterprise',
    '"centralize releases" across teams OR "single pane of glass" releases',
    '"release governance" across pipelines',

    # 🔐 Governance / Compliance / Audit evidence (enterprise buyer language)
    '"audit-ready" release evidence OR "audit evidence" CI/CD',
    '"SOX" release process OR "SOC 2" release approvals OR "ISO 27001" release evidence',
    '"change management" ITIL DevOps OR ITIL change enablement CI/CD',
    '"separation of duties" CI/CD OR "segregation of duties" CI/CD',
    '"policy as code" approvals OR "policy driven" release gates',
    '"approval workflow" CI/CD OR "electronic approvals" release management',
    '"traceability" from code to production OR "end-to-end traceability" releases',

    # 🚦 Controls / Gates / Risk (how it works)
    '"quality gates" release process OR "release gates" CI/CD',
    '"progressive delivery" approvals OR "deployment gates" progressive delivery',
    '"release promotion" dev to prod OR "environment promotion" pipeline',
    '"release freeze" automation OR "change window" automation',
    '"release calendar" tool OR "release schedule" automation',
    '"release readiness" criteria OR "release sign-off" workflow',

    # 📊 Visibility / analytics / value stream signals
    '"release visibility" dashboard OR "release status" dashboard',
    '"lead time for changes" bottleneck approvals OR "deployment frequency" governance',
    '"value stream" release governance OR "VSM" release orchestration',
    '"deployment approvals" analytics OR "release metrics" approvals',

    # 🧩 Implementation patterns (technical evaluator bait)
    '"orchestrate deployments" Kubernetes multi-service OR "microservices" release coordination',
    '"environment management" CI/CD OR "promotion model" CI/CD',
    '"release pipelines" vs "deployment pipelines" OR "pipeline templates" governance',
    '"pipeline as code" governance OR "workflow orchestration" CI/CD',
    '"artifact promotion" enterprise OR "immutable artifacts" promotion',

    # 🏷️ Competitors / adjacent categories (market tracking)
    '"Digital.ai Release" OR "XebiaLabs" release orchestration',
    '"Octopus Deploy" enterprise OR "Octopus Deploy" orchestration',
    '"Harness" release automation OR "Harness" governance',
    '"Jenkins" release orchestration plugin OR "Jenkins" pipeline orchestration',
    '"ServiceNow" change approvals CI/CD OR "ServiceNow DevOps" release',
    '"GitLab" release orchestration OR "GitHub" release management',
    '"Spinnaker" deployment orchestration OR "Argo Rollouts" progressive delivery',

    # 🧵 Practitioner sentiment sources (unfiltered)
    '"release orchestration" site:reddit.com OR "release management" site:reddit.com',
    '"release war room" site:reddit.com OR "release weekend" site:reddit.com',
    '"change approvals" site:news.ycombinator.com OR "release process" site:news.ycombinator.com',
    '"release checklist" site:github.com issues OR "release pipeline" site:github.com discussions',

    # 📈 Trend / 2026 narrative queries
    '"release orchestration" trends 2026 OR "enterprise release management" trends 2026',
    '"DevOps governance" trends 2026 OR "policy as code" approvals trends 2026',
    '"value stream orchestration" trends 2026 OR "VSM" trends 2026',
]

# ✅ Smart Tests Signals — added as a distinct, dedupable block
SMART_TESTS_QUERIES = [
    # 🧠 Problem / Pain Signals (user sentiment)
    'flaky tests are killing us OR "tests are flaky" OR "flake rate"',
    '"rerun until green" OR "rerun until it passes" OR "retry until green"',
    '"CI pipeline too slow" OR "CI is slow" OR "pipeline takes hours"',
    '"test suite takes hours" OR "test suite is too slow" OR "tests take forever"',
    '"mean time to green" OR MTTG OR "time to green"',
    '"false negatives" tests OR "spurious failures" tests OR "non-deterministic" tests',

    # 🧪 Category / Solution Language
    '"test impact analysis" OR "impact analysis for tests"',
    '"intelligent test selection" OR "smart test selection" OR "selective test execution"',
    '"change-based testing" OR "change based testing" OR "change-aware testing"',
    '"test prioritization" OR "test prioritisation" OR "risk-based testing" CI',
    '"predictive test selection" OR "ML-based test selection" OR "machine learning test selection"',
    '"test optimization" CI OR "test optimisation" CI',
    '"test intelligence" platform OR "test analytics" CI',

    # 🧯 Flaky test management + triage automation
    '"flaky test detection" OR "detect flaky tests"',
    '"flaky test quarantine" OR "quarantine flaky tests" OR "auto-quarantine tests"',
    '"automated test triage" OR "test failure classification" OR "failure clustering"',
    '"root cause analysis" test failures OR "classify test failures"',

    # ⚙️ Implementation / How-it-works
    '"select tests based on code changes" OR "tests based on changed files"',
    '"coverage-based test selection" OR "map tests to code coverage"',
    '"monorepo" "test selection" OR "microservices" "test selection"',
    '"distributed test execution" vs "test selection" OR "test sharding" vs "test selection"',

    # 💸 CI cost / FinOps angle (compute waste + reruns)
    '"CI cost" tests OR "build minutes" cost OR "compute waste" CI',
    '"reduce CI/CD cost" testing OR "cut CI cost" tests',
    '"reruns" "compute cost" OR "re-runs" "compute waste"',

    # 🧵 Unfiltered practitioner sources (append to keywords)
    # NOTE: These work best as separate queries to avoid Serper truncation.
    'flaky tests site:reddit.com OR "flaky tests" site:news.ycombinator.com',
    '"test impact analysis" site:reddit.com OR "selective test execution" site:news.ycombinator.com',
    '"automated test triage" site:reddit.com OR "test failure" "triage" site:news.ycombinator.com',
    '"flaky test quarantine" site:github.com issues OR "test selection" site:github.com discussions',
]

# ✅ Feature Management / Feature Flags Market Intel — Serper Search Queries
FEATURE_MGMT_QUERIES = [
    # 🧠 Problem / Pain Signals (sentiment + failure modes)
    '"feature flags" pain OR "feature flag" pain OR "flag debt"',
    '"feature flag sprawl" OR "flag explosion" OR "too many feature flags"',
    '"stale feature flags" OR "old feature flags" OR "remove feature flags"',
    '"feature flag cleanup" OR "flag cleanup" OR "flag lifecycle"',
    '"flag governance" OR "feature flag governance" OR "policy for feature flags"',
    '"feature flags" outage OR "feature flag" incident OR "flag misconfiguration"',
    '"feature flag" security risk OR "feature flags" compliance',
    '"feature flags" performance impact OR "feature flag" latency',

    # 🧪 Category / Solution Language (how buyers describe it)
    '"feature management" platform OR "feature management platform"',
    '"feature flags" platform OR "feature flag service"',
    '"release flags" OR "deployment flags" OR "ops flags"',
    '"progressive delivery" OR "progressive rollout" OR "safe rollout"',
    '"canary release" feature flags OR "canary" flags',
    '"blue green" feature flags OR "blue-green" flags',
    '"dark launch" OR "dark launching" OR "launch darkly" practices',
    '"kill switch" OR "feature kill switch" OR "remote kill switch"',
    '"remote config" vs "feature flags" OR "remote configuration" feature flags',

    # 🚀 Rollouts, experimentation, and control (why now / value framing)
    '"percentage rollout" OR "gradual rollout" OR "ramped rollout" feature flags',
    '"targeting rules" feature flags OR "audience targeting" feature flags',
    '"rollout guardrails" OR "rollout safety" feature flags',
    '"instant rollback" feature flags OR "rollback" "feature flag"',
    '"A/B testing" feature flags OR experimentation feature flags',
    '"feature flag" + "experiment" OR "experimentation platform" feature flags',

    # 🔐 Governance / Compliance / Auditability (enterprise angle)
    '"audit trail" feature flags OR "audit logging" feature flags',
    '"approval workflow" feature flags OR "change management" feature flags',
    '"SOX" feature flags OR "SOC 2" feature flags OR "ISO 27001" feature flags',
    '"least privilege" feature flags OR "RBAC" feature flags',
    '"separation of duties" feature flags',

    # ⚙️ Platform engineering / IDP integration patterns
    '"feature flags" internal developer platform OR "feature flags" platform engineering',
    '"GitOps" feature flags OR "config as code" feature flags',
    '"Kubernetes" feature flags OR "microservices" feature flags',
    '"edge" feature flags OR "mobile" remote config feature flags',
    '"OpenFeature" OR "Open Feature" OR "feature flag standard"',

    # 📊 Observability / metrics / guardrails (operational maturity)
    '"feature flag" monitoring OR "flag" observability OR "flag health"',
    '"SLO" feature flags OR "error budget" rollout guardrails',
    '"release health" metrics OR "deployment health" progressive delivery',
    '"automated rollback" progressive delivery OR "automatic rollback" canary',

    # 🏷️ Competitors / adjacent tools (market tracking)
    '"LaunchDarkly" pricing OR "LaunchDarkly" enterprise',
    '"Split" feature flags OR "Harness" feature flags OR "ConfigCat" feature flags',
    '"Flagsmith" OR "Unleash" feature flags OR "Optimizely" feature flags',
    '"feature management" vendor comparison OR "feature flags" comparison',

    # 🧵 Unfiltered practitioner sentiment (append sources)
    'feature flags pain site:reddit.com OR feature flag debt site:reddit.com',
    '"feature flag" outage site:news.ycombinator.com OR "feature flags" incident site:news.ycombinator.com',
    '"OpenFeature" site:github.com discussions OR "feature flag" site:github.com issues',
    '"LaunchDarkly" site:reddit.com OR "Split" site:reddit.com OR "Unleash" site:reddit.com',

    # 📈 Trend / 2026 narrative queries
    '"feature flags" trends 2026 OR "progressive delivery" trends 2026',
    '"remote config" trends 2026 OR "experimentation" trends 2026',
]

SEARCH_QUERIES = [
    # 🧱 Legacy CI/CD + Migration Signals
    'jenkins plugin compatibility issues OR jenkins upgrade friction',
    'migrated from jenkins OR moved to github actions OR ci/cd migration',
    'cloudbees migration OR migrated to cloudbees experience',
    'jenkins vs github actions OR gitlab vs cloudbees OR ci/cd tool comparisons',
    'github actions vs jenkins 2026 OR jenkins vs harness OR devops platform comparison',
    'CI/CD',

    # 🚀 Platform Engineering / Internal Developer Platforms
    '"internal developer platform" OR IDP OR platform engineering reviews',
    'enterprise developer platform adoption OR idp team success',
    'cloudbees platform vs backstage OR internal platform tools ci/cd',

    # 🔐 DevSecOps + Compliance Trends
    'devsecops in ci/cd OR pipeline security best practices',
    'policy as code devops OR compliance pipelines enterprise',
    'secure ci/cd implementation OR infrastructure as code security tools',

    # 🧠 AI in DevOps / AIOps Signals
    'ai-assisted devops tools OR ai-enhanced pipelines OR devops automation AI',
    'ai for build optimization OR ci/cd performance tuning with ai',
    'aiops case studies 2026 OR ai tools for dev workflows',
    'open claw',
    'openclaw',
    'ai devops',
    'ai CI/CD',
    'agentic CI/CD',
    'agentic devops',
    'latest devops ai trends',
    'ai gitops',

    # 📊 Observability / Monitoring / FinOps
    'observability pipelines OR full stack observability devops',
    'finops best practices ci/cd OR cloud cost optimization pipelines',
    'monitoring platform reviews OR logs metrics traces devops',
    'devops control plane',
    'control plane CI/CD'

    # ⚙️ Cloud Native / Kubernetes / GitOps
    'gitops pipelines OR gitops vs traditional ci/cd OR flux argo case study',
    'kubernetes ci/cd patterns OR cloud native deployment workflows',
    'serverless ci/cd 2026 OR modern cloud deployment pipeline',

    # 🧪 Tooling + Dev Experience
    'new ci/cd tools 2026 OR devops tooling landscape',
    'modern devops stack OR emerging ci/cd platforms',
    'developer experience feedback OR internal tools for dev productivity',

    # 🧭 Strategic Insights + Market Positioning
    'ci/cd enterprise tool ROI OR devops platform total cost of ownership',
    'which ci/cd platform to choose OR 2026 ci/cd buyer guide',
    'top devops platforms gartner OR ci/cd vendor comparison reviews',

    # 💬 Community/Practitioner Signals
    'reddit devops pain points OR ci/cd tool complaints 2026',
    'stackoverflow ci/cd migration issues OR internal dev tooling questions',
    'devops linkedin post OR platform engineering success story',
]



# --------------------------
# Helper: Retry Wrapper
# --------------------------
def safe_post(url, headers, payload, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            resp.raise_for_status()
            return resp.json()

        except Exception as e:
            print(f"❌ Serper request failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("⚠️ Giving up on this query.")
                return None


# --------------------------
# Main Fetcher
# --------------------------
def fetch_google_results():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    all_posts = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching (Serper): {query}")

        payload = {
            "q": query,
            "num": 10,
            "gl": "us",
            "hl": "en",
            "autocorrect": True,
            "type": "search",
            "tbs": "qdr:w"  # Filter: past week only
        }

        data = safe_post(API_URL, headers, payload)

        if not data:
            continue

        organic = data.get("organic", [])
        if not organic:
            print("⚠️ No organic results returned.")
            continue

        for result in organic:
            title = result.get("title")
            url = result.get("link")
            snippet = result.get("snippet", "")

            # Required fields
            if not title or not url:
                continue

            # Dedupe URLs across all queries
            if url in seen_urls:
                continue
            seen_urls.add(url)

            # Clean summary of any HTML tags
            clean_summary = BeautifulSoup(snippet, "html.parser").get_text()

            print(f"📌 Found: {title} ({url})")

            all_posts.append({
                "title": title,
                "url": url,
                "summary": clean_summary,
                "source": "Google",
                "type": "💬 Social Buzz",
                "timestamp": datetime.utcnow().isoformat(),
            })

    print(f"\n✅ Google posts collected: {len(all_posts)}")
    return all_posts
