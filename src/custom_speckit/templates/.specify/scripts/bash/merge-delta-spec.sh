#!/usr/bin/env bash

# Unset CDPATH to prevent issues with cd command when calculating script directory
unset CDPATH

# Merge delta specification into main spec
#
# This script prepares paths and validates prerequisites for delta merging.
# The actual merge logic is performed by the AI agent in /speckit.approve-delta
# 
# Usage: ./merge-delta-spec.sh [OPTIONS]
#
# OPTIONS:
#   --spec-path PATH    Path to specs/spec.md
#   --delta-path PATH   Path to delta-spec.md
#   --branch NAME       Branch name
#   --json              Output in JSON format
#   --help, -h          Show help message
#
# OUTPUTS:
#   JSON mode: {"SUCCESS":true/false, "SPEC_PATH":"...", "DELTA_PATH":"...", "ERROR":"..."}
#   Text mode: SUCCESS: true/false \n SPEC_PATH: ... \n DELTA_PATH: ...

set -e

# Parse command line arguments
JSON_MODE=false
SPEC_PATH=""
DELTA_PATH=""
BRANCH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --spec-path)
            SPEC_PATH="$2"
            shift 2
            ;;
        --delta-path)
            DELTA_PATH="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --json)
            JSON_MODE=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Usage: merge-delta-spec.sh [OPTIONS]

Validate and prepare for merging delta specification into main spec.
The actual merge is performed by the AI agent.

OPTIONS:
  --spec-path PATH    Path to main specification (specs/spec.md)
  --delta-path PATH   Path to delta specification (.deltas/{branch}/delta-spec.md)
  --branch NAME       Branch name for tracking
  --json              Output in JSON format
  --help, -h          Show this help message

EXAMPLES:
  # Prepare merge with JSON output
  ./merge-delta-spec.sh --spec-path .specify/specs/spec.md \
    --delta-path .specify/.deltas/001-feature/delta-spec.md \
    --branch 001-feature --json

NOTE:
  This script only validates prerequisites and prepares paths.
  The actual text merging is done by the AI agent in /speckit.approve-delta
  to ensure intelligent handling of additions, modifications, and deletions.

EOF
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$1'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$SPEC_PATH" ]]; then
    echo "ERROR: --spec-path is required" >&2
    exit 1
fi

if [[ -z "$DELTA_PATH" ]]; then
    echo "ERROR: --delta-path is required" >&2
    exit 1
fi

if [[ -z "$BRANCH" ]]; then
    echo "ERROR: --branch is required" >&2
    exit 1
fi

# Validate file existence
ERROR=""
SUCCESS=true

if [[ ! -f "$SPEC_PATH" ]]; then
    ERROR="Main spec not found: $SPEC_PATH"
    SUCCESS=false
fi

if [[ ! -f "$DELTA_PATH" ]]; then
    ERROR="Delta spec not found: $DELTA_PATH"
    SUCCESS=false
fi

# Check if spec is writable
if [[ "$SUCCESS" == "true" ]] && [[ ! -w "$SPEC_PATH" ]]; then
    ERROR="Main spec is not writable: $SPEC_PATH"
    SUCCESS=false
fi

# Get absolute paths
if [[ "$SUCCESS" == "true" ]]; then
    SPEC_PATH=$(cd "$(dirname "$SPEC_PATH")" && pwd)/$(basename "$SPEC_PATH")
    DELTA_PATH=$(cd "$(dirname "$DELTA_PATH")" && pwd)/$(basename "$DELTA_PATH")
fi

# Output results
if $JSON_MODE; then
    if [[ "$SUCCESS" == "true" ]]; then
        printf '{"SUCCESS":true,"SPEC_PATH":"%s","DELTA_PATH":"%s","BRANCH":"%s"}\n' \
            "$SPEC_PATH" "$DELTA_PATH" "$BRANCH"
    else
        printf '{"SUCCESS":false,"ERROR":"%s"}\n' "$ERROR"
    fi
else
    echo "SUCCESS: $SUCCESS"
    if [[ "$SUCCESS" == "true" ]]; then
        echo "SPEC_PATH: $SPEC_PATH"
        echo "DELTA_PATH: $DELTA_PATH"
        echo "BRANCH: $BRANCH"
    else
        echo "ERROR: $ERROR"
    fi
fi

# Exit with appropriate code
if [[ "$SUCCESS" == "true" ]]; then
    exit 0
else
    exit 1
fi

