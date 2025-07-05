# llm-pr-summary

A tool to analyze GitHub Pull Request diffs using OpenRouter AI and generate high-level summaries.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenRouter API key:
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```

3. Analyze a Pull Request:
   ```bash
   python3 main.py --repo owner/repo --pr 123
   ```

## Documentation

- **[Usage Guide](USAGE.md)**: Complete guide with examples and troubleshooting
- **[Setup Guide](docs/SETUP.md)**: Original setup documentation

## Features

- ✅ Fetch diffs from any public GitHub Pull Request
- ✅ Analyze code changes using OpenRouter AI models
- ✅ Generate structured markdown summaries
- ✅ Support for custom output files
- ✅ Environment variable configuration
- ✅ Rate limit handling with GitHub tokens

## Usage Examples

```bash
# Basic analysis
python3 main.py --repo microsoft/vscode --pr 200000

# Custom output file
python3 main.py --repo facebook/react --pr 25000 --output react_analysis.md

# Test without API key
python3 test_fetch.py
```

## References

* https://github.com/edverma/git-smart-squash
* https://github.com/behrouz-rad/AI-PR-Summarizer

## Tools

* https://openrouter.ai/
* https://api.github.com/
