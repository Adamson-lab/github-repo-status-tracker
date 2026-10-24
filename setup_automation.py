import os

def setup_tracker():
    # 1. Ensure workflow directory exists
    os.makedirs(".github/workflows", exist_ok=True)

    # 2. Create requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write("requests\n")
    print("✓ Created requirements.txt")

    # 3. Create update_status.py script
    script_content = '''import os
import requests
from datetime import datetime, timezone

USERNAME = "Adamson-lab"
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

if __name__ == "__main__":
    print(f"Fetching repositories for {USERNAME}...")
    repositories = fetch_repositories()
    print(f"Successfully fetched {len(repositories)} repositories.")
'''
    with open("update_status.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    print("✓ Created update_status.py")

    # 4. Create GitHub Action Workflow
    workflow_content = '''name: Update Repository Status

on:
  schedule:
    - cron: "0 */6 * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run status tracker script
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python update_status.py
'''
    with open(".github/workflows/update-tracker.yml", "w", encoding="utf-8") as f:
        f.write(workflow_content)
    print("✓ Created .github/workflows/update-tracker.yml")

if __name__ == "__main__":
    setup_tracker()
    print("Effortless setup completed successfully!")
'''
