#!/usr/bin/env bash

# Compare current spec with new requirements to determine if delta is needed
#
# This script checks if an existing spec exists and provides information
# needed for the AI agent to generate a delta specification.
#
# Usage: ./compare-specs.sh [OPTIONS]
#
# OPTIONS:
#   --json              Output in JSON format
#   --help, -h          Show help message
#
# OUTPUTS:
#   JSON mode: {"HAS_EXISTING_SPEC":true/false, "SPEC_PATH":"...", "DELTA_DIR":"..."}
#   Text mode: HAS_EXISTING_SPEC: true/false \n SPEC_PATH: ... \n DELTA_DIR: ...

set -e

# Parse command line arguments
JSON_MODE=false

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --help|-h)
            cat << 'EOF'
Usage: compare-specs.sh [OPTIONS]

Check if existing spec exists to determine if delta workflow is needed.

OPTIONS:
  --json              Output in JSON format
  --help, -h          Show this help message

EXAMPLES:
  # Check for existing spec in JSON format
  ./compare-specs.sh --json
  
  # Check for existing spec in text format
  ./compare-specs.sh
  
OUTPUT:
  - HAS_EXISTING_SPEC: true if specs/spec.md exists, false otherwise
  - SPEC_PATH: absolute path to specs/spec.md
  - DELTA_DIR: absolute path to .deltas/{branch}/ directory
  - CURRENT_BRANCH: current git branch or feature name

EOF
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get repository information
REPO_ROOT=$(get_repo_root)
CURRENT_BRANCH=$(get_current_branch)

# Define paths
SPEC_PATH="$REPO_ROOT/.specify/specs/spec.md"
DELTA_DIR="$REPO_ROOT/.specify/.deltas/$CURRENT_BRANCH"

# Check if existing spec exists
HAS_EXISTING_SPEC=false
if [[ -f "$SPEC_PATH" ]]; then
    HAS_EXISTING_SPEC=true
fi

# Get spec modification time if it exists
SPEC_MODIFIED=""
if [[ -f "$SPEC_PATH" ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        SPEC_MODIFIED=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$SPEC_PATH")
    else
        # Linux
        SPEC_MODIFIED=$(stat -c "%y" "$SPEC_PATH" | cut -d'.' -f1)
    fi
fi

# Output results
if $JSON_MODE; then
    printf '{"HAS_EXISTING_SPEC":%s,"SPEC_PATH":"%s","DELTA_DIR":"%s","CURRENT_BRANCH":"%s","SPEC_MODIFIED":"%s"}\n' \
        "$HAS_EXISTING_SPEC" "$SPEC_PATH" "$DELTA_DIR" "$CURRENT_BRANCH" "$SPEC_MODIFIED"
else
    echo "HAS_EXISTING_SPEC: $HAS_EXISTING_SPEC"
    echo "SPEC_PATH: $SPEC_PATH"
    echo "DELTA_DIR: $DELTA_DIR"
    echo "CURRENT_BRANCH: $CURRENT_BRANCH"
    if [[ -n "$SPEC_MODIFIED" ]]; then
        echo "SPEC_MODIFIED: $SPEC_MODIFIED"
    fi
fi

