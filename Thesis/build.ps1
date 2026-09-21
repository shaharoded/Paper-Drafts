# Build the thesis end to end: pdflatex -> bibtex -> pdflatex x2.
# Usage:  .\build.ps1
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"

pdflatex -interaction=nonstopmode main.tex | Out-Null
bibtex main | Out-Null
pdflatex -interaction=nonstopmode main.tex | Out-Null
pdflatex -interaction=nonstopmode main.tex | Out-Null

$errs = (Select-String -Path main.log -Pattern '^!' ).Count
$undef = (Select-String -Path main.log -Pattern 'Warning:.*(Reference|Citation).*undefined').Count
$pages = (Select-String -Path main.log -Pattern 'Output written on main.pdf \((\d+) pages').Matches.Groups[1].Value

Write-Host ""
Write-Host "  pages            : $pages"
Write-Host "  errors           : $errs"
Write-Host "  undefined refs   : $undef"
if ($errs -eq 0 -and $undef -eq 0) { Write-Host "  clean build" -ForegroundColor Green }
else { Write-Host "  see main.log" -ForegroundColor Yellow }
