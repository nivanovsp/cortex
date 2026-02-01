"""cortex bootstrap - Chunk methodology resources into Cortex."""

import os
from pathlib import Path
from typing import Optional

import typer


def run(
    force: bool = False,
    project_root: Optional[Path] = None
):
    """Chunk agents/ directory into Cortex as METHODOLOGY domain."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.config import Config
    from core.chunker import chunk_document, get_chunks_by_source, delete_chunks

    cortex_path = Config.get_cortex_path(str(root))
    if not os.path.exists(cortex_path):
        typer.echo("Error: Cortex not initialized. Run 'python -m cli init' first.", err=True)
        raise typer.Exit(1)

    agents_path = root / "agents"
    if not agents_path.exists():
        typer.echo("Error: agents/ directory not found.", err=True)
        raise typer.Exit(1)

    domain = "METHODOLOGY"
    extensions = {".md", ".yaml", ".yml"}
    total_chunks = 0
    total_deleted = 0

    # Walk agents/ directory and chunk all relevant files
    for dirpath, _, files in os.walk(str(agents_path)):
        for filename in sorted(files):
            if Path(filename).suffix not in extensions:
                continue

            file_path = os.path.join(dirpath, filename)

            # If --force, delete old chunks from this source first
            if force:
                old_chunks = get_chunks_by_source(file_path, str(root))
                if old_chunks:
                    deleted = delete_chunks(old_chunks, str(root))
                    total_deleted += deleted

            chunks = chunk_document(file_path, str(root), domain)
            total_chunks += len(chunks)

    if total_deleted > 0:
        typer.echo(f"Deleted {total_deleted} old chunks")

    typer.echo(f"Bootstrapped {total_chunks} chunks from agents/ (domain: {domain})")
    typer.echo("Run 'python -m cli index' to rebuild indices")
