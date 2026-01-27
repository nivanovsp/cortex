"""cortex extract - Extract learnings from session text."""

import json
from pathlib import Path
from typing import Optional

import typer


def run(
    text: str,
    auto_save: bool = False,
    project_root: Optional[Path] = None
):
    """Extract learnings from session text."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    sys.path.insert(0, str(root))

    from core.extractor import extract_and_format, save_proposed_memories

    result = extract_and_format(text, str(root))

    typer.echo("Extracted Learnings:")
    typer.echo("=" * 40)
    typer.echo()

    memories = result.get('memories', [])

    if not memories:
        typer.echo("No learnings extracted.")
        return

    for i, mem in enumerate(memories, 1):
        typer.echo(f"{i}. [{mem.get('domain', 'GENERAL')}] ({mem.get('confidence', 'medium')})")
        typer.echo(f"   Type: {mem.get('type', 'experiential')}")
        typer.echo(f"   Learning: {mem.get('learning', '')}")
        typer.echo()

    if auto_save:
        saved = save_proposed_memories(memories, str(root))
        typer.echo(f"Saved {len(saved)} memories.")
    else:
        typer.echo("Use --auto-save to save these memories, or save selectively via 'cortex memory add'")
