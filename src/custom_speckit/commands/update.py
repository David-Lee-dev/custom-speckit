"""Update Custom Speckit in a project."""

from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from custom_speckit import __version__
from custom_speckit.utils.version import (
    is_custom_speckit_installed,
    get_installed_version,
    get_installed_files,
    save_version_and_files,
)
from custom_speckit.utils.file_manager import (
    sync_directory,
    backup_directory,
    ensure_gitignore,
)

console = Console()


def update(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Project directory to update (defaults to current directory)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be updated without making changes",
    ),
    skip_backup: bool = typer.Option(
        False,
        "--skip-backup",
        help="Skip creating backups (not recommended)",
    ),
):
    """Update Custom Speckit to the latest version.
    
    This command will:
    - Update .specify/scripts/, .specify/templates/
    - Update .cursor/commands/, .cursor/rules/
    - Preserve user files (.specify/memory/, .specify/specs/, .specify/features/)
    - Create backups before updating (unless --skip-backup)
    - Leave other project files untouched
    """
    project_root = path.resolve()
    
    console.print(Panel.fit(
        f"[bold cyan]Custom Speckit Update[/bold cyan]\n"
        f"Project: [yellow]{project_root}[/yellow]\n"
        f"Target Version: [green]{__version__}[/green]",
        border_style="cyan"
    ))
    
    # Check if installed
    if not is_custom_speckit_installed(project_root):
        console.print("[red]✗ Custom Speckit is not installed in this project.[/red]")
        console.print("[dim]Run 'custom-speckit init' first.[/dim]")
        raise typer.Exit(1)
    
    # Get current version
    current_version = get_installed_version(project_root)
    console.print(f"Current version: [yellow]{current_version or 'unknown'}[/yellow]")
    
    if current_version == __version__ and not dry_run:
        console.print("[green]✓ Already on the latest version![/green]")
        console.print("[dim]Files will be refreshed to ensure consistency.[/dim]")
    
    # Get template directory
    template_dir = Path(__file__).parent.parent / "templates"
    
    if not template_dir.exists():
        console.print("[red]✗ Template directory not found. Installation may be corrupted.[/red]")
        raise typer.Exit(1)
    
    # Get previous installed files
    previous_files = get_installed_files(project_root)
    
    # Analyze changes
    console.print("\n[cyan]→[/cyan] Analyzing changes...")
    
    specify_src = template_dir / ".specify"
    specify_dst = project_root / ".specify"
    cursor_src = template_dir / ".cursor"
    cursor_dst = project_root / ".cursor"
    
    # Get previous files for each directory
    previous_specify = {f.replace(".specify/", "") for f in previous_files if f.startswith(".specify/")}
    previous_cursor = {f.replace(".cursor/", "") for f in previous_files if f.startswith(".cursor/")}
    
    # Dry run mode - just show what would change
    if dry_run:
        spec_added, spec_updated, spec_removed = sync_directory(
            specify_src, specify_dst, previous_specify
        ) if specify_src.exists() else ([], [], [])
        
        cursor_added, cursor_updated, cursor_removed = sync_directory(
            cursor_src, cursor_dst, previous_cursor
        ) if cursor_src.exists() else ([], [], [])
        
        total_changes = len(spec_added) + len(spec_updated) + len(spec_removed) + \
                       len(cursor_added) + len(cursor_updated) + len(cursor_removed)
        
        if total_changes == 0:
            console.print("[green]✓ No changes detected. Everything is up to date![/green]")
            raise typer.Exit(0)
        
        console.print("\n[bold]Changes preview:[/bold]")
        
        if spec_added or cursor_added:
            console.print(f"\n[green]+ Added ({len(spec_added) + len(cursor_added)}):[/green]")
            for f in (spec_added + cursor_added)[:5]:
                console.print(f"  + {f.relative_to(project_root)}")
            if len(spec_added) + len(cursor_added) > 5:
                console.print(f"  ... and {len(spec_added) + len(cursor_added) - 5} more")
        
        if spec_updated or cursor_updated:
            console.print(f"\n[yellow]~ Updated ({len(spec_updated) + len(cursor_updated)}):[/yellow]")
            for f in (spec_updated + cursor_updated)[:5]:
                console.print(f"  ~ {f.relative_to(project_root)}")
            if len(spec_updated) + len(cursor_updated) > 5:
                console.print(f"  ... and {len(spec_updated) + len(cursor_updated) - 5} more")
        
        if spec_removed or cursor_removed:
            console.print(f"\n[red]- Removed ({len(spec_removed) + len(cursor_removed)}):[/red]")
            for f in (spec_removed + cursor_removed)[:5]:
                console.print(f"  - {f.relative_to(project_root)}")
            if len(spec_removed) + len(cursor_removed) > 5:
                console.print(f"  ... and {len(spec_removed) + len(cursor_removed) - 5} more")
        
        console.print("\n[dim]Note: Template files will be synced. User files (not in template) will be preserved.[/dim]")
        console.print("\n[yellow]--dry-run enabled. No changes made.[/yellow]")
        raise typer.Exit(0)
    
    # Create backups
    if not skip_backup:
        console.print("\n[cyan]→[/cyan] Creating backups...")
        backup_specify = backup_directory(specify_dst)
        backup_cursor = backup_directory(cursor_dst)
        console.print("[green]✓[/green] Backups created")
        console.print(f"  • {backup_specify.relative_to(project_root)}")
        console.print(f"  • {backup_cursor.relative_to(project_root)}")
    
    # Sync files
    console.print("\n[cyan]→[/cyan] Syncing files...")
    
    spec_added, spec_updated, spec_removed = sync_directory(
        specify_src, specify_dst, previous_specify
    )
    
    cursor_added, cursor_updated, cursor_removed = sync_directory(
        cursor_src, cursor_dst, previous_cursor
    )
    
    total_added = len(spec_added) + len(cursor_added)
    total_updated = len(spec_updated) + len(cursor_updated)
    total_removed = len(spec_removed) + len(cursor_removed)
    
    if total_added:
        console.print(f"[green]✓[/green] Added {total_added} files")
    if total_updated:
        console.print(f"[green]✓[/green] Updated {total_updated} files")
    if total_removed:
        console.print(f"[green]✓[/green] Removed {total_removed} files")
    
    # Make scripts executable
    console.print("[cyan]→[/cyan] Setting script permissions...")
    scripts_dir = project_root / ".specify" / "scripts" / "bash"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.sh"):
            script.chmod(0o755)
        console.print("[green]✓[/green] Made scripts executable")
    
    # Get all current files for manifest
    all_current_specify = list((project_root / ".specify").rglob("*"))
    all_current_specify = [f for f in all_current_specify if f.is_file()]
    
    all_current_cursor = list((project_root / ".cursor").rglob("*"))
    all_current_cursor = [f for f in all_current_cursor if f.is_file()]
    
    # Save version and file manifest
    save_version_and_files(project_root, __version__, all_current_specify, all_current_cursor)
    console.print(f"[green]✓[/green] Updated version to {__version__}")
    
    # Update .gitignore
    console.print("[cyan]→[/cyan] Checking .gitignore...")
    ensure_gitignore(project_root)
    console.print("[green]✓[/green] .gitignore is up to date")
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold green]✓ Custom Speckit updated successfully![/bold green]\n")
    
    table = Table(show_header=False, box=None)
    table.add_row("[cyan]Previous version:[/cyan]", current_version or "unknown")
    table.add_row("[cyan]Current version:[/cyan]", f"[green]{__version__}[/green]")
    if total_added:
        table.add_row("[cyan]Added:[/cyan]", f"{total_added} files")
    if total_updated:
        table.add_row("[cyan]Updated:[/cyan]", f"{total_updated} files")
    if total_removed:
        table.add_row("[cyan]Removed:[/cyan]", f"{total_removed} files")
    console.print(table)
    
    console.print("\n[dim]Template files synced. User files (not in template) preserved.[/dim]")

