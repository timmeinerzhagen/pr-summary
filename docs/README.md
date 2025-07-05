# GitHub PR Analysis Website

A beautiful dashboard to display AI-powered summaries of GitHub Pull Requests.

## Features

- 📊 **Interactive Dashboard**: Clean, modern interface showing PR summaries
- 🔍 **Search Functionality**: Search PRs by number, title, author, or content
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🤖 **AI-Powered**: Uses OpenRouter API for intelligent PR analysis
- 📈 **Statistics**: Shows total PRs, repositories, and latest analysis dates

## Structure

```
docs/
├── index.html          # Main website file
├── pr-data.js          # Generated PR data (JavaScript)
├── pr-data.json        # Generated PR data (JSON)
└── USAGE.md           # Original usage documentation
```

## Setup

### 1. Generate PR Data

Run the data generation script to parse markdown files and create website data:

```bash
python3 scripts/generate_website_data.py
```

This will:
- Parse all markdown files in `data/analysis/github/docs/`
- Extract PR information and summaries
- Generate `docs/pr-data.js` and `docs/pr-data.json`

### 2. GitHub Pages Setup

The website is automatically deployed to GitHub Pages using GitHub Actions. To set it up:

1. Go to your repository settings
2. Navigate to "Pages" in the sidebar
3. Select "GitHub Actions" as the source
4. The workflow will automatically build and deploy the site

### 3. Manual Local Testing

To test the website locally:

```bash
# Serve the docs directory
cd docs
python3 -m http.server 8000

# Or use any static file server
npx serve .
```

Then visit `http://localhost:8000`

## GitHub Actions Workflow

The `.github/workflows/deploy-website.yml` workflow:

- Triggers on pushes to `main` branch
- Runs when analysis files, docs, or scripts are modified
- Generates fresh PR data
- Deploys to GitHub Pages automatically

## Customization

### Adding New Repositories

To add PRs from other repositories:

1. Add analysis files to `data/analysis/[owner]/[repo]/`
2. Update the data generation script if needed
3. The website will automatically include the new data

### Styling

Modify the CSS in `index.html` to customize:
- Colors and themes
- Layout and spacing
- Typography
- Responsive breakpoints

### Data Format

The generated data includes:
- PR number, title, author, state, dates
- AI-generated summary and details
- Commit information
- GitHub URL for direct access

## Troubleshooting

### No Data Showing

1. Check that `pr-data.js` exists in the `docs/` directory
2. Verify the console for JavaScript errors
3. Ensure the markdown files are properly formatted

### Build Failures

1. Check the GitHub Actions workflow logs
2. Verify Python dependencies are installed
3. Ensure the markdown files are valid

### Pages Not Updating

1. Check that GitHub Pages is enabled in repository settings
2. Verify the workflow completed successfully
3. Clear browser cache and try again

## Contributing

1. Add new PR analysis files to `data/analysis/`
2. Run the data generation script
3. Test the website locally
4. Commit and push changes
5. The website will automatically update

## License

This project is part of the llm-pr-summary tool. See the main README for license information.
