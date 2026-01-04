#!/usr/bin/env python3
"""
V10: Cumulative Element Tracking
Each prompt explicitly lists ALL elements that should be visible.
Uses previous day as reference for better continuity.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v10-cumulative")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_STYLE = """
A floating isometric concrete garage floor platform (20x20cm square) with exposed brick edges,
the concrete surface is slightly worn with oil stains and tire marks,
the brick edge is reddish-brown, weathered look,
plain solid bright blue background (#0000FF), completely flat, NO gradients,
neutral white studio lighting ONLY, NO colored environmental light, NO color cast,
claymation stop-motion style, soft even lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition, warm nostalgic garage feeling
"""

# Track cumulative elements - each day adds to this list
# Format: { day: { "permanent": [...], "action": "..." } }
# permanent = elements that persist, action = what's happening today

DAYS = {
    1: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell (no wheels, no engine, no doors, no glass) - just the skeleton"
        ],
        "action": "The bare rusted shell sits alone on the platform"
    },
    2: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell (no wheels, no engine, no doors)",
            "A small red metal toolbox in the far left corner"
        ],
        "action": "A red toolbox has appeared"
    },
    3: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A single metal wrench on the floor near the car"
        ],
        "action": "A wrench lies on the floor"
    },
    4: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear of the car"
        ],
        "action": "A car jack has been placed near the rear"
    },
    5: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear of the car",
            "A bearded mechanic in blue overalls standing next to the car, holding a clipboard"
        ],
        "action": "The mechanic has arrived, inspecting the car with a clipboard"
    },
    6: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A bearded mechanic in blue overalls holding a wire brush, scrubbing rust off the car"
        ],
        "action": "The mechanic is scrubbing rust with a wire brush"
    },
    7: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A bearded mechanic in blue overalls",
            "A wooden workbench in the back corner"
        ],
        "action": "A wooden workbench has appeared in the background"
    },
    8: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A bearded mechanic in blue overalls",
            "A wooden workbench in the back corner",
            "A desk lamp on the workbench"
        ],
        "action": "A desk lamp has been placed on the workbench"
    },
    9: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp in the back corner",
            "The mechanic under the car - only his legs in blue overalls sticking out"
        ],
        "action": "The mechanic is under the car, only legs visible"
    },
    10: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "A bearded mechanic in blue overalls",
            "ONE rusted wheel rim leaning against the workbench"
        ],
        "action": "A rusted wheel rim has appeared, leaning against the workbench"
    },
    11: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "A bearded mechanic in blue overalls",
            "TWO rusted wheel rims leaning against the workbench"
        ],
        "action": "A second rusted wheel rim has appeared"
    },
    12: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO wheel rims near the workbench",
            "The mechanic in blue overalls cleaning one wheel rim with a cloth"
        ],
        "action": "The mechanic is cleaning the first wheel rim"
    },
    13: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "ONE SHINY SILVER wheel rim (cleaned)",
            "ONE rusted wheel rim next to it",
            "The mechanic in blue overalls standing proudly"
        ],
        "action": "The first wheel rim is now shiny silver!"
    },
    14: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO SHINY SILVER wheel rims (both cleaned)",
            "The mechanic in blue overalls"
        ],
        "action": "Both wheel rims are now shiny silver!"
    },
    15: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO SHINY SILVER wheel rims",
            "TWO NEW RUSTED wheel rims (just arrived)",
            "The mechanic in blue overalls looking at the new rims"
        ],
        "action": "Two more rusted wheel rims have arrived (4 total now)"
    },
}


def get_prompt_for_day(day: int) -> str:
    """Generate explicit prompt with ALL elements listed."""

    if day not in DAYS:
        return None

    day_data = DAYS[day]
    elements = day_data["elements"]
    action = day_data["action"]

    elements_list = "\n".join(f"- {e}" for e in elements)

    return f"""
{BASE_STYLE}

=== DAY {day} OF 200 ===

MANDATORY ELEMENTS (must ALL be visible):
{elements_list}

TODAY'S FOCUS: {action}

IMPORTANT RULES:
1. Every element listed above MUST appear in the image
2. The platform with brick edges must stay EXACTLY the same
3. The rusted car shell is the center focus
4. Maintain claymation stop-motion miniature style
5. Blue background (#0000FF) with no gradients
"""


def generate_image(day: int) -> Path:
    """Generate image using previous day as reference."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"Day {day:3d}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    if not prompt:
        print(f"Day {day:3d}: no prompt defined")
        return None

    contents = [prompt]

    # Use previous day as reference for continuity
    if day > 1:
        prev_path = OUTPUT_DIR / f"day-{(day-1):03d}.png"
        if prev_path.exists():
            prev_image = Image.open(prev_path)
            contents = [
                f"This is Day {day-1}. Create Day {day} by ADDING the new element while keeping EVERYTHING from this image:\n\n" + prompt,
                prev_image
            ]

    print(f"Day {day:3d}: generating...", end=" ", flush=True)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
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
                part.as_image().save(filename)
                print("done")
                return filename

        print("failed (no image)")
        return None

    except Exception as e:
        print(f"failed ({e})")
        return None


def main():
    """Generate images with cumulative element tracking."""
    print("=" * 60)
    print("V10: Cumulative Element Tracking")
    print("=" * 60)
    print()
    print("Each prompt lists ALL elements that must be visible.")
    print("Using previous day as reference for continuity.")
    print()

    for day in range(1, 16):
        result = generate_image(day)
        if result is None:
            time.sleep(3)
            # Retry without reference
            generate_image(day)
        time.sleep(2)

    print()
    print("=" * 60)
    images = list(OUTPUT_DIR.glob("day-*.png"))
    print(f"Done! Generated {len(images)} images")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
