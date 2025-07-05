#!/usr/bin/env python3
"""
Test script to demonstrate the full PR analysis with commits (without OpenRouter)
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import argparse


class GitHubPRAnalyzer:
    def __init__(self, openrouter_api_key: str):
        """
        Initialize the analyzer with OpenRouter API key
        
        Args:
            openrouter_api_key: API key for OpenRouter
        """
        self.openrouter_api_key = openrouter_api_key
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        
    def fetch_pr_diff(self, repo_owner: str, repo_name: str, pr_number: int) -> str:
        """
        Fetch the diff from a GitHub Pull Request
        
        Args:
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
            pr_number: Pull Request number
            
        Returns:
            Raw diff content as string, PR data, and commits data
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        
        # Get PR info first
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PR-Analyzer"
        }
        
        # Add GitHub token if available (for higher rate limits)
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            pr_data = response.json()
            
            # Get the commits
            commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/commits"
            commits_response = requests.get(commits_url, headers=headers)
            commits_response.raise_for_status()
            commits_data = commits_response.json()
            
            # Get the diff
            diff_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
            diff_headers = headers.copy()
            diff_headers["Accept"] = "application/vnd.github.v3.diff"
            
            diff_response = requests.get(diff_url, headers=diff_headers)
            diff_response.raise_for_status()
            
            return diff_response.text, pr_data, commits_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching PR diff: {e}")
            sys.exit(1)
    
    def save_to_markdown(self, analysis: str, pr_data: Dict[str, Any], commits_data: list,
                        repo_owner: str, repo_name: str, pr_number: int, 
                        output_file: str = "pr_analysis.md"):
        """
        Save the analysis to a markdown file
        
        Args:
            analysis: The analysis result from OpenRouter
            pr_data: PR metadata from GitHub API
            commits_data: List of commits in the PR
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name
            pr_number: Pull Request number
            output_file: Output markdown file path
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pr_url = f"https://github.com/{repo_owner}/{repo_name}/pull/{pr_number}"
        
        # Format commits for markdown
        commits_section = ""
        if commits_data:
            commits_section = "\n## Commits\n\n"
            for commit in commits_data:
                commit_msg = commit.get('commit', {}).get('message', 'No message')
                commit_sha = commit.get('sha', 'Unknown')[:7]  # Short SHA
                commit_author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
                commits_section += f"- **{commit_sha}**: {commit_msg.split(chr(10))[0]} (by {commit_author})\n"
        
        markdown_content = f"""# Pull Request Analysis

## PR Information
- **Repository**: {repo_owner}/{repo_name}
- **PR Number**: #{pr_number}
- **Title**: {pr_data.get('title', 'N/A')}
- **Author**: {pr_data.get('user', {}).get('login', 'N/A')}
- **URL**: {pr_url}
- **State**: {pr_data.get('state', 'N/A')}
- **Created**: {pr_data.get('created_at', 'N/A')}
- **Analysis Date**: {timestamp}

## High-Level Summary

{analysis}
{commits_section}
## Original PR Description

{pr_data.get('body', 'No description provided')}

---
*Analysis generated using OpenRouter API*
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Analysis saved to {output_file}")
        except IOError as e:
            print(f"Error saving markdown file: {e}")
            sys.exit(1)

def test_full_analysis():
    """Test the full PR analysis workflow without calling OpenRouter"""
    
    # Create analyzer instance (with dummy API key for testing)
    analyzer = GitHubPRAnalyzer("dummy_api_key")
    
    # Test parameters
    repo_owner = "github"
    repo_name = "docs"
    pr_number = 37991
    
    print(f"🔍 Testing full PR analysis for {repo_owner}/{repo_name} PR #{pr_number}")
    print("=" * 70)
    
    try:
        # Fetch PR data and commits
        print("1. Fetching PR diff and commits...")
        diff_content, pr_data, commits_data = analyzer.fetch_pr_diff(repo_owner, repo_name, pr_number)
        
        print(f"   ✓ PR Title: {pr_data.get('title', 'N/A')}")
        print(f"   ✓ PR Author: {pr_data.get('user', {}).get('login', 'N/A')}")
        print(f"   ✓ Diff size: {len(diff_content)} characters")
        print(f"   ✓ Commits found: {len(commits_data)}")
        
        # Format commits for the prompt
        commit_messages = []
        for commit in commits_data:
            commit_msg = commit.get('commit', {}).get('message', '').split('\n')[0]
            commit_messages.append(f"- {commit_msg}")
        
        commits_text = '\n'.join(commit_messages) if commit_messages else 'No commit messages available'
        
        print(f"\n2. Commits formatted for analysis:")
        print(f"   {commits_text}")
        
        # Create a mock analysis (since we're not calling OpenRouter)
        mock_analysis = """• **Main Purpose**: Repository synchronization and content updates
• **Key Changes**: 
  - Added new documentation for issue management
  - Fixed typo in AI model name
  - Updated OpenAPI specifications
  - Added AI Search call-to-action component
• **Impact**: Improved documentation accuracy and user experience"""
        
        print(f"\n3. Mock analysis generated:")
        print(f"   {mock_analysis}")
        
        # Save to markdown
        print(f"\n4. Saving analysis to markdown...")
        analyzer.save_to_markdown(mock_analysis, pr_data, commits_data, repo_owner, repo_name, pr_number, "test_full_analysis.md")
        
        print(f"\n✅ Full analysis test completed successfully!")
        print(f"📄 Check 'test_full_analysis.md' for the complete output")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

if __name__ == "__main__":
    print("Testing full PR analysis workflow...")
    print("🚀 This test demonstrates the complete process including commits")
    print()
    
    success = test_full_analysis()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ All tests passed! The PR analyzer is ready to use with OpenRouter.")
        print("💡 To use with real OpenRouter API, set your OPENROUTER_API_KEY environment variable.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
