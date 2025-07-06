#!/usr/bin/env python3
"""
Generate website data from PR analysis JSON files
"""

import os
import json
from datetime import datetime
from pathlib import Path

def parse_json_file(file_path):
    """Parse a JSON file and extract PR information"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            pr_info = json.load(f)
        
        # Ensure all required fields are present
        required_fields = ['number', 'title', 'author', 'state', 'created', 'url', 'repository']
        for field in required_fields:
            if field not in pr_info:
                print(f"Warning: Missing required field '{field}' in {file_path}")
                return None
        
        return pr_info
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_website_data():
    """Generate data for the website from all JSON files"""
    
    # Path to the analysis files
    analysis_dir = Path('data/analysis/github/docs')
    
    if not analysis_dir.exists():
        print(f"Analysis directory not found: {analysis_dir}")
        return
    
    # Parse all JSON files
    pr_data = []
    
    for json_file in analysis_dir.glob('*.json'):
        print(f"Parsing {json_file.name}...")
        pr_info = parse_json_file(json_file)
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
