#Requires -Version 5.1
<#
.SYNOPSIS
    Chunk documents into semantic units.

.DESCRIPTION
    Breaks markdown documents into ~500 token chunks with embeddings.

.PARAMETER Path
    Path to document or directory to chunk.

.PARAMETER Domain
    Optional domain override. If not provided, auto-detected from path.

.PARAMETER Force
    Re-chunk even if chunks already exist.

.EXAMPLE
    .\cortex-chunk.ps1 -Path "docs/auth.md"
    .\cortex-chunk.ps1 -Path "docs/" -Force
    .\cortex-chunk.ps1 -Path "docs/auth.md" -Domain "AUTH"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Path,

    [string]$Domain,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "Cortex Chunking" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host ""

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Resolve path
$targetPath = Resolve-Path $Path -ErrorAction Stop

Write-Host "Path: $targetPath" -ForegroundColor Gray
if ($Domain) {
    Write-Host "Domain: $Domain" -ForegroundColor Gray
}
Write-Host ""

# Set PYTHONPATH to include project root
$env:PYTHONPATH = $projectRoot

# Build Python command
$isDir = Test-Path $targetPath -PathType Container
$forceArg = if ($Force) { "True" } else { "False" }
$domainArg = if ($Domain) { "'$Domain'" } else { "None" }

# Write Python script to temp file to avoid quoting issues
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

if ($isDir) {
    $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.chunker import chunk_directory
chunk_directory(r'$targetPath', r'$projectRoot', domain=$domainArg, force=$forceArg)
"@
} else {
    $pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.chunker import chunk_document
chunk_document(r'$targetPath', r'$projectRoot', domain=$domainArg, force=$forceArg)
"@
}

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    python $tempScript
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "Chunking complete!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Chunking failed!" -ForegroundColor Red
    exit 1
}
