#!/usr/bin/env python3
"""
Test consistent image generation using image-to-image approach.
Uses the previous day's image as reference to maintain consistency.
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import io

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/consistent-test-v2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Very specific base platform description to use consistently
BASE_PLATFORM = """
EXACT PLATFORM SPECIFICATION (must match exactly):
- Square isometric platform, viewed from above at 45 degrees
- Platform is 15cm x 15cm with rounded organic edges
- Soil layers visible on sides: dark brown top (2cm), reddish-brown middle (1.5cm), dark bottom (1cm)
- Small pebbles embedded in soil layers on all sides
- Thin roots poking out from soil edges
- Light brown/tan raised rim around the top edge
- SOLID BRIGHT GREEN CHROMA KEY BACKGROUND (#00FF00) - pure green, no gradients
- Soft shadow beneath platform

IMPORTANT COLOR RULES:
- NO pink, magenta, or purple tones anywhere in the image
- The background must be PURE GREEN (#00FF00) with no color spill onto the platform
- All browns should be warm/earthy (no pink undertones)
- Keep lighting neutral, avoid any colored light reflections

TOP SURFACE DECORATION (fixed elements):
- 4 moss patches: top-left corner, top-right corner, bottom-left corner, bottom-right edge
- 3 small pebbles: 1 blue (near top-left moss), 1 yellow (near bottom-right), 1 orange (right side)
- Rich brown soil texture in center area
"""


def generate_base_image():
    """Generate the base platform with just a seed (Day 1)."""
    prompt = f"""
{BASE_PLATFORM}

Claymation stop-motion style, highly detailed clay textures.

IN THE CENTER OF THE PLATFORM:
- A single round brown seed, about 1cm diameter
- The seed sits in a small depression in the soil
- No cracks yet - perfectly round and smooth
- Slightly glossy surface

This is Day 1 - the seed has just been planted.
The platform should look exactly as described above with no variations.
"""

    print("Generating Day 1 (base image with seed)...")

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
            filepath = OUTPUT_DIR / "day-001.png"
            image.save(filepath)
            print(f"  Saved: {filepath}")
            return filepath

    print("  Failed to generate base image")
    return None


def generate_next_day(previous_image_path: Path, day: int):
    """Generate the next day's image based on the previous day."""

    # Load previous image
    with open(previous_image_path, "rb") as f:
        previous_image_bytes = f.read()

    # Define growth progression
    if day <= 5:
        growth_descriptions = {
            2: "The seed now has a tiny hairline crack forming on top",
            3: "The crack is larger, you can see a hint of pale green inside",
            4: "The seed is splitting open, a tiny white root tip is emerging downward into the soil",
            5: "The seed shell is cracked open, a small pale sprout (5mm) is pushing upward",
        }
        plant_desc = growth_descriptions.get(day, "")
    elif day <= 10:
        heights = {6: 10, 7: 15, 8: 20, 9: 25, 10: 30}
        height = heights.get(day, 10)
        if day <= 7:
            plant_desc = f"A pale green sprout, {height}mm tall, curving upward. The seed shell is still visible at the base, cracked open."
        else:
            plant_desc = f"A small green sprout, {height}mm tall, standing more upright. Seed shell fallen to the side. Two tiny round cotyledon leaves ({(day-7)*2}mm each) are starting to unfold at the top."
    elif day <= 15:
        height = 30 + (day - 10) * 8  # 38mm to 70mm
        leaves = 2  # cotyledons
        true_leaves = max(0, day - 12)  # true leaves start appearing at day 13
        plant_desc = f"Young sprout, {height}mm tall. Two round cotyledon leaves fully open. {true_leaves} tiny pointed true leaves emerging from center."
    elif day <= 25:
        # Young plant stage - developing into small jade plant
        height_cm = 7 + (day - 15) * 0.3  # 7cm to 10cm
        leaf_pairs = 3 + (day - 15) // 3  # 3 to 6 pairs
        plant_desc = f"""Young jade plant, about {height_cm:.1f}cm tall.
- Stem becoming slightly woody at the base
- {leaf_pairs} pairs of thick, fleshy oval jade leaves
- Leaves are vibrant green with slightly reddish edges
- The cotyledons have withered and fallen off
- Plant is healthy and growing steadily"""
    elif day <= 35:
        # Maturing plant - becoming a small tree
        height_cm = 10 + (day - 25) * 0.25  # 10cm to 12.5cm
        leaf_pairs = 6 + (day - 25) // 3  # 6 to 9 pairs
        extras = ""
        if day >= 28:
            extras = "- A tiny snail has appeared on the soil near the moss"
        if day >= 32:
            extras += "\n- 1-2 small red-capped mushrooms growing near the plant base"
        plant_desc = f"""Maturing jade plant, about {height_cm:.1f}cm tall.
- Trunk is noticeably woody at the bottom third
- {leaf_pairs} pairs of thick oval jade leaves
- Starting to develop small branches
- Leaves are lush green with red-tinged edges
{extras}"""
    elif day <= 45:
        # Gnome arrives around day 42!
        height_cm = 12.5 + (day - 35) * 0.15  # 12.5cm to 14cm
        if day < 42:
            gnome_status = "NO gnome yet - just the plant and creatures"
            creatures = "- Snail on soil\n- 2-3 red mushrooms near base\n- Maybe a ladybug on a leaf"
        elif day == 42:
            gnome_status = "A TINY GNOME has just arrived! (red pointed hat, blue outfit, about 2cm tall) Standing at the edge of the platform, looking at the plant with wonder and excitement"
            creatures = "- Snail, mushrooms, ladybug present"
        else:
            activities = {
                43: "exploring the platform, examining the mushrooms curiously",
                44: "sitting on a pebble, resting and admiring the plant",
                45: "gathering tiny stones in a small pile (planning something)",
            }
            gnome_status = f"The gnome (red hat, blue outfit) is {activities.get(day, 'exploring the platform')}"
            creatures = "- Snail, mushrooms, ladybug present"
        plant_desc = f"""Beautiful jade plant, about {height_cm:.1f}cm tall.
- Thick woody trunk with multiple branches forming
- Many pairs of fleshy oval leaves creating bushy appearance
- Plant looks healthy and established

CREATURES/CHARACTERS:
- {gnome_status}
{creatures}"""
    elif day <= 50:
        # Gnome settling in, starting to build
        height_cm = 14 + (day - 45) * 0.1  # 14cm to 14.5cm
        activities = {
            46: "arranging stones in a circle on the soil (campfire ring foundation)",
            47: "continuing to build the stone circle, adding more stones",
            48: "the stone circle is complete, gnome is gathering tiny sticks",
            49: "placing sticks inside the stone ring (preparing campfire)",
            50: "sitting proudly next to the completed campfire ring with tiny sticks inside, looking happy",
        }
        plant_desc = f"""Flourishing jade plant, about {height_cm:.1f}cm tall.
- Strong woody trunk with spreading branches
- Dense foliage of thick oval leaves
- Looking like a proper miniature tree

THE GNOME'S PROGRESS:
- The gnome (red pointed hat, blue outfit) is {activities.get(day, 'working on the campfire')}
- Small stone circle visible on the soil (campfire ring in progress)
- Snail, mushrooms (3-4 now), ladybug present"""
    else:
        plant_desc = "Continue growing the plant naturally, slightly larger than yesterday. The gnome continues settling in."

    prompt = f"""
Look at this image of a growing plant on a floating earth platform.

YOUR TASK: Create the NEXT DAY's image (Day {day}).

CRITICAL RULES:
1. The PLATFORM must stay EXACTLY the same - same shape, same moss positions, same pebbles, same soil layers
2. ONLY the plant in the center should change - it should be slightly more grown than yesterday
3. BACKGROUND must be SOLID BRIGHT GREEN (#00FF00) - chroma key green, pure green, no gradients
4. Same camera angle, same lighting, same style
5. NO pink, magenta, or purple tones anywhere - avoid any color spill from background

PLANT CHANGE FOR DAY {day}:
{plant_desc}

The change should be subtle and natural - this is one day of growth.
Everything else (platform, moss, pebbles, soil) must be IDENTICAL to the input image.
The background MUST be pure bright green (#00FF00) for chroma key removal.
"""

    print(f"Generating Day {day}...")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[
                types.Part.from_bytes(data=previous_image_bytes, mime_type="image/png"),
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
                filepath = OUTPUT_DIR / f"day-{day:03d}.png"
                image.save(filepath)
                print(f"  Saved: {filepath}")
                return filepath

        print(f"  Failed - no image in response")
        return None

    except Exception as e:
        print(f"  Error: {e}")
        return None


def main():
    """Generate a sequence of consistent images."""
    print("=" * 60)
    print("CONSISTENT IMAGE GENERATION TEST")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print()

    # Generate more days to see growth stages and gnome arrival
    max_day = 50

    # Check if we have existing images to continue from
    existing = sorted(OUTPUT_DIR.glob("day-*.png"))

    if existing:
        last_day = int(existing[-1].stem.split("-")[1])
        print(f"Found existing images up to day {last_day}")
        start_day = last_day + 1
        previous_path = existing[-1]
    else:
        # Generate base image
        previous_path = generate_base_image()
        if not previous_path:
            print("Failed to generate base image. Exiting.")
            return
        start_day = 2
        time.sleep(2)

    # Generate subsequent days
    for day in range(start_day, max_day + 1):
        result = generate_next_day(previous_path, day)
        if result:
            previous_path = result
        else:
            print(f"Failed at day {day}, stopping.")
            break

        time.sleep(2)  # Rate limiting

    print()
    print("=" * 60)
    print("DONE! Check the images in:")
    print(f"  {OUTPUT_DIR.absolute()}")
    print()
    print("Compare consecutive days to check consistency.")
    print("=" * 60)


if __name__ == "__main__":
    main()
