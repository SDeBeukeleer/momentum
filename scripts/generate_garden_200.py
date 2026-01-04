#!/usr/bin/env python3
"""Generate all 200 Garden theme images with incremental progression."""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/garden-new")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Base isometric platform style - use bright magenta background for easy removal
BASE_STYLE = """
Isometric 3D view from above at 45 degree angle,
a square earthen platform tile floating in space,
the platform shows layered soil cross-section on the edges (dark rich soil layers, small pebbles, roots visible),
the platform has rounded organic edges like a chunk of earth,
claymation stop-motion style,
BRIGHT MAGENTA/PINK SOLID BACKGROUND (#FF00FF) for easy background removal,
soft studio lighting with gentle shadows beneath the platform,
highly detailed clay textures,
NO glass container, NO jar, NO terrarium, NO enclosure - just the floating earth platform
"""


def get_prompt_for_day(day: int) -> str:
    """Generate the appropriate prompt for a given day with incremental changes."""

    # === PHASE 1: SEED (Days 1-5) ===
    if day <= 5:
        crack_stages = {
            1: "perfectly round seed, no cracks yet, freshly planted",
            2: "seed with a tiny hairline crack beginning to form",
            3: "seed with a small visible crack, moisture beading",
            4: "seed with a pronounced crack, hint of green inside",
            5: "seed splitting open, tiny white root tip emerging"
        }
        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Seed Stage):
- Rich brown soil covering the top surface
- A single brown seed in the center: {crack_stages[day]}
- Seed is about 1cm, clearly visible
- A few tiny moss patches starting to grow on the soil edges
- 2-3 small colorful pebbles decorating the soil
- Soil looks freshly watered, slightly dark and moist

The platform is about 15cm x 15cm square.
Early days - the journey is just beginning.
"""

    # === PHASE 2: SPROUTING (Days 6-15) ===
    elif day <= 15:
        height_mm = (day - 5) * 8  # 8mm to 80mm
        progress = day - 5  # 1 to 10

        if day <= 8:
            desc = f"tiny white/pale green sprout, {height_mm}mm tall, seed shell still attached at base"
            leaves = "no leaves yet, just the sprout tip"
        elif day <= 11:
            desc = f"small green sprout, {height_mm}mm tall, seed shell fallen off"
            leaves = f"{(day-8)} tiny round cotyledon leaves (seed leaves) unfolding"
        else:
            desc = f"young sprout, {height_mm}mm tall, stem thickening slightly"
            leaves = f"2 cotyledons fully open, {day-10} tiny true leaves starting to form"

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Sprouting Stage):
- Rich brown soil with moss patches around the edges
- In the center: {desc}
- Leaves: {leaves}
- The sprout is reaching toward the light
- Small pebbles and moss decorating the soil surface
- Maybe a tiny dewdrop on the sprout

The platform is about 15cm x 15cm square.
New life emerging - growing stronger each day.
"""

    # === PHASE 3: YOUNG PLANT (Days 16-35) ===
    elif day <= 35:
        height_cm = 3 + (day - 15) * 0.25  # 3cm to 8cm
        leaf_pairs = 2 + (day - 15) // 4  # 2 to 7 pairs
        progress = day - 15  # 1 to 20

        stem_desc = "thin green stem" if day < 25 else "stem starting to become woody at the base"
        if day >= 30:
            stem_desc = "noticeably woody lower stem, green upper growth"

        extras = ""
        if day >= 25:
            extras = "- A tiny snail has appeared on the soil, exploring"
        if day >= 30:
            extras += "\n- First tiny red-capped mushroom growing near the base"

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Young Plant Stage):
- Rich soil with lush moss patches and small pebbles
- A young jade plant (Crassula ovata) growing in the center:
  - About {height_cm:.1f}cm tall
  - {leaf_pairs} pairs of thick, fleshy oval leaves
  - {stem_desc}
  - Leaves are vibrant green, some with reddish edges
- The plant takes up about 1/4 of the platform height
{extras}

