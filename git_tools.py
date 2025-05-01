import os
import shutil
from git import Repo

CLONE_BASE = "./repos"

def clone_pr_repo(repo_url, branch_name, repo_name):
    # Create local path
    local_path = os.path.join(CLONE_BASE, repo_name)

    # Clean up if already cloned
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    print(f"🔁 Cloning {branch_name} from {repo_url}...")
    repo = Repo.clone_from(repo_url, local_path)
    repo.git.checkout(branch_name)

    print(f"✅ Cloned to {local_path}")
    return local_path

