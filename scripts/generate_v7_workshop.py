#!/usr/bin/env python3
"""
V7: Old Timer Workshop - An antique clock/watch being restored in a workshop.
Uses the proven frosted dome approach with blue background.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v7-workshop")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style description - frosted dome on floating tile, workshop theme
WORKSHOP_STYLE = """
A floating isometric wooden workbench platform (15x15cm square, rounded edges) with a frosted glass dome on top,
the dome is matte finish with NO reflections, NO shine, small brass knob handle on top,
the workbench has visible wood grain, a small drawer on the front, brass corner brackets,
plain solid bright blue background (#0000FF), completely flat, NO gradients,
neutral white studio lighting ONLY, NO colored environmental light, NO color cast,
claymation stop-motion style, soft even lighting,
highly detailed clay textures, miniature diorama aesthetic, warm cozy workshop feeling,
centered in frame, clean composition
"""


def get_prompt_for_day(day: int) -> str:
    """Generate the appropriate prompt for a given day."""

    # === PHASE 1: THE BROKEN TIMER (Days 1-3) ===
    if day <= 3:
        states = {
            1: """
Inside the dome, on the workbench:
- An old broken pocket watch lying in the center (brass case, cracked glass face, hands stopped)
- The watch looks dusty and neglected
- Empty workbench surface, worn wood texture
- A small oil lamp in the corner (unlit)
- Plenty of empty space inside the dome

Day 1 - a forgotten timepiece awaits restoration.""",

            2: """
KEEP the same dome, workbench, brass pocket watch, oil lamp.

The scene evolves slightly:
- The pocket watch is now open, revealing its intricate brass gears inside
- A small magnifying glass has appeared next to the watch
- The oil lamp is now lit with a warm tiny flame
- Everything else stays exactly the same

Day 2 - someone has taken interest in the old timer.""",

            3: """
KEEP the same dome, workbench, open pocket watch, magnifying glass, lit oil lamp.

Small additions:
- A tiny screwdriver and tweezers now lie next to the watch
- A small cloth has been placed under the watch
- The watch gears are more visible, some look rusty
- Everything else stays exactly the same

Day 3 - the restoration begins."""
        }
        return f"{WORKSHOP_STYLE}\n{states[day]}"

    # === PHASE 2: EXAMINATION & CLEANING (Days 4-6) ===
    elif day <= 6:
        if day == 4:
            progress = """
KEEP the same dome, workbench, pocket watch, magnifying glass, oil lamp, tools, cloth.

New progress:
- A small jar of oil has appeared on the workbench
- Some tiny gears have been removed and placed on the cloth
- A tiny brush lies next to the gears (for cleaning)
- The watch face is being cleaned, looking slightly shinier

Day 4 - careful disassembly in progress."""

        elif day == 5:
            progress = """
KEEP ALL previous elements (dome, workbench, watch, tools, oil, lamp, cloth, gears).

New progress:
- More gears now arranged neatly on the cloth
- A small parts tray has appeared with tiny screws
- The watch case is being polished, brass starting to shine
- A tiny pair of spectacles rests on the workbench (the watchmaker was here)

Day 5 - meticulous cleaning continues."""

        else:  # day 6
            progress = """
KEEP ALL previous elements.

New progress:
- The gears on the cloth are now clean and shiny
- A small bottle of polish next to the case
- The watch case is now gleaming brass
- A tiny notepad with sketches has appeared (repair notes)
- The spectacles have moved slightly

Day 6 - all parts are cleaned and ready."""

        return f"{WORKSHOP_STYLE}\n{progress}"

    # === PHASE 3: REASSEMBLY (Days 7-10) ===
    elif day <= 10:
        if day == 7:
            progress = """
KEEP ALL previous elements (dome, workbench, watch, all tools, lamp, cloth, gears, spectacles, notepad).

Reassembly begins:
- Some gears are being placed back into the watch
- Tweezers hold a tiny gear mid-placement
- The mainspring is visible, coiled and ready
- Fewer loose gears on the cloth now

Day 7 - the heart of the watch is being rebuilt."""

        elif day == 8:
            progress = """
KEEP ALL previous elements.

More reassembly:
- Most gears are now back inside the watch
- The watch mechanism is taking shape
- A tiny drop of oil being applied with a needle
- Only 2-3 small gears remain on the cloth

Day 8 - the mechanism comes together."""

        elif day == 9:
            progress = """
KEEP ALL previous elements.

Nearly complete:
- All gears are now inside the watch
- The watch face is being reattached
- New glass crystal ready to be placed
- A tiny polishing cloth wipes the face

Day 9 - the face is restored."""

        else:  # day 10
            progress = """
KEEP ALL previous elements.

The watch is whole again:
- The pocket watch is now closed and complete
- The brass case gleams beautifully
- The glass face is crystal clear, hands visible
- The watch chain has been attached
- It sits proudly on a small velvet cushion

Day 10 - the restoration is complete!"""

        return f"{WORKSHOP_STYLE}\n{progress}"

    # === PHASE 4: CELEBRATION & DISPLAY (Days 11-15) ===
    else:
        if day == 11:
            scene = """
KEEP ALL previous elements, the restored pocket watch on velvet cushion.

The workshop celebrates:
- A tiny cup of tea has appeared (steaming)
- The spectacles rest next to the tea
- The watch is ticking! (tiny motion lines near hands)
- A satisfied feeling in the scene

Day 11 - tea time for the craftsman."""

        elif day == 12:
            scene = """
KEEP ALL previous elements.

The workshop gets cozy:
- A tiny framed photo has appeared (old watchmaker portrait)
- A small plant in a tiny pot in the corner
- More tools organized neatly in a small rack
- The oil lamp glows warmly

Day 12 - personal touches appear."""

        elif day == 13:
            scene = """
KEEP ALL previous elements.

More character:
- A second pocket watch has appeared (next project, closed)
- Tiny books stacked near the corner (watchmaking manuals)
- A small medal or badge on display (master craftsman)
- The plant has a tiny flower bud

Day 13 - a master's workshop."""

        elif day == 14:
            scene = """
KEEP ALL previous elements.

The workshop comes alive:
- A tiny cat figurine sits near the lamp (workshop mascot)
- More personal items: tiny calendar on wall, small clock
- The plant's flower has bloomed
- Warm, lived-in feeling

Day 14 - home of a craftsman."""

        else:  # day 15
            scene = """
KEEP ALL previous elements - this is the culmination!

ULTIMATE COZY WORKSHOP:
- The restored pocket watch gleaming on velvet, ticking happily
- Second watch ready for restoration
- Warm oil lamp glow
- Steaming tea cup
- Tiny spectacles, tools neatly arranged
- Framed photo of old watchmaker
- Small blooming plant
- Watchmaking books and manuals
- Master craftsman medal
- Tiny cat figurine
- Personal calendar and small clock
- Everything warm, cozy, full of character
- A master craftsman's beloved workshop!

Day 15 - the perfect workshop sanctuary."""

        return f"{WORKSHOP_STYLE}\n{scene}"


def get_reference_day(day: int) -> int:
    """Get the best reference image day for a given day."""
    if day <= 1:
        return None
    # For 15 days, use day 1 as reference for all
    return 1


def generate_image(day: int, use_reference: bool = True) -> Path:
    """Generate a single day's image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Day {day}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    contents = [prompt]

    # Add reference image if available
    ref_day = get_reference_day(day)
    if use_reference and ref_day:
        ref_path = OUTPUT_DIR / f"day-{ref_day:03d}.png"
        if ref_path.exists():
            ref_image = Image.open(ref_path)
            contents = [
                f"Use this image as reference for style, dome shape, workbench, and existing elements. Evolve it to day {day}:\n\n" + prompt,
                ref_image
            ]

    print(f"  Day {day}: generating...", end=" ", flush=True)

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
                image = part.as_image()
                image.save(filename)
                print("done")
                return filename

        print("failed (no image)")
        return None

    except Exception as e:
        print(f"failed ({e})")
        return None


def main():
    """Generate workshop evolution images."""
    print("=" * 60)
    print("V7: Old Timer Workshop Evolution")
    print("=" * 60)
    print()

    max_day = 15

    print("Generating 15 days of workshop evolution...")
    print()

    for day in range(1, max_day + 1):
        result = generate_image(day)
        if result is None:
            time.sleep(3)
            generate_image(day, use_reference=False)
        time.sleep(2)

    print()
    print("=" * 60)
    images = list(OUTPUT_DIR.glob("day-*.png"))
    print(f"Done! Generated {len(images)} images")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