The platform is about 15cm x 15cm square.
Growing stronger every day - establishing roots.
"""

    # === PHASE 4: MATURING + GNOME ARRIVES (Days 36-55) ===
    elif day <= 55:
        height_cm = 8 + (day - 35) * 0.15  # 8cm to 11cm
        progress = day - 35  # 1 to 20

        if day < 42:
            gnome_status = "NO gnome yet"
            creatures = "- A ladybug resting on one of the leaves\n- Snail on the soil\n- 2-3 red mushrooms near the base"
        elif day == 42:
            gnome_status = "A tiny gnome (red pointed hat, blue outfit) has JUST ARRIVED, standing at the edge of the platform looking at the plant with wonder"
            creatures = "- Ladybug, snail, mushrooms present"
        elif day < 48:
            gnome_status = f"The gnome (red hat, blue outfit) is exploring, currently examining the {'mushrooms' if day < 45 else 'plant trunk'}"
            creatures = "- Ladybug on a leaf\n- Snail nearby\n- 3-4 mushrooms"
        else:
            gnome_status = "The gnome has settled in and is starting to gather small stones in a circle (future campfire spot)"
            creatures = "- Ladybug, snail present\n- 4-5 mushrooms now\n- Small pile of gathered pebbles"

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Maturing Stage):
- Lush soil with moss, pebbles, mushrooms
- The jade plant continues to mature:
  - About {height_cm:.1f}cm tall with thickening trunk
  - Multiple branches starting to form
  - Many thick oval leaves creating bushy appearance
  - Trunk becoming properly woody

LIFE ON THE PLATFORM:
- {gnome_status}
{creatures}

The platform is about 15cm x 15cm square.
The terrarium is becoming a home.
"""

    # === PHASE 5: GNOME SETTLING IN (Days 56-85) ===
    elif day <= 85:
        height_cm = 11 + (day - 55) * 0.1  # 11cm to 14cm
        progress = day - 55  # 1 to 30

        if day < 65:
            gnome_activity = "sitting on a pebble, resting after exploring"
            building = "- Circle of stones laid out (campfire ring foundation)"
        elif day < 72:
            gnome_activity = "actively building the campfire ring, placing stones carefully"
            building = "- Campfire ring taking shape (stones stacked)\n- Small pile of tiny sticks gathered for fire"
        elif day < 78:
            gnome_activity = "adding sticks to the completed campfire ring"
            building = "- Campfire ring COMPLETE with stones\n- Sticks arranged inside\n- Tiny wooden sign planted: 'Home'"
        else:
            gnome_activity = "warming hands by a small glowing campfire!"
            building = "- CAMPFIRE NOW LIT with tiny orange flames!\n- Smoke wisps rising\n- Wooden sign nearby\n- Gnome's tiny backpack set down"

        flowers = ""
        if day >= 75:
            flowers = "- Plant now has small white-pink flower BUDS forming at branch tips"
        if day >= 80:
            flowers = "- Plant has 2-3 small white-pink FLOWERS opening!"

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Settling In):
- Rich soil with lush moss, pebbles, mushrooms (5-6 now)
- The jade plant grows taller:
  - About {height_cm:.1f}cm tall - becoming a proper small tree
  - Thick woody trunk with nice bark texture
  - Spreading branches with dense foliage
{flowers}

THE GNOME'S PROGRESS:
- The gnome (red pointed hat, blue outfit) is {gnome_activity}
{building}

OTHER LIFE:
- Ladybug, snail present
- A butterfly has appeared, fluttering near the top

The platform is about 15cm x 15cm square.
Making this place home.
"""

    # === PHASE 6: BUILDING HOUSE (Days 86-115) ===
    elif day <= 115:
        height_cm = 14 + (day - 85) * 0.07  # 14cm to 16cm
        progress = day - 85  # 1 to 30

        if day < 92:
            construction = """- Gnome measuring and planning with tiny blueprint
- Foundation stones being laid (flat stones in a square)
- Campfire burning nearby for warmth while working
- Small pile of building materials (twigs, clay chunks)"""
        elif day < 100:
            construction = f"""- WALLS GOING UP! Tiny house frame {(day-92)*12}% complete
- Gnome actively hammering with tiny tools
- Walls made of clay and tiny sticks
- Door frame visible
- Campfire crackling nearby
- "UNDER CONSTRUCTION" tiny sign"""
        elif day < 108:
            construction = f"""- House walls COMPLETE, roof being added
- Gnome on tiny ladder working on roof
- Roof made of layered leaves/bark
- Window hole cut out
- Chimney being built
- Tool bench with tiny tools nearby"""
        else:
            construction = """- HOUSE NEARLY COMPLETE!
- Proper door installed (tiny wooden door)
- Window with tiny frame
- Roof finished with leaf shingles
- Chimney complete
- Gnome adding finishing touches (painting/decorating)
- Pebble path started leading to door"""

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Building Phase):
- Lush platform with moss, mushrooms (6-7), flowers
- The jade plant flourishes:
  - About {height_cm:.1f}cm tall - magnificent small tree
  - Thick gnarled trunk
  - Wide branching canopy with many leaves
  - White-pink star flowers blooming throughout

CONSTRUCTION PROGRESS:
{construction}

OTHER LIFE:
- Ladybug, snail, butterfly present
- A tiny bird has appeared, watching curiously

The platform is about 15cm x 15cm square.
Building a dream home!
"""

    # === PHASE 7: HOUSE COMPLETE + COMMUNITY (Days 116-155) ===
    elif day <= 155:
        height_cm = 16 + (day - 115) * 0.05  # 16cm to 18cm
        progress = day - 115  # 1 to 40

        if day < 125:
            scene = """- HOUSE COMPLETE! Cozy tiny cottage with:
  - Wooden door (slightly open, warm glow inside)
  - Window with tiny curtains
  - Chimney with smoke rising
  - Pebble path to front door
- Gnome proudly standing by their home
- Small fence posts being installed (garden fence starting)"""
        elif day < 135:
            scene = """- Cozy cottage with smoking chimney
- Fenced garden area started (tiny vegetable garden!)
- SECOND GNOME HAS ARRIVED! (blue pointed hat)
- The two gnomes meeting/greeting each other
- 1-2 tiny lanterns hanging from low branches
- Garden has tiny planted seedlings"""
        elif day < 145:
            scene = """- Cottage with both gnomes living together
- Fenced vegetable garden with tiny veggies growing!
- 3-4 lanterns on branches (glowing warmly)
- A tiny bird has built a NEST in upper branches
- Small well being constructed
- Gnomes doing different activities (one gardening, one by fire)"""
        else:
            scene = """- Thriving homestead!
- Cottage with warm glowing windows
- Vegetable garden producing tiny crops
- Stone WELL complete with tiny bucket
- Multiple lanterns glowing
- Bird nest with small BIRD visible
- Both gnomes busy with daily activities
- More mushrooms, snail has a friend now (2 snails)
- Tiny clothesline with mini clothes drying"""

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Community Growing):
- Abundant platform covered in moss, flowers, mushrooms (8+)
- The jade plant is magnificent:
  - About {height_cm:.1f}cm tall - ancient-looking small tree
  - Very thick gnarled trunk with beautiful bark
  - Expansive canopy reaching toward edges
  - Abundant flowers throughout

