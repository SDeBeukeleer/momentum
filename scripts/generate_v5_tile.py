#!/usr/bin/env python3
"""
V5: Floating tile version using the EXACT same approach as the glass bell script.
Mirror the glass bell prompt structure but with floating tile instead.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v5-tile")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Floating tile style - consistent across all images (mirrors TERRARIUM_STYLE)
TILE_STYLE = """
A floating isometric earth platform tile - square (15x15cm) with rounded organic edges,
visible soil cross-section showing layers (dark brown top, reddish clay middle, dark bottom),
light tan raised rim around top edge, small roots poking from sides,
plain solid bright blue background (#0000FF) for easy cutout,
claymation stop-motion style, soft even studio lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition, gentle shadow beneath
"""


def get_prompt_for_day(day: int) -> str:
    """Generate the appropriate prompt for a given day - mirrors glass bell structure."""

    # === PHASE 1: SEED (Days 1-5) ===
    if day <= 5:
        crack_progress = ["tiny", "small", "visible", "pronounced", "splitting"][min(day-1, 4)]
        return f"""
{TILE_STYLE}

On top of the platform:
- Rich brown soil with 4 fluffy green moss patches in corners
- Blue pebble near top-left, orange pebble right side, yellow pebble bottom
- A single brown seed in the center with a {crack_progress} crack forming
- Plenty of empty space above the seed

Day {day} - the seed is just beginning its journey.
"""

    # === PHASE 2: SPROUTING (Days 6-15) ===
    elif day <= 15:
        sprout_height = (day - 5) * 0.3  # 0.3cm to 3cm
        leaves = min((day - 5) // 2, 4)  # 0 to 4 leaf pairs
        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches in corners, pebbles (blue, orange, yellow).

The seed has sprouted into a tiny jade plant (Crassula ovata):
- About {sprout_height:.1f}cm tall
- {leaves} pair(s) of small thick oval leaves
- Thin green stem just starting to form
- The seed shell may still be visible at the base

Day {day} - a tiny sprout reaching for light.
"""

    # === PHASE 3: YOUNG PLANT (Days 16-35) ===
    elif day <= 35:
        height = 3 + (day - 15) * 0.2  # 3cm to 7cm
        leaf_pairs = 2 + (day - 15) // 4  # 2 to 7 pairs
        woody = "starting to become" if day < 25 else "noticeably"
        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.

The jade plant is growing stronger:
- About {height:.0f}cm tall
- {leaf_pairs} pairs of thick fleshy oval leaves
- Stem is {woody} woody at the base
- Small visible roots at soil surface
- The plant takes up about 1/4 of the vertical space above platform

Day {day} - a healthy young jade plant.
"""

    # === PHASE 4: MATURING + FIRST LIFE (Days 36-55) ===
    elif day <= 55:
        height = 7 + (day - 35) * 0.15  # 7cm to 10cm

        # Life appears gradually
        if day < 45:
            life_desc = "A tiny ladybug rests on one of the leaves"
        elif day < 50:
            life_desc = """
- A tiny ladybug on a leaf
- 2-3 small red-capped mushrooms growing near the base"""
        else:
            life_desc = """
- A tiny cute gnome (red pointed hat, blue outfit) has just arrived, peeking curiously from behind the trunk
- A ladybug on a leaf
- 3-4 red-capped mushrooms in the soil"""

        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.

The jade plant continues to mature:
- About {height:.0f}cm tall with a thickening trunk
- Multiple branches starting to form
- Many thick oval leaves creating a bushy appearance
- Trunk becoming properly woody

NEW - First signs of life:
{life_desc}

Day {day} - the platform is becoming a home.
"""

    # === PHASE 5: SETTLING IN (Days 56-85) ===
    elif day <= 85:
        height = 10 + (day - 55) * 0.1  # 10cm to 13cm

        # Progressive additions
        if day < 65:
            additions = """
- The gnome (red hat) is exploring, maybe sitting on a pebble
- Ladybug, mushrooms present
- A snail has appeared on the soil"""
        elif day < 75:
            additions = """
- The gnome is busy with a tiny shovel, digging near the trunk
- Small pile of dirt from digging
- A circle of small stones (future campfire)
- Ladybug, mushrooms, snail all present"""
        else:
            additions = """
- The gnome has set up a small campfire ring (stones with tiny sticks)
- A tiny wooden sign in the soil
- The gnome holds tools, preparing to build
- Ladybug, mushrooms (more now), snail present
- Plant has small white flower buds forming"""

        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.
KEEP all previous elements (gnome, ladybug, mushrooms, snail).

The jade plant grows taller:
- About {height:.0f}cm tall - a proper small tree now
- Thick woody trunk with nice texture
- Spreading branches with dense foliage

The gnome is settling in:
{additions}

Day {day} - the gnome is making this place home.
"""

    # === PHASE 6: BUILDING (Days 86-115) ===
    elif day <= 115:
        height = 13 + (day - 85) * 0.1  # 13cm to 16cm

        if day < 95:
            building = """
- Foundation laid: small flat stones arranged in a square
- Gnome actively working with tiny hammer
- Small pile of building materials (twigs, clay)
- A butterfly has appeared"""
        elif day < 105:
            building = """
- Walls going up! Tiny house frame visible (half-built)
- Gnome working hard with tools
- "GNOME HOME" wooden sign planted
- The campfire now has a small flame
- Butterfly fluttering near top"""
        else:
            building = """
- House nearly complete - has walls, tiny door frame, roof being added
- Gnome putting finishing touches
- Campfire burning cozily
- Pebble path forming toward the house
- Plant now has white-pink flowers blooming"""

        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.
KEEP: gnome, campfire ring, sign, ladybug, mushrooms, snail, butterfly.

The jade plant flourishes:
- About {height:.0f}cm tall
- Magnificent thick trunk
- Wide branching canopy
- White-pink star flowers appearing

BUILDING PROGRESS:
{building}

Day {day} - construction is underway!
"""

    # === PHASE 7: HOME COMPLETE + COMMUNITY (Days 116-155) ===
    elif day <= 155:
        height = 16 + (day - 115) * 0.05  # 16cm to 18cm

        if day < 125:
            community = """
- The tiny house is COMPLETE! Door, window, chimney with smoke
- Gnome admiring their work proudly
- Pebble path leads to the front door
- A small fence started around a garden area"""
        elif day < 140:
            community = """
- A SECOND gnome has arrived! (blue pointed hat)
- Complete house with smoking chimney
- Fenced garden with tiny vegetables growing
- 2-3 lanterns hanging from lower branches
- A bird has built a nest in upper branches"""
        else:
            community = """
- Two gnomes living happily (red and blue hats)
- Cozy house, fenced vegetable garden
- Glowing lanterns on branches
- Stone well near the house
- Bird nest with small bird visible
- More mushrooms, the snail has friends"""

        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.
KEEP ALL previous elements and BUILD on them.

The jade plant is now magnificent:
- About {height:.0f}cm tall - ancient looking
- Very thick gnarled trunk
- Expansive canopy with abundant flowers

COMMUNITY GROWS:
{community}

Day {day} - a cozy home has been established.
"""

    # === PHASE 8: THRIVING VILLAGE (Days 156-200) ===
    else:
        height = 18 + (day - 155) * 0.04  # 18cm to 20cm

        if day < 170:
            village = """
- A THIRD gnome arrives (green hat)!
- Two complete houses now
- Expanded garden with tiny crops
- Treehouse platform starting to be built in branches
- Tiny ladder going up"""
        elif day < 185:
            village = """
- Three gnomes doing different activities
- One gnome on a tiny swing hanging from a branch
- Treehouse with ladder complete
- A small pond (reflective surface with ripples)
- One gnome fishing at the pond
- Tiny clothesline with miniature clothes"""
        elif day < 195:
            village = """
- Thriving community of three gnomes
- One swinging, one fishing, one gardening
- Fireflies (glowing dots) appearing
- Fairy lights strung between branches
- Bird nest now has baby birds
- Tiny bridge over the pond
- A gnome having a picnic with tiny blanket and food"""
        else:
            village = """
- ULTIMATE SCENE - maximum detail and life!
- Three gnomes: fishing at pond, on swing, having picnic
- Two houses with smoking chimneys
- Treehouse with ladder
- Pond with bridge, fishing gnome
- Swing hanging from branch
- Fairy lights and fireflies glowing
- Bird nest with baby birds
- Tiny clothesline with clothes
- Fenced garden with vegetables
- Multiple lanterns glowing warmly
- All creatures present: ladybug, butterfly, snail, bird
- The most magical, cozy, alive miniature world!"""

        return f"""
{TILE_STYLE}

KEEP the same platform, soil, moss patches, pebbles.
KEEP ALL previous elements - this is the accumulation of everything!

The jade plant has reached its maximum glory:
- About {height:.0f}cm tall - fills the upper space
- Massive ancient trunk with beautiful texture
- Canopy spreading wide
- Abundant flowers throughout
- Some aerial roots hanging down
- Looks wise and magnificent

THRIVING VILLAGE:
{village}

Day {day} - a complete thriving world under an ancient tree!
"""


def get_reference_day(day: int) -> int:
    """Get the best reference image day for a given day - mirrors glass bell approach."""
    # Use closest lower milestone as reference
    milestones = [1, 25, 50, 75, 100, 140, 200]

    for i, m in enumerate(milestones):
        if day <= m:
            if i == 0:
                return None  # No reference for day 1
            return milestones[i-1]
    return milestones[-2]  # Use 140 for anything beyond


def generate_image(day: int, use_reference: bool = True) -> Path:
    """Generate a single day's image - mirrors glass bell approach."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Day {day}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    contents = [prompt]

    # Add reference image if available and requested
    ref_day = get_reference_day(day)
    if use_reference and ref_day:
        ref_path = OUTPUT_DIR / f"day-{ref_day:03d}.png"
        if ref_path.exists():
            ref_image = Image.open(ref_path)
            contents = [
                f"Use this image as reference for style, platform shape, and existing elements. Evolve it to day {day}:\n\n" + prompt,
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
    """Generate images - mirrors glass bell main function."""
    print("=" * 60)
    print("V5: Floating Tile (Glass Bell Approach)")
    print("=" * 60)
    print()

    # Test with first 15 days
    max_day = 15

    # Key milestone days
    milestones = [1]

    # First ensure milestone exists
    print("Phase 1: Generating milestone day 1...")
    generate_image(1)
    time.sleep(2)
    print()

    # Generate remaining days
    print(f"Phase 2: Generating days 2-{max_day}...")
    for day in range(2, max_day + 1):
        result = generate_image(day)
        if result is None:
            # Retry once
            time.sleep(3)
            generate_image(day, use_reference=False)
        time.sleep(2)

    print()
    print("=" * 60)

    # Count successful images
    images = list(OUTPUT_DIR.glob("day-*.png"))
    print(f"Done! Generated {len(images)} images")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
