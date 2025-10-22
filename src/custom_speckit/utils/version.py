"""Version management utilities."""

import json
from pathlib import Path
from typing import Optional, Set, List


VERSION_FILE = ".specify/VERSION"
MANIFEST_FILE = ".specify/.manifest.json"


def get_installed_version(project_root: Path) -> Optional[str]:
    """Get the currently installed Custom Speckit version in the project."""
    version_file = project_root / VERSION_FILE
    if version_file.exists():
        content = version_file.read_text().strip()
        # Handle old format (just version string) and new format (JSON)
        if content.startswith("{"):
            try:
                data = json.loads(content)
                return data.get("version")
            except json.JSONDecodeError:
                return content
        return content
    return None


def get_installed_files(project_root: Path) -> Set[str]:
    """Get the list of files that were installed in the previous version."""
    manifest_file = project_root / MANIFEST_FILE
    if manifest_file.exists():
        try:
            data = json.loads(manifest_file.read_text())
            return set(data.get("files", []))
        except json.JSONDecodeError:
            pass
    return set()


def save_version_and_files(
    project_root: Path,
    version: str,
    specify_files: List[Path],
    cursor_files: List[Path],
) -> None:
    """Save the Custom Speckit version and installed file list."""
    # Save version
    version_file = project_root / VERSION_FILE
    version_file.parent.mkdir(parents=True, exist_ok=True)
    version_file.write_text(f"{version}\n")
    
    # Save manifest with file list
    specify_root = project_root / ".specify"
    cursor_root = project_root / ".cursor"
    
    file_list = []
    for file_path in specify_files:
        relative = file_path.relative_to(specify_root)
        file_list.append(f".specify/{relative}")
    for file_path in cursor_files:
        relative = file_path.relative_to(cursor_root)
        file_list.append(f".cursor/{relative}")
    
    manifest_file = project_root / MANIFEST_FILE
    manifest_data = {
        "version": version,
        "files": sorted(file_list),
    }
    manifest_file.write_text(json.dumps(manifest_data, indent=2))


def save_version(project_root: Path, version: str) -> None:
    """Save the Custom Speckit version to the project (legacy method)."""
    version_file = project_root / VERSION_FILE
    version_file.parent.mkdir(parents=True, exist_ok=True)
    version_file.write_text(f"{version}\n")


def is_custom_speckit_installed(project_root: Path) -> bool:
    """Check if Custom Speckit is already installed in the project."""
    specify_dir = project_root / ".specify"
    cursor_dir = project_root / ".cursor"
    return specify_dir.exists() and cursor_dir.exists()

