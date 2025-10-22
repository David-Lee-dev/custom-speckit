#!/bin/bash
set -e

# Custom Speckit을 로컬 PyPI 서버에 업로드하는 스크립트

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📦 Building Custom Speckit..."
uv build

echo ""
echo "📋 Built packages:"
ls -lh dist/

echo ""
echo "📤 Copying to local PyPI server..."
cp -v dist/*.whl dist/*.tar.gz .docker/packages/ 2>/dev/null || true

echo ""
echo "✅ Upload complete!"
echo ""
echo "📍 Local PyPI server: http://localhost:8080"
echo "📦 Package index: http://localhost:8080/simple/"
echo ""
echo "Usage in other projects:"
echo "  uvx --index-url http://localhost:8080/simple/ custom-speckit init"
echo ""

