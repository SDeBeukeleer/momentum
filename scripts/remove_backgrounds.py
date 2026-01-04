#!/usr/bin/env python3
"""Remove backgrounds from all diorama images to make them transparent."""

from pathlib import Path
from rembg import remove
from PIL import Image
from tqdm import tqdm


INPUT_DIR = Path("public/diorama/v13-auto-anchor")
OUTPUT_DIR = Path("public/diorama/v13-auto-anchor-nobg")


def process_image(input_path: Path, output_path: Path) -> bool:
    """Remove background from a single image."""
    try:
        with Image.open(input_path) as img:
            # Remove background
            output = remove(img)
            # Save as PNG with transparency
            output.save(output_path, "PNG")
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def main():
    """Process all images."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get all PNG files
    input_files = sorted(INPUT_DIR.glob("day-*.png"))

    print(f"Found {len(input_files)} images to process")
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print()

    success_count = 0
    for input_path in tqdm(input_files, desc="Removing backgrounds"):
        output_path = OUTPUT_DIR / input_path.name

        # Skip if already processed
        if output_path.exists():
            success_count += 1
            continue

        if process_image(input_path, output_path):
            success_count += 1

    print()
    print(f"Done! Processed {success_count}/{len(input_files)} images")
    print(f"Transparent images saved to: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
