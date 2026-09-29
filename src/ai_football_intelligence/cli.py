from __future__ import annotations
import typer
from ai_football_intelligence.orchestrator import run_research_and_review

app = typer.Typer()
app = typer.Typer(no_args_is_help=True)

@app.command()
def version():
    """Show a placeholder version command (keeps CLI in multi-command mode)."""
    typer.echo("ai-football-intelligence v0.1")

@app.command()
def research(
    goal: str = typer.Argument(..., help="Research goal / search query"),
    max_results: int = typer.Option(5, help="Max papers to fetch"),
):
    """Search, save, enrich, and review papers for a research goal."""
    report = run_research_and_review(goal, max_results=max_results)

    typer.echo(f"Goal: {report.goal}")
    typer.echo(f"Found: {report.papers_found}")
    typer.echo(f"Passed review: {report.papers_passed_review}")
    typer.echo(f"Failed review: {report.papers_failed_review}")

    if report.failures:
        typer.echo("\nFailures:")
        for f in report.failures:
            typer.echo(f"  - {f}")


if __name__ == "__main__":
    app()