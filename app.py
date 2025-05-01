from flask import Flask, request, jsonify
from pathlib import Path

from git_tools import clone_pr_repo
from github_api import get_changed_files
from code_extractor import extract_java_methods
from ai_agent import get_refactor_suggestion

import json
import os

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    SUGGESTIONS_FILE = Path("output/suggestions.json")
    all_suggestions = []
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == "pull_request" and payload.get("action") in ["opened", "synchronize", "reopened"]:
        pr = payload["pull_request"]
        repo_info = payload["repository"]

        repo_url = repo_info["clone_url"]
        repo_name = repo_info["name"]
        pr_branch = pr["head"]["ref"]
        owner = repo_info["owner"]["login"]
        pr_number = pr["number"]

        print(f"\n🔔 PR received for {repo_name}")
        local_path = clone_pr_repo(repo_url, pr_branch, repo_name)

        changed_java_files = get_changed_files(owner, repo_name, pr_number)

        print("📄 Changed Java files:")
        for file_rel_path in changed_java_files:
            file_path = os.path.join(local_path, file_rel_path)
            if not os.path.exists(file_path):
                print(f"⚠️ Skipped (not found): {file_path}")
                continue

            methods = extract_java_methods(file_path)
            print(f"\n📦 Extracted {len(methods)} method(s) from {file_rel_path}:")
            for method in methods:
                print("-----")
                print(method.strip()[:300], "..." if len(method) > 300 else "")

                try:
                    suggestion = get_refactor_suggestion(method)
                    all_suggestions.append({
                         "file": file_rel_path,
                         "original": method.strip(),
                         "suggested": suggestion.strip()
                    })
                    print("\n✨ Suggested Refactor (trimmed):")
                    print(suggestion[:500], "..." if len(suggestion) > 500 else "")
                except Exception as e:
                    print("❌ OpenAI failed:", e)
    SUGGESTIONS_FILE.parent.mkdir(exist_ok=True)
    SUGGESTIONS_FILE.write_text(json.dumps(all_suggestions, indent=2))

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)