import os
import argparse
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from pathlib import Path

def get_pull_requests(owner: str, repo: str, token: str, days: int) -> List[Dict]:
    """
    Fetch merged pull requests from GitHub repository within the specified number of days.
    
    Args:
        owner: Repository owner
        repo: Repository name
        token: GitHub personal access token
        days: Number of days to look back
        
    Returns:
        List of pull request dictionaries
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    since_date = datetime.now() - timedelta(days=days)
    
    all_prs = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {
            "state": "closed",  # Changed from "all" to "closed" since merged PRs are closed
            "sort": "created",
            "direction": "desc",
            "page": page,
            "per_page": per_page
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        prs = response.json()
        if not prs:
            break
            
        for pr in prs:
            # Only include merged PRs
            if pr.get("merged_at") is None:
                continue
                
            created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if created_at < since_date:
                return all_prs
            all_prs.append(pr)
        
        page += 1
    
    return all_prs


def check_summary_exists(owner: str, repo: str, pr_number: int, data_folder: str = "data/analysis") -> bool:
    """
    Check if a summary file exists for the given PR number.
    
    Args:
        pr_number: Pull request number
        data_folder: Path to the analysis folder
        
    Returns:
        True if summary file exists, False otherwise
    """
    summary_path = Path(data_folder) / f"{owner}/{repo}/{pr_number}.md"
    return summary_path.exists()


def list_prs_without_summaries(owner: str, repo: str, token: str, days: int) -> List[Dict]:
    """
    Get list of merged PRs without summary files.
    
    Args:
        owner: Repository owner
        repo: Repository name
        token: GitHub personal access token
        days: Number of days to look back
        
    Returns:
        List of PR dictionaries without summaries
    """
    prs = get_pull_requests(owner, repo, token, days)
    prs_without_summaries = []
    
    for pr in prs:
        pr_number = pr["number"]
        if not check_summary_exists(owner, repo, pr_number):
            prs_without_summaries.append(pr_number)
    
    return prs_without_summaries


def main():
    parser = argparse.ArgumentParser(description="List merged PRs without summaries")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back (default: 7)")
    parser.add_argument("--data-folder", default="data/analysis", help="Path to analysis folder")
    
    args = parser.parse_args()
    
    # Ensure data folder exists
    Path(args.data_folder).mkdir(parents=True, exist_ok=True)
    
    try:
        prs_without_summaries = list_prs_without_summaries(
            args.owner, args.repo, args.token, args.days
        )

        # Convert PR numbers to string with newlines
        return '\n'.join(str(pr) for pr in prs_without_summaries)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PRs: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())