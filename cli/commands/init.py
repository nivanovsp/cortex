"""cortex init - Initialize Cortex in a project."""

import os
from pathlib import Path
from typing import Optional

import typer


def run(project_root: Optional[Path] = None):
    """Initialize Cortex directory structure."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.config import Config

    cortex_path = Config.get_cortex_path(str(root))

    if os.path.exists(cortex_path):
        typer.echo(f"Cortex already initialized at: {cortex_path}")
        return

    # Create directory structure
    os.makedirs(Config.get_chunks_path(str(root)), exist_ok=True)
    os.makedirs(Config.get_index_path(str(root)), exist_ok=True)
    os.makedirs(os.path.join(cortex_path, Config.MEMORIES_DIR), exist_ok=True)

    typer.echo(f"Initialized Cortex at: {cortex_path}")
    typer.echo("  Created: chunks/")
    typer.echo("  Created: index/")
    typer.echo("  Created: memories/")
