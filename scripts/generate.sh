#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SDK_ROOT="$(dirname "$SCRIPT_DIR")"
SPEC_DIR="$SDK_ROOT/spec"
GEN_DIR="$SDK_ROOT/src/fermata/_generated"
DEMETRA_OPENAPI="$(cd "$SDK_ROOT/.." && pwd)/demetra/api/openapi"
VENV_BIN="$SDK_ROOT/.venv/bin"
FILTER="$VENV_BIN/python $SCRIPT_DIR/filter_spec.py"
VERSION_FILE="$SPEC_DIR/VERSION"

# All domains by default; pass domain names as arguments to regenerate a subset,
# e.g. `scripts/generate.sh greenhouses`.
ALL_DOMAINS=(observations aivision catalog pipelines cultivation greenhouses)
if [[ $# -gt 0 ]]; then
    DOMAINS=("$@")
else
    DOMAINS=("${ALL_DOMAINS[@]}")
fi
for domain in "${DOMAINS[@]}"; do
    if [[ ! " ${ALL_DOMAINS[*]} " == *" $domain "* ]]; then
        echo "Error: unknown domain '$domain' (expected one of: ${ALL_DOMAINS[*]})" >&2
        exit 1
    fi
done

# Operations the SDK actually uses (matched by operationId).
# Only these are kept in the filtered specs — everything else is stripped.
declare -A OPS
OPS[observations]="createPhoto createPhotoUploadLink"
OPS[aivision]="submitInference getInferenceTask"
OPS[catalog]="listAIModels getAIModelByName"
OPS[pipelines]="listSchedules getSchedule createFire startFire completeFire"
OPS[cultivation]="getCycle listActiveCyclesAtTime"
OPS[greenhouses]="listGreenhouses listGreenhouseObjects getGreenhouseObject"

# Load pinned spec versions from spec/VERSION (format: "domain: X.Y.Z").
declare -A PINNED
while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    domain="${line%%:*}"
    version="${line#*:}"
    version="${version// /}"
    PINNED[$domain]="$version"
done < "$VERSION_FILE"

echo "=== Copying and filtering specs from demetra ==="
for domain in "${DOMAINS[@]}"; do
    expected="${PINNED[$domain]:-}"
    if [[ -z "$expected" ]]; then
        echo "Error: domain '$domain' is not pinned in $VERSION_FILE" >&2
        echo "  Add a line: $domain: <version>" >&2
        exit 1
    fi

    cp "$DEMETRA_OPENAPI/$domain.yml" "$SPEC_DIR/$domain.full.yml"

    actual=$("$VENV_BIN/python" -c "import yaml,sys; print(yaml.safe_load(open(sys.argv[1]))['info']['version'])" "$SPEC_DIR/$domain.full.yml")
    if [[ "$actual" != "$expected" ]]; then
        rm -f "$SPEC_DIR/$domain.full.yml"
        echo "Error: $domain spec version mismatch" >&2
        echo "  pinned ($VERSION_FILE): $expected" >&2
        echo "  upstream (demetra):     $actual" >&2
        echo "  → If the change is intentional, bump $VERSION_FILE to $actual and rerun 'make generate'." >&2
        exit 1
    fi

    ops="${OPS[$domain]}"
    $FILTER "$SPEC_DIR/$domain.full.yml" $ops > "$SPEC_DIR/$domain.yml"
    rm "$SPEC_DIR/$domain.full.yml"
    echo "  $domain@$actual: kept $(echo $ops | wc -w | tr -d ' ') operations"
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
