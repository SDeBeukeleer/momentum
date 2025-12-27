#!/usr/bin/env python3
"""Generate v4 terrarium images - bigger jar, persistent elements, continuous growth."""

import os
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v4")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# New bigger terrarium style
TERRARIUM_STYLE = """
A large bell jar terrarium (cloche style) - tall and spacious with a round knob handle on top,
clear glass with subtle reflections, sitting on a round wooden base,
plenty of room inside for a growing plant and miniature world,
plain solid cream/beige background for easy cutout,
claymation stop-motion style, soft even studio lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition
"""

# Test images to generate
# Days 1-75: Plant growth (3 images)
# Days 50+: Life begins and evolves (4 images showing life phases)

STAGES = {
    # === PLANT GROWTH PHASE ===
    1: {
        "name": "Seed",
        "reference": None,  # Start fresh
        "prompt": f"""
Create a claymation terrarium diorama:

{TERRARIUM_STYLE}

Inside the terrarium:
- Rich brown soil with small pebbles filling the bottom third
- A single small brown seed half-buried in the center of the soil
- The seed has a tiny crack forming on top
- A few tiny moss patches on the soil
- Empty space above, waiting for growth

This is day 1 - just a planted seed, nothing else yet.
"""
    },

    25: {
        "name": "Young Plant",
        "reference": "day-001.png",
        "prompt": """
Evolve this terrarium to day 25:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

THE PLANT HAS GROWN:
- The seed has sprouted into a young jade plant (Crassula ovata)
- About 4cm tall now with a small woody stem
- Two pairs of thick fleshy oval leaves
- The stem is starting to thicken at the base
- Small roots visible at soil surface

The soil and moss remain similar. The terrarium has lots of empty space still.
The plant is growing but still small compared to the jar size.
"""
    },

    50: {
        "name": "Mature Plant + First Visitor",
        "reference": "day-025.png",
        "prompt": """
Evolve this terrarium to day 50:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

THE PLANT HAS GROWN MORE:
- The jade plant is now about 8cm tall - a proper small tree
- Thick woody trunk with nice branching structure
- Many pairs of plump oval leaves creating a bushy canopy
- The plant takes up maybe 1/3 of the vertical space now
- Still has room to grow taller

NEW - FIRST SIGNS OF LIFE:
- A tiny cute gnome (about 1.5cm tall) with a red pointed hat has arrived
- The gnome is peeking curiously from behind the trunk, just discovering the place
- A small ladybug rests on one of the leaves
- 2-3 small red-capped mushrooms growing in the soil near the base

This is the beginning of life in the terrarium - the gnome just arrived.
"""
    },

    75: {
        "name": "Growing Plant + Settlement Begins",
        "reference": "day-050.png",
        "prompt": """
Evolve this terrarium to day 75:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

KEEP THESE ELEMENTS (they were added before):
- The gnome with red pointed hat (still there!)
- The ladybug (can be on a different leaf)
- The mushrooms at the base

THE PLANT HAS GROWN MORE:
- The jade plant is now about 12cm tall - getting impressive
- Thicker trunk, more branches spreading out
- Fuller canopy of leaves, some with slight red edges
- The plant now takes up about half the vertical space
- Small white flower buds starting to form

NEW ADDITIONS:
- The gnome is now busy - holding a tiny shovel, starting to dig
- A small pile of dirt from digging
- A tiny campfire ring made of small stones (unlit, just prepared)
- A snail slowly crossing the soil
- A few more mushrooms have grown

The gnome is settling in and starting to make this place home.
"""
    },

    100: {
        "name": "Larger Plant + House Being Built",
        "reference": "day-075.png",
        "prompt": """
Evolve this terrarium to day 100:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

KEEP ALL THESE ELEMENTS (added before):
- The gnome with red pointed hat
- The ladybug
- The mushrooms (maybe a few more now)
- The campfire ring of stones
- The snail (different position)

THE PLANT HAS GROWN MORE:
- The jade plant is now about 15cm tall - a magnificent tree
- Very thick gnarled trunk showing age
- Wide spreading branches with dense foliage
- White-pink star flowers now blooming in clusters
- The plant fills about 2/3 of the vertical space but still has room

NEW ADDITIONS:
- A tiny house is being built! Half-constructed from tiny twigs and clay
- The gnome is working on it with a tiny hammer
- A small wooden sign stuck in the soil
- The campfire now has tiny sticks and a small glow/flame
- A butterfly fluttering near the top
- Tiny pebble path starting to form

The gnome is building a home - construction in progress!
"""
    },

    140: {
        "name": "Tall Plant + Complete Home",
        "reference": "day-100.png",
        "prompt": """
Evolve this terrarium to day 140:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

KEEP ALL THESE ELEMENTS (added before):
- The gnome with red pointed hat (now has a friend!)
- The ladybug, mushrooms, snail
- The campfire ring (now a cozy fire)
- The wooden sign
- The butterfly
- The pebble path (now more complete)

THE PLANT HAS GROWN MORE:
- The jade plant is now about 18cm tall - truly ancient looking
- Massive thick trunk with beautiful gnarled texture
- Expansive canopy nearly reaching the top of the jar
- Flowers in full bloom, some forming seed pods
- A few branches touch the glass walls

NEW ADDITIONS:
- The tiny house is now COMPLETE with door, window, and chimney with smoke
- A second gnome has arrived (blue pointed hat) - they're friends now
- A tiny fence around a small garden patch with mini vegetables
- 2-3 tiny lanterns hanging from lower branches (glowing warmly)
- A small bird nest in the upper branches with a tiny bird
- A miniature well made of tiny stones
- The pebble path now leads to the house door

A cozy home has been established - two gnomes living happily!
"""
    },

    200: {
        "name": "Maximum Growth + Thriving Village",
        "reference": "day-140.png",
        "prompt": """
Evolve this terrarium to day 200 - the ultimate stage:

KEEP EXACTLY THE SAME:
- The same tall bell jar terrarium with knob handle
- The same wooden base
- The same camera angle and background
- The same claymation style

KEEP ALL PREVIOUS ELEMENTS:
- Both gnomes (red and blue hats) - now add a third (green hat)
- The complete house with smoking chimney
- The fenced garden with vegetables
- The lanterns, bird nest with bird, well
- The campfire, mushrooms, snail, ladybug, butterfly
- The pebble path, wooden sign

THE PLANT HAS REACHED MAXIMUM SIZE:
- The jade plant now fills the entire upper portion of the jar
- Massive ancient trunk, incredibly thick and textured
- Canopy touches the top and sides of the glass
- Abundant flowers and seed pods throughout
- The tree looks ancient, wise, and magnificent
- Some aerial roots hanging down

NEW ADDITIONS FOR THE ULTIMATE SCENE:
- A THIRD gnome (green hat) has joined the community
- A second tiny house (different style) has been built
- A tiny treehouse platform in the branches with a small ladder
- One gnome on a tiny swing hanging from a branch
- One gnome fishing at a tiny pond (small water feature with ripples)
- One gnome having a picnic on a tiny blanket with mini food
- Tiny clothesline with miniature clothes drying
- The bird nest now has baby birds peeking out
- Fireflies (small glowing dots) floating around
- Fairy lights/tiny lanterns strung between branches
- A small bridge made of twigs
- The most cozy, detailed, alive miniature world imaginable

This is the ultimate reward - a complete thriving village under an ancient tree!
"""
    },
}


