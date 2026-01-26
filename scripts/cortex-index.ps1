#Requires -Version 5.1
<#
.SYNOPSIS
    Rebuild vector indices.

.DESCRIPTION
    Regenerates the chunk and memory indices from stored embeddings.

.PARAMETER Full
    Full rebuild (re-embed everything).

.EXAMPLE
    .\cortex-index.ps1
    .\cortex-index.ps1 -Full
#>

param(
    [switch]$Full
)

$ErrorActionPreference = "Stop"

Write-Host "Cortex Index Rebuild" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH to include project root
$env:PYTHONPATH = $projectRoot

$fullArg = if ($Full) { "True" } else { "False" }

# Write Python script to temp file to avoid quoting issues
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

$pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.indexer import build_index

print('Building chunks index...')
build_index(r'$projectRoot', 'chunks', full_rebuild=$fullArg)
print('')

print('Building memories index...')
build_index(r'$projectRoot', 'memories', full_rebuild=$fullArg)
"@

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    python $tempScript
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "Index rebuild complete!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Index rebuild failed!" -ForegroundColor Red
    exit 1
}
