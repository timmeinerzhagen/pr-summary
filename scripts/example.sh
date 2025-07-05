#!/bin/bash
# Example usage of the PR analyzer

# Make sure you have set your OpenRouter API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Please set your OPENROUTER_API_KEY environment variable"
    echo "Example: export OPENROUTER_API_KEY='your_api_key_here'"
    exit 1
fi

# Example 1: Analyze a Microsoft VS Code PR
echo "Analyzing Microsoft VS Code PR..."
python3 src/main.py --repo microsoft/vscode --pr 200000 --output data/vscode_pr_analysis.md

# Example 2: Analyze a Facebook React PR
echo "Analyzing Facebook React PR..."
python3 src/main.py --repo facebook/react --pr 25000 --output data/react_pr_analysis.md

echo "Analysis complete! Check the generated markdown files."
