"""cortex status - Show Cortex status and statistics."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer


def run(
    json_output: bool = False,
    project_root: Optional[Path] = None
):
    """Show Cortex status and statistics."""
    root = Path(project_root) if project_root else Path.cwd()
    root = root.resolve()

    # Import core modules
    import sys
    engine_root = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, engine_root)

    from core.config import Config
    from core.indexer import get_index_stats
    from core.memory import list_memories
    from core.chunker import get_stale_chunks

    cortex_path = Config.get_cortex_path(str(root))

    status = {
        'initialized': os.path.exists(cortex_path),
        'chunks': {'count': 0, 'domains': []},
        'memories': {'count': 0, 'by_type': {}, 'by_domain': {}},
        'indices': {},
        'stale': [],
        'last_updated': None
    }

    if status['initialized']:
        # Count chunks by domain
        chunks_path = Config.get_chunks_path(str(root))
        if os.path.exists(chunks_path):
            for domain in os.listdir(chunks_path):
                domain_path = os.path.join(chunks_path, domain)
                if os.path.isdir(domain_path):
                    count = len([f for f in os.listdir(domain_path) if f.endswith('.md')])
                    if count > 0:
                        status['chunks']['domains'].append({'name': domain, 'count': count})
                        status['chunks']['count'] += count

        # Check for stale chunks
        stale_chunks = get_stale_chunks(str(root))
        # Group by source_path
        stale_by_source = {}
        for chunk in stale_chunks:
            src = chunk['source_path']
            if src not in stale_by_source:
                stale_by_source[src] = {'count': 0, 'status': chunk['status']}
            stale_by_source[src]['count'] += 1

        status['stale'] = [
            {'source': src, 'count': info['count'], 'status': info['status']}
            for src, info in stale_by_source.items()
        ]

        # Count memories
        memories = list_memories(str(root))
        status['memories']['count'] = len(memories)

        for mem in memories:
            t = mem.type
            d = mem.domain
            status['memories']['by_type'][t] = status['memories']['by_type'].get(t, 0) + 1
            status['memories']['by_domain'][d] = status['memories']['by_domain'].get(d, 0) + 1

        # Get index stats
        status['indices'] = get_index_stats(str(root))

        # Find last updated time
        index_path = Config.get_index_path(str(root))
        if os.path.exists(index_path):
            for f in os.listdir(index_path):
                fp = os.path.join(index_path, f)
                mtime = os.path.getmtime(fp)
                if status['last_updated'] is None or mtime > status['last_updated']:
                    status['last_updated'] = mtime

        if status['last_updated']:
            status['last_updated'] = datetime.fromtimestamp(status['last_updated']).isoformat()

    if json_output:
        typer.echo(json.dumps(status, indent=2))
    else:
        typer.echo("Cortex Status")
        typer.echo("=============")
        typer.echo()

        if not status['initialized']:
            typer.secho("Status: NOT INITIALIZED", fg=typer.colors.RED)
            typer.echo()
            typer.echo("Run: python -m cli init")
            return

        typer.secho("Status: INITIALIZED", fg=typer.colors.GREEN)
        typer.echo()

        # Chunks
        typer.echo(f"Chunks: {status['chunks']['count']} total")
        for domain in status['chunks']['domains']:
            typer.echo(f"  - {domain['name']}: {domain['count']}")

        # Stale chunks warning
        if status['stale']:
            typer.echo()
            typer.secho("Stale Chunks:", fg=typer.colors.YELLOW)
            for stale in status['stale']:
                status_icon = "modified" if stale['status'] == 'modified' else "source deleted"
                typer.secho(f"  - {stale['source']} ({stale['count']} chunks, {status_icon})", fg=typer.colors.YELLOW)
            typer.echo()
            typer.echo("  Refresh with: python -m cli chunk --path <source> --refresh")
        typer.echo()

        # Memories
        typer.echo(f"Memories: {status['memories']['count']} total")
        if status['memories']['by_type']:
            typer.echo("  By type:")
            for t, count in status['memories']['by_type'].items():
                typer.echo(f"    - {t}: {count}")
        if status['memories']['by_domain']:
            typer.echo("  By domain:")
            for d, count in status['memories']['by_domain'].items():
                typer.echo(f"    - {d}: {count}")
        typer.echo()

        # Indices
        typer.echo("Indices:")
        if status['indices'].get('chunks'):
            size_kb = status['indices']['chunks']['size_bytes'] / 1024
            typer.echo(f"  - chunks: {status['indices']['chunks']['count']} vectors ({size_kb:.1f} KB)")
        else:
            typer.secho("  - chunks: NOT BUILT", fg=typer.colors.YELLOW)

        if status['indices'].get('memories'):
            size_kb = status['indices']['memories']['size_bytes'] / 1024
            typer.echo(f"  - memories: {status['indices']['memories']['count']} vectors ({size_kb:.1f} KB)")
        else:
            typer.secho("  - memories: NOT BUILT", fg=typer.colors.YELLOW)
        typer.echo()

        if status['last_updated']:
            typer.echo(f"Last updated: {status['last_updated']}")
