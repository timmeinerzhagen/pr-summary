#!/bin/bash
# Example usage of the PR analyzer

# Make sure you have set your OpenRouter API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Please set your OPENROUTER_API_KEY environment variable"
    echo "Example: export OPENROUTER_API_KEY='your_api_key_here'"
    exit 1
fi

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "Analyzing PR..."
python3 src/generate_summary.py --repo github/docs --pr $1 --output "data/analysis/github/docs/$1.json"

echo "Analysis complete! Check the generated JSON file."
echo "Run 'python scripts/generate_website_data.py' to update the website data."
