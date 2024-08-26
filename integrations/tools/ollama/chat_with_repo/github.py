import base64
import requests
from typing import Dict, Any, List

class GitHubService:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def github_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_repo_info(self, repo_name: str) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{repo_name}"
        return self.github_request(url)

    def fetch_pr_info(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
        return self.github_request(url)

    def fetch_file_changes(self, repo_name: str, pr_number: int) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
        return self.github_request(url)

    def fetch_repo_readme(self, repo_name: str) -> str:
        readme_url = f"https://api.github.com/repos/{repo_name}/readme"
        response = self.github_request(readme_url)
        return base64.b64decode(response['content']).decode('utf-8')