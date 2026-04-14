#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SDK_ROOT="$(dirname "$SCRIPT_DIR")"
SPEC_DIR="$SDK_ROOT/spec"
GEN_DIR="$SDK_ROOT/src/fermata/_generated"
DEMETRA_OPENAPI="$(cd "$SDK_ROOT/.." && pwd)/demetra/api/openapi"
VENV_BIN="$SDK_ROOT/.venv/bin"

DOMAINS=(observations aivision catalog pipelines)

echo "=== Copying specs from demetra ==="
for domain in "${DOMAINS[@]}"; do
    cp "$DEMETRA_OPENAPI/$domain.yml" "$SPEC_DIR/"
    echo "  Copied $domain.yml"
done

echo ""
echo "=== Generating clients ==="
for domain in "${DOMAINS[@]}"; do
    output="$GEN_DIR/$domain"
    echo "  Generating $domain..."
    rm -rf "$output"
    "$VENV_BIN/openapi-python-client" generate \
        --path "$SPEC_DIR/$domain.yml" \
        --output-path "$output" \
        --config "$SDK_ROOT/openapi-config.yml" \
        --meta none \
        --overwrite 2>&1 | sed 's/^/    /'
done

echo ""
echo "=== Cleaning up generated scaffolding ==="
for domain in "${DOMAINS[@]}"; do
    output="$GEN_DIR/$domain"
    # Remove generated project files we don't need (we have our own pyproject.toml)
    rm -f "$output/pyproject.toml" "$output/README.md" "$output/.gitignore"
    rm -rf "$output/.ruff_cache"
    # The generated package is nested under a derived name — move contents up
    pkg_dir=$(find "$output" -maxdepth 1 -type d -name "*_client" | head -1)
    if [ -n "$pkg_dir" ]; then
        # Move package contents to domain root
        mv "$pkg_dir"/* "$output/"
        rm -rf "$pkg_dir"
    fi
done

echo ""
echo "Done. Generated clients in $GEN_DIR"
