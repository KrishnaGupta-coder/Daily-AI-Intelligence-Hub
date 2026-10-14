import urllib.request
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def fetch_arxiv_papers():
    """Fetches top 5 recent AI / Machine Learning papers from arXiv."""
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CV+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=5"
    papers = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            # Namespace for Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                link = entry.find('atom:id', ns).text.strip()
                published = entry.find('atom:published', ns).text.strip()[:10]
                papers.append({
                    'title': title,
                    'summary': summary[:250] + '...',
                    'link': link,
                    'date': published
                })
    except Exception as e:
        print(f"Error fetching arXiv: {e}")
    return papers

def fetch_huggingface_models():
    """Fetches trending AI models from Hugging Face."""
    url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=5"
    models = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for m in data:
                models.append({
                    'id': m.get('id', 'Unknown'),
                    'downloads': m.get('downloads', 0),
                    'likes': m.get('likes', 0),
                    'link': f"https://huggingface.co/{m.get('id')}"
                })
    except Exception as e:
        print(f"Error fetching HuggingFace: {e}")
    return models

from datetime import datetime, timezone

def generate_report():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    report_file = os.path.join("reports", f"{today}.md")

    papers = fetch_arxiv_papers()
    models = fetch_huggingface_models()

    content = f"""# 🧠 AI Intelligence Digest — {today}

Automated daily intelligence synthesis tracking breaking machine learning papers and trending open weights.

---

### 📄 Breaking arXiv Research Papers (AI / CV / LG)

| Paper Title | Date | Link | Abstract Snippet |
| :--- | :--- | :--- | :--- |
"""
    for p in papers:
        content += f"| **{p['title']}** | `{p['date']}` | [Read Paper]({p['link']}) | {p['summary']} |\n"

    content += "\n---\n\n### 🔥 Trending Hugging Face Models\n\n| Model Name | Downloads | Likes | Hugging Face URL |\n| :--- | :--- | :--- | :--- |\n"
    for m in models:
        content += f"| `{m['id']}` | {m['downloads']:,} | {m['likes']:,} | [View Model]({m['link']}) |\n"

    content += f"\n\n---\n*Report generated automatically by [Krishna Gupta's Daily AI Intelligence Hub](https://github.com/KrishnaGupta-coder/Daily-AI-Intelligence-Hub) on {today} UTC.*"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Report generated: {report_file}")
    update_main_readme(today, papers, models)

def update_main_readme(today, papers, models):
    reports = sorted(os.listdir("reports"), reverse=True)
    
    table_rows = ""
    for r in reports[:10]:
        date = r.replace(".md", "")
        table_rows += f"| 📅 `{date}` | [View Full Intelligence Report](reports/{r}) | Verified Automated Digest |\n"

    readme_content = f"""<div align="center">

  <h1>⚡ Daily AI Intelligence Hub</h1>
  <p><b>Autonomous Daily Engine Tracking Frontier AI Models, Research Papers & Computer Vision Benchmarks</b></p>

  <img src="https://img.shields.io/badge/Status-Automated_Daily-00C7B7?style=for-the-badge&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/Total_Digests-{len(reports)}-7928CA?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Maintained_By-Krishna_Gupta-3776AB?style=for-the-badge&logo=python&logoColor=white" />

</div>

---

### 🛰️ Overview
This repository operates as an **autonomous intelligence agent** maintained by [Krishna Gupta](https://github.com/KrishnaGupta-coder). Every 24 hours at 00:00 UTC, a GitHub Action wakes up, queries the **arXiv AI/ML repository** and **Hugging Face API**, parses latest publications, compiles a structured intelligence report, and commits it directly to the archive.

---

### 📡 Latest Digest Summary (`{today}`)

#### Top arXiv Papers Detected Today:
"""
    for p in papers[:3]:
        readme_content += f"- **[{p['title']}]({p['link']})** — `{p['date']}`\n"

    readme_content += f"""
---

### 📚 Intelligence Archive (Latest 10 Days)

| Date | Report Link | Validation |
| :--- | :--- | :--- |
{table_rows}

---

### 🛠️ Architecture & Workflow

```mermaid
flowchart LR
    A[⏰ GitHub Action Cron] --> B[🐍 Python Intelligence Agent]
    B --> C[📡 arXiv API - CS.AI / CV / LG]
    B --> D[🤗 Hugging Face Model API]
    C --> E[📊 Compile Daily Report]
    D --> E
    E --> F[📝 Commit & Push to Repo]
```

---

<div align="center">
  <sub>Autonomous AI Data Pipeline • Designed by <a href="https://github.com/KrishnaGupta-coder">Krishna Gupta</a> • Jaipur, India</sub>
</div>
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("README.md updated successfully!")

if __name__ == "__main__":
    generate_report()
