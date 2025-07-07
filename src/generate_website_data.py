#!/usr/bin/env python3

import os
import json
from datetime import datetime
from pathlib import Path
import argparse

def parse_json_file(file_path):
    """Parse a JSON file and extract PR information"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            pr_info = json.load(f)
        
        return pr_info
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def generate_website_data(analysis_dir_name: str, output: str):
    """Generate data for the website from all JSON files"""
    
    # Path to the analysis files
    analysis_dir = Path(analysis_dir_name)
    
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
        
    with open(Path(output), 'w', encoding='utf-8') as f:
        f.write(json.dumps(pr_data, indent=2))
    
    print(f"Generated pr-data.json with {len(pr_data)} PRs")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total PRs: {len(pr_data)}")
    if pr_data:
        print(f"Latest PR: #{pr_data[0].get('number', 'N/A')} - {pr_data[0].get('title', 'N/A')}")
        print(f"Oldest PR: #{pr_data[-1].get('number', 'N/A')} - {pr_data[-1].get('title', 'N/A')}")

def main():
    parser = argparse.ArgumentParser(description="Generate website data from PR analyses")
    parser.add_argument("--analysis-folder", default="data/analysis/github/docs", help="Path to analysis folder")
    parser.add_argument("--output", default="public/pr-data.json", help="Output file path")
    
    args = parser.parse_args()

        
    try:        
        generate_website_data(args.analysis_folder, args.output)
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the folders exist and contain valid JSON files.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())