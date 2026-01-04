#!/usr/bin/env python3
"""Generate day 75 test images for all theme variations."""

import os
from pathlib import Path
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/theme-tests")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Base isometric style for all themes
BASE_STYLE = """
Isometric 3D view from above at 45 degree angle,
a square platform tile floating in space,
the platform shows layered cross-section on the edges,
claymation stop-motion style,
TRANSPARENT BACKGROUND (PNG with alpha channel),
soft studio lighting with gentle shadows beneath the platform,
highly detailed clay textures,
NO glass container, NO jar, NO enclosure - just the floating platform
"""

THEMES = {
    "crystal": {
        "name": "Crystal Cave",
        "prompt": f"""
{BASE_STYLE}

THEME: CRYSTAL CAVE - mystical underground crystals

The platform is made of dark stone/slate with purple-blue crystal veins visible in the cross-section.

ON TOP of the floating stone platform:
- A magnificent cluster of glowing crystals growing from the center
- Main crystal is about 12cm tall, surrounded by smaller ones
- Colors: deep purple, blue, and cyan with inner glow
- Some crystals are clear/transparent, others opaque
- The crystals emit a soft magical light

AROUND the crystals on the platform surface:
- Dark rocky surface with moss in crevices
- A tiny miner gnome (with pickaxe and helmet lamp) examining a crystal
- Small geodes scattered around, some cracked open showing gems inside
- Glowing mushrooms (bioluminescent blue)
- Tiny cave spider on the rocks
- Small pile of mined gems near the gnome

The platform is about 15cm x 15cm square, tilted to show depth.
Mystical underground cave aesthetic with magical glow.
Day 75 - the crystal garden flourishes deep underground.
"""
    },
    "ocean": {
        "name": "Ocean Coral",
        "prompt": f"""
{BASE_STYLE}

THEME: OCEAN CORAL - underwater reef ecosystem

The platform is made of sandy rock/coral base with visible shells and sand layers in the cross-section.

ON TOP of the floating reef platform:
- A beautiful branching coral formation in the center
- Main coral is about 12cm tall with multiple branches
- Colors: vibrant orange, pink, and purple coral varieties
- Some brain coral, some fan coral, some branching staghorn coral
- Coral looks healthy and vibrant

AROUND the coral on the platform surface:
- Sandy base with small seashells scattered
- A tiny mer-person/mermaid (cute claymation style) tending to the coral
- Colorful tropical fish swimming around (2-3 small ones)
- A friendly octopus peeking from behind a rock
- Sea anemones with clownfish
- Starfish on the sandy floor
- Small treasure chest half-buried in sand

The platform is about 15cm x 15cm square, tilted to show depth.
Vibrant underwater reef aesthetic with tropical colors.
Day 75 - the coral reef teems with life.
"""
    },
    "space": {
        "name": "Space Asteroid",
        "prompt": f"""
{BASE_STYLE}

THEME: SPACE - alien plants on asteroid

The platform is a chunk of asteroid with visible metallic ore and space rock layers in the cross-section, some areas glowing with alien minerals.

ON TOP of the floating asteroid chunk:
- Strange alien plant/tree growing from the center
- About 12cm tall with bioluminescent properties
- Glowing cyan/teal leaves that emit soft light
- Twisted alien trunk with iridescent bark
- Some floating spores/particles around it
- Small alien fruits or pods hanging from branches

AROUND the alien plant on the asteroid surface:
- Rocky grey asteroid surface with glowing mineral veins
- A tiny astronaut/space explorer in a cute spacesuit exploring
- Strange alien mushrooms that glow different colors
- A small friendly alien creature (cute, big eyes)
- Crater marks on the surface
- Tiny space crystals growing
- A small planted flag

The platform is about 15cm x 15cm square, tilted to show depth.
Sci-fi alien world aesthetic with bioluminescence and cosmic wonder.
Day 75 - life thrives even in the void of space.
"""
    },
    "desert": {
        "name": "Desert Oasis",
        "prompt": f"""
{BASE_STYLE}

THEME: DESERT - cacti and succulents in arid landscape

The platform is made of sandy/clay desert earth with visible sediment layers, small fossils, and terracotta-colored bands in the cross-section.

ON TOP of the floating desert platform:
- A magnificent saguaro cactus in the center
- About 12cm tall with characteristic arms
- Healthy green with visible spines (not too sharp looking, clay style)
- Small white/pink cactus flowers blooming on top
- Surrounded by smaller cacti varieties (barrel cactus, prickly pear)

AROUND the cacti on the platform surface:
- Sandy desert floor with small rocks and pebbles
- A tiny desert nomad/explorer (with tiny hat and canteen) resting in shade
- Cute gecko/lizard sunbathing on a rock
- Small scorpion (friendly looking, claymation style)
- Tiny desert flowers blooming (after rain)
- A small oasis puddle with a tiny palm tree
- Tumbleweeds and desert grass tufts

The platform is about 15cm x 15cm square, tilted to show depth.
Warm desert aesthetic with terracotta and sand tones.
Day 75 - the desert blooms with resilient life.
"""
    }
}


def generate_theme(theme_key: str):
    """Generate a single theme's day 75 image."""
    theme = THEMES[theme_key]
    filename = OUTPUT_DIR / f"day-075-{theme_key}.png"

    if filename.exists():
        print(f"  {theme['name']}: already exists, skipping")
        return filename

    print(f"  Generating {theme['name']}...", end=" ", flush=True)

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[theme["prompt"]],
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
                print("✓")
                return filename

        print("✗ (no image)")
        return None

    except Exception as e:
        print(f"✗ ({e})")
        return None


def main():
    """Generate all theme variations."""
    print("=" * 50)
    print("Generating Day 75 Theme Variations")
    print("=" * 50)
    print()

    for theme_key in THEMES:
        generate_theme(theme_key)

    print()
    print("=" * 50)
    print("Done! Check public/diorama/theme-tests/")
    print("=" * 50)


if __name__ == "__main__":
    main()
