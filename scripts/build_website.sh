#!/bin/bash

# Build and serve the PR analysis website
# Usage: ./scripts/build_website.sh [serve]

set -e

echo "🔧 Building PR Analysis Website..."

# Generate website data
echo "📊 Generating website data..."
python3 scripts/generate_website_data.py

echo "✅ Website data generated successfully!"

# Check if we should serve the website
if [ "$1" = "serve" ]; then
    echo "🌐 Starting local server..."
    echo "Website will be available at: http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    cd docs
    python3 -m http.server 8000
else
    echo "🚀 Website ready! To serve locally, run:"
    echo "   ./scripts/build_website.sh serve"
    echo ""
    echo "📁 Files generated:"
    echo "   - docs/pr-data.js"
    echo "   - docs/pr-data.json"
    echo "   - docs/index.html"
    echo ""
    echo "🎯 Next steps:"
    echo "   1. Commit and push to trigger GitHub Pages deployment"
    echo "   2. Or test locally with the serve option"
fi
