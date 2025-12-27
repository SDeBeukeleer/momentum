#!/usr/bin/env python3
"""Generate terrarium life phase test images using Gemini API."""

import os
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v3-life")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Use day-075 from v2 as reference (mature jade plant)
REFERENCE_IMAGE = Path("public/diorama/v2/day-075.png")

# Base style - keep consistent with v2
BASE_STYLE = """
claymation stop-motion style, miniature diorama,
soft even studio lighting from above,
plain solid cream/beige background,
the same round glass terrarium jar,
the same mature jade plant (Crassula ovata) with thick trunk and fleshy oval leaves,
highly detailed clay texture,
clean composition, centered in frame
"""

# Four phases to test
LIFE_PHASES = {
    85: {
        "name": "Phase 1: Discovery",
        "description": """
The mature jade plant in the terrarium, and now a tiny visitor has arrived:
- A small cute gnome (about 2cm tall) with a red pointed hat and brown clothes
- The gnome is peeking curiously from behind the trunk of the jade plant
- A tiny ladybug rests on one of the jade leaves
- Small mushrooms (2-3) growing at the base of the tree in the soil
- The gnome looks friendly and curious, just discovering this place
- Everything is miniature and adorable, claymation style
"""
    },

    110: {
        "name": "Phase 2: Settlement",
        "description": """
The mature jade plant in the terrarium, and the gnome is now building a home:
- The same cute gnome with red pointed hat is now busy working
- A tiny house is being constructed at the base of the tree (half-built, made of tiny twigs and clay)
- Small pile of dirt next to a tiny hole the gnome has dug
- A miniature wooden sign stuck in the soil
- Tiny campfire ring made of pebbles with small sticks
- The gnome is holding a tiny shovel or hammer
- A snail is slowly crossing the soil nearby
- Still the same jade plant, same jar, claymation style
"""
    },

    140: {
        "name": "Phase 3: Community",
        "description": """
The mature jade plant in the terrarium, now with a small community:
- Two gnomes now live here (one with red hat, one with blue hat)
- The tiny house is now complete with a door, window, and chimney with tiny smoke
- A small wooden fence surrounds a tiny garden patch with miniature vegetables
- Tiny lanterns (2-3) hanging from the lower branches of the jade plant
- A miniature well made of tiny stones near the house
- A small bird nest visible in the upper branches with a tiny bird
- A butterfly near the top of the jar
- Pebble pathway leading to the house
- Warm, cozy, lived-in feeling, claymation style
"""
    },

    200: {
        "name": "Phase 4: Thriving World",
        "description": """
The mature jade plant in the terrarium, now a complete thriving tiny world:
- Three gnomes visible doing different activities (red, blue, green hats)
- Two tiny houses now, the original and a newer one
- A gnome fishing at a tiny pond (small reflective water area)
- Another gnome on a tiny swing hanging from a branch
- A small treehouse platform in the upper branches with a tiny ladder
- Tiny clothesline with miniature clothes drying
- The bird nest now has baby birds peeking out
- Fireflies (small glowing dots) floating around
- Tiny picnic blanket with miniature food items
- Small bridge made of twigs over a pebble path
- Fairy lights (tiny lanterns) strung between branches
- A ladybug, butterfly, and snail all visible
- The ultimate cozy miniature village, full of life and detail
- Still claymation style, same jar, same jade plant as the foundation
"""
    },
}


def generate_life_phase(day: int, phase_info: dict, reference_path: Path) -> Path:
    """Generate a terrarium life phase image."""
    filename = OUTPUT_DIR / f"day-{day:03d}-{phase_info['name'].split(':')[0].lower().replace(' ', '-')}.png"

    if filename.exists():
        print(f"  Skipping {phase_info['name']} (already exists)")
        return filename

    # Load reference image (mature jade plant)
    ref_image = Image.open(reference_path)

    prompt = f"""
Transform this terrarium image to show {phase_info['name']}:

{phase_info['description']}

KEEP EXACTLY THE SAME:
- The same glass jar shape and style
- The same mature jade plant (don't change the plant at all)
- The same camera angle and framing
- The same plain cream/beige background
- The same claymation art style
- The same lighting

ADD the new elements described above while keeping the plant and jar identical.
The new inhabitants and structures should look like they're made of clay, matching the style.
Everything should be miniature, cute, and charming.
"""

    print(f"Generating {phase_info['name']} (day {day})...")

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

    print(f"  ✗ Failed to generate {phase_info['name']}")
    return reference_path


def main():
    """Generate all four phase test images."""
    print("=" * 50)
    print("Generating Terrarium Life Phase Tests")
    print("=" * 50)
    print()

    if not REFERENCE_IMAGE.exists():
        print(f"ERROR: Reference image not found: {REFERENCE_IMAGE}")
        print("Please run generate_consistent_images.py first.")
        return

    print(f"Using reference: {REFERENCE_IMAGE}")
    print()

    for day, phase_info in LIFE_PHASES.items():
        generate_life_phase(day, phase_info, REFERENCE_IMAGE)
        print()

    print("=" * 50)
    print(f"Done! Images saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
