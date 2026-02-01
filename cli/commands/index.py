"""cortex index - Build or rebuild vector indices."""

from pathlib import Path
from typing import Optional

import typer


def run(project_root: Optional[Path] = None):
    """Build vector indices for chunks and memories."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.indexer import build_index

    typer.echo("Building indices...")

    # Build chunks index
    try:
        chunks_stats = build_index(str(root), "chunks")
        typer.echo(f"  chunks: {chunks_stats['count']} vectors indexed")
    except Exception as e:
        typer.echo(f"  chunks: skipped ({e})")

    # Build memories index
    try:
        memories_stats = build_index(str(root), "memories")
        typer.echo(f"  memories: {memories_stats['count']} vectors indexed")
    except Exception as e:
        typer.echo(f"  memories: skipped ({e})")

    typer.echo("Done.")
