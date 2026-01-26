#Requires -Version 5.1
<#
.SYNOPSIS
    Test chunk/memory retrieval.

.DESCRIPTION
    Query the index and show top-k results for debugging.

.PARAMETER Query
    The query string to search for.

.PARAMETER TopK
    Number of results to return. Default: 10

.PARAMETER Type
    What to search: chunks, memories, or both. Default: both

.PARAMETER Content
    Include full content in results.

.EXAMPLE
    .\cortex-retrieve.ps1 -Query "token refresh authentication"
    .\cortex-retrieve.ps1 -Query "form validation" -TopK 5 -Type chunks
    .\cortex-retrieve.ps1 -Query "error handling" -Content
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,

    [int]$TopK = 10,

    [ValidateSet("chunks", "memories", "both")]
    [string]$Type = "both",

    [switch]$Content
)

$ErrorActionPreference = "Stop"

Write-Host "Cortex Retrieval" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Query: $Query" -ForegroundColor Gray
Write-Host "Top-K: $TopK" -ForegroundColor Gray
Write-Host "Type:  $Type" -ForegroundColor Gray
Write-Host ""

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH to include project root
$env:PYTHONPATH = $projectRoot

$contentArg = if ($Content) { "True" } else { "False" }

# Escape query for Python (replace backslashes and quotes)
$escapedQuery = $Query -replace "\\", "\\\\" -replace "'", "\\'"

# Write Python script to temp file to avoid quoting issues
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

$pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.retriever import retrieve

results = retrieve(
    query='$escapedQuery',
    project_root=r'$projectRoot',
    top_k=$TopK,
    index_type='$Type',
    include_content=$contentArg
)

if not results:
    print('No results found. Make sure you have:')
    print('  1. Chunked documents (cortex-chunk.ps1)')
    print('  2. Built the index (cortex-index.ps1)')
else:
    print(f'Found {len(results)} results:\n')
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['id']} (score: {r['score']:.4f})")
        print(f"   Semantic: {r['semantic_score']:.4f} | Keywords: {r['keyword_score']:.4f}")
        meta = r.get('metadata', {})
        if 'source_section' in meta:
            print(f"   Section: {meta['source_section']}")
        if 'keywords' in meta:
            kw = meta['keywords'][:5]
            print(f"   Keywords: {', '.join(kw)}")
        if $contentArg and 'content' in r:
            content = r['content'][:200] + '...' if len(r.get('content', '')) > 200 else r.get('content', '')
            print(f"   Content: {content}")
        print()
"@

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    python $tempScript
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "Retrieval failed!" -ForegroundColor Red
    exit 1
}
