import json
from pathlib import Path
from github_api import post_pr_comment

# SET THESE:
owner = "REPO_OWNER"
repo = "REPO_NAME"
pr_number = 7  # The real PR number

REVIEWED_FILE = Path("output/reviewed.json")
if not REVIEWED_FILE.exists():
    print("❌ No reviewed.json found. Run Streamlit review first.")
    exit()

data = json.loads(REVIEWED_FILE.read_text())

for i, item in enumerate(data):
    decision = item.get("edited") if item.get("edited") else item.get("suggested")
    approved = item.get("edited") or decision == item.get("suggested")

    if approved:
        comment = f"""💡 **CodeSage Suggestion for `{item['file']}`**
                       ```java {item['edited'] or item['suggested']}````
                   """
    else:
        print(f"❌ Suggestion #{i+1} was rejected. Skipping.")

    post_pr_comment(owner, repo, pr_number, comment)