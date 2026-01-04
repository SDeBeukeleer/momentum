#!/usr/bin/env python3
"""
V11: Dual Reference System
- Day 1 as QUALITY/STYLE anchor (prevents degradation)
- Previous day as ELEMENT reference (maintains continuity)
This prevents the quality loss from pure image-to-image chaining.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v11-dual-ref")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_STYLE = """
STYLE REQUIREMENTS (CRITICAL - maintain high detail):
- Floating isometric concrete garage floor platform (20x20cm square)
- Exposed brick edges - each brick clearly defined, reddish-brown, weathered
- Concrete surface with realistic texture, oil stains, tire marks
- Plain solid bright blue background (#0000FF), NO gradients
- Neutral white studio lighting, NO colored light
- Claymation stop-motion style with HIGHLY DETAILED clay textures
- Miniature diorama aesthetic - every element crisp and detailed
- Centered in frame, clean composition
"""

DAYS = {
    1: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell (no wheels, no engine, no doors, no glass) - detailed rust texture"
        ],
        "action": "The bare rusted shell sits alone"
    },
    2: {
        "elements": [
            "A rusted Porsche 356 car shell with detailed rust texture",
            "A small red metal toolbox (detailed, with visible latches) in the far left corner"
        ],
        "action": "A red toolbox has appeared"
    },
    3: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench (chrome, detailed) on the floor near the car"
        ],
        "action": "A wrench lies on the floor"
    },
    4: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack (detailed metal) near the rear of the car"
        ],
        "action": "A car jack placed near the rear"
    },
    5: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A bearded mechanic (detailed face, blue overalls) holding a clipboard, standing next to the car"
        ],
        "action": "The mechanic has arrived with a clipboard"
    },
    6: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A bearded mechanic in blue overalls scrubbing the car with a wire brush"
        ],
        "action": "The mechanic is scrubbing rust"
    },
    7: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A bearded mechanic in blue overalls",
            "A wooden workbench (detailed wood grain, shelf underneath) in the back corner"
        ],
        "action": "A wooden workbench has appeared"
    },
    8: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A bearded mechanic in blue overalls",
            "A wooden workbench in the back corner",
            "A desk lamp (articulated arm, metal shade) on the workbench, turned on"
        ],
        "action": "A desk lamp on the workbench"
    },
    9: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "The mechanic's legs (blue overalls) sticking out from under the car"
        ],
        "action": "The mechanic is under the car - only legs visible"
    },
    10: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "A bearded mechanic in blue overalls standing",
            "ONE rusted wheel rim (detailed spokes) leaning against the workbench"
        ],
        "action": "A rusted wheel rim appeared"
    },
    11: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "A bearded mechanic in blue overalls",
            "TWO rusted wheel rims leaning against the workbench"
        ],
        "action": "A second rusted wheel rim appeared"
    },
    12: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO wheel rims near the workbench",
            "The mechanic in blue overalls cleaning one wheel rim with a cloth"
        ],
        "action": "Mechanic cleaning the first wheel rim"
    },
    13: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "ONE SHINY CHROME wheel rim (polished, reflective)",
            "ONE rusted wheel rim next to it",
            "The mechanic in blue overalls standing proudly"
        ],
        "action": "First wheel rim is now shiny chrome!"
    },
    14: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims (polished, reflective)",
            "The mechanic in blue overalls"
        ],
        "action": "Both wheel rims are now shiny chrome!"
    },
    15: {
        "elements": [
            "A rusted Porsche 356 car shell",
            "A small red metal toolbox in the far left corner",
            "A metal wrench on the floor",
            "A scissor car jack near the rear",
            "A wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims",
            "TWO NEW RUSTED wheel rims (just arrived)",
            "The mechanic in blue overalls examining the new rims"
        ],
        "action": "Two more rusted wheel rims arrived (4 total)"
    },
}


def get_prompt_for_day(day: int) -> str:
    """Generate prompt with quality emphasis."""
    if day not in DAYS:
        return None

    day_data = DAYS[day]
    elements = day_data["elements"]
    action = day_data["action"]
    elements_list = "\n".join(f"  - {e}" for e in elements)

    return f"""
{BASE_STYLE}

=== DAY {day} OF 200 - VINTAGE PORSCHE 356 RESTORATION ===

ALL ELEMENTS THAT MUST BE VISIBLE:
{elements_list}

TODAY: {action}

QUALITY RULES:
1. Match the DETAIL LEVEL of the reference image (Day 1)
2. Every brick on the platform edge must be individually visible
3. The concrete texture must be crisp and detailed
4. All elements must be sharp, not blurry
5. Maintain miniature diorama aesthetic with high craftsmanship
"""


def generate_image(day: int) -> Path:
    """Generate image using dual reference system."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"Day {day:3d}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    if not prompt:
        print(f"Day {day:3d}: no prompt defined")
        return None

    # Build content with dual reference
    day1_path = OUTPUT_DIR / "day-001.png"
    prev_path = OUTPUT_DIR / f"day-{(day-1):03d}.png" if day > 1 else None

    print(f"Day {day:3d}: generating...", end=" ", flush=True)

    try:
        if day == 1:
            # Day 1: Generate fresh, high quality
            contents = [prompt]
        elif day1_path.exists() and prev_path and prev_path.exists():
            # DUAL REFERENCE: Day 1 for quality + previous day for elements
            day1_image = Image.open(day1_path)
            prev_image = Image.open(prev_path)
            contents = [
                "REFERENCE IMAGE 1 (for QUALITY and STYLE - match this detail level):",
                day1_image,
                f"\nREFERENCE IMAGE 2 (for ELEMENTS - this is Day {day-1}, add today's new element):",
                prev_image,
                f"\nNow create Day {day} with the QUALITY of Image 1 and the ELEMENTS from Image 2 plus today's addition:\n\n" + prompt
            ]
        elif day1_path.exists():
            # Just Day 1 reference
            day1_image = Image.open(day1_path)
            contents = [
                "Match the QUALITY and DETAIL of this reference image:",
                day1_image,
                f"\nCreate Day {day}:\n\n" + prompt
            ]
        else:
            contents = [prompt]

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
    """Generate images with dual reference system."""
    print("=" * 60)
    print("V11: Dual Reference System")
    print("=" * 60)
    print()
    print("Day 1 = QUALITY anchor (always referenced)")
    print("Previous day = ELEMENT reference (for continuity)")
    print()

    for day in range(1, 16):
        result = generate_image(day)
        if result is None:
            time.sleep(3)
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
