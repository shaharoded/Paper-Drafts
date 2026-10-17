"""Export the four editable JAMIA tables using Pandoc (no CSV conversion)."""
import json
import re
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
source = root / "jamia" / "results.tex"
# Pandoc misreads numeric cells with tabularx >{...} column declarations.
# Normalize only the column declarations before parsing; retain every cell.
text = source.read_text(encoding="utf-8")
text = re.sub(r"\\makecell\[[^]]*\]\{([^{}]*)\}",
              lambda match: match[1].replace(r"\\", "; "), text)
columns = iter(["ll", "lllllll"])
text = re.sub(r"\\begin\{tabularx\}\{\\textwidth\}\{.*?\n\}",
              lambda match: r"\begin{tabular}{" + next(columns) + "}",
              text, flags=re.S).replace(r"\end{tabularx}", r"\end{tabular}")
document = json.loads(subprocess.check_output(
    ["pandoc", "-f", "latex", "-t", "json"], input=text, encoding="utf-8"))
tables = [block for block in document["blocks"] if block["t"] == "Table"]
if len(tables) != 4:
    raise ValueError(f"Expected four main tables; found {len(tables)}")
destination = root / "jamia" / "submission"
destination.mkdir(exist_ok=True)
for number, table in enumerate(tables, 1):
    output = {"pandoc-api-version": document["pandoc-api-version"], "meta": {},
              "blocks": [{"t": "Header", "c": [1, ["", [], []],
                          [{"t": "Str", "c": f"Table {number}"}]]}, table]}
    subprocess.run(["pandoc", "-f", "json", "-t", "docx", "-o",
                    str(destination / f"Table{number}.docx")],
                   input=json.dumps(output), text=True, check=True)
print("Exported four editable Word tables, including captions.")
