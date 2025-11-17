#!/usr/bin/env bash

# Unset CDPATH to prevent issues with cd command when calculating script directory
unset CDPATH

# Get project version from multiple sources
#
# This script attempts to determine the project version by checking:
# 1. Git tags (semver format: v*.*.*)
# 2. pyproject.toml (Python projects)
# 3. package.json (Node.js projects)
# 4. User input (if none of the above exist)
#
# Usage: ./get-version.sh [OPTIONS]
#
# OPTIONS:
#   --json              Output in JSON format
#   --auto              Don't prompt user, use "v1.0.0" as default
#   --version VERSION   Use specified version instead of detecting
#   --help, -h          Show help message
#
# OUTPUTS:
#   JSON mode: {"VERSION":"v1.0.0","SOURCE":"git|pyproject|package|default|user"}
#   Text mode: VERSION: v1.0.0 \n SOURCE: git

set -e

# Parse command line arguments
JSON_MODE=false
AUTO_MODE=false
SPECIFIED_VERSION=""

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --auto)
            AUTO_MODE=true
            ;;
        --version)
            shift
            SPECIFIED_VERSION="$1"
            ;;
        --help|-h)
            cat << 'EOF'
Usage: get-version.sh [OPTIONS]

Detect project version from various sources.

OPTIONS:
  --json              Output in JSON format
  --auto              Don't prompt user, use "v1.0.0" as default if no version found
  --version VERSION   Use specified version instead of detecting
  --help, -h          Show this help message

VERSION DETECTION ORDER:
  1. --version flag (if provided)
  2. Git tags (latest tag matching v*.*.*)
  3. pyproject.toml (Python projects)
  4. package.json (Node.js projects)
  5. User input (interactive) or v1.0.0 (if --auto)

VERSION FORMAT:
  - Must start with 'v' (e.g., v1.0.0)
  - Follows semantic versioning: MAJOR.MINOR.PATCH
  - Can include pre-release: v1.0.0-beta.1
  - Can include build metadata: v1.0.0+20230615

EXAMPLES:
  # Detect version automatically
  ./get-version.sh --json
  
  # Use specific version
  ./get-version.sh --version v2.1.0 --json
  
  # Auto mode (no prompts)
  ./get-version.sh --auto

EOF
            exit 0
            ;;
        *)
            # Skip unknown args (might be from other tools)
            ;;
    esac
done

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get repository root
REPO_ROOT=$(get_repo_root)

VERSION=""
SOURCE="unknown"

# Function to validate version format
validate_version() {
    local ver="$1"
    # Check if version starts with 'v' and follows semver pattern
    if [[ "$ver" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to ensure version starts with 'v'
ensure_v_prefix() {
    local ver="$1"
    if [[ "$ver" =~ ^v ]]; then
        echo "$ver"
    else
        echo "v$ver"
    fi
}

# 1. Check if version was specified via --version flag
if [[ -n "$SPECIFIED_VERSION" ]]; then
    VERSION=$(ensure_v_prefix "$SPECIFIED_VERSION")
    if validate_version "$VERSION"; then
        SOURCE="specified"
    else
        if $JSON_MODE; then
            printf '{"ERROR":"Invalid version format: %s"}\n' "$SPECIFIED_VERSION" >&2
        else
            echo "ERROR: Invalid version format: $SPECIFIED_VERSION" >&2
            echo "Expected format: v1.0.0 or 1.0.0" >&2
        fi
        exit 1
    fi
fi

# 2. Check Git tags (if version not already set)
if [[ -z "$VERSION" ]] && has_git; then
    # Get latest tag that matches semver pattern
    LATEST_TAG=$(git tag -l "v*.*.*" --sort=-v:refname | head -n 1)
    if [[ -n "$LATEST_TAG" ]]; then
        VERSION="$LATEST_TAG"
        SOURCE="git"
    fi
fi

# 3. Check pyproject.toml (if version not already set)
if [[ -z "$VERSION" ]] && [[ -f "$REPO_ROOT/pyproject.toml" ]]; then
    # Try to extract version from pyproject.toml
    if command -v python3 &> /dev/null; then
        PYPROJECT_VERSION=$(python3 -c "
import sys
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        sys.exit(1)

try:
    with open('$REPO_ROOT/pyproject.toml', 'rb') as f:
        data = tomllib.load(f)
    version = data.get('project', {}).get('version') or data.get('tool', {}).get('poetry', {}).get('version')
    if version:
        print(version)
except Exception:
    sys.exit(1)
" 2>/dev/null || echo "")
        
        if [[ -n "$PYPROJECT_VERSION" ]]; then
            VERSION=$(ensure_v_prefix "$PYPROJECT_VERSION")
            SOURCE="pyproject"
        fi
    else
        # Fallback: simple grep (less reliable)
        PYPROJECT_VERSION=$(grep -E '^version\s*=' "$REPO_ROOT/pyproject.toml" | head -n 1 | sed -E 's/.*version\s*=\s*"([^"]+)".*/\1/' || echo "")
        if [[ -n "$PYPROJECT_VERSION" ]]; then
            VERSION=$(ensure_v_prefix "$PYPROJECT_VERSION")
            SOURCE="pyproject"
        fi
    fi
fi

# 4. Check package.json (if version not already set)
if [[ -z "$VERSION" ]] && [[ -f "$REPO_ROOT/package.json" ]]; then
    if command -v node &> /dev/null; then
        PACKAGE_VERSION=$(node -p "require('$REPO_ROOT/package.json').version" 2>/dev/null || echo "")
        if [[ -n "$PACKAGE_VERSION" ]]; then
            VERSION=$(ensure_v_prefix "$PACKAGE_VERSION")
            SOURCE="package"
        fi
    else
        # Fallback: grep and simple parsing
        PACKAGE_VERSION=$(grep -E '"version"' "$REPO_ROOT/package.json" | head -n 1 | sed -E 's/.*"version"\s*:\s*"([^"]+)".*/\1/' || echo "")
        if [[ -n "$PACKAGE_VERSION" ]]; then
            VERSION=$(ensure_v_prefix "$PACKAGE_VERSION")
            SOURCE="package"
        fi
    fi
fi

# 5. If still no version, ask user or use default
if [[ -z "$VERSION" ]]; then
    if $AUTO_MODE; then
        # Use default version in auto mode
        VERSION="v1.0.0"
        SOURCE="default"
    else
        # Prompt user for version
        echo "No version detected from git tags, pyproject.toml, or package.json" >&2
        echo "Please enter project version (e.g., v1.0.0 or 1.0.0):" >&2
        read -r USER_VERSION
        
        if [[ -z "$USER_VERSION" ]]; then
            VERSION="v1.0.0"
            SOURCE="default"
        else
            VERSION=$(ensure_v_prefix "$USER_VERSION")
            if validate_version "$VERSION"; then
                SOURCE="user"
            else
                if $JSON_MODE; then
                    printf '{"ERROR":"Invalid version format: %s"}\n' "$USER_VERSION" >&2
                else
                    echo "ERROR: Invalid version format: $USER_VERSION" >&2
                    echo "Using default: v1.0.0" >&2
                fi
                VERSION="v1.0.0"
                SOURCE="default"
            fi
        fi
    fi
fi

# Output results
if $JSON_MODE; then
    printf '{"VERSION":"%s","SOURCE":"%s"}\n' "$VERSION" "$SOURCE"
else
    echo "VERSION: $VERSION"
    echo "SOURCE: $SOURCE"
fi

