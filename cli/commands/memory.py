"""cortex memory - Memory management commands."""

import json
from pathlib import Path
from typing import Optional

import typer


def add(
    learning: str,
    context: str = "",
    domain: str = "GENERAL",
    memory_type: str = "experiential",
    confidence: str = "medium",
    project_root: Optional[Path] = None
):
    """Add a new memory."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    sys.path.insert(0, str(root))

    from core.memory import create_memory

    memory = create_memory(
        learning=learning,
        context=context,
        memory_type=memory_type,
        domain=domain,
        confidence=confidence,
        project_root=str(root)
    )

    typer.echo(f"Created memory: {memory.id}")


def list_memories(
    domain: Optional[str] = None,
    memory_type: Optional[str] = None,
    json_output: bool = False,
    project_root: Optional[Path] = None
):
    """List memories."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    sys.path.insert(0, str(root))

    from core.memory import list_memories as core_list_memories

    memories = core_list_memories(
        project_root=str(root),
        domain=domain,
        memory_type=memory_type
    )

    if json_output:
        output = [
            {
                "id": m.id,
                "type": m.type,
                "domain": m.domain,
                "confidence": m.confidence,
                "learning": m.learning,
                "created": m.created
            }
            for m in memories
        ]
        typer.echo(json.dumps(output, indent=2))
    else:
        if not memories:
            typer.echo("No memories found.")
            return

        for m in memories:
            typer.echo(f"{m.id} [{m.type}] ({m.confidence})")
            typer.echo(f"  Domain: {m.domain}")
            typer.echo(f"  {m.learning[:80]}...")
            typer.echo()


def delete(
    memory_id: str,
    project_root: Optional[Path] = None
):
    """Delete a memory."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    sys.path.insert(0, str(root))

    from core.memory import delete_memory

    if delete_memory(memory_id, str(root)):
        typer.echo(f"Deleted memory: {memory_id}")
    else:
        typer.echo(f"Memory not found: {memory_id}", err=True)
        raise typer.Exit(1)
