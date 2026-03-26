#!/bin/bash

cd "$(dirname "$0")/.." || exit

TMP_DIR="${RUNNER_TEMP:-/tmp/mermaid_out_$$}"

# Process .mmd files
find docs/adr -name "*.mmd" | while read -r mmd_file; do
    echo "Processing $mmd_file..."
    out_file="${mmd_file%.mmd}.png"

    tmp_out_file="$TMP_DIR/$out_file"
    mkdir -p "$(dirname "$tmp_out_file")"
    chmod 777 "$(dirname "$tmp_out_file")"
    
    docker run --rm -v "$PWD:/workspace" -v "$TMP_DIR:/tmp_workspace" minlag/mermaid-cli -p /workspace/scripts/puppeteer-config.json -i "/workspace/$mmd_file" -o "/tmp_workspace/$out_file"
    
    # Copy generated image safely back to the user's workspace
    cp "$tmp_out_file" "$out_file"
done

# Cleanup standalone temp directories locally
if [ "$CI" != "true" ]; then
    rm -rf "$TMP_DIR"
fi

echo "Done generating mermaid diagrams."
