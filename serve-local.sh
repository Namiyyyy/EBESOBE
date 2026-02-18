#!/bin/bash
# Serve the site locally so custom fonts load correctly.
# Browsers block font loading when opening HTML via file://
cd "$(dirname "$0")"
echo "Starting server at http://localhost:8000"
echo "Open that URL in your browser. Press Ctrl+C to stop."
python3 -m http.server 8000
