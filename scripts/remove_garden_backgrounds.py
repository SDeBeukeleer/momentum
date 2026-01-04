#!/usr/bin/env python3
"""Remove backgrounds from all Garden theme images."""

from pathlib import Path
from rembg import remove
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

INPUT_DIR = Path("public/diorama/garden-new")
OUTPUT_DIR = Path("public/diorama/garden-final")


def process_image(input_path: Path) -> tuple[str, bool]:
    """Remove background from a single image."""
    output_path = OUTPUT_DIR / input_path.name

    if output_path.exists():
        return (input_path.name, True)

    try:
        with Image.open(input_path) as img:
            output = remove(img)
            output.save(output_path, "PNG")
            return (input_path.name, True)
    except Exception as e:
        return (input_path.name, False)


def main():
    """Process all images."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    input_files = sorted(INPUT_DIR.glob("day-*.png"))

    if not input_files:
        print(f"No images found in {INPUT_DIR}")
        return

    print("=" * 60)
    print("REMOVING BACKGROUNDS FROM GARDEN IMAGES")
    print("=" * 60)
    print(f"Input: {INPUT_DIR.absolute()}")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print(f"Found {len(input_files)} images to process")
    print()

    success_count = 0

    # Process images (can be parallelized but rembg is memory heavy)
    for i, input_path in enumerate(input_files, 1):
        print(f"  [{i:3d}/{len(input_files)}] {input_path.name}...", end=" ", flush=True)
        name, success = process_image(input_path)
        if success:
            print("✓")
            success_count += 1
        else:
            print("✗")

    print()
    print("=" * 60)
    print(f"DONE! Processed {success_count}/{len(input_files)} images")
    print(f"Transparent images saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
