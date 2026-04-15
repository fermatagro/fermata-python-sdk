#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SDK_ROOT="$(dirname "$SCRIPT_DIR")"
SPEC_DIR="$SDK_ROOT/spec"
GEN_DIR="$SDK_ROOT/src/fermata/_generated"
DEMETRA_OPENAPI="$(cd "$SDK_ROOT/.." && pwd)/demetra/api/openapi"
VENV_BIN="$SDK_ROOT/.venv/bin"
FILTER="$VENV_BIN/python $SCRIPT_DIR/filter_spec.py"

DOMAINS=(observations aivision catalog pipelines cultivation greenhouses)

# Operations the SDK actually uses (matched by operationId).
# Only these are kept in the filtered specs — everything else is stripped.
declare -A OPS
OPS[observations]="createPhoto createPhotoUploadLink"
OPS[aivision]="submitInference getInferenceTask"
OPS[catalog]="listAIModels getAIModelByName"
OPS[pipelines]="listSchedules getSchedule createFire"
OPS[cultivation]="getCycle listActiveCyclesAtTime"
OPS[greenhouses]="listGreenhouses"

echo "=== Copying and filtering specs from demetra ==="
for domain in "${DOMAINS[@]}"; do
    cp "$DEMETRA_OPENAPI/$domain.yml" "$SPEC_DIR/$domain.full.yml"
    ops="${OPS[$domain]}"
    $FILTER "$SPEC_DIR/$domain.full.yml" $ops > "$SPEC_DIR/$domain.yml"
    rm "$SPEC_DIR/$domain.full.yml"
    echo "  $domain: kept $(echo $ops | wc -w | tr -d ' ') operations"
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
    rm -f "$output/pyproject.toml" "$output/README.md" "$output/.gitignore"
    rm -rf "$output/.ruff_cache"
    pkg_dir=$(find "$output" -maxdepth 1 -type d -name "*_client" | head -1)
    if [ -n "$pkg_dir" ]; then
        mv "$pkg_dir"/* "$output/"
        rm -rf "$pkg_dir"
    fi
done

echo ""
echo "Done. Generated clients in $GEN_DIR"
