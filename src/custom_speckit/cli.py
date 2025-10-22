"""Main CLI entry point for Custom Speckit."""

import typer
from rich.console import Console
from rich.panel import Panel
from custom_speckit.commands import init, update

app = typer.Typer(
    name="custom-speckit",
    help="AI-powered Spec-Driven Development toolkit",
    add_completion=False,
)
console = Console()

app.command()(init.init)
app.command()(update.update)


@app.command()
def version():
    """Show Custom Speckit version."""
    from custom_speckit import __version__
    console.print(f"[bold cyan]Custom Speckit[/bold cyan] version [bold]{__version__}[/bold]")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Custom Speckit - AI-powered Spec-Driven Development toolkit."""
    if ctx.invoked_subcommand is None:
        from custom_speckit import __version__
        console.print(Panel.fit(
            f"[bold cyan]Custom Speckit[/bold cyan]\n"
            f"Version: [bold green]{__version__}[/bold green]\n\n"
            f"AI-powered Spec-Driven Development toolkit\n\n"
            f"[dim]Commands:[/dim]\n"
            f"  • [cyan]init[/cyan]     - Initialize Custom Speckit in your project\n"
            f"  • [cyan]update[/cyan]   - Update Custom Speckit to latest version\n"
            f"  • [cyan]version[/cyan]  - Show version information\n\n"
            f"[dim]Usage:[/dim] [yellow]uvx custom-speckit <command>[/yellow]",
            border_style="cyan"
        ))


if __name__ == "__main__":
    app()

