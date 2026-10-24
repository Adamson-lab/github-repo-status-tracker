import os
import requests
from datetime import datetime, timezone

USERNAME = "Adamson-lab"  # Your GitHub username
TOKEN = os.environ.get("GH_TOKEN")

def fetch_repositories():
    repos = []
    page = 1
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    
    while True:
        url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}&type=public"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        for repo in data:
            if not repo.get("fork"):
                repos.append({
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "issues": repo["open_issues_count"],
                    "ci": "—",
                    "updated": repo["updated_at"].split("T")[0]
                })
        page += 1
        
    repos = sorted(repos, key=lambda x: x["stars"], reverse=True)
    return repos

def generate_markdown(repos):
    total_stars = sum(r["stars"] for r in repos)
    total_forks = sum(r["forks"] for r in repos)
    total_issues = sum(r["issues"] for r in repos)
    
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    md = f"""![Last Updated](https://img.shields.io/badge/Last%20Updated-{now}%20UTC-blue?style=flat-square)

# GitHub Repository Status Tracker

Live status dashboard for @{USERNAME} repositories. Updates automatically every 6 hours via GitHub Actions.

**{len(repos)} repositories tracked · {total_stars:,} combined stars**

---

### Quick overview

| # | Repository | Stars | Forks | Issues | CI | Updated |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
"""

    for i, repo in enumerate(repos, 1):
        md += f"| {i} | [{repo['name']}]({repo['url']}) | {repo['stars']:,} | {repo['forks']:,} | {repo['issues']} | {repo['ci']} | {repo['updated']} |\n"
        
    return md

if __name__ == "__main__":
    print(f"Fetching repositories for {USERNAME}...")
    repositories = fetch_repositories()
    markdown_content = generate_markdown(repositories)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print("README.md updated successfully!")
