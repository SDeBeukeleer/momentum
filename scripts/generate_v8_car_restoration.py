#!/usr/bin/env python3
"""
V8: Vintage Car Restoration Diorama
A classic Porsche 356 being restored by a tiny mechanic over 15 days.
Based on the theme-tests car image style.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v8-car")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Style description - concrete garage floor platform, no dome
CAR_RESTORATION_STYLE = """
A floating isometric concrete garage floor platform (20x20cm square) with exposed brick edges,
the concrete surface is slightly worn with oil stains and tire marks,
the brick edge is reddish-brown, weathered look,
plain solid bright blue background (#0000FF), completely flat, NO gradients,
neutral white studio lighting ONLY, NO colored environmental light, NO color cast,
claymation stop-motion style, soft even lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition, warm nostalgic garage feeling
"""


def get_prompt_for_day(day: int) -> str:
    """Generate the appropriate prompt for a given day."""

    # === PHASE 1: THE BARN FIND (Days 1-3) ===
    if day == 1:
        return f"""
{CAR_RESTORATION_STYLE}

On the garage floor platform:
- A dusty, rusty vintage Porsche 356 (red paint faded and patchy, covered in dust)
- The car is a "barn find" - neglected for years
- Flat tires, missing hubcaps
- Windshield is dirty and cracked
- The platform is mostly empty, just the sad old car
- A single bare light bulb hanging (unlit)

Day 1 - a forgotten classic discovered in a barn.
"""

    elif day == 2:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP the same platform, the dusty rusty Porsche 356.

Small changes:
- A tiny mechanic has appeared (blue overalls, blue cap, friendly face)
- He stands next to the car, examining it with wonder
- A small toolbox has been placed nearby
- The light bulb is now on, casting warm light
- Everything else stays exactly the same

Day 2 - the mechanic meets his new project.
"""

    elif day == 3:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP the same platform, Porsche 356, mechanic, toolbox, light.

New additions:
- The car's hood is now open, revealing the dusty engine
- A red rolling tool cabinet has appeared on the left side
- Some wrenches and screwdrivers scattered on the floor
- A clipboard with notes hangs nearby (inspection checklist)
- The mechanic is peering into the engine bay

Day 3 - assessment begins.
"""

    # === PHASE 2: DISASSEMBLY (Days 4-6) ===
    elif day == 4:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP the same platform, Porsche 356, mechanic, tool cabinet, toolbox, light.

Progress:
- The car's wheels have been removed, car on jack stands
- 4 old tires stacked near the tool cabinet
- More tools spread on the floor
- A parts cleaning station has appeared (small tub with brushes)
- Oil stain visible under where the engine was drained
- The mechanic is removing a wheel bearing

Day 4 - wheels off, real work begins.
"""

    elif day == 5:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements (platform, car on stands, removed wheels, tool cabinet, cleaning station, mechanic).

More disassembly:
- Chrome trim pieces removed and laid on a cloth
- Bumpers removed and leaning against wall
- Hood removed and standing upright nearby
- Engine parts being cleaned in the tub
- A small radio has appeared on the tool cabinet (playing music)
- The mechanic is polishing a chrome piece

Day 5 - stripping it down.
"""

    elif day == 6:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

Deep disassembly:
- The car body is now primer grey (being prepped for paint)
- Engine removed and sitting on an engine stand
- Interior seats removed and stacked nearby
- Dashboard visible, being restored
- A workbench has appeared with a desk lamp
- Spray paint cans visible near the car
- The mechanic inspects the bare metal body

Day 6 - down to bare bones.
"""

    # === PHASE 3: RESTORATION (Days 7-10) ===
    elif day == 7:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements (platform, car body, engine on stand, removed parts, tools, workbench, mechanic).

Restoration begins:
- The car body is now gleaming RED (fresh paint!)
- Masking tape and paper still on windows
- Paint booth plastic sheeting visible
- The freshly painted body looks stunning
- The mechanic admires the paint job proudly
- A fan is drying the paint

Day 7 - the red beauty emerges!
"""

    elif day == 8:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

Engine rebuild:
- The engine is being rebuilt on the stand
- Shiny new parts visible (chrome air cleaner, new hoses)
- Engine is now clean and painted
- Some chrome trim being polished on the workbench
- New leather seats visible (being prepared)
- The mechanic is working on the engine with precision

Day 8 - bringing the heart back to life.
"""

    elif day == 9:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

Reassembly starts:
- The engine is back IN the car!
- Hood being refitted
- Chrome bumpers back on (gleaming!)
- New chrome hubcaps visible near the car
- Interior seats being reinstalled
- The mechanic tightens engine bolts
- Excitement building!

Day 9 - putting it back together.
"""

    elif day == 10:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

Nearly complete:
- All 4 wheels back on with shiny chrome hubcaps
- Car is off the jack stands, sitting on its tires
- Chrome trim all reinstalled and gleaming
- Windshield replaced (crystal clear)
- Interior complete with tan leather
- The mechanic closes the hood with satisfaction

Day 10 - she's almost ready!
"""

    # === PHASE 4: FINISHING TOUCHES (Days 11-15) ===
    elif day == 11:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

Final details:
- The car is COMPLETE and BEAUTIFUL
- Gleaming red paint, chrome shining
- The mechanic is polishing the hood with a cloth
- A bucket of soapy water nearby
- The car looks showroom perfect
- All tools being organized and put away

Day 11 - the final polish.
"""

    elif day == 12:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements, the completed restored Porsche 356.

Celebration:
- A small "DONE!" banner or checkered flag near the car
- The mechanic stands proudly next to his masterpiece
- A camera on tripod (taking photos for the album)
- A cup of coffee steaming on the workbench
- The radio plays victory music
- Confetti or small celebration elements

Day 12 - project complete, time to celebrate!
"""

    elif day == 13:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

The garage becomes a showroom:
- A red carpet leading to the car
- Velvet rope barrier around the Porsche
- A small trophy or "Best in Show" ribbon
- Framed photos of the restoration process on a small display
- The mechanic poses next to the car
- A visitor (second small figure) admiring the car

Day 13 - showing off the masterpiece.
"""

    elif day == 14:
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements.

The perfect garage:
- Vintage gas pump decoration added
- Neon "GARAGE" sign glowing
- Classic car posters on a small board
- A comfy chair for the mechanic to rest
- A small fridge with drinks
- The car gleams under professional lighting
- Cozy, lived-in garage atmosphere

Day 14 - a dream garage takes shape.
"""

    else:  # day 15
        return f"""
{CAR_RESTORATION_STYLE}

KEEP ALL previous elements - this is the ULTIMATE scene!

THE PERFECT VINTAGE GARAGE:
- The stunning red Porsche 356, fully restored and gleaming
- Red tool cabinet, organized and professional
- Workbench with lamp, tools neatly arranged
- Vintage gas pump decoration
- Glowing neon "GARAGE" sign
- Classic car posters displayed
- Trophy and "Best in Show" ribbon
- Framed restoration photos
- The proud mechanic (blue overalls, blue cap)
- A visitor admiring the car
- Velvet rope around the masterpiece
- Comfy viewing chair
- Small fridge with drinks
- Radio playing
- Oil stains tell the story of hard work
- Warm, nostalgic, perfect miniature garage!

Day 15 - the ultimate car enthusiast's dream garage!
"""


def get_reference_day(day: int) -> int:
    """Get the best reference image day."""
    if day <= 1:
        return None
    return 1  # Always use day 1 as reference for consistency


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
                f"Use this image as reference for style, platform shape, and overall aesthetic. Evolve it to day {day}:\n\n" + prompt,
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
    """Generate car restoration evolution images."""
    print("=" * 60)
    print("V8: Vintage Car Restoration Diorama")
    print("=" * 60)
    print()

    max_day = 15

    print("Generating 15 days of car restoration...")
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
