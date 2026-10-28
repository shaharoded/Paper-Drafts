"""Upscale existing manuscript figures with Lanczos; preserve source PNGs."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
source = root / "jamia" / "figures"
destination = root / "jamia" / "submission" / "figures"
destination.mkdir(parents=True, exist_ok=True)
names = ["adherence_trend", "adherence_mortality",
         "death_feature_importance", "recurring_guideline_components"]
for number, name in enumerate(names, 1):
    with Image.open(source / f"{name}.png") as original:
        size = (original.width * 4, original.height * 4)
        enlarged = original.resize(size, Image.Resampling.LANCZOS)
        output = destination / f"Figure{number}.png"
        enlarged.save(output, dpi=(600, 600), optimize=True)
        with Image.open(output) as check:
            assert check.size == size
            assert all(abs(value - 600) < 1 for value in check.info["dpi"])
        print(f"Figure {number}: {original.width} x {original.height} -> {size[0]} x {size[1]}; 600 DPI")
