#!/bin/bash

cd "$(dirname "$0")/.." || exit

# Process .mmd files
find docs/adr -name "*.mmd" | while read -r mmd_file; do
    echo "Processing $mmd_file..."
    # npx mmdc compiles the .mmd file to a .png file of the same name
    out_file="${mmd_file%.mmd}.png"
    npx -y -p @mermaid-js/mermaid-cli mmdc -p scripts/puppeteer-config.json -i "$mmd_file" -o "$out_file"
done

echo "Done generating mermaid diagrams."
