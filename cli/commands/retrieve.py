"""cortex retrieve - Search for relevant chunks or memories."""

import json
from pathlib import Path
from typing import Optional

import typer


def run(
    query: str,
    top_k: int = 5,
    index_type: str = "both",
    project_root: Optional[Path] = None
):
    """Search for relevant context."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.retriever import retrieve

    results = retrieve(
        query,
        str(root),
        top_k=top_k,
        index_type=index_type,
        include_content=True
    )

    if not results:
        typer.echo("No results found.")
        return

    typer.echo(f"Found {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        score = result.get('score', 0)
        rid = result.get('id', 'unknown')
        content = result.get('content', '')[:200]

        typer.echo(f"{i}. [{rid}] (score: {score:.3f})")
        typer.echo(f"   {content}...")
        typer.echo()
