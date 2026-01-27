"""cortex assemble - Assemble a context frame for a task."""

from pathlib import Path
from typing import Optional

import typer


def run(
    task: str,
    budget: Optional[int] = None,
    output: Optional[Path] = None,
    project_root: Optional[Path] = None
):
    """Assemble context frame for a task."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    sys.path.insert(0, str(root))

    from core.assembler import assemble_and_render

    markdown = assemble_and_render(
        task=task,
        project_root=str(root),
        budget=budget,
        output_path=str(output) if output else None
    )

    if output:
        typer.echo(f"Context frame written to: {output}")
    else:
        typer.echo(markdown)
