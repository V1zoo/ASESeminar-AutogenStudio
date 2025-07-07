import requests
import os
import subprocess
import json
import sys

def get_problem_details(index: int) -> str:
    try:
        API_URL = "http://localhost:8081/task/index/"
        api_url = f"{API_URL}{index}"
        start_dir = os.getcwd()     #get current working directory
        repo_dir = os.path.join(start_dir, f"repos\\repo_{index}")
        responseJSON = requests.get(api_url, timeout=10).json()
        taskNumber = responseJSON['taskNumber']
        instance_id = responseJSON['instance_id']
        prompt = responseJSON["Problem_statement"]
        git_clone = responseJSON["git_clone"]
        fail_to_pass = json.loads(responseJSON.get("FAIL_TO_PASS","[]"))
        pass_to_pass = json.loads(responseJSON.get("PASS_TO_PASS","[]"))
        parts = git_clone.split("&&")
        clone_part = parts[0].strip()
        checkout_part = parts[-1].strip() if len(parts) > 1 else None
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMT"] = "0"
        repo_url = clone_part.split()[2]
        if not os.path.isdir(repo_dir):
            subprocess.run(["git", "clone", repo_url, repo_dir], check=True, env= env)
            if checkout_part:
                commit_hash = checkout_part.split()[-1]
                subprocess.run(["git", "checkout", commit_hash], cwd=repo_dir, check=True, env=env)
        
        result = {
            "index": index,
            "directory": repo_dir,
            "problem_description": prompt
        }
        return result
    except Exception as e:
        return f"Error: {str(e)}"
