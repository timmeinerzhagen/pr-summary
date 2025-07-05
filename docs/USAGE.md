# GitHub PR Analyzer Usage Guide

This guide shows how to use the GitHub PR analyzer to get high-level summaries of Pull Requests using OpenRouter AI.

## Prerequisites

1. **OpenRouter API Key**: Sign up at [OpenRouter.ai](https://openrouter.ai/) and get your API key
2. **Python 3.7+**: Make sure you have Python installed
3. **GitHub Token (Optional)**: For higher rate limits when fetching PRs

## Installation

```bash
# Clone or download the repository
cd llm-pr-summary

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
export GITHUB_TOKEN="your_github_token_here"  # Optional but recommended
```

## Basic Usage

### Analyze a Pull Request

```bash
python3 main.py --repo owner/repo --pr PR_NUMBER
```

### Examples

```bash
# Analyze a Microsoft VS Code PR
python3 main.py --repo microsoft/vscode --pr 200000

# Analyze a React PR with custom output file
python3 main.py --repo facebook/react --pr 25000 --output react_analysis.md

# Use API key from command line
python3 main.py --repo owner/repo --pr 123 --api-key your_api_key_here
```

## Advanced Usage

### Environment Variables

Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your keys
```

Or export them:
```bash
export OPENROUTER_API_KEY="your_key_here"
export GITHUB_TOKEN="your_token_here"
```

### Batch Processing

Create a script to analyze multiple PRs:

```bash
#!/bin/bash
# analyze_multiple_prs.sh

REPO="microsoft/vscode"
OUTPUT_DIR="analyses"

mkdir -p $OUTPUT_DIR

for PR in 200000 200001 200002; do
    echo "Analyzing PR #$PR..."
    python3 main.py --repo $REPO --pr $PR --output "$OUTPUT_DIR/pr_${PR}_analysis.md"
done
```

## Output Format

The tool generates a markdown file with:

- **PR Information**: Repository, PR number, title, author, URL, state, dates
- **High-Level Summary**: AI-generated analysis of what the PR does
- **Original PR Description**: The description from GitHub

## Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Error: OpenRouter API key is required
   ```
   Solution: Set the `OPENROUTER_API_KEY` environment variable

2. **Rate Limit Exceeded**
   ```
   Error fetching PR diff: 403 Client Error
   ```
   Solution: Set a GitHub token with `GITHUB_TOKEN` environment variable

3. **PR Not Found**
   ```
   Error fetching PR diff: 404 Client Error
   ```
   Solution: Check that the repository and PR number are correct

4. **Repository Format Error**
   ```
   Error: Repository must be in format 'owner/repo'
   ```
   Solution: Use the correct format like `microsoft/vscode`

## API Costs

The tool uses OpenRouter's API. Costs depend on:
- **Model used**: Currently uses `anthropic/claude-3-haiku` (cost-effective)
- **Diff size**: Larger diffs cost more to analyze
- **Usage frequency**: Pay per request

To minimize costs:
- Use the tool selectively on important PRs
- Consider using cheaper models for simple analyses
- Monitor your OpenRouter usage dashboard

## Supported Repositories

Works with any **public** GitHub repository. For private repositories, you'll need:
- A GitHub token with appropriate access
- The repository owner's permission

## Examples of Good Use Cases

1. **Code Review Preparation**: Get a summary before diving into detailed review
2. **Release Notes**: Understand what changed in a PR for documentation
3. **Team Updates**: Quick summaries for standup meetings
4. **Learning**: Understand how other teams structure their changes

## Customization

You can modify the `main.py` script to:
- Change the AI model used (see OpenRouter's model list)
- Adjust the analysis prompt for different focus areas
- Change the output format
- Add additional PR metadata

## Test the Setup

Run the test script to verify everything works:

```bash
python3 test_fetch.py
```

This will fetch a real PR diff without calling OpenRouter, so you can test the GitHub API integration first.

## Support

For issues with:
- **OpenRouter API**: Check [OpenRouter documentation](https://openrouter.ai/docs)
- **GitHub API**: Check [GitHub API documentation](https://docs.github.com/en/rest)
- **This tool**: Check the error messages and troubleshooting section above
