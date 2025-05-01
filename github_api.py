import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_changed_files(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    files = response.json()
    java_files = [f["filename"] for f in files if f["filename"].endswith(".java")]

    return java_files

def post_pr_comment(owner, repo, pr_number, body_text):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(url, headers=headers, json={"body": body_text})
    if response.status_code != 201:
        print("❌ Failed to post comment:", response.text)
    else:
        print("✅ Comment posted successfully")
