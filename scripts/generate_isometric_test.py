#!/usr/bin/env python3
"""Generate test isometric platform image for day 75."""

import os
from pathlib import Path
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/isometric-test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# New isometric platform style - no terrarium/glass bell
PLATFORM_STYLE = """
Isometric 3D view from above at 45 degree angle,
a square earthen platform tile floating in space,
the platform shows layered soil cross-section on the edges (dark rich soil layers, small pebbles visible),
the platform has rounded organic edges like a chunk of earth,
claymation stop-motion style,
TRANSPARENT BACKGROUND (PNG with alpha channel),
soft studio lighting with gentle shadows beneath the platform,
highly detailed clay textures,
NO glass container, NO jar, NO enclosure - just the floating earth platform
"""


def generate_day_75():
    """Generate the day 75 test image."""
    day = 75
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    prompt = f"""
{PLATFORM_STYLE}

ON TOP of the floating earth platform:
- A beautiful mature jade plant/small tree about 12cm tall
- Thick gnarled woody trunk with nice bark texture
- Spreading branches with dense thick oval leaves
- Small white-pink flower clusters starting to bloom
- The plant is the centerpiece, taking up about half the platform

AROUND the plant on the platform surface:
- Rich brown soil with moss patches
- A tiny cute gnome (red pointed hat, blue outfit) building a small stone campfire ring
- A few red-capped mushrooms near the trunk
- Colorful small pebbles scattered around
- A tiny ladybug on one of the leaves
- A snail slowly moving across the soil

The platform is about 15cm x 15cm square, tilted to show depth.
Magical cozy miniature world aesthetic.
Day {day} - the gnome is making this floating island home.
"""

    print(f"Generating day {day} with isometric platform style...")
    print(f"Prompt: {prompt[:200]}...")
    print()

    try:
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
                image.save(filename)
                print(f"Success! Saved to: {filename}")
                return filename

        print("Failed - no image in response")
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    generate_day_75()
    print()
    print("Check the image at: public/diorama/isometric-test/day-075.png")
    print("If you like it, we can generate all 200 images with this style!")
