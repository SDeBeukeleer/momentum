#!/usr/bin/env python3
"""
V12: Milestone Refresh System
- When a NEW element appears → Generate fresh (high quality introduction)
- Continuation days → Reference the milestone where that element appeared
- This preserves quality of each element from when it was introduced
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v12-milestone")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_STYLE = """
CRITICAL STYLE REQUIREMENTS:
- Floating isometric concrete garage floor platform (20x20cm square)
- Exposed brick edges - EACH BRICK individually defined, reddish-brown, weathered texture
- Concrete surface with realistic cracks, oil stains, tire marks
- Plain solid bright blue background (#0000FF), completely flat
- Neutral white studio lighting only
- Claymation stop-motion style with MAXIMUM DETAIL on every element
- Every object must be crisp, sharp, highly detailed miniature
- Centered in frame, clean composition
"""

# Define which days introduce NEW elements (milestones)
# These days get generated FRESH for maximum quality
MILESTONES = {
    1: "car_shell",      # Car shell introduced
    2: "toolbox",        # Toolbox introduced
    5: "mechanic",       # Mechanic introduced
    7: "workbench",      # Workbench introduced
    8: "lamp",           # Lamp introduced
    10: "wheel_rim_1",   # First wheel rim
    13: "chrome_rim",    # Chrome rim (transformation)
    15: "four_rims",     # Four rims scene
}

# For non-milestone days, which milestone should they reference?
def get_reference_milestone(day: int) -> int:
    """Get the most recent milestone day to use as reference."""
    milestone_days = sorted(MILESTONES.keys())
    for i, m in enumerate(milestone_days):
        if day < m:
            return milestone_days[i-1] if i > 0 else 1
    return milestone_days[-1]


DAYS = {
    1: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell - HIGHLY DETAILED rust texture, visible metal grain, no wheels/engine/doors/glass"
        ],
        "focus": "The bare rusted shell sits alone - establish maximum detail baseline"
    },
    2: {
        "elements": [
            "The same rusted Porsche 356 car shell from Day 1",
            "NEW: A small red metal toolbox - HIGHLY DETAILED with visible latches, hinges, texture, scratches - in the far left corner"
        ],
        "focus": "Toolbox appears - must be MAXIMUM DETAIL as this is its introduction"
    },
    3: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox (detailed, with latches) in far left corner",
            "NEW: A chrome metal wrench - detailed, reflective surface - on the floor near the car"
        ],
        "focus": "Wrench appears on floor"
    },
    4: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "NEW: A scissor car jack - detailed metal mechanism - near the rear of the car"
        ],
        "focus": "Car jack placed near rear"
    },
    5: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "NEW: A bearded mechanic - HIGHLY DETAILED face, realistic blue overalls with stitching, holding clipboard - standing next to car"
        ],
        "focus": "Mechanic appears - must be MAXIMUM DETAIL as this is his introduction"
    },
    6: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls, now holding a wire brush, scrubbing rust off the car"
        ],
        "focus": "Mechanic scrubbing rust with wire brush"
    },
    7: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls",
            "NEW: A wooden workbench - HIGHLY DETAILED wood grain, visible joints, shelf underneath, tools hanging on pegboard back - in the back corner"
        ],
        "focus": "Workbench appears - must be MAXIMUM DETAIL as this is its introduction"
    },
    8: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls",
            "The wooden workbench with detailed wood grain in the back corner",
            "NEW: An articulated desk lamp - HIGHLY DETAILED metal joints, chrome shade, on the workbench, turned ON with warm glow"
        ],
        "focus": "Desk lamp appears on workbench - must be MAXIMUM DETAIL"
    },
    9: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp (turned on)",
            "The mechanic's legs in blue overalls sticking out from under the car (he's working underneath)"
        ],
        "focus": "Mechanic under car - only detailed legs visible"
    },
    10: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "The bearded mechanic in blue overalls standing",
            "NEW: ONE rusted wheel rim - HIGHLY DETAILED spokes, rust texture, metal grain visible - leaning against the workbench"
        ],
        "focus": "First wheel rim appears - must be MAXIMUM DETAIL"
    },
    11: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "The bearded mechanic in blue overalls",
            "TWO rusted wheel rims (detailed rust texture) leaning against the workbench"
        ],
        "focus": "Second wheel rim appears"
    },
    12: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO wheel rims near the workbench",
            "The mechanic in blue overalls kneeling, cleaning one wheel rim with a cloth"
        ],
        "focus": "Mechanic cleaning wheel rim"
    },
    13: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "NEW: ONE SHINY CHROME wheel rim - HIGHLY DETAILED mirror finish, reflective, gleaming - this is the cleaned rim",
            "ONE rusted wheel rim next to it (before/after contrast)",
            "The bearded mechanic standing proudly with hands on hips"
        ],
        "focus": "Chrome wheel rim debut - must be MAXIMUM DETAIL to show the transformation"
    },
    14: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims (mirror finish, gleaming)",
            "The bearded mechanic in blue overalls"
        ],
        "focus": "Both wheel rims now chrome"
    },
    15: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox in far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims (polished, reflective)",
            "TWO NEW RUSTED wheel rims (just arrived, contrasting with the chrome ones)",
            "The bearded mechanic examining the new rusted rims"
        ],
        "focus": "Four wheel rims total - 2 chrome + 2 rusted"
    },
}


def get_prompt_for_day(day: int) -> str:
    """Generate detailed prompt."""
    if day not in DAYS:
        return None

    day_data = DAYS[day]
    elements = day_data["elements"]
    focus = day_data["focus"]
    elements_list = "\n".join(f"  • {e}" for e in elements)

    is_milestone = day in MILESTONES

    quality_note = ""
    if is_milestone:
        quality_note = """
⚠️ THIS IS A MILESTONE DAY - NEW ELEMENT INTRODUCTION
The new element must be rendered at MAXIMUM QUALITY with fine details.
This image will serve as the quality reference for this element going forward.
"""

    return f"""
{BASE_STYLE}

═══════════════════════════════════════════════════════════
DAY {day} OF 200 - PORSCHE 356 RESTORATION
═══════════════════════════════════════════════════════════
{quality_note}
SCENE ELEMENTS (all must be visible):
{elements_list}

TODAY'S FOCUS: {focus}

QUALITY CHECKLIST:
✓ Platform bricks individually defined
✓ Concrete texture crisp and detailed
✓ Every accessory sharp and detailed
✓ Mechanic (if present) has detailed face and clothing
✓ Metal objects show realistic reflections/texture
✓ No blurry or muddy areas
"""


def generate_image(day: int) -> Path:
    """Generate image with milestone refresh system."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"Day {day:3d}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    if not prompt:
        print(f"Day {day:3d}: no prompt defined")
        return None

    is_milestone = day in MILESTONES

    print(f"Day {day:3d}: generating", end="")
    if is_milestone:
        print(f" [MILESTONE: {MILESTONES[day]}]", end="")
    print("...", end=" ", flush=True)

    try:
        if day == 1:
            # Day 1: Pure prompt, no reference
            contents = [prompt]
        elif is_milestone:
            # MILESTONE DAY: Only use Day 1 for style, generate new element fresh
            day1_path = OUTPUT_DIR / "day-001.png"
            if day1_path.exists():
                day1_image = Image.open(day1_path)
                contents = [
                    "STYLE REFERENCE (match this quality level for platform and overall aesthetic):",
                    day1_image,
                    f"\nGenerate Day {day} with a NEW element at MAXIMUM QUALITY:\n\n" + prompt
                ]
            else:
                contents = [prompt]
        else:
            # NON-MILESTONE: Reference both Day 1 AND the most recent milestone
            day1_path = OUTPUT_DIR / "day-001.png"
            milestone_day = get_reference_milestone(day)
            milestone_path = OUTPUT_DIR / f"day-{milestone_day:03d}.png"

            if day1_path.exists() and milestone_path.exists():
                day1_image = Image.open(day1_path)
                milestone_image = Image.open(milestone_path)
                contents = [
                    "REFERENCE 1 - Platform quality standard:",
                    day1_image,
                    f"\nREFERENCE 2 - Day {milestone_day} (current scene with all elements):",
                    milestone_image,
                    f"\nCreate Day {day}, maintaining quality of both references:\n\n" + prompt
                ]
            elif day1_path.exists():
                day1_image = Image.open(day1_path)
                contents = [
                    "Match this quality level:",
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
    """Generate images with milestone refresh system."""
    print("=" * 60)
    print("V12: Milestone Refresh System")
    print("=" * 60)
    print()
    print("MILESTONES (fresh generation for max quality):")
    for day, element in sorted(MILESTONES.items()):
        print(f"  Day {day:2d}: {element}")
    print()
    print("Other days reference their nearest milestone.")
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
