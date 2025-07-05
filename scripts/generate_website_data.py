#!/usr/bin/env python3
"""
Generate website data from PR analysis markdown files
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

def parse_markdown_file(file_path):
    """Parse a markdown file and extract PR information"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract PR information using regex
        pr_info = {}
        
        # Extract PR number
        pr_match = re.search(r'- \*\*PR Number\*\*: #(\d+)', content)
        if pr_match:
            pr_info['number'] = int(pr_match.group(1))
        
        # Extract title
        title_match = re.search(r'- \*\*Title\*\*: (.+)', content)
        if title_match:
            pr_info['title'] = title_match.group(1).strip()
        
        # Extract author
        author_match = re.search(r'- \*\*Author\*\*: (.+)', content)
        if author_match:
            pr_info['author'] = author_match.group(1).strip()
        
        # Extract state
        state_match = re.search(r'- \*\*State\*\*: (.+)', content)
        if state_match:
            pr_info['state'] = state_match.group(1).strip()
        
        # Extract created date
        created_match = re.search(r'- \*\*Created\*\*: (.+)', content)
        if created_match:
            pr_info['created'] = created_match.group(1).strip()
        
        # Extract URL
        url_match = re.search(r'- \*\*URL\*\*: (.+)', content)
        if url_match:
            pr_info['url'] = url_match.group(1).strip()
        
        # Extract repository
        repo_match = re.search(r'- \*\*Repository\*\*: (.+)', content)
        if repo_match:
            pr_info['repository'] = repo_match.group(1).strip()
        
        # Extract analysis date
        analysis_match = re.search(r'- \*\*Analysis Date\*\*: (.+)', content)
        if analysis_match:
            pr_info['analysis_date'] = analysis_match.group(1).strip()
        
        # Extract high-level summary
        summary_match = re.search(r'## High-Level Summary\n\n(.+?)(?=\n## |$)', content, re.DOTALL)
        if summary_match:
            summary_text = summary_match.group(1).strip()
            
            # Try to extract structured summary (### Summary section)
            structured_summary_match = re.search(r'### Summary\n(.+?)(?=\n### |$)', summary_text, re.DOTALL)
            if structured_summary_match:
                summary_content = structured_summary_match.group(1).strip()
                # Extract bullet points as details
                details = []
                for line in summary_content.split('\n'):
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('• '):
                        details.append(line[2:].strip())
                    elif line.startswith('  - ') or line.startswith('  • '):
                        details.append(line[4:].strip())
                
                if details:
                    pr_info['details'] = details
                    # Use first detail as main summary if available
                    pr_info['summary'] = details[0] if details else summary_content
                else:
                    pr_info['summary'] = summary_content
            else:
                # Fallback to old parsing logic
                lines = summary_text.split('\n')
                pr_info['summary'] = lines[0].strip()
                
                # Extract bullet points as details
                details = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('• '):
                        details.append(line[2:].strip())
                    elif line.startswith('  - ') or line.startswith('  • '):
                        details.append(line[4:].strip())
                
                if details:
                    pr_info['details'] = details
                else:
                    # If no bullet points, try to extract from the summary text
                    # Look for lines that contain key changes
                    detail_lines = []
                    for line in lines[1:]:  # Skip first line (main summary)
                        line = line.strip()
                        if line and not line.startswith('**') and len(line) > 20:
                            detail_lines.append(line)
                    
                    if detail_lines:
                        pr_info['details'] = detail_lines[:5]  # Limit to 5 details
            
            # Try to extract structured title (### Title section)
            structured_title_match = re.search(r'### Title\n(.+?)(?=\n### |$)', summary_text, re.DOTALL)
            if structured_title_match:
                title_content = structured_title_match.group(1).strip()
                pr_info['generated_title'] = title_content
        
        # Extract commits
        commits_match = re.search(r'## Commits\n\n(.+?)(?=\n## |$)', content, re.DOTALL)
        if commits_match:
            commits_text = commits_match.group(1).strip()
            commits = []
            for line in commits_text.split('\n'):
                line = line.strip()
                if line.startswith('- **'):
                    commits.append(line[4:])  # Remove '- **' prefix
            pr_info['commits'] = commits
        
        return pr_info
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_website_data():
    """Generate data for the website from all markdown files"""
    
    # Path to the analysis files
    analysis_dir = Path('data/analysis/github/docs')
    
    if not analysis_dir.exists():
        print(f"Analysis directory not found: {analysis_dir}")
        return
    
    # Parse all markdown files
    pr_data = []
    
    for md_file in analysis_dir.glob('*.md'):
        print(f"Parsing {md_file.name}...")
        pr_info = parse_markdown_file(md_file)
        if pr_info:
            pr_data.append(pr_info)
    
    # Sort by PR number (descending)
    pr_data.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    print(f"Parsed {len(pr_data)} PR analyses")
    
    # Generate JavaScript data file
    js_data = f"""// Generated PR data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
const prData = {json.dumps(pr_data, indent=2)};

// Update the global prData array
if (typeof window !== 'undefined') {{
    window.prData = prData;
}}

// For Node.js environments
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = prData;
}}
"""
    
    # Write to docs directory
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    with open(docs_dir / 'pr-data.js', 'w', encoding='utf-8') as f:
        f.write(js_data)
    
    print(f"Generated pr-data.js with {len(pr_data)} PRs")
    
    # Also create a JSON file for other uses
    with open(docs_dir / 'pr-data.json', 'w', encoding='utf-8') as f:
        json.dump(pr_data, f, indent=2)
    
    print(f"Generated pr-data.json with {len(pr_data)} PRs")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total PRs: {len(pr_data)}")
    if pr_data:
        print(f"Latest PR: #{pr_data[0].get('number', 'N/A')} - {pr_data[0].get('title', 'N/A')}")
        print(f"Oldest PR: #{pr_data[-1].get('number', 'N/A')} - {pr_data[-1].get('title', 'N/A')}")

if __name__ == '__main__':
    generate_website_data()
