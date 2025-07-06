#!/usr/bin/env python3
"""
GitHub PR Diff Analyzer using OpenRouter
Fetches a GitHub Pull Request diff and analyzes it using OpenRouter API
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
    
    def analyze_with_openrouter(self, diff_content: str, pr_data: Dict[str, Any], commits_data: list) -> str:
        """
        Analyze the diff using OpenRouter API
        
        Args:
            diff_content: The git diff content
            pr_data: PR metadata from GitHub API
            commits_data: List of commits in the PR
            
        Returns:
            Analysis result from OpenRouter
        """
        # Format commit messages
        commit_messages = []
        for commit in commits_data:
            commit_msg = commit.get('commit', {}).get('message', '').split('\n')[0]  # Get first line only
            commit_messages.append(f"- {commit_msg}")
        
        commits_text = '\n'.join(commit_messages) if commit_messages else 'No commit messages available'
        
        prompt = f"""You are a technical expert with deep knowledge of software development practices.
You have been given the output of a git diff from a GitHub Pull Request, which shows the differences between the original and modified versions of a set of files.

Please provide a summary of what this Pull Request does. Focus on:
1. Key changes made in the code. Grouped by topic or functionality if applicable.
2. A short meaningful title describing the gist of these changes. This should be able to give a good understanding of the PR at a glance without additional context.

Your response is formatted in markdown with the following structure:
### Summary
### Title

Keep your response concise but informative, suitable for a technical audience. Your response must be extremely concise, no more than 100 words. Answer in bullet points, not in paragraphs.

Commits in this PR:
{commits_text}

Here is the git diff output for analysis:

{diff_content}"""

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referrer": "https://pr.tim.ad",
            "X-Title": "GitHub PR Diff Analysis",
        }
        
        # Use a capable model for code analysis
        data = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
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

## Commits

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


def main():
    """Main function to run the PR analyzer"""
    parser = argparse.ArgumentParser(description="Analyze GitHub Pull Request using OpenRouter")
    parser.add_argument("--repo", required=True, help="Repository in format owner/repo")
    parser.add_argument("--pr", required=True, type=int, help="Pull Request number")
    parser.add_argument("--output", default="pr_analysis.md", help="Output markdown file")
    parser.add_argument("--api-key", help="OpenRouter API key (or use OPENROUTER_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Get API key from argument or environment
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable or use --api-key argument.")
        sys.exit(1)
    
    # Parse repository
    try:
        repo_owner, repo_name = args.repo.split("/")
    except ValueError:
        print("Error: Repository must be in format 'owner/repo'")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = GitHubPRAnalyzer(api_key)
    
    print(f"Fetching PR #{args.pr} from {args.repo}...")
    diff_content, pr_data, commits_data = analyzer.fetch_pr_diff(repo_owner, repo_name, args.pr)
    
    print("Analyzing diff with OpenRouter...")
    analysis = analyzer.analyze_with_openrouter(diff_content, pr_data, commits_data)
    
    print("Saving analysis to markdown...")
    analyzer.save_to_markdown(analysis, pr_data, commits_data, repo_owner, repo_name, args.pr, args.output)
    
    print("Done!")


if __name__ == "__main__":
    main()