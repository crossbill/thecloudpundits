import json
from pathlib import Path
from html import unescape
import feedparser

BASE = Path(__file__).resolve().parent.parent / "public" / "data"
BASE.mkdir(parents=True, exist_ok=True)

FEEDS = {
    "cloud": [
        "https://aws.amazon.com/blogs/aws/feed/",
        "https://cloud.google.com/blog/rss/",
    ],
    "ai": [
        "https://huggingface.co/blog/feed.xml",
        "https://www.anthropic.com/news/rss.xml",
    ],
    "devops": [
        "https://dev.to/feed/tag/devops",
    ],
    "finops": [
        "https://www.finops.org/feed/",
    ],
    "secops": [
        "https://www.securityweek.com/feed/",
        "https://www.darkreading.com/rss.xml"
    ]
}


def clean(text):
    return unescape(text or "").strip()


def classify(title, summary=""):
    text = (title + " " + summary).lower()

    # Cloud providers
    if any(x in text for x in ["aws", "amazon web services"]):
        return "aws"

    if any(x in text for x in ["azure", "microsoft"]):
        return "azure"

    if any(x in text for x in ["google cloud", "gcp"]):
        return "gcp"

    # Kubernetes / DevOps
    if any(x in text for x in ["kubernetes", "k8s"]):
        return "kubernetes"

    if any(x in text for x in ["docker", "container"]):
        return "docker"

    if any(x in text for x in ["terraform"]):
        return "terraform"

    # AI / LLMs
    if any(x in text for x in ["openai", "chatgpt"]):
        return "openai"

    if "anthropic" in text or "claude" in text:
        return "anthropic"

    if "hugging face" in text or "huggingface" in text:
        return "huggingface"

    if "finops" in text or "cost optimization" in text:
        return "finops"
        # 🔐 SECOPS
    if any(x in text for x in [
        "security", "breach", "vulnerability",
        "zero trust", "ransomware", "attack",
        "cyber", "incident", "iam"
    ]):
        return "secops"

    if any(x in text for x in [
        "ai safety",
        "guardrails",
        "alignment",
        "responsible ai",
        "ai governance",
        "model risk",
        "prompt injection",
        "jailbreak"
    ]):
        return "guardrails"

    return "general"


def fetch(url):
    feed = feedparser.parse(url)

    results = []

    for e in feed.entries[:8]:
        title = clean(e.get("title"))

        results.append({
            "title": title,
            "desc": clean(e.get("summary", ""))[:140],
            "link": e.get("link"),
            "topic": classify(title)
        })

    return results


for cat, urls in FEEDS.items():
    items = []

    for url in urls:
        items.extend(fetch(url))

    seen = set()
    unique = []

    for item in items:
        if item["link"] not in seen:
            seen.add(item["link"])
            unique.append(item)

    with open(BASE / f"{cat}.json", "w") as f:
        json.dump(unique[:8], f, indent=2)

    print(f"{cat}: {len(unique)}")