def generate_image(day: int, stage_info: dict) -> Path:
    """Generate a single stage image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Skipping day {day} (already exists)")
        return filename

    print(f"Generating day {day}: {stage_info['name']}...")

    contents = [stage_info['prompt']]

    # Add reference image if specified
    if stage_info['reference']:
        ref_path = OUTPUT_DIR / stage_info['reference']
        if ref_path.exists():
            ref_image = Image.open(ref_path)
            contents = [stage_info['prompt'], ref_image]
            print(f"  Using reference: {stage_info['reference']}")
        else:
            print(f"  Warning: Reference {stage_info['reference']} not found, generating without it")

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
                print(f"  ✓ Saved: {filename}")
                return filename

        print(f"  ✗ No image in response")
        return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def main():
    """Generate all v4 terrarium images."""
    print("=" * 60)
    print("Generating V4 Terrarium Images")
    print("Bigger jar, persistent elements, continuous growth")
    print("=" * 60)
    print()

    for day in sorted(STAGES.keys()):
        stage_info = STAGES[day]
        result = generate_image(day, stage_info)
        if result is None and stage_info['reference']:
            print(f"  Retrying without reference...")
            stage_info_copy = stage_info.copy()
            stage_info_copy['reference'] = None
            generate_image(day, stage_info_copy)
        print()

    print("=" * 60)
    print(f"Done! Images saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
