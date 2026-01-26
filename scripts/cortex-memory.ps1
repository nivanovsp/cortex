#Requires -Version 5.1
<#
.SYNOPSIS
    Manage Cortex memories.

.DESCRIPTION
    Create, list, update, and query memories.

.PARAMETER Action
    Action to perform: add, list, query, update, delete, related

.PARAMETER Learning
    Memory learning content (for add action)

.PARAMETER Context
    Memory context (for add action)

.PARAMETER Type
    Memory type: factual, experiential, procedural (for add action)

.PARAMETER Domain
    Domain tag (for add action)

.PARAMETER Confidence
    Confidence level: high, medium, low (for add/update action)

.PARAMETER Id
    Memory ID (for update/delete/related actions)

.PARAMETER Query
    Query string (for query action)

.PARAMETER TopK
    Number of results for query/related (default: 5)

.PARAMETER Verified
    Mark memory as verified (for update action)

.EXAMPLE
    .\cortex-memory.ps1 -Action add -Learning "FormField required for PasswordInput" -Type experiential -Domain AUTH
    .\cortex-memory.ps1 -Action list
    .\cortex-memory.ps1 -Action list -Domain AUTH
    .\cortex-memory.ps1 -Action query -Query "form validation"
    .\cortex-memory.ps1 -Action update -Id "MEM-2026-01-26-001" -Confidence high -Verified
    .\cortex-memory.ps1 -Action delete -Id "MEM-2026-01-26-001"
    .\cortex-memory.ps1 -Action related -Id "MEM-2026-01-26-001"
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("add", "list", "query", "update", "delete", "related")]
    [string]$Action,

    [string]$Learning,

    [string]$Context = "",

    [ValidateSet("factual", "experiential", "procedural")]
    [string]$Type = "experiential",

    [string]$Domain = "GENERAL",

    [ValidateSet("high", "medium", "low")]
    [string]$Confidence = "medium",

    [string]$Id,

    [string]$Query,

    [int]$TopK = 5,

    [switch]$Verified
)

$ErrorActionPreference = "Stop"

Write-Host "Cortex Memory Management" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH to include project root
$env:PYTHONPATH = $projectRoot

# Write Python script to temp file to avoid quoting issues
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

# Escape strings for Python
function EscapePython($str) {
    if ($str) {
        return $str -replace "\\", "\\\\" -replace "'", "\\'" -replace "`n", "\\n" -replace "`r", ""
    }
    return ""
}

$escapedLearning = EscapePython $Learning
$escapedContext = EscapePython $Context
$escapedQuery = EscapePython $Query

switch ($Action) {
    "add" {
        if (-not $Learning) {
            Write-Host "Error: -Learning is required for add action" -ForegroundColor Red
            exit 1
        }
        Write-Host "Adding memory..." -ForegroundColor Gray
        Write-Host "  Type: $Type" -ForegroundColor DarkGray
        Write-Host "  Domain: $Domain" -ForegroundColor DarkGray
        Write-Host "  Confidence: $Confidence" -ForegroundColor DarkGray
        Write-Host ""

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.memory import create_memory

create_memory(
    learning='$escapedLearning',
    context='$escapedContext',
    memory_type='$Type',
    domain='$Domain',
    confidence='$Confidence',
    project_root=r'$projectRoot'
)
"@
    }

    "list" {
        Write-Host "Listing memories..." -ForegroundColor Gray
        if ($Domain -and $Domain -ne "GENERAL") {
            Write-Host "  Domain filter: $Domain" -ForegroundColor DarkGray
        }
        Write-Host ""

        $domainFilter = if ($Domain -and $Domain -ne "GENERAL") { "'$Domain'" } else { "None" }
        $typeFilter = "None"

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.memory import list_memories

memories = list_memories(
    project_root=r'$projectRoot',
    domain=$domainFilter,
    memory_type=$typeFilter
)

if not memories:
    print('No memories found.')
else:
    print(f'Found {len(memories)} memories:\n')
    for m in memories:
        verified = '[v]' if m.verified else '[ ]'
        print(f"{verified} {m.id} [{m.type}] ({m.confidence})")
        print(f"    Domain: {m.domain}")
        print(f"    Learning: {m.learning[:80]}{'...' if len(m.learning) > 80 else ''}")
        if m.keywords:
            print(f"    Keywords: {', '.join(m.keywords[:5])}")
        print()
"@
    }

    "query" {
        if (-not $Query) {
            Write-Host "Error: -Query is required for query action" -ForegroundColor Red
            exit 1
        }
        Write-Host "Querying memories..." -ForegroundColor Gray
        Write-Host "  Query: $Query" -ForegroundColor DarkGray
        Write-Host "  Top-K: $TopK" -ForegroundColor DarkGray
        Write-Host ""

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.retriever import retrieve

results = retrieve(
    query='$escapedQuery',
    project_root=r'$projectRoot',
    top_k=$TopK,
    index_type='memories'
)

if not results:
    print('No matching memories found.')
    print('Make sure you have:')
    print('  1. Created memories (cortex-memory.ps1 -Action add)')
    print('  2. Built the index (cortex-index.ps1)')
else:
    print(f'Found {len(results)} matching memories:\n')
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['id']} (score: {r['score']:.4f})")
        meta = r.get('metadata', {})
        if 'type' in meta:
            print(f"   Type: {meta['type']} | Confidence: {meta.get('confidence', 'unknown')}")
        if 'domain' in meta:
            print(f"   Domain: {meta['domain']}")
        print()
"@
    }

    "update" {
        if (-not $Id) {
            Write-Host "Error: -Id is required for update action" -ForegroundColor Red
            exit 1
        }
        Write-Host "Updating memory: $Id" -ForegroundColor Gray

        $updates = @()
        $updateArgs = ""

        if ($Confidence) {
            $updates += "Confidence: $Confidence"
            $updateArgs += ", confidence='$Confidence'"
        }
        if ($Verified) {
            $updates += "Verified: True"
            $updateArgs += ", verified=True"
        }

        if ($updates.Count -gt 0) {
            Write-Host "  Updates: $($updates -join ', ')" -ForegroundColor DarkGray
        }
        Write-Host ""

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.memory import update_memory

update_memory(
    memory_id='$Id',
    project_root=r'$projectRoot'$updateArgs
)
"@
    }

    "delete" {
        if (-not $Id) {
            Write-Host "Error: -Id is required for delete action" -ForegroundColor Red
            exit 1
        }
        Write-Host "Deleting memory: $Id" -ForegroundColor Gray
        Write-Host ""

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.memory import delete_memory

delete_memory(
    memory_id='$Id',
    project_root=r'$projectRoot'
)
"@
    }

    "related" {
        if (-not $Id) {
            Write-Host "Error: -Id is required for related action" -ForegroundColor Red
            exit 1
        }
        Write-Host "Finding memories related to: $Id" -ForegroundColor Gray
        Write-Host "  Top-K: $TopK" -ForegroundColor DarkGray
        Write-Host ""

        $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.memory import find_related_memories, get_memory

source = get_memory('$Id', r'$projectRoot')
if not source:
    print(f"Memory not found: $Id")
else:
    print(f"Source: {source.learning[:60]}...")
    print()

    related = find_related_memories('$Id', r'$projectRoot', top_k=$TopK)

    if not related:
        print('No related memories found.')
    else:
        print(f'Found {len(related)} related memories:\n')
        for m, score in related:
            print(f"  [{m.type}] {m.id} (similarity: {score:.4f})")
            print(f"      {m.learning[:60]}...")
            print()
"@
    }
}

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    python $tempScript
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "Operation failed!" -ForegroundColor Red
    exit 1
}