THE GROWING COMMUNITY:
{scene}

CREATURES:
- Ladybug, butterfly, snails, bird
- Occasional bee visiting flowers

The platform is about 15cm x 15cm square.
A community is flourishing!
"""

    # === PHASE 8: THRIVING VILLAGE (Days 156-200) ===
    else:
        height_cm = 18 + (day - 155) * 0.04  # 18cm to 20cm
        progress = day - 155  # 1 to 45

        if day < 170:
            village = """- THIRD GNOME ARRIVES! (green hat) - Being welcomed by the others
- Two cottages now (second one being built or just finished)
- Expanded garden with variety of tiny vegetables
- TREEHOUSE platform starting in the branches!
- Tiny ladder going up to treehouse
- Multiple lanterns creating cozy atmosphere
- Well, garden, paths all established"""
        elif day < 185:
            village = """- Three gnomes living happily
- Two complete cottages with smoking chimneys
- Treehouse platform COMPLETE in the branches
- One gnome relaxing in treehouse
- A SWING hanging from a branch (gnome swinging!)
- Small POND appeared (with reflective surface)
- One gnome fishing at the tiny pond
- Fairy lights strung between branches"""
        elif day < 195:
            village = """- Thriving three-gnome village
- Two cottages, treehouse, swing
- Pond with tiny wooden bridge over it
- FIREFLIES appearing (glowing dots in the air)
- Fairy lights throughout branches
- Bird nest now has BABY BIRDS
- Gnomes doing activities: fishing, swinging, gardening
- Tiny picnic setup (blanket, tiny food)
- More creatures: bees, butterflies, snails"""
        else:
            village = """- ULTIMATE THRIVING WORLD!
- Three gnomes: one fishing at pond, one on swing, one having picnic
- Two cozy cottages with smoking chimneys and glowing windows
- Treehouse with tiny furnishings visible
- Pond with wooden bridge, lily pads
- Swing gently swaying
- MANY fairy lights and fireflies creating magical glow
- Bird nest with baby birds chirping
- Tiny clothesline with clothes
- Lush vegetable garden with harvest ready
- Multiple lanterns
- ALL creatures present: ladybugs, butterflies, bees, snails, bird family
- Some aerial roots hanging from ancient tree
- Maximum detail - the most magical miniature world possible!"""

        return f"""
{BASE_STYLE}

ON TOP of the floating earth platform (Day {day}/200 - Thriving Village):
- Incredibly lush platform overflowing with life
- The jade plant has reached MAXIMUM GLORY:
  - About {height_cm:.1f}cm tall - fills most of vertical space
  - Massive ancient trunk with beautiful gnarled texture
  - Expansive canopy touching edges
  - Abundant flowers and some tiny fruits
  - Looks ancient, wise, magnificent
  - Some aerial roots hanging down

THE THRIVING VILLAGE:
{village}

The platform is about 15cm x 15cm square.
A complete, magical, thriving world!
"""


def generate_image(day: int) -> bool:
    """Generate a single day's image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Day {day:3d}: exists, skipping")
        return True

    prompt = get_prompt_for_day(day)

    print(f"  Day {day:3d}: generating...", end=" ", flush=True)

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
                print("✓")
                return True

        print("✗ (no image)")
        return False

    except Exception as e:
        print(f"✗ ({e})")
        return False


def main():
    """Generate all 200 images."""
    print("=" * 60)
    print("GENERATING ALL 200 GARDEN THEME IMAGES")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print()

    success_count = 0
    failed_days = []

    for day in range(1, 201):
        if generate_image(day):
            success_count += 1
        else:
            failed_days.append(day)

        # Rate limiting
        time.sleep(1.5)

        # Progress update every 25 days
        if day % 25 == 0:
            print(f"\n  === Progress: {day}/200 ({success_count} successful) ===\n")

    print()
    print("=" * 60)
    print(f"DONE! Generated {success_count}/200 images")
    if failed_days:
        print(f"Failed days: {failed_days}")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print()
    print("Next step: Run remove_backgrounds.py to make them transparent")
    print("=" * 60)


if __name__ == "__main__":
    main()
