$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & python prepare_results.py
    if ($LASTEXITCODE -ne 0) { throw 'Result preparation failed' }
    & pdflatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw 'Main first pass failed' }
    & bibtex main
    if ($LASTEXITCODE -ne 0) { throw 'Bibliography failed' }
    foreach ($pass in 1..2) {
        & pdflatex -interaction=nonstopmode -halt-on-error main.tex
        if ($LASTEXITCODE -ne 0) { throw 'Main build failed' }
    }
    & pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex
    if ($LASTEXITCODE -ne 0) { throw 'Supplement first pass failed' }
    & bibtex supplementary
    if ($LASTEXITCODE -ne 0) { throw 'Supplement bibliography failed' }
    foreach ($pass in 1..2) {
        & pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex
        if ($LASTEXITCODE -ne 0) { throw 'Supplement build failed' }
    }
} finally { Pop-Location }
