#Requires -Version 5.1
<#
.SYNOPSIS
    Extract memories from session text.

.DESCRIPTION
    Analyzes text for potential learnings and proposes memories.
    Use at session end to capture insights.

.PARAMETER Text
    Text to analyze for memories.

.PARAMETER File
    File containing text to analyze.

.PARAMETER MinConfidence
    Minimum confidence threshold: high, medium, low. Default: medium

.PARAMETER AutoSave
    Automatically save high-confidence memories without prompting.

.PARAMETER Session
    Session identifier for tracking.

.EXAMPLE
    .\cortex-extract.ps1 -Text "Fixed the bug by adding a null check."
    .\cortex-extract.ps1 -File "session-log.txt" -MinConfidence high
    .\cortex-extract.ps1 -Text "Found that FormField is required." -AutoSave
#>

param(
    [string]$Text,

    [string]$File,

    [ValidateSet("high", "medium", "low")]
    [string]$MinConfidence = "medium",

    [switch]$AutoSave,

    [string]$Session
)

$ErrorActionPreference = "Stop"

Write-Host "Cortex Memory Extraction" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Validate input
if (-not $Text -and -not $File) {
    Write-Host "Error: Provide either -Text or -File parameter" -ForegroundColor Red
    exit 1
}

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH
$env:PYTHONPATH = $projectRoot

# Read file if provided
if ($File) {
    if (-not (Test-Path $File)) {
        Write-Host "Error: File not found: $File" -ForegroundColor Red
        exit 1
    }
    $Text = Get-Content $File -Raw
    Write-Host "Analyzing file: $File" -ForegroundColor Gray
} else {
    Write-Host "Analyzing provided text..." -ForegroundColor Gray
}
Write-Host "Min confidence: $MinConfidence" -ForegroundColor Gray
Write-Host ""

# Escape text for Python
$escapedText = $Text -replace "\\", "\\\\" -replace "'", "\\'" -replace "`n", "\\n" -replace "`r", ""
$sessionArg = if ($Session) { "'$Session'" } else { "None" }

# Write Python script to temp file
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

$pythonCode = @"
import sys
import json
sys.path.insert(0, r'$projectRoot')
from core.extractor import extract_memories, save_proposed_memories

text = '''$escapedText'''
proposed = extract_memories(text, min_confidence='$MinConfidence')

if not proposed:
    print('No potential memories detected.')
    print(json.dumps({'count': 0, 'memories': []}))
else:
    # Output as JSON for PowerShell to parse
    output = {
        'count': len(proposed),
        'memories': []
    }
    for i, mem in enumerate(proposed, 1):
        output['memories'].append({
            'index': i,
            'learning': mem.learning,
            'context': mem.context[:100] if mem.context else '',
            'type': mem.memory_type,
            'confidence': mem.confidence,
            'domain': mem.domain,
            'trigger': mem.trigger
        })
    print(json.dumps(output))
"@

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    $result = python $tempScript 2>$null | Select-Object -Last 1
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0 -or -not $result) {
        Write-Host "Extraction failed or no output" -ForegroundColor Red
        exit 1
    }

    $data = $result | ConvertFrom-Json

    if ($data.count -eq 0) {
        Write-Host "No potential memories detected in the text." -ForegroundColor Yellow
        exit 0
    }

    Write-Host "Found $($data.count) potential memories:" -ForegroundColor Green
    Write-Host ""

    foreach ($mem in $data.memories) {
        $confIcon = switch ($mem.confidence) {
            'high' { '[H]' }
            'medium' { '[M]' }
            'low' { '[L]' }
        }
        $typeIcon = switch ($mem.type) {
            'factual' { 'F' }
            'experiential' { 'E' }
            'procedural' { 'P' }
        }

        Write-Host "$($mem.index). $confIcon [$typeIcon] $($mem.domain)" -ForegroundColor White
        Write-Host "   Learning: $($mem.learning)" -ForegroundColor Gray
        if ($mem.context) {
            Write-Host "   Context: $($mem.context)..." -ForegroundColor DarkGray
        }
        Write-Host ""
    }

    # Auto-save high confidence or prompt
    if ($AutoSave) {
        $highConf = $data.memories | Where-Object { $_.confidence -eq 'high' }
        if ($highConf) {
            Write-Host "Auto-saving $($highConf.Count) high-confidence memories..." -ForegroundColor Cyan

            $indices = ($highConf | ForEach-Object { $_.index }) -join ','

            $saveScript = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.extractor import extract_memories, save_proposed_memories

text = '''$escapedText'''
proposed = extract_memories(text, min_confidence='$MinConfidence')
indices = [$indices]
saved = save_proposed_memories(proposed, indices, r'$projectRoot', $sessionArg)
for mem_id in saved:
    print(f'Saved: {mem_id}')
"@
            $saveScript | Out-File -FilePath $tempScript -Encoding utf8
            python $tempScript
        } else {
            Write-Host "No high-confidence memories to auto-save." -ForegroundColor Yellow
        }
    } else {
        Write-Host "To save memories, run:" -ForegroundColor Cyan
        Write-Host "  cortex-memory.ps1 -Action add -Learning `"<learning>`" -Type <type> -Domain <domain>" -ForegroundColor White
        Write-Host ""
        Write-Host "Or use -AutoSave to automatically save high-confidence memories." -ForegroundColor Gray
    }

} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}
