#Requires -Version 5.1
<#
.SYNOPSIS
    Build a context frame for a task.

.DESCRIPTION
    Retrieves relevant chunks and memories, assembles them into a
    position-optimized context frame for LLM consumption.

.PARAMETER Task
    Task description to build context for.

.PARAMETER Criteria
    Acceptance criteria (comma-separated).

.PARAMETER State
    Current state description.

.PARAMETER Instructions
    Custom instructions for the task.

.PARAMETER Budget
    Token budget for the context frame. Default: 15000

.PARAMETER Output
    Output file path. If not specified, outputs to console.

.EXAMPLE
    .\cortex-assemble.ps1 -Task "Implement token refresh"
    .\cortex-assemble.ps1 -Task "Add user settings page" -Budget 10000 -Output "context.md"
    .\cortex-assemble.ps1 -Task "Fix login bug" -Criteria "User can log in,Session persists" -State "Login page exists"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Task,

    [string]$Criteria,

    [string]$State,

    [string]$Instructions,

    [int]$Budget = 15000,

    [string]$Output
)

# DEPRECATION WARNING
Write-Host ""
Write-Host "WARNING: This PowerShell script is DEPRECATED." -ForegroundColor Yellow
Write-Host "Use the cross-platform Python CLI instead:" -ForegroundColor Yellow
Write-Host "  python -m cli assemble --task `"$Task`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "See scripts/README.md for migration guide." -ForegroundColor Gray
Write-Host ""

$ErrorActionPreference = "Stop"

Write-Host "Cortex Context Assembly" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Task:   $Task" -ForegroundColor Gray
Write-Host "Budget: $Budget tokens" -ForegroundColor Gray
if ($Output) {
    Write-Host "Output: $Output" -ForegroundColor Gray
}
Write-Host ""

# Get script directory and project root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Set PYTHONPATH to include project root
$env:PYTHONPATH = $projectRoot

# Escape strings for Python
function EscapePython($str) {
    if ($str) {
        return $str -replace "\\", "\\\\" -replace "'", "\\'" -replace "`n", "\\n" -replace "`r", ""
    }
    return ""
}

$escapedTask = EscapePython $Task
$escapedState = EscapePython $State
$escapedInstructions = EscapePython $Instructions

# Parse criteria
$criteriaArg = "None"
if ($Criteria) {
    $criteriaList = $Criteria -split "," | ForEach-Object { "'$(EscapePython $_.Trim())'" }
    $criteriaArg = "[" + ($criteriaList -join ", ") + "]"
}

# Build output arg
$outputArg = if ($Output) { "r'$Output'" } else { "None" }

# State and instructions args
$stateArg = if ($State) { "'$escapedState'" } else { "None" }
$instructionsArg = if ($Instructions) { "'$escapedInstructions'" } else { "None" }

# Write Python script to temp file
$tempScript = [System.IO.Path]::GetTempFileName() + ".py"

$pythonCode = @"
import sys
sys.path.insert(0, r'$projectRoot')
from core.assembler import assemble_and_render

markdown = assemble_and_render(
    task='$escapedTask',
    project_root=r'$projectRoot',
    acceptance_criteria=$criteriaArg,
    current_state=$stateArg,
    instructions=$instructionsArg,
    budget=$Budget,
    output_path=$outputArg
)

if $outputArg == None:
    print(markdown)
"@

$pythonCode | Out-File -FilePath $tempScript -Encoding utf8

try {
    python $tempScript
    $exitCode = $LASTEXITCODE
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}

if ($exitCode -eq 0) {
    if ($Output) {
        Write-Host ""
        Write-Host "Context frame assembled successfully!" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "Assembly failed!" -ForegroundColor Red
    exit 1
}
