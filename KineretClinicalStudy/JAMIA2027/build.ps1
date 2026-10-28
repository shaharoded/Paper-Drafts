param(
    [ValidateSet('medrxiv', 'jamia')]
    [string]$Version = 'jamia'
)
$ErrorActionPreference = 'Stop'
$sourceDirectory = Join-Path $PSScriptRoot $Version
$buildDirectory = Join-Path $sourceDirectory 'build'
New-Item -ItemType Directory -Force -Path $buildDirectory | Out-Null
Push-Location $sourceDirectory
try {
    foreach ($document in @('main', 'supplementary')) {
        & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$document.tex"
        if ($LASTEXITCODE -ne 0) { throw "First LaTeX pass failed: $document" }
        & bibtex "build/$document"
        if ($LASTEXITCODE -ne 0) { throw "BibTeX failed: $document" }
        foreach ($pass in 1..2) {
            & pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$document.tex"
            if ($LASTEXITCODE -ne 0) { throw "LaTeX pass failed: $document" }
        }
    }
    if ($Version -eq 'jamia') {
        New-Item -ItemType Directory -Force -Path 'submission/figures' | Out-Null
        & python (Join-Path $PSScriptRoot 'export_tables.py')
        if ($LASTEXITCODE -ne 0) { throw 'Word table export failed (requires Pandoc and Python)' }
        & python (Join-Path $PSScriptRoot 'export_figures.py')
        if ($LASTEXITCODE -ne 0) { throw 'Figure export failed (requires Python and Pillow)' }
        foreach ($document in @('main', 'supplementary')) {
            Copy-Item -LiteralPath "build/$document.pdf" -Destination "submission/$document.pdf" -Force
        }
        # Supplementary code ZIP is retained locally; portal rejects archive uploads.

    }
} finally {
    Pop-Location
}
