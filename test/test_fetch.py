#!/usr/bin/env python3
"""
Test script to demonstrate fetching a GitHub PR diff without calling OpenRouter
"""

import requests
import json
from datetime import datetime

def test_fetch_pr_diff():
    """Test fetching a GitHub PR diff"""
    
    # Using a public PR from GitHub's docs repository
    repo_owner = "github"
    repo_name = "docs"
    pr_number = 37991
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    
    # Get PR info first
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PR-Analyzer-Test"
    }
    
    try:
        print(f"Fetching PR #{pr_number} from {repo_owner}/{repo_name}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pr_data = response.json()
        
        print(f"✓ PR Title: {pr_data.get('title', 'N/A')}")
        print(f"✓ PR Author: {pr_data.get('user', {}).get('login', 'N/A')}")
        print(f"✓ PR State: {pr_data.get('state', 'N/A')}")
        print(f"✓ Created: {pr_data.get('created_at', 'N/A')}")
        
        # Get the diff
        diff_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        diff_headers = headers.copy()
        diff_headers["Accept"] = "application/vnd.github.v3.diff"
        
        diff_response = requests.get(diff_url, headers=diff_headers)
        diff_response.raise_for_status()
        
        diff_content = diff_response.text
        print(f"✓ Diff fetched successfully ({len(diff_content)} characters)")
        print(f"✓ First 300 characters of diff:")
        print("-" * 50)
        print(diff_content[:300])
        print("-" * 50)
        
        # Save example output
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pr_url = f"https://github.com/{repo_owner}/{repo_name}/pull/{pr_number}"
        
        markdown_content = f"""# Pull Request Analysis (Test)

## PR Information
- **Repository**: {repo_owner}/{repo_name}
- **PR Number**: #{pr_number}
- **Title**: {pr_data.get('title', 'N/A')}
- **Author**: {pr_data.get('user', {}).get('login', 'N/A')}
- **URL**: {pr_url}
- **State**: {pr_data.get('state', 'N/A')}
- **Created**: {pr_data.get('created_at', 'N/A')}
- **Test Date**: {timestamp}

## Test Results

✓ Successfully fetched PR data from GitHub API
✓ Successfully fetched diff content ({len(diff_content)} characters)
✓ Ready for OpenRouter analysis

## Sample Diff (first 300 characters)

```diff
{diff_content[:300]}
```

## Original PR Description

{pr_data.get('body', 'No description provided')[:500]}{'...' if len(pr_data.get('body', '')) > 500 else ''}

---
*Test run - would normally analyze with OpenRouter API*
"""
        
        with open("test_pr_analysis.md", 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print("✓ Test analysis saved to test_pr_analysis.md")
        print("✓ Ready to use with OpenRouter API key!")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching PR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing GitHub PR diff fetching...")
    print("=" * 50)
    test_fetch_pr_diff()
    print("=" * 50)
    print("Test complete!")
