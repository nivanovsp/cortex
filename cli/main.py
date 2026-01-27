"""
Cortex CLI - Main entry point.

Usage:
    python -m cli init
    python -m cli chunk --path "docs/"
    python -m cli index
    python -m cli retrieve --query "authentication"
    python -m cli assemble --task "implement login"
    python -m cli memory add --learning "..." --domain AUTH
    python -m cli extract --text "session learnings..."
    python -m cli status
"""

import typer
from typing import Optional
from pathlib import Path

app = typer.Typer(
    name="cortex",
    help="Cortex - LLM-Native Context Management",
    no_args_is_help=True,
)


@app.command()
def init(
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory (default: current directory)"
    )
):
    """Initialize Cortex in a project directory."""
    from cli.commands import init as init_cmd
    init_cmd.run(project_root)


@app.command()
def chunk(
    path: Path = typer.Option(
        ..., "--path", "-p",
        help="Path to file or directory to chunk"
    ),
    domain: Optional[str] = typer.Option(
        None, "--domain", "-d",
        help="Domain tag (auto-detected if not provided)"
    ),
    refresh: bool = typer.Option(
        False, "--refresh",
        help="Delete old chunks from this source and re-chunk"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Chunk documents into semantic units."""
    from cli.commands import chunk as chunk_cmd
    chunk_cmd.run(path, domain, refresh, project_root)


@app.command()
def index(
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Build or rebuild vector indices."""
    from cli.commands import index as index_cmd
    index_cmd.run(project_root)


@app.command()
def retrieve(
    query: str = typer.Option(
        ..., "--query", "-q",
        help="Search query"
    ),
    top_k: int = typer.Option(
        5, "--top-k", "-k",
        help="Number of results to return"
    ),
    index_type: str = typer.Option(
        "chunks", "--type", "-t",
        help="Index to search: chunks or memories"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Search for relevant chunks or memories."""
    from cli.commands import retrieve as retrieve_cmd
    retrieve_cmd.run(query, top_k, index_type, project_root)


@app.command()
def assemble(
    task: str = typer.Option(
        ..., "--task", "-t",
        help="Task description"
    ),
    budget: Optional[int] = typer.Option(
        None, "--budget", "-b",
        help="Token budget (default from config)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output file path"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Assemble a context frame for a task."""
    from cli.commands import assemble as assemble_cmd
    assemble_cmd.run(task, budget, output, project_root)


# Memory subcommands
memory_app = typer.Typer(help="Memory management commands")
app.add_typer(memory_app, name="memory")


@memory_app.command("add")
def memory_add(
    learning: str = typer.Option(
        ..., "--learning", "-l",
        help="The learning/insight to save"
    ),
    context: str = typer.Option(
        "", "--context", "-c",
        help="Additional context"
    ),
    domain: str = typer.Option(
        "GENERAL", "--domain", "-d",
        help="Domain tag (AUTH, UI, API, etc.)"
    ),
    memory_type: str = typer.Option(
        "experiential", "--type", "-t",
        help="Memory type: factual, experiential, procedural"
    ),
    confidence: str = typer.Option(
        "medium", "--confidence",
        help="Confidence level: high, medium, low"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Add a new memory."""
    from cli.commands import memory as memory_cmd
    memory_cmd.add(learning, context, domain, memory_type, confidence, project_root)


@memory_app.command("list")
def memory_list(
    domain: Optional[str] = typer.Option(
        None, "--domain", "-d",
        help="Filter by domain"
    ),
    memory_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Filter by type"
    ),
    json_output: bool = typer.Option(
        False, "--json",
        help="Output as JSON"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """List memories."""
    from cli.commands import memory as memory_cmd
    memory_cmd.list_memories(domain, memory_type, json_output, project_root)


@memory_app.command("delete")
def memory_delete(
    memory_id: str = typer.Argument(
        ..., help="Memory ID to delete"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Delete a memory."""
    from cli.commands import memory as memory_cmd
    memory_cmd.delete(memory_id, project_root)


@app.command()
def extract(
    text: str = typer.Option(
        ..., "--text", "-t",
        help="Session text to extract learnings from"
    ),
    auto_save: bool = typer.Option(
        False, "--auto-save",
        help="Automatically save all extracted memories"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Extract learnings from session text."""
    from cli.commands import extract as extract_cmd
    extract_cmd.run(text, auto_save, project_root)


@app.command()
def status(
    json_output: bool = typer.Option(
        False, "--json",
        help="Output as JSON"
    ),
    project_root: Optional[Path] = typer.Option(
        None, "--root", "-r",
        help="Project root directory"
    )
):
    """Show Cortex status and statistics."""
    from cli.commands import status as status_cmd
    status_cmd.run(json_output, project_root)


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
