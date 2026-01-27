#Requires -Version 5.1
<#
.SYNOPSIS
    Show Cortex status and statistics.

.DESCRIPTION
    Displays chunk count, memory count, index stats, and system health.
    Useful for quick status checks in Claude Code sessions.

.PARAMETER Json
    Output as JSON for programmatic use.

.EXAMPLE
    .\cortex-status.ps1
    .\cortex-status.ps1 -Json
#>

param(
    [switch]$Json
)

# DEPRECATION WARNING (only show for non-JSON output)
if (-not $Json) {
    Write-Host ""
    Write-Host "WARNING: This PowerShell script is DEPRECATED." -ForegroundColor Yellow
    Write-Host "Use the cross-platform Python CLI instead:" -ForegroundColor Yellow
    Write-Host "  python -m cli status" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "See scripts/README.md for migration guide." -ForegroundColor Gray
    Write-Host ""
}

$ErrorActionPreference = "Stop"

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH
$env:PYTHONPATH = $projectRoot

# Write Python script to temp file
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

$pythonCode = @"
import sys
import os
import json
from datetime import datetime
sys.path.insert(0, r'$projectRoot')
from core.config import Config
from core.indexer import get_index_stats

project_root = r'$projectRoot'
cortex_path = Config.get_cortex_path(project_root)

status = {
    'initialized': os.path.exists(cortex_path),
    'chunks': {'count': 0, 'domains': []},
    'memories': {'count': 0, 'by_type': {}, 'by_domain': {}},
    'indices': {},
    'last_updated': None
}

if status['initialized']:
    # Count chunks by domain
    chunks_path = Config.get_chunks_path(project_root)
    if os.path.exists(chunks_path):
        for domain in os.listdir(chunks_path):
            domain_path = os.path.join(chunks_path, domain)
            if os.path.isdir(domain_path):
                count = len([f for f in os.listdir(domain_path) if f.endswith('.md')])
                if count > 0:
                    status['chunks']['domains'].append({'name': domain, 'count': count})
                    status['chunks']['count'] += count

    # Count memories
    memories_path = os.path.join(cortex_path, Config.MEMORIES_DIR)
    if os.path.exists(memories_path):
        from core.memory import list_memories
        memories = list_memories(project_root)
        status['memories']['count'] = len(memories)

        # Group by type and domain
        for mem in memories:
            t = mem.type
            d = mem.domain
            status['memories']['by_type'][t] = status['memories']['by_type'].get(t, 0) + 1
            status['memories']['by_domain'][d] = status['memories']['by_domain'].get(d, 0) + 1

    # Get index stats
    status['indices'] = get_index_stats(project_root)

    # Find last updated time
    index_path = Config.get_index_path(project_root)
    if os.path.exists(index_path):
        for f in os.listdir(index_path):
            fp = os.path.join(index_path, f)
            mtime = os.path.getmtime(fp)
            if status['last_updated'] is None or mtime > status['last_updated']:
                status['last_updated'] = mtime

    if status['last_updated']:
        status['last_updated'] = datetime.fromtimestamp(status['last_updated']).isoformat()

print(json.dumps(status))
"@

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    $result = python $tempScript 2>$null
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        if ($Json) {
            Write-Output '{"error": "Failed to get status"}'
        } else {
            Write-Host "Failed to get Cortex status" -ForegroundColor Red
        }
        exit 1
    }

    $status = $result | ConvertFrom-Json

    if ($Json) {
        Write-Output $result
    } else {
        Write-Host "Cortex Status" -ForegroundColor Cyan
        Write-Host "=============" -ForegroundColor Cyan
        Write-Host ""

        if (-not $status.initialized) {
            Write-Host "Status: NOT INITIALIZED" -ForegroundColor Red
            Write-Host ""
            Write-Host "Run: .\cortex-init.ps1 to initialize Cortex" -ForegroundColor Yellow
            exit 0
        }

        Write-Host "Status: INITIALIZED" -ForegroundColor Green
        Write-Host ""

        # Chunks
        Write-Host "Chunks: $($status.chunks.count) total" -ForegroundColor White
        if ($status.chunks.domains) {
            foreach ($domain in $status.chunks.domains) {
                Write-Host "  - $($domain.name): $($domain.count)" -ForegroundColor Gray
            }
        }
        Write-Host ""

        # Memories
        Write-Host "Memories: $($status.memories.count) total" -ForegroundColor White
        if ($status.memories.by_type.PSObject.Properties.Count -gt 0) {
            Write-Host "  By type:" -ForegroundColor Gray
            foreach ($prop in $status.memories.by_type.PSObject.Properties) {
                Write-Host "    - $($prop.Name): $($prop.Value)" -ForegroundColor Gray
            }
        }
        if ($status.memories.by_domain.PSObject.Properties.Count -gt 0) {
            Write-Host "  By domain:" -ForegroundColor Gray
            foreach ($prop in $status.memories.by_domain.PSObject.Properties) {
                Write-Host "    - $($prop.Name): $($prop.Value)" -ForegroundColor Gray
            }
        }
        Write-Host ""

        # Indices
        Write-Host "Indices:" -ForegroundColor White
        if ($status.indices.chunks) {
            $size = [math]::Round($status.indices.chunks.size_bytes / 1024, 1)
            Write-Host "  - chunks: $($status.indices.chunks.count) vectors ($($size) KB)" -ForegroundColor Gray
        } else {
            Write-Host "  - chunks: NOT BUILT" -ForegroundColor Yellow
        }
        if ($status.indices.memories) {
            $size = [math]::Round($status.indices.memories.size_bytes / 1024, 1)
            Write-Host "  - memories: $($status.indices.memories.count) vectors ($($size) KB)" -ForegroundColor Gray
        } else {
            Write-Host "  - memories: NOT BUILT" -ForegroundColor Yellow
        }
        Write-Host ""

        # Last updated
        if ($status.last_updated) {
            Write-Host "Last updated: $($status.last_updated)" -ForegroundColor Gray
        }
    }

} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}
