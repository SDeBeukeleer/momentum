#!/usr/bin/env python3
"""
V3: Generate consistent images using ORIGINAL base as reference for ALL images.
This prevents quality degradation and platform drift.
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v3-blue")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Highly detailed base platform description
BASE_STYLE = """
STYLE: Claymation stop-motion style, highly detailed clay textures, miniature diorama aesthetic.
Professional studio photography lighting, sharp focus, high detail.

CAMERA: Isometric 3D view from above at 45 degree angle.

BACKGROUND: Solid bright blue chroma key background (#0000FF), pure flat blue, no gradients.

PLATFORM SPECIFICATION (MUST BE EXACTLY THIS):
- Square floating earth platform, 15cm x 15cm
- Rounded organic edges like a chunk of earth cut from the ground
- Platform height about 5cm
- Light tan/beige raised rim around top edge (like a ceramic pot rim)

SOIL LAYERS (visible on all sides):
- Top layer: Dark rich brown soil (2cm thick)
- Middle layer: Reddish-brown clay with small pebbles embedded (2cm)
- Bottom layer: Dark brown/black soil (1cm)
- Thin roots poking out from sides

TOP SURFACE ELEMENTS (FIXED - same every image):
- 4 moss patches in corners: bright green, fluffy texture
- Blue pebble near top-left moss
- Orange pebble near right moss
- Yellow pebble near bottom moss
- Rich brown soil texture in center

NO pink, magenta, or purple tones anywhere.
"""


def get_plant_description(day: int) -> str:
    """Get precise plant description for each day."""

    if day == 1:
        return """
PLANT: A single round brown seed (1cm diameter) sitting in a small depression in the center of the soil.
- Seed is smooth, glossy, no cracks
- Freshly planted
- Nothing else growing yet
"""
    elif day == 2:
        return """
PLANT: The same brown seed, now with a tiny hairline crack visible on top.
- Seed still mostly round
- Just the beginning of germination
- Crack is subtle but visible
"""
    elif day == 3:
        return """
PLANT: The seed with a larger crack, pale green visible inside.
- Seed shell splitting
- Hint of the embryo inside
- Moisture visible on seed surface
"""
    elif day == 4:
        return """
PLANT: Seed cracked open, tiny white root tip (3mm) emerging downward.
- Root pushing into soil
- Seed shell clearly split
- Beginning of life
"""
    elif day == 5:
        return """
PLANT: Seed shell cracked open, small pale green sprout (5mm) pushing upward.
- Sprout is curved, pushing through
- Seed shell still attached at base
- Root established in soil
"""
    elif day <= 10:
        height_mm = 5 + (day - 5) * 5  # 10mm to 30mm
        return f"""
PLANT: A pale green sprout, {height_mm}mm tall, growing from the cracked seed.
- Sprout curving upward toward light
- Seed shell {'still attached at base' if day <= 7 else 'fallen to the side nearby'}
- Stem is pale green/white
- {'No leaves yet' if day <= 7 else 'Two tiny round cotyledon leaves (seed leaves) starting to unfold at top'}
"""
    elif day <= 15:
        height_mm = 30 + (day - 10) * 8  # 38mm to 70mm
        return f"""
PLANT: Young sprout, {height_mm}mm tall, with developing leaves.
- Two round cotyledon leaves fully open (about 8mm each)
- {day - 11} tiny pointed true leaves emerging from center
- Stem is light green
- Seed shell on soil nearby (discarded)
- Plant is upright and healthy
"""
    elif day <= 25:
        height_cm = 7 + (day - 15) * 0.3  # 7cm to 10cm
        leaf_pairs = 3 + (day - 15) // 2
        return f"""
PLANT: Young jade plant, about {height_cm:.1f}cm tall.
- Thick fleshy stem, slightly woody at base
- {leaf_pairs} pairs of thick oval jade leaves
- Leaves are vibrant green with reddish edges
- Cotyledons have withered/fallen
- Healthy, compact growth
"""
    elif day <= 35:
        height_cm = 10 + (day - 25) * 0.25
        leaf_pairs = 6 + (day - 25) // 2
        return f"""
PLANT: Maturing jade plant, about {height_cm:.1f}cm tall.
- Woody trunk at bottom third
- {leaf_pairs} pairs of thick fleshy oval leaves
- Starting to branch slightly
- Leaves are lush green with red-tinged edges
- Small red-capped mushroom near base (1-2)
- Tiny snail on soil near moss
"""
    elif day <= 45:
        height_cm = 12.5 + (day - 35) * 0.15
        gnome_desc = ""
        if day >= 42:
            if day == 42:
                gnome_desc = "- A tiny gnome (2cm tall, red pointed hat, blue outfit) has just arrived, standing at platform edge looking at tree with wonder"
            else:
                gnome_desc = "- The tiny gnome (red hat, blue outfit) is exploring the platform"
        return f"""
PLANT: Beautiful jade plant/small tree, about {height_cm:.1f}cm tall.
- Thick woody trunk with bark texture
- Multiple branches forming canopy
- Many pairs of thick oval jade leaves
- Looks like a miniature bonsai tree
- 2-3 red mushrooms near base
- Snail present
- Ladybug on one leaf
{gnome_desc}
"""
    else:
        height_cm = 14 + (day - 45) * 0.1
        return f"""
PLANT: Flourishing jade tree, about {height_cm:.1f}cm tall.
- Strong woody trunk with spreading branches
- Dense canopy of thick oval leaves
- Looks ancient and wise for its size
- 3-4 red mushrooms near base
- Snail on soil
- Ladybug on leaf
- The gnome (red hat, blue outfit) is building a small stone circle campfire ring on the soil
- Small pile of gathered sticks nearby
"""


def generate_day_1():
    """Generate the base day 1 image with seed."""
    filepath = OUTPUT_DIR / "day-001.png"

    if filepath.exists():
        print(f"Day 1 exists, using as base reference")
        return filepath

    prompt = f"""
{BASE_STYLE}

{get_plant_description(1)}

This is Day 1 - the very beginning of the journey.
Create a beautiful, highly detailed claymation-style image.
"""

    print("Generating Day 1 (base image)...", end=" ", flush=True)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="1K"
                ),
            ),
        )

        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                image.save(filepath)
                print("done")
                return filepath

        print("failed - no image")
        return None

    except Exception as e:
        print(f"error: {e}")
        return None


def generate_day(day: int, base_image_path: Path):
    """Generate a day's image using the ORIGINAL day 1 as reference."""
    filepath = OUTPUT_DIR / f"day-{day:03d}.png"

    if filepath.exists():
        print(f"  Day {day:3d}: exists, skipping")
        return filepath

    # Load base image
    with open(base_image_path, "rb") as f:
        base_image_bytes = f.read()

    plant_desc = get_plant_description(day)

    prompt = f"""
Look at this base image of a floating earth platform with a seed.

YOUR TASK: Create Day {day} showing the plant at a more grown stage.

CRITICAL - MUST FOLLOW:
1. Keep the PLATFORM EXACTLY THE SAME - identical shape, colors, moss positions, pebbles, soil layers
2. Keep the same camera angle and lighting
3. Keep the BRIGHT BLUE BACKGROUND (#0000FF)
4. ONLY change the plant/growth in the center
5. Maintain high detail and sharp claymation style - DO NOT let quality degrade

{plant_desc}

The platform must look IDENTICAL to the reference image.
Only the plant and any creatures should be different.
Maintain the same high quality and detail as the original.
"""

    print(f"  Day {day:3d}: generating...", end=" ", flush=True)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_bytes(data=base_image_bytes, mime_type="image/png"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="1K"
                ),
            ),
        )

        for part in response.parts:
            if part.inline_data:
                image = part.as_image()
                image.save(filepath)
                print("done")
                return filepath

        print("failed - no image")
        return None

    except Exception as e:
        print(f"error: {e}")
        return None


def main():
    """Generate images with consistent base reference."""
    print("=" * 60)
    print("V3: CONSISTENT GENERATION (Base Reference Method)")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print()
    print("This method uses Day 1 as reference for ALL images")
    print("to prevent quality degradation and platform drift.")
    print()

    # Test with first 10 days
    max_day = 10

    # Generate or load day 1
    base_path = generate_day_1()
    if not base_path:
        print("Failed to generate base image. Exiting.")
        return

    time.sleep(2)

    # Generate subsequent days using day 1 as reference
    print()
    print("Generating days 2-10 using Day 1 as reference...")

    for day in range(2, max_day + 1):
        generate_day(day, base_path)
        time.sleep(2)

    print()
    print("=" * 60)
    print(f"Done! Check: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
