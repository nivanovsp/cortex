"""cortex chunk - Chunk documents into semantic units."""

import os
from pathlib import Path
from typing import Optional

import typer


def run(
    path: Path,
    domain: Optional[str] = None,
    refresh: bool = False,
    project_root: Optional[Path] = None
):
    """Chunk a file or directory."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()
    target = Path(path).resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.chunker import (
        chunk_document,
        chunk_directory,
        get_chunks_by_source,
        delete_chunks
    )

    if not target.exists():
        typer.echo(f"Error: Path not found: {target}", err=True)
        raise typer.Exit(1)

    # Handle --refresh flag
    if refresh:
        if target.is_dir():
            # Find all .md files in directory and delete their chunks
            deleted_total = 0
            for dirpath, _, files in os.walk(str(target)):
                for f in files:
                    if f.endswith('.md'):
                        file_path = os.path.join(dirpath, f)
                        old_chunks = get_chunks_by_source(file_path, str(root))
                        if old_chunks:
                            deleted = delete_chunks(old_chunks, str(root))
                            deleted_total += deleted
            if deleted_total > 0:
                typer.echo(f"Deleted {deleted_total} old chunks")
        else:
            # Delete chunks from this specific file
            old_chunks = get_chunks_by_source(str(target), str(root))
            if old_chunks:
                deleted = delete_chunks(old_chunks, str(root))
                typer.echo(f"Deleted {deleted} old chunks from {target.name}")

    if target.is_dir():
        chunks = chunk_directory(str(target), str(root), domain)
    else:
        chunks = chunk_document(str(target), str(root), domain)

    typer.echo(f"Created {len(chunks)} chunks")

    if refresh:
        typer.echo("Note: Run 'python -m cli index' to rebuild indices")
