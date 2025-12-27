#!/usr/bin/env python3
"""Generate test diorama images using Gemini API."""

import os
from pathlib import Path

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Base style for consistency
BASE_STYLE = """
claymation stop-motion style, miniature diorama inside a cute round glass terrarium jar,
soft warm studio lighting, cozy aesthetic, highly detailed clay texture,
rich brown soil base with tiny pebbles, whimsical and charming,
tilt-shift photography effect, shallow depth of field,
the terrarium sits on a rustic wooden surface
"""

# Test images at key milestone days
TEST_PROMPTS = {
    1: f"A tiny brown seed half-buried in rich dark soil, the seed has a small crack forming on top hinting at life within, {BASE_STYLE}",

    7: f"A small green sprout with two tiny round cotyledon leaves emerging from the soil, the seed shell still visible at the base, fresh and delicate, {BASE_STYLE}",

    14: f"A young seedling plant with 4-5 small vibrant green leaves on a thin stem, the plant is about 2 inches tall, some tiny roots visible at soil surface, {BASE_STYLE}",

    30: f"A healthy bushy plant with many lush green leaves and small flower buds just starting to form, the stem is sturdy, some decorative moss around the base, {BASE_STYLE}",

    50: f"A beautiful flowering plant in full bloom with colorful pink and white flowers, abundant green foliage, a tiny ladybug on one leaf, magical and vibrant, {BASE_STYLE}",

    75: f"A magnificent mature plant with large flowers and dense foliage, some flowers turning into seed pods, the plant fills most of the terrarium, lush and thriving, {BASE_STYLE}",

    100: f"An ancient magical bonsai-like tree with a thick gnarled trunk, crystalline leaves that seem to glow softly, tiny fairy lights floating around it, mystical and wise appearance, ethereal atmosphere, {BASE_STYLE}",

    150: f"A legendary mythical tree with golden and silver leaves, soft magical glow emanating from within, tiny sparkling particles floating in the air, the tree has an otherworldly celestial beauty, aurora-like colors, {BASE_STYLE}",

    200: f"The ultimate transcendent cosmic tree, its leaves contain tiny galaxies and stars, prismatic rainbow light effects, the most beautiful and magical plant imaginable, divine and awe-inspiring, particles of stardust swirling around, {BASE_STYLE}",
}


def generate_image(day: int, prompt: str) -> bool:
    """Generate a single plant image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Skipping day {day} (already exists)")
        return True

    print(f"Generating day {day}...")

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
                print(f"  ✓ Saved: {filename}")
                return True

        print(f"  ✗ No image in response for day {day}")
        return False

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Generate all test images."""
    print("=" * 50)
    print("Generating test diorama images")
    print("=" * 50)
    print()

    success_count = 0
    for day, prompt in TEST_PROMPTS.items():
        if generate_image(day, prompt):
            success_count += 1
        print()

    print("=" * 50)
    print(f"Done! Generated {success_count}/{len(TEST_PROMPTS)} images")
    print(f"Images saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
