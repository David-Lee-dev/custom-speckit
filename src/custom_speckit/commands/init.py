"""Initialize Custom Speckit in a project."""

from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from custom_speckit import __version__
from custom_speckit.utils.version import (
    save_version_and_files,
)
from custom_speckit.utils.file_manager import (
    copy_directory,
    ensure_gitignore,
)

console = Console()


def init(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Project directory to initialize (defaults to current directory)",
    ),
):
    """Initialize Custom Speckit in your project.
    
    This command will:
    - Create .specify/ directory with scripts, templates, and memory
    - Create .cursor/ directory with commands and rules
    - Add necessary entries to .gitignore
    - Leave other project files untouched (package.json, Cargo.toml, etc.)
    """
    project_root = path.resolve()
    
    console.print(Panel.fit(
        f"[bold cyan]Custom Speckit Initialization[/bold cyan]\n"
        f"Project: [yellow]{project_root}[/yellow]\n"
        f"Version: [green]{__version__}[/green]",
        border_style="cyan"
    ))
    
    # Always overwrite - no warning needed
    
    # Get template directory
    template_dir = Path(__file__).parent.parent / "templates"
    
    if not template_dir.exists():
        console.print("[red]✗ Template directory not found. Installation may be corrupted.[/red]")
        raise typer.Exit(1)
    
    # Copy .specify directory
    console.print("\n[cyan]→[/cyan] Installing .specify/ directory...")
    specify_src = template_dir / ".specify"
    specify_dst = project_root / ".specify"
    
    if specify_src.exists():
        copied_specify = copy_directory(specify_src, specify_dst, skip_existing=False)
        console.print(f"[green]✓[/green] Installed {len(copied_specify)} files to .specify/")
    else:
        console.print("[red]✗ .specify template not found[/red]")
        raise typer.Exit(1)
    
    # Copy .cursor directory
    console.print("[cyan]→[/cyan] Installing .cursor/ directory...")
    cursor_src = template_dir / ".cursor"
    cursor_dst = project_root / ".cursor"
    
    if cursor_src.exists():
        copied_cursor = copy_directory(cursor_src, cursor_dst, skip_existing=False)
        console.print(f"[green]✓[/green] Installed {len(copied_cursor)} files to .cursor/")
    else:
        console.print("[red]✗ .cursor template not found[/red]")
        raise typer.Exit(1)
    
    # Make scripts executable
    console.print("[cyan]→[/cyan] Setting script permissions...")
    scripts_dir = project_root / ".specify" / "scripts" / "bash"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.sh"):
            script.chmod(0o755)
        console.print("[green]✓[/green] Made scripts executable")
    
    # Save version and file manifest
    save_version_and_files(project_root, __version__, copied_specify, copied_cursor)
    console.print(f"[green]✓[/green] Saved version {__version__}")
    
    # Update .gitignore
    console.print("[cyan]→[/cyan] Updating .gitignore...")
    ensure_gitignore(project_root)
    console.print("[green]✓[/green] Updated .gitignore")
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold green]✓ Custom Speckit initialized successfully![/bold green]\n")
    
    table = Table(show_header=False, box=None)
    table.add_row("[cyan]Installed:[/cyan]", f".specify/ ({len(copied_specify)} files)")
    table.add_row("", f".cursor/ ({len(copied_cursor)} files)")
    table.add_row("[cyan]Version:[/cyan]", f"{__version__}")
    table.add_row("[cyan]Status:[/cyan]", "[green]Ready to use[/green]")
    console.print(table)
    
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Edit [cyan].specify/memory/constitution.md[/cyan] to define your project principles")
    console.print("2. Open your project in [cyan]Cursor AI[/cyan] editor")
    console.print("3. Run [cyan]/speckit.specify[/cyan] to create your first specification")
    console.print("\n[dim]Tip: Run 'custom-speckit update' to update to the latest version[/dim]")

