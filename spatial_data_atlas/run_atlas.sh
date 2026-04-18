#!/bin/bash
echo ""
echo "  Spatial & Geographical Data Visualization Atlas"
echo "  89 charts | 18 3D scenes | 14 thematic groups"
echo ""
PORT=${1:-8000}
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "  Starting at http://localhost:$PORT"
echo "  Press Ctrl+C to stop"
cd "$DIR" && python3 -m http.server $PORT 2>/dev/null || python -m SimpleHTTPServer $PORT
