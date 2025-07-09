#!/usr/bin/env python3

import os
import json
from datetime import datetime
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

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

def generate_atom_feed(pr_data, output_path, base_url="https://llm-pr-summary.com"):
    """Generate an Atom feed from PR data"""
    
    # Create the root feed element
    feed = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
    
    # Feed metadata
    title = ET.SubElement(feed, "title")
    title.text = "LLM PR Summary Feed"
    
    link = ET.SubElement(feed, "link", href=base_url, rel="alternate")
    link_self = ET.SubElement(feed, "link", href=f"{base_url}/feed.xml", rel="self")
    
    feed_id = ET.SubElement(feed, "id")
    feed_id.text = f"{base_url}/feed.xml"
    
    subtitle = ET.SubElement(feed, "subtitle")
    subtitle.text = "AI-generated summaries of GitHub pull requests"
    
    author = ET.SubElement(feed, "author")
    author_name = ET.SubElement(author, "name")
    author_name.text = "LLM PR Summary"
    
    # Use the latest PR date as the feed updated time, or current time if no PRs
    if pr_data:
        latest_date = pr_data[0].get('created', datetime.now().isoformat())
        # Convert to ISO format if needed
        if 'T' in latest_date and not latest_date.endswith('Z'):
            latest_date = latest_date + 'Z' if not latest_date.endswith('Z') else latest_date
    else:
        latest_date = datetime.now().isoformat() + 'Z'
    
    updated = ET.SubElement(feed, "updated")
    updated.text = latest_date
    
    # Add entries for each PR (limit to most recent 20 for feed size)
    for pr in pr_data[:20]:
        entry = ET.SubElement(feed, "entry")
        
        entry_title = ET.SubElement(entry, "title")
        entry_title.text = f"#{pr.get('number', 'N/A')}: {pr.get('title', 'No title')}"
        
        entry_link = ET.SubElement(entry, "link", href=f"https://pr.tim.ad/?search={pr.get('number', '')}")
        
        entry_id = ET.SubElement(entry, "id")
        entry_id.text = pr.get('url', f"{base_url}/pr/{pr.get('number', 'unknown')}")
        
        entry_updated = ET.SubElement(entry, "updated")
        pr_date = pr.get('created', datetime.now().isoformat())
        if 'T' in pr_date and not pr_date.endswith('Z'):
            pr_date = pr_date + 'Z' if not pr_date.endswith('Z') else pr_date
        entry_updated.text = pr_date
        
        entry_published = ET.SubElement(entry, "published")
        entry_published.text = pr_date
        
        entry_author = ET.SubElement(entry, "author")
        entry_author_name = ET.SubElement(entry_author, "name")
        entry_author_name.text = pr.get('author', 'Unknown')
        
        # Use summary as content
        entry_summary = ET.SubElement(entry, "summary", type="text")
        summary_text = pr.get('summary', '')
        if not summary_text and pr.get('details'):
            # Fallback to details if no summary
            summary_text = '\n'.join(pr.get('details', []))
        entry_summary.text = summary_text
        
        # Add content with more detailed information
        entry_content = ET.SubElement(entry, "content", type="html")
        content_html = f"""
        <h3>Summary</h3>
        <p>{summary_text}</p>
        
        <h3>Details</h3>
        <ul>
        """
        for detail in pr.get('details', []):
            content_html += f"<li>{detail}</li>\n"
        
        content_html += """
        </ul>
        
        <p><strong>Repository:</strong> {}</p>
        <p><strong>State:</strong> {}</p>
        <p><strong>Analysis Date:</strong> {}</p>
        """.format(
            pr.get('repository', 'Unknown'),
            pr.get('state', 'Unknown'),
            pr.get('analysis_date', 'Unknown')
        )
        
        entry_content.text = content_html
    
    # Pretty print the XML
    rough_string = ET.tostring(feed, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Remove extra blank lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"Generated atom feed with {min(len(pr_data), 20)} entries at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate website data from PR analyses")
    parser.add_argument("--analysis-folder", default="data/analysis/github/docs", help="Path to analysis folder")
    parser.add_argument("--output", default="public/pr-data.json", help="Output file path")
    
    args = parser.parse_args()

        
    try:        
        generate_website_data(args.analysis_folder, args.output)
        generate_atom_feed(json.load(open(args.output, 'r', encoding='utf-8')), 
                          output_path="app/public/feed.atom",
                          base_url="https://pr.tim.ad")
    
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
