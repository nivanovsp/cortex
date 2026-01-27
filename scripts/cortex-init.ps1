#Requires -Version 5.1
<#
.SYNOPSIS
    Initialize Cortex in a project.

.DESCRIPTION
    Creates the .cortex/ directory structure and installs dependencies.

.PARAMETER Path
    Project root path. Defaults to current directory.

.EXAMPLE
    .\cortex-init.ps1
    .\cortex-init.ps1 -Path "D:\Projects\MyApp"
#>

param(
    [string]$Path = (Get-Location).Path
)

# DEPRECATION WARNING
Write-Host ""
Write-Host "WARNING: This PowerShell script is DEPRECATED." -ForegroundColor Yellow
Write-Host "Use the cross-platform Python CLI instead:" -ForegroundColor Yellow
Write-Host "  python -m cli init" -ForegroundColor Cyan
Write-Host ""
Write-Host "See scripts/README.md for migration guide." -ForegroundColor Gray
Write-Host ""

$ErrorActionPreference = "Stop"

Write-Host "Cortex Initialization" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# Check if already initialized
$cortexPath = Join-Path $Path ".cortex"
if (Test-Path $cortexPath) {
    Write-Host "Cortex already initialized at $cortexPath" -ForegroundColor Yellow
    exit 0
}

# Create directory structure
Write-Host "Creating directory structure..." -ForegroundColor Gray

$directories = @(
    ".cortex/chunks",
    ".cortex/memories",
    ".cortex/index",
    ".cortex/cache/embeddings"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $Path $dir
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    Write-Host "  Created: $dir" -ForegroundColor DarkGray
}

# Check Python
Write-Host ""
Write-Host "Checking Python..." -ForegroundColor Gray

try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor DarkGray
} catch {
    Write-Host "  Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Gray

$packages = @(
    "sentence-transformers",
    "numpy",
    "tiktoken"
)

foreach ($package in $packages) {
    Write-Host "  Installing: $package" -ForegroundColor DarkGray
    pip install $package --quiet 2>&1 | Out-Null
}

# Download embedding model (will happen on first use, but we can pre-warm)
Write-Host ""
Write-Host "Pre-downloading embedding model (e5-small-v2)..." -ForegroundColor Gray
Write-Host "  This may take a minute on first run (~130MB)" -ForegroundColor DarkGray

$pythonScript = @"
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('intfloat/e5-small-v2')
print('Model loaded successfully')
"@

python -c $pythonScript

Write-Host ""
Write-Host "Cortex initialized successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Chunk your documents:  cortex-chunk.ps1 -Path 'docs/'" -ForegroundColor White
Write-Host "  2. Build context frame:   cortex-assemble.ps1 -Task 'Your task'" -ForegroundColor White
Write-Host ""
