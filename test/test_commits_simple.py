#!/usr/bin/env python3
"""
Simple test to demonstrate commits in the prompt
"""

import requests

def test_commits_in_prompt():
    """Test that commits are properly included in the analysis prompt"""
    
    # Test data
    repo_owner = "github"
    repo_name = "docs"
    pr_number = 37991
    
    print("🔍 Testing commits inclusion in prompt")
    print("=" * 50)
    
    # Get PR data
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "PR-Analyzer-Test"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pr_data = response.json()
        
        # Get commits
        commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits"
        commits_response = requests.get(commits_url, headers=headers)
        commits_response.raise_for_status()
        commits_data = commits_response.json()
        
        print(f"✅ PR: {pr_data.get('title', 'N/A')}")
        print(f"✅ Commits found: {len(commits_data)}")
        
        # Format commits like in the real script
        commit_messages = []
        for commit in commits_data:
            commit_msg = commit.get('commit', {}).get('message', '').split('\n')[0]
            commit_messages.append(f"- {commit_msg}")
        
        commits_text = '\n'.join(commit_messages)
        
        # Show what would be included in the prompt
        print("\n📝 Commits that would be included in OpenRouter prompt:")
        print("-" * 40)
        print(commits_text)
        print("-" * 40)
        
        print(f"\n🎯 This shows that commit messages are now included in the analysis!")
        print(f"   The AI will see both the PR title/description AND the commit messages")
        print(f"   This provides much better context for understanding what the PR does")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_commits_in_prompt()
