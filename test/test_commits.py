#!/usr/bin/env python3
"""
Test script to verify commit fetching functionality
"""

import requests
import json
from datetime import datetime

def test_fetch_pr_with_commits():
    """Test fetching a GitHub PR with commits"""
    
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
        
        # Get the commits
        commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits"
        commits_response = requests.get(commits_url, headers=headers)
        commits_response.raise_for_status()
        commits_data = commits_response.json()
        
        print(f"✓ Found {len(commits_data)} commits")
        
        # Show first few commits
        print("\n📝 Commits in this PR:")
        for i, commit in enumerate(commits_data[:5]):  # Show first 5 commits
            commit_msg = commit.get('commit', {}).get('message', 'No message')
            commit_sha = commit.get('sha', 'Unknown')[:7]  # Short SHA
            commit_author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
            print(f"  {i+1}. {commit_sha}: {commit_msg.split(chr(10))[0]} (by {commit_author})")
        
        if len(commits_data) > 5:
            print(f"  ... and {len(commits_data) - 5} more commits")
        
        # Test the formatting for the prompt
        commit_messages = []
        for commit in commits_data:
            commit_msg = commit.get('commit', {}).get('message', '').split('\n')[0]
            commit_messages.append(f"- {commit_msg}")
        
        commits_text = '\n'.join(commit_messages) if commit_messages else 'No commit messages available'
        
        print(f"\n📋 Formatted for prompt (first 500 chars):")
        print("-" * 50)
        print(commits_text[:500])
        if len(commits_text) > 500:
            print("...")
        print("-" * 50)
        
        print("✓ Commit fetching functionality works correctly!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching PR: {e}")
        return False

if __name__ == "__main__":
    print("Testing GitHub PR commit fetching...")
    print("=" * 60)
    test_fetch_pr_with_commits()
    print("=" * 60)
    print("Test complete!")
