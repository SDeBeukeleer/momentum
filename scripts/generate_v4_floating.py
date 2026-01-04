#!/usr/bin/env python3
"""
V4: Floating platform with glass bell consistency approach.
Uses milestone references and explicit "KEEP" instructions.
"""

import os
import time
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v4-floating")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Consistent platform style - detailed like the glass bell approach
PLATFORM_STYLE = """
A floating isometric earth platform tile viewed from above at 45 degrees,
square platform (15cm x 15cm) with rounded organic edges,
visible soil cross-section on sides showing layers: dark brown topsoil, reddish clay middle, dark bottom layer,
small pebbles and thin roots visible in the soil layers,
light tan/beige raised rim around the top edge,
plain solid bright blue background (#0000FF) for easy cutout,
claymation stop-motion style, soft even studio lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition, gentle shadow beneath platform
"""

# Fixed platform elements - same every image
PLATFORM_ELEMENTS = """
TOP SURFACE (KEEP EXACTLY THE SAME EVERY IMAGE):
- 4 fluffy bright green moss patches in corners (top-left, top-right, bottom-left, bottom-right)
- Blue pebble near top-left moss
- Orange pebble near right edge
- Yellow pebble near bottom
- Rich brown soil texture in center area
"""


def get_prompt_for_day(day: int) -> str:
    """Generate prompt focused on incremental changes from previous day."""

    # === PHASE 1: SEED (Days 1-7) ===
    if day == 1:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CENTER OF PLATFORM:
- One perfectly round brown seed (1cm diameter)
- Smooth glossy surface, no cracks
- Sitting in a small depression in the soil

Day 1 - a seed has been planted. Nothing else, just the seed.
"""

    elif day == 2:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The seed now has a tiny hairline crack on top.

CENTER: The same brown seed, but with a small crack forming on its surface.
Everything else IDENTICAL to Day 1.
"""

    elif day == 3:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The crack is slightly larger. A hint of green visible inside.

CENTER: The same seed with a bigger crack. You can see pale green inside the crack.
Everything else IDENTICAL.
"""

    elif day == 4:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The seed is splitting open more.

CENTER: The seed shell is now clearly split, with a tiny pale sprout tip (2mm) just emerging upward.
Everything else IDENTICAL.
"""

    elif day == 5:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout has grown taller.

CENTER: A small pale green sprout (5mm tall) growing from the split seed. The seed shell is still attached at the base of the sprout.
Everything else IDENTICAL.
"""

    elif day == 6:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is taller (now 10mm).

CENTER: The same sprout, now 10mm tall, pale green curved stem. Seed shell still at base.
NO new elements. Everything else IDENTICAL.
"""

    elif day == 7:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is taller (now 15mm) and straightening.

CENTER: The same sprout, now 15mm tall, stem becoming straighter. Seed shell still at base.
NO new elements. Everything else IDENTICAL.
"""

    elif day == 8:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is taller (20mm) and two tiny round leaves are starting to unfold at the top.

CENTER: The same sprout, now 20mm tall. Two tiny round cotyledon leaves (3mm each) just beginning to unfold at the tip. Seed shell at base.
NO new elements. Everything else IDENTICAL.
"""

    elif day == 9:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is taller (25mm) and the cotyledon leaves are more open.

