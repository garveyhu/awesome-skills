#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v node >/dev/null 2>&1; then
    echo "Node.js was not detected."
    echo "Please install Node.js (>=14) and rerun this script."
    exit 1
fi

if ! command -v docsify >/dev/null 2>&1; then
    echo "Installing docsify-cli..."
    npm install -g docsify-cli
fi

echo "Launching Docsify server..."

cd "$DOCS_ROOT" || exit 1
docsify serve . --port 3000
