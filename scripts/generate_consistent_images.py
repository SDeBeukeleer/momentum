#!/usr/bin/env python3
"""Generate consistent diorama images using Gemini API with image-to-image."""

import os
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Consistent style description - same jar, same plant type
JAR_STYLE = """
The exact same round glass terrarium jar with a wide opening at the top,
simple clean glass with subtle reflections, no lid,
the jar sits centered on a plain solid background
"""

PLANT_TYPE = """
a single jade plant (Crassula ovata) succulent with thick fleshy oval leaves,
the same plant in every image just at different growth stages
"""

BASE_STYLE = """
claymation stop-motion style, miniature diorama,
soft even studio lighting from above,
plain solid cream/beige background for easy cutout,
rich brown soil with small pebbles inside the jar,
highly detailed clay texture on the plant,
the terrarium is centered in frame,
clean composition, no other objects in scene
"""

# Progressive growth stages - same plant evolving
GROWTH_STAGES = {
    1: "a single tiny brown oval seed half-buried in the soil, just planted, no growth yet",

    3: "the same seed now has a tiny crack on top, hint of pale green visible inside the crack",

    7: "a tiny jade sprout just emerging from the cracked seed, two very small round cotyledon leaves, pale green, about 1cm tall",

    14: "the same jade plant now 2cm tall with the first pair of true thick oval leaves forming above the cotyledons, short stubby stem",

    21: "the same jade plant now 3cm tall, two pairs of thick fleshy oval leaves on a thickening stem, the cotyledons starting to shrivel",

    30: "the same jade plant now 4cm tall, three pairs of plump oval leaves, stem becoming woody at the base, looking like a tiny tree",

    45: "the same jade plant now 5cm tall, multiple branches starting to form, thick trunk, lush green oval leaves throughout",

    60: "the same jade plant now a small bushy tree about 6cm tall, well-branched structure, many thick oval leaves, established woody trunk",

    75: "the same jade plant now 7cm tall, dense branching, some leaves showing slight red edges (sun stress), very healthy and full",

    90: "the same jade plant now a beautiful miniature tree 8cm tall, thick gnarled trunk, full canopy of plump leaves, tiny white flower buds forming",

    100: "the same jade plant in full bloom, tiny star-shaped white-pink flowers in clusters at branch tips, the plant looks ancient and wise, soft magical glow around the flowers",

    120: "the same jade plant even more magnificent, flowers fully open, some beginning to form seed pods, ethereal soft golden light emanating from within",

    150: "the same jade plant now transcendent, the leaves have a subtle crystalline shimmer, tiny points of light like stars scattered among the branches, magical atmosphere",

    175: "the same jade plant at mythical stage, leaves appear semi-translucent with inner glow, delicate aurora-like colors in the air around it, cosmic beauty",

    200: "the same jade plant at its ultimate cosmic form, leaves contain tiny swirling galaxies, stardust particles floating around, the most beautiful magical plant imaginable while still recognizable as the same jade plant",
}


def generate_base_image() -> Path:
    """Generate the initial seed image that all others will reference."""
    filename = OUTPUT_DIR / "day-001.png"

    if filename.exists():
        print(f"Base image exists: {filename}")
        return filename

    prompt = f"""
    Create a claymation style terrarium diorama image:

    {JAR_STYLE}

    Inside the jar: {GROWTH_STAGES[1]}

    {BASE_STYLE}

    IMPORTANT: Use a plain solid cream or light beige background (not a room or table).
    The jar should be the only object, perfectly centered, ready for transparent background cutout.
    """

    print("Generating base seed image (day 1)...")

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
            image.save(filename)
            print(f"  ✓ Saved: {filename}")
            return filename

    raise Exception("Failed to generate base image")


def generate_from_reference(day: int, description: str, reference_path: Path) -> Path:
    """Generate a new stage based on the previous image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Skipping day {day} (already exists)")
        return filename

    # Load reference image
    ref_image = Image.open(reference_path)

    prompt = f"""
    Evolve this terrarium to show the plant at a later growth stage.

    KEEP EXACTLY THE SAME:
    - The same glass jar shape, size, and style
    - The same soil and pebbles arrangement
    - The same camera angle and framing
    - The same plain background color
    - The same lighting setup
    - The same claymation art style

    CHANGE ONLY THE PLANT:
    The plant has grown and now looks like: {description}

    This must look like the SAME plant, just more mature.
    The growth should be gradual and believable.

    Keep the plain solid background for easy cutout.
    """

    print(f"Generating day {day}...")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt, ref_image],
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
            image.save(filename)
            print(f"  ✓ Saved: {filename}")
            return filename

    print(f"  ✗ Failed to generate day {day}")
    return reference_path  # Return previous image as fallback


def main():
    """Generate all images with consistency."""
    print("=" * 50)
    print("Generating CONSISTENT diorama images")
    print("=" * 50)
    print()

    # Start with base image
    current_ref = generate_base_image()
    print()

    # Generate each subsequent stage, using previous as reference
    days = sorted(GROWTH_STAGES.keys())

    for i, day in enumerate(days):
        if day == 1:
            continue  # Already generated

        description = GROWTH_STAGES[day]
        current_ref = generate_from_reference(day, description, current_ref)

    print()
    print("=" * 50)
    print(f"Done! Images saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