CENTER: The same sprout, now 25mm tall. The two round cotyledon leaves (5mm each) are opening wider. Seed shell at base.
NO new elements. Everything else IDENTICAL.
"""

    elif day == 10:
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is taller (30mm) and leaves fully open.

CENTER: The same sprout, now 30mm tall. Two round cotyledon leaves (7mm each) fully open and horizontal. Seed shell at base.
NO new elements. Everything else IDENTICAL.
"""

    # === Continue pattern for later days ===
    elif day <= 15:
        height_mm = 30 + (day - 10) * 6  # 36mm to 60mm
        return f"""
{PLATFORM_STYLE}

{PLATFORM_ELEMENTS}

CHANGE FROM YESTERDAY: The sprout is slightly taller ({height_mm}mm) and a tiny true leaf is emerging.

CENTER: The same sprout, now {height_mm}mm tall. Two cotyledon leaves open. {day - 10} tiny pointed true leaf/leaves emerging from center between cotyledons.
NO new elements. Everything else IDENTICAL.
"""

    # === PHASE 3: YOUNG PLANT (Days 16-35) ===
    elif day <= 35:
        height_cm = 3 + (day - 15) * 0.2  # 3cm to 7cm
        leaf_pairs = 2 + (day - 15) // 4  # 2 to 7 pairs
        woody = "starting to become" if day < 25 else "noticeably"

        extras = ""
        if day >= 30:
            extras = "- 1-2 small red-capped mushrooms appearing near the plant base"

        return f"""
{PLATFORM_STYLE}

KEEP EXACTLY: platform shape, soil layers, moss patches, pebbles. DO NOT change these.

THE JADE PLANT (Crassula ovata) - growing in center:
- About {height_cm:.1f}cm tall
- {leaf_pairs} pairs of thick fleshy oval leaves
- Leaves are vibrant green with slightly reddish edges
- Stem is {woody} woody at the base
- Plant takes up about 1/4 of vertical space above platform
{extras}

Day {day}/200 - a healthy young jade plant.
Platform elements stay IDENTICAL. ONLY the plant grows.
"""

    # === PHASE 4: MATURING (Days 36-55) ===
    elif day <= 55:
        height_cm = 7 + (day - 35) * 0.15  # 7cm to 10cm

        if day < 42:
            life = """
- A tiny ladybug (red with black spots) resting on one of the leaves
- 2-3 small red-capped mushrooms near the trunk base
- A small snail on the soil near moss"""
        elif day < 50:
            life = """
- Ladybug on a leaf
- 3-4 red-capped mushrooms near trunk
- Snail on soil
- A tiny gnome (2cm tall, red pointed hat, blue outfit) has JUST ARRIVED, standing at edge of platform looking at tree with wonder"""
        else:
            life = """
- Ladybug on leaf
- 4-5 mushrooms near trunk
- Snail present
- The gnome (red hat, blue outfit) is exploring, examining the mushrooms curiously"""

        return f"""
{PLATFORM_STYLE}

KEEP EXACTLY: platform, soil layers, moss patches, pebbles.
KEEP: all previously established elements.

THE JADE PLANT - continuing to mature:
- About {height_cm:.1f}cm tall
- Thickening woody trunk with bark texture
- Multiple small branches starting to form
- Many thick oval leaves creating bushy appearance

LIFE ON THE PLATFORM:
{life}

Day {day}/200 - the platform is becoming a home.
"""

    # === PHASE 5: SETTLING (Days 56-75) ===
    elif day <= 75:
        height_cm = 10 + (day - 55) * 0.1  # 10cm to 12cm

        if day < 65:
            scene = """
- Gnome (red hat) sitting on a pebble, resting
- Ladybug, mushrooms (5-6 now), snail present"""
        else:
            scene = """
- Gnome working on a small stone circle (future campfire)
- Small pile of gathered pebbles nearby
- Ladybug, mushrooms, snail present
- Plant showing first tiny flower buds at branch tips"""

        return f"""
{PLATFORM_STYLE}

KEEP: platform, moss, pebbles. KEEP: gnome, ladybug, mushrooms, snail.

THE JADE PLANT:
- About {height_cm:.1f}cm tall - a proper small tree now
- Thick woody trunk with nice bark texture
- Spreading branches with dense foliage
- Takes up about 1/3 of vertical space

THE GNOME'S PROGRESS:
{scene}

Day {day}/200 - making this place home.
"""

    # === PHASE 6+: Later stages ===
    else:
        height_cm = 12 + (day - 75) * 0.05
        return f"""
{PLATFORM_STYLE}

KEEP ALL previous elements.

THE JADE PLANT: About {height_cm:.1f}cm tall, magnificent small tree.
- Strong woody trunk, spreading branches, dense foliage
- White-pink flowers blooming

SCENE:
- Gnome (red hat) with completed stone campfire ring
- Small sticks arranged inside the ring
- All creatures present (ladybug, mushrooms, snail)

Day {day}/200.
"""


def get_reference_day(day: int) -> int:
    """Use PREVIOUS day as reference for smooth progression."""
    if day <= 1:
        return None
    # Always use the previous day for smooth growth
    return day - 1


def generate_image(day: int) -> Path:
    """Generate image using milestone reference."""
    filepath = OUTPUT_DIR / f"day-{day:03d}.png"

    if filepath.exists():
        print(f"  Day {day:3d}: exists, skipping")
        return filepath

    prompt = get_prompt_for_day(day)
    contents = [prompt]

    # Use PREVIOUS day as reference for smooth growth
    ref_day = get_reference_day(day)
    if ref_day:
        ref_path = OUTPUT_DIR / f"day-{ref_day:03d}.png"
        if ref_path.exists():
            with open(ref_path, "rb") as f:
                ref_bytes = f.read()
            contents = [
                types.Part.from_bytes(data=ref_bytes, mime_type="image/png"),
                f"""This is Day {ref_day}. Create Day {day} with these rules:

1. PLATFORM: Keep EXACTLY identical (same moss, pebbles, soil layers, shape)
2. PLANT: Must be SLIGHTLY LARGER than in this image - it grew overnight
3. DO NOT remove any leaves or features the plant already has
4. The plant can ONLY grow, never shrink

{prompt}"""
            ]

    print(f"  Day {day:3d}: generating...", end=" ", flush=True)

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
                image.save(filepath)
                print("done")
                return filepath

        print("failed")
        return None

    except Exception as e:
        print(f"error: {e}")
        return None


def main():
    print("=" * 60)
    print("V4: Sequential Chain Generation")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR}")
    print()
    print("Each day uses PREVIOUS day as reference for smooth growth.")
    print()

    # Generate sequentially: 1, 2, 3, 4... (each uses previous as reference)
    max_day = 10

    for day in range(1, max_day + 1):
        generate_image(day)
        time.sleep(2)

    print()
    print("=" * 60)
    print(f"Done! Check: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
