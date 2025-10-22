"""File management utilities for copying and updating templates."""

import shutil
from pathlib import Path
from typing import List, Set
from datetime import datetime


def copy_directory(
    src: Path,
    dst: Path,
    skip_existing: bool = False,
) -> List[Path]:
    """
    Copy directory recursively.
    
    Args:
        src: Source directory
        dst: Destination directory
        skip_existing: If True, skip files that already exist
        
    Returns:
        List of copied file paths
    """
    copied_files = []
    
    for src_file in src.rglob("*"):
        if src_file.is_file():
            relative_path = src_file.relative_to(src)
            dst_file = dst / relative_path
            
            # Skip existing files if requested
            if skip_existing and dst_file.exists():
                continue
            
            # Create parent directory
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(src_file, dst_file)
            copied_files.append(dst_file)
    
    return copied_files


def sync_directory(
    src: Path,
    dst: Path,
    previous_files: Set[str] = None,
) -> tuple[List[Path], List[Path], List[Path]]:
    """
    Sync directory with template (add, update, remove).
    
    Args:
        src: Source directory (template)
        dst: Destination directory (project)
        previous_files: Set of previously installed file paths (relative to dst)
        
    Returns:
        Tuple of (added_files, updated_files, removed_files)
    """
    added = []
    updated = []
    removed = []
    
    # Get all files in template
    template_files = set()
    for src_file in src.rglob("*"):
        if src_file.is_file():
            relative_path = src_file.relative_to(src)
            template_files.add(str(relative_path))
    
    # Copy/update files from template
    for src_file in src.rglob("*"):
        if src_file.is_file():
            relative_path = src_file.relative_to(src)
            dst_file = dst / relative_path
            
            # Create parent directory
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            
            if dst_file.exists():
                # Check if file changed
                if src_file.read_bytes() != dst_file.read_bytes():
                    shutil.copy2(src_file, dst_file)
                    updated.append(dst_file)
            else:
                # New file
                shutil.copy2(src_file, dst_file)
                added.append(dst_file)
    
    # Remove files that were in previous version but not in current template
    if previous_files:
        for prev_file in previous_files:
            if prev_file not in template_files:
                file_path = dst / prev_file
                if file_path.exists():
                    file_path.unlink()
                    removed.append(file_path)
                    # Remove empty parent directories
                    try:
                        file_path.parent.rmdir()
                    except OSError:
                        pass  # Directory not empty
    
    return added, updated, removed


def backup_file(file_path: Path) -> Path:
    """Create a backup of a file with timestamp."""
    if not file_path.exists():
        return file_path
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
    shutil.copy2(file_path, backup_path)
    return backup_path


def backup_directory(directory: Path) -> Path:
    """Create a backup of an entire directory."""
    if not directory.exists():
        return directory
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = directory.parent / f"{directory.name}_backup_{timestamp}"
    shutil.copytree(directory, backup_path)
    return backup_path


def get_changed_files(src: Path, dst: Path) -> List[Path]:
    """Get list of files that would be changed during update."""
    changed = []
    
    for src_file in src.rglob("*"):
        if src_file.is_file():
            relative_path = src_file.relative_to(src)
            dst_file = dst / relative_path
            
            # Skip preserved files
            if should_preserve(str(relative_path)):
                continue
            
            # Check if file doesn't exist or is different
            if not dst_file.exists():
                changed.append(dst_file)
            elif src_file.read_bytes() != dst_file.read_bytes():
                changed.append(dst_file)
    
    return changed


def ensure_gitignore(project_root: Path) -> None:
    """Ensure .gitignore has Custom Speckit entries."""
    gitignore_path = project_root / ".gitignore"
    
    required_entries = [
        "# Custom Speckit - Temporary Files",
        ".specify/.deltas/",
        ".cursor/.agent-tools/",
    ]
    
    if not gitignore_path.exists():
        gitignore_path.write_text("\n".join(required_entries) + "\n")
        return
    
    content = gitignore_path.read_text()
    lines = content.splitlines()
    
    # Check if entries already exist
    has_deltas = any(".specify/.deltas/" in line for line in lines)
    has_agent_tools = any(".cursor/.agent-tools/" in line for line in lines)
    
    if not has_deltas or not has_agent_tools:
        # Add missing entries
        new_lines = lines.copy()
        if not has_deltas or not has_agent_tools:
            new_lines.append("")
            if not any("Custom Speckit" in line for line in lines):
                new_lines.append("# Custom Speckit - Temporary Files")
            if not has_deltas:
                new_lines.append(".specify/.deltas/")
            if not has_agent_tools:
                new_lines.append(".cursor/.agent-tools/")
        
        gitignore_path.write_text("\n".join(new_lines) + "\n")

