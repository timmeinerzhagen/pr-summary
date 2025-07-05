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

- **[Usage Guide](docs/USAGE.md)**: Complete guide with examples and troubleshooting
- **[Website Documentation](docs/README.md)**: Setup and customization for the web dashboard

## Web Dashboard

The project includes a beautiful web dashboard that displays your PR analyses:

- 📊 **Interactive Interface**: Clean, modern design with search functionality
- 📱 **Responsive**: Works on desktop and mobile devices
- 🚀 **Auto-Deploy**: Automatically deploys to GitHub Pages
- 🔍 **Searchable**: Find PRs by number, title, author, or content

### Quick Setup

1. Analyze some PRs to create data files
2. Run `./scripts/build_website.sh serve` to view locally
3. Push to GitHub to automatically deploy via GitHub Pages

The website will show all your PR analyses in an easy-to-browse format with statistics and search capabilities.

## Features

- ✅ Fetch diffs from any public GitHub Pull Request
- ✅ Analyze code changes using OpenRouter AI models
- ✅ Generate structured markdown summaries
- ✅ Support for custom output files
- ✅ Environment variable configuration
- ✅ Rate limit handling with GitHub tokens
- ✅ **Web dashboard** for viewing PR summaries
- ✅ **GitHub Pages** deployment for easy sharing

## Quick Start

### Analyze a Single PR

```bash
# Basic analysis
python3 main.py --repo microsoft/vscode --pr 200000

# Custom output file
python3 main.py --repo facebook/react --pr 25000 --output react_analysis.md

# Test without API key
python3 test_fetch.py
```

### Build the Website

```bash
# Generate website data and serve locally
./scripts/build_website.sh serve

# Or just generate the data
./scripts/build_website.sh
```

The website will be available at `http://localhost:8000` and shows all your PR analyses in a beautiful dashboard format.

## References

* https://github.com/edverma/git-smart-squash
* https://github.com/behrouz-rad/AI-PR-Summarizer

## Tools

* https://openrouter.ai/
* https://api.github.com/
