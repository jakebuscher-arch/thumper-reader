#!/bin/bash
# One-click launcher for the Interactive Thumper 5-Book Reader

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Use port 8899 to avoid collisions with other projects on 8080
PORT=8899

# Find local IP address for tablet/phone access over Wi-Fi
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

echo "=========================================================="
echo "  THE COMPLETE THUMPER SERIES — INTERACTIVE READER"
echo "=========================================================="
echo ""
echo "Starting local book server from:"
echo "  $DIR"
echo ""
echo "📖 Read on your Mac:   http://localhost:$PORT"
echo "📱 Read on your iPad:  http://$LOCAL_IP:$PORT"
echo "📱 Read on your Phone: http://$LOCAL_IP:$PORT"
echo ""
echo "Press Ctrl+C to stop the reader server at any time."
echo "=========================================================="

cd "$DIR"

# Open default browser on Mac
(sleep 1 && open "http://localhost:$PORT") &

python3 -m http.server $PORT
