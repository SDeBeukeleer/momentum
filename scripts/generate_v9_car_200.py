#!/usr/bin/env python3
"""
V9: Complete 200-Day Car Restoration Journey
A rusted Porsche shell transformed into a dream machine over 200 days.
"""

import os
import time
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v9-car-200")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Base style - concrete garage floor platform
BASE_STYLE = """
A floating isometric concrete garage floor platform (20x20cm square) with exposed brick edges,
the concrete surface is slightly worn with oil stains and tire marks,
the brick edge is reddish-brown, weathered look,
plain solid bright blue background (#0000FF), completely flat, NO gradients,
neutral white studio lighting ONLY, NO colored environmental light, NO color cast,
claymation stop-motion style, soft even lighting,
highly detailed clay textures, miniature diorama aesthetic,
centered in frame, clean composition, warm nostalgic garage feeling
"""

# All 200 day descriptions
DAY_DESCRIPTIONS = {
    # === PHASE 1: The Skeleton & Shop Setup (Days 1-40) ===
    1: "Bare concrete slab on bricks. A rusted, hollow metal car shell (no wheels, no engine, no doors). Just the skeleton of a vintage Porsche 356.",
    2: "KEEP: rusted car shell. NEW: A small red toolbox appears in the far left corner of the platform.",
    3: "KEEP: rusted car shell, red toolbox. NEW: A single metal wrench is placed on the floor next to the shell.",
    4: "KEEP: rusted car shell, red toolbox, wrench. NEW: A car jack is placed near the rear of the car.",
    5: "KEEP: rusted car shell, red toolbox, wrench, car jack. NEW: The mechanic (bearded man in blue overalls) appears, looking at the car with a clipboard.",
    6: "KEEP: all previous elements, mechanic. NEW: The mechanic is now holding a wire brush, scrubbing a small patch of rust on the car.",
    7: "KEEP: all previous elements. NEW: A wooden workbench appears in the background.",
    8: "KEEP: all previous elements, workbench. NEW: A desk lamp is placed on the workbench.",
    9: "KEEP: all previous elements. NEW: The mechanic is under the car; only his legs are sticking out.",
    10: "KEEP: all previous elements. NEW: A single rusted wheel rim is leaning against the workbench.",
    11: "KEEP: all previous elements, first wheel rim. NEW: A second rusted wheel rim appears next to the first.",
    12: "KEEP: all previous elements, two wheel rims. NEW: The mechanic is cleaning the first wheel rim with a cloth.",
    13: "KEEP: all previous elements. CHANGE: The first wheel rim is now shiny silver (cleaned).",
    14: "KEEP: all previous elements. CHANGE: The second wheel rim is now shiny silver (cleaned).",
    15: "KEEP: all previous elements, two shiny rims. NEW: A third and fourth wheel rim appear, both rusted.",
    16: "KEEP: all previous elements. CHANGE: All four wheel rims are now shiny silver.",
    17: "KEEP: all previous elements, four shiny rims. NEW: An engine block (bare metal) is placed on the workbench.",
    18: "KEEP: all previous elements, engine block. NEW: The mechanic is bolting a small part onto the engine block.",
    19: "KEEP: all previous elements. NEW: A set of spark plug wires is added to the engine.",
    20: "KEEP: all previous elements. CHANGE: The engine is now complete with a fan belt and chrome cover.",
    21: "KEEP: all previous elements, complete engine. NEW: An engine hoist (yellow crane) appears next to the car.",
    22: "KEEP: all previous elements. CHANGE: The engine is hanging from the hoist over the engine bay.",
    23: "KEEP: all previous elements. CHANGE: The engine is bolted inside the car (engine bay open, visible).",
    24: "KEEP: all previous elements, engine in car. NEW: The mechanic is connecting a hose to the engine.",
    25: "KEEP: all previous elements. NEW: A small oil can appears on the floor.",
    26: "KEEP: all previous elements, oil can. NEW: The mechanic is pouring oil into the engine.",
    27: "KEEP: all previous elements. NEW: A battery is placed in the front trunk area.",
    28: "KEEP: all previous elements, battery. NEW: Wires are connected from the battery to the interior.",
    29: "KEEP: all previous elements. NEW: The mechanic is holding a steering column.",
    30: "KEEP: all previous elements. CHANGE: The steering column is installed inside the cabin.",
    31: "KEEP: all previous elements, steering column in car. NEW: A bare metal seat frame is placed next to the car.",
    32: "KEEP: all previous elements, first seat frame. NEW: A second bare metal seat frame appears.",
    33: "KEEP: all previous elements, two seat frames. NEW: The mechanic is padding the first seat with foam.",
    34: "KEEP: all previous elements. CHANGE: The first seat is now covered in black leather.",
    35: "KEEP: all previous elements, first leather seat. CHANGE: The second seat is now covered in black leather.",
    36: "KEEP: all previous elements. CHANGE: The driver's seat is installed in the car.",
    37: "KEEP: all previous elements. CHANGE: The passenger seat is installed in the car.",
    38: "KEEP: all previous elements, both seats in car. NEW: A gear shifter is installed on the floor.",
    39: "KEEP: all previous elements, gear shifter. NEW: The mechanic is testing the gear shifter.",
    40: "KEEP: all previous elements. NEW: A radio appears on the workbench.",

    # === PHASE 2: Bodywork & Priming (Days 41-80) ===
    41: "KEEP: all previous elements, radio. NEW: The mechanic is wearing a dust mask and holding sandpaper.",
    42: "KEEP: all previous elements. CHANGE: A small patch on the front hood is sanded to smooth grey metal.",
    43: "KEEP: all previous elements. CHANGE: Half of the front hood is now smooth grey metal.",
    44: "KEEP: all previous elements. CHANGE: The entire front hood is smooth grey metal.",
    45: "KEEP: all previous elements, grey hood. CHANGE: The left front fender is sanded to grey metal.",
    46: "KEEP: all previous elements. CHANGE: The left door area is sanded to grey metal.",
    47: "KEEP: all previous elements. CHANGE: The rear left fender is sanded to grey metal.",
    48: "KEEP: all previous elements. CHANGE: The roof is sanded to grey metal.",
    49: "KEEP: all previous elements. CHANGE: The right side of the car is now half-sanded.",
    50: "KEEP: all previous elements. CHANGE: The entire car body is now smooth, uniform grey metal (no rust visible).",
    51: "KEEP: all previous elements, smooth grey car. NEW: A can of 'Body Filler' appears on the workbench.",
    52: "KEEP: all previous elements. NEW: The mechanic is applying filler to a small dent on the door.",
    53: "KEEP: all previous elements. CHANGE: The filler is sanded flat and smooth.",
    54: "KEEP: all previous elements. NEW: The mechanic is masking the windows with blue tape and paper.",
    55: "KEEP: all previous elements. CHANGE: All 'glass' areas are now covered in masking paper.",
    56: "KEEP: all previous elements, masked windows. NEW: A spray gun appears in the mechanic's hand.",
    57: "KEEP: all previous elements. CHANGE: The front nose of the car is sprayed in light grey primer.",
    58: "KEEP: all previous elements. CHANGE: The front fenders are sprayed in primer.",
    59: "KEEP: all previous elements. CHANGE: The left door is sprayed in primer.",
    60: "KEEP: all previous elements. CHANGE: The roof is sprayed in primer.",
    61: "KEEP: all previous elements. CHANGE: The rear of the car is sprayed in primer.",
    62: "KEEP: all previous elements. CHANGE: The entire car is now uniform light grey primer.",
    63: "KEEP: all previous elements, primer car. NEW: The mechanic is 'wet sanding' the primer with a bucket of water.",
    64: "KEEP: all previous elements. NEW: A small red paint can appears on the workbench.",
    65: "KEEP: all previous elements, red paint can. NEW: The mechanic is mixing the red paint with a wooden stick.",
    66: "KEEP: all previous elements. CHANGE: The engine lid is painted bright red.",
    67: "KEEP: all previous elements. CHANGE: The rear fenders are painted bright red.",
    68: "KEEP: all previous elements. CHANGE: The roof is painted bright red.",
    69: "KEEP: all previous elements. CHANGE: The right door is painted bright red.",
    70: "KEEP: all previous elements. CHANGE: The left door is painted bright red.",
    71: "KEEP: all previous elements. CHANGE: The front fenders are painted bright red.",
    72: "KEEP: all previous elements. CHANGE: The front hood is painted bright red.",
    73: "KEEP: all previous elements. CHANGE: The whole car is red, but looks dull (matte finish).",
    74: "KEEP: all previous elements, matte red car. NEW: The mechanic is holding a buffer/polisher.",
    75: "KEEP: all previous elements. NEW: The mechanic is working on the front wheel area with the buffer.",
    76: "KEEP: all previous elements. CHANGE: All areas now painted red, no more primer visible.",
    77: "KEEP: all previous elements. NEW: The mechanic is polishing the hood; a small 'shine' glint appears.",
    78: "KEEP: all previous elements. CHANGE: The roof is polished and shiny.",
    79: "KEEP: all previous elements. CHANGE: The side panels are polished and shiny.",
    80: "KEEP: all previous elements. CHANGE: The entire car body is now a deep, glossy, mirror-finish red.",

    # === PHASE 3: Assembly & Chrome (Days 81-120) ===
    81: "KEEP: all previous elements, glossy red car. CHANGE: The masking paper is removed from the front windshield area.",
    82: "KEEP: all previous elements. NEW: A glass windshield is placed on the workbench.",
    83: "KEEP: all previous elements, windshield on bench. NEW: The mechanic is applying sealant to the window frame.",
    84: "KEEP: all previous elements. CHANGE: The windshield is installed on the car.",
    85: "KEEP: all previous elements. CHANGE: The rear window is installed.",
    86: "KEEP: all previous elements. CHANGE: The side windows are installed.",
    87: "KEEP: all previous elements, all windows in. NEW: A chrome headlight ring is placed on the workbench.",
    88: "KEEP: all previous elements. CHANGE: The left headlight is installed.",
    89: "KEEP: all previous elements. CHANGE: The right headlight is installed.",
    90: "KEEP: all previous elements, both headlights. NEW: The mechanic is testing the lights (they are glowing yellow).",
    91: "KEEP: all previous elements. NEW: A chrome front bumper is on the floor.",
    92: "KEEP: all previous elements. CHANGE: The front bumper is bolted onto the car.",
    93: "KEEP: all previous elements, front bumper on. CHANGE: The rear bumper is bolted onto the car.",
    94: "KEEP: all previous elements, both bumpers. NEW: Chrome door handles are installed.",
    95: "KEEP: all previous elements. NEW: A chrome side-view mirror is installed on the left.",
    96: "KEEP: all previous elements. NEW: The 'Porsche' lettering is added to the rear.",
    97: "KEEP: all previous elements. NEW: Chrome hubcaps are placed on the workbench.",
    98: "KEEP: all previous elements. CHANGE: The front left hubcap is installed.",
    99: "KEEP: all previous elements. CHANGE: All four hubcaps are installed.",
    100: "KEEP: all previous elements, all hubcaps. NEW: The mechanic stands back with hands on hips, looking proud at the car.",
    101: "KEEP: all previous elements. NEW: A black rubber seal is added around the front hood.",
    102: "KEEP: all previous elements. NEW: Windshield wipers are installed.",
    103: "KEEP: all previous elements. NEW: A tiny antenna is added to the right fender.",
    104: "KEEP: all previous elements. NEW: The mechanic is installing the dashboard gauges.",
    105: "KEEP: all previous elements. NEW: The wooden steering wheel is installed.",
    106: "KEEP: all previous elements. NEW: A rear-view mirror is glued to the windshield inside.",
    107: "KEEP: all previous elements. NEW: The mechanic is vacuuming the interior with a small vacuum.",
    108: "KEEP: all previous elements. NEW: Floor mats are placed inside the car.",
    109: "KEEP: all previous elements. NEW: A license plate bracket is added to the rear.",
    110: "KEEP: all previous elements. NEW: A 'custom' license plate is attached to the bracket.",
    111: "KEEP: all previous elements. NEW: The mechanic is checking the tire pressure with a gauge.",
    112: "KEEP: all previous elements. NEW: A spare tire is placed in the front trunk.",
    113: "KEEP: all previous elements. NEW: The mechanic is polishing the chrome bumpers with a cloth.",
    114: "KEEP: all previous elements. NEW: A small oil puddle on the floor is being wiped clean.",
    115: "KEEP: all previous elements. NEW: A fuel cap is installed on the side.",
    116: "KEEP: all previous elements. NEW: The mechanic is 'filling' the car with a gas can.",
    117: "KEEP: all previous elements. CHANGE: The car is lowered off the jacks; it now sits on its wheels on the floor.",
    118: "KEEP: all previous elements, car on ground. CHANGE: The jack is folded and put away against the wall.",
    119: "KEEP: all previous elements. NEW: The mechanic is sitting in the driver's seat.",
    120: "KEEP: all previous elements. NEW: Smoke comes out of the exhaust (the engine starts!).",

    # === PHASE 4: Pimping & Customization (Days 121-160) ===
    121: "KEEP: all previous elements, car running. NEW: A 'performance' air filter appears on the workbench.",
    122: "KEEP: all previous elements. CHANGE: The mechanic installs the performance filter on the engine.",
    123: "KEEP: all previous elements. NEW: A set of yellow 'fog lights' appears on the workbench.",
    124: "KEEP: all previous elements. CHANGE: Fog lights are mounted on the front bumper.",
    125: "KEEP: all previous elements, fog lights on. NEW: The mechanic is sketching a flame design on a piece of paper.",
    126: "KEEP: all previous elements. NEW: Blue painter's tape is used to outline flames on the front fenders.",
    127: "KEEP: all previous elements. CHANGE: The tips of the flames are painted bright yellow.",
    128: "KEEP: all previous elements. CHANGE: The middle of the flames is painted orange.",
    129: "KEEP: all previous elements. CHANGE: The base of the flames is painted red (blending into the car body).",
    130: "KEEP: all previous elements. CHANGE: The tape is removed; the flames are finished and visible.",
    131: "KEEP: all previous elements, flames done. NEW: A 'racing number' circle (white) is painted on the door.",
    132: "KEEP: all previous elements. CHANGE: The number '75' is painted inside the white circle.",
    133: "KEEP: all previous elements. NEW: A second racing number '75' is painted on the hood.",
    134: "KEEP: all previous elements. NEW: A leather strap is added to hold the hood down (vintage racer style).",
    135: "KEEP: all previous elements. NEW: The mechanic is holding a 'ducktail' spoiler.",
    136: "KEEP: all previous elements. CHANGE: The spoiler is mounted on the rear engine lid.",
    137: "KEEP: all previous elements. CHANGE: The spoiler is painted to match the car's red.",
    138: "KEEP: all previous elements, red spoiler. NEW: A wider set of tires appears next to the car.",
    139: "KEEP: all previous elements. CHANGE: The rear wheels are replaced with 'Deep Dish' racing wheels.",
    140: "KEEP: all previous elements. CHANGE: The front wheels are replaced with matching racing wheels.",
    141: "KEEP: all previous elements, racing wheels. CHANGE: The car is lowered further (low-profile stance).",
    142: "KEEP: all previous elements, lowered car. NEW: A roll cage (yellow bars) is visible inside the cabin.",
    143: "KEEP: all previous elements. NEW: A racing helmet is placed on the workbench.",
    144: "KEEP: all previous elements. NEW: A dual-exit chrome exhaust pipe is installed at the rear.",
    145: "KEEP: all previous elements. NEW: Red 'tow hooks' are added to the front and back.",
    146: "KEEP: all previous elements. NEW: A 'sponsor' sticker (small eagle logo) is added to the rear window.",
    147: "KEEP: all previous elements. NEW: Another small racing sticker is added to the fender.",
    148: "KEEP: all previous elements. NEW: The mechanic is installing a tachometer on top of the dashboard.",
    149: "KEEP: all previous elements. NEW: The headlights are covered with 'X' shaped tape (race look).",
    150: "KEEP: all previous elements. NEW: A fire extinguisher is mounted inside the cabin.",
    151: "KEEP: all previous elements. NEW: Underglow neon lights (purple) are installed under the chassis.",
    152: "KEEP: all previous elements. NEW: The mechanic is testing the purple underglow (the floor glows purple).",
    153: "KEEP: all previous elements, underglow on. NEW: A 'Nitrous Oxide' tank (blue cylinder) is placed in the passenger area.",
    154: "KEEP: all previous elements. NEW: The engine gets a 'Turbo' charger attached (visible chrome pipes).",
    155: "KEEP: all previous elements. NEW: An intercooler is visible through the front bumper.",
    156: "KEEP: all previous elements. NEW: The mechanic is polishing the new 'Turbo' piping.",
    157: "KEEP: all previous elements. NEW: Carbon fiber wrap is applied to the side mirrors.",
    158: "KEEP: all previous elements. NEW: The roof is covered in a checkered flag pattern.",
    159: "KEEP: all previous elements. NEW: The mechanic is holding a 'Quick Release' steering wheel.",
    160: "KEEP: all previous elements. CHANGE: The car now has 'vertical' scissor doors (one door opened upwards).",

    # === PHASE 5: The Ultimate Workshop & Legacy (Days 161-200) ===
    161: "KEEP: all previous elements, scissor doors. NEW: A 'No Smoking' sign is hung on the back wall.",
    162: "KEEP: all previous elements. NEW: A calendar is hung on the wall with days crossed off.",
    163: "KEEP: all previous elements. NEW: A coffee machine appears on the workbench.",
    164: "KEEP: all previous elements. NEW: The mechanic is holding a steaming mug of coffee.",
    165: "KEEP: all previous elements. NEW: A second toolbox (taller red rolling cabinet) is added.",
    166: "KEEP: all previous elements. NEW: A vintage petrol pump is placed in the corner.",
    167: "KEEP: all previous elements. NEW: A 'Winner's Trophy' (gold cup) is placed on a shelf.",
    168: "KEEP: all previous elements. NEW: A stack of spare racing tires is piled in the corner.",
    169: "KEEP: all previous elements. NEW: A poster of the completed car is hung on the wall.",
    170: "KEEP: all previous elements. NEW: A rug with a racing stripe pattern is placed under the car.",
    171: "KEEP: all previous elements, rug. NEW: A shop dog (small bulldog) appears, sleeping on the rug.",
    172: "KEEP: all previous elements, bulldog. NEW: The dog now has a small red collar.",
    173: "KEEP: all previous elements. NEW: A food bowl for the dog appears next to it.",
    174: "KEEP: all previous elements. NEW: The mechanic is petting the dog.",
    175: "KEEP: all previous elements. NEW: A 'Checkered Flag' is draped over the workbench.",
    176: "KEEP: all previous elements. NEW: A 'Restoration of the Year' plaque is on the wall.",
    177: "KEEP: all previous elements. NEW: The mechanic is painting the brick base edge bright white.",
    178: "KEEP: all previous elements. CHANGE: The entire brick base edge is now clean white.",
    179: "KEEP: all previous elements, white brick edge. NEW: A red velvet rope appears on gold stanchions around the car.",
    180: "KEEP: all previous elements. CHANGE: The mechanic is wearing a clean suit (no longer dirty overalls).",
    181: "KEEP: all previous elements, suited mechanic. NEW: A 'Grand Opening' banner is hung above the car.",
    182: "KEEP: all previous elements. NEW: A second car shell (blue, rusted) appears in the background corner, waiting.",
    183: "KEEP: all previous elements, blue shell in back. NEW: The mechanic is waxing the red car one last time.",
    184: "KEEP: all previous elements. NEW: A camera on a tripod is set up to take a photo.",
    185: "KEEP: all previous elements. NEW: A 'For Sale: $1,000,000' sign is placed on the windshield.",
    186: "KEEP: all previous elements. NEW: A 'SOLD' sticker is placed over the price sign.",
    187: "KEEP: all previous elements. CHANGE: Gold plating is added to the door handles.",
    188: "KEEP: all previous elements. CHANGE: Gold plating is added to the hubcaps.",
    189: "KEEP: all previous elements, gold trim. NEW: The engine cover is opened to show a 'Gold Engine' (gold-painted).",
    190: "KEEP: all previous elements. NEW: The mechanic is holding a champagne bottle.",
    191: "KEEP: all previous elements. NEW: Confetti is scattered on the floor around the car.",
    192: "KEEP: all previous elements, confetti. NEW: A spotlight is shining down on the car from above.",
    193: "KEEP: all previous elements. NEW: The mechanic is leaning against the car, smiling at the camera.",
    194: "KEEP: all previous elements. NEW: The bulldog is sitting in the driver's seat.",
    195: "KEEP: all previous elements, dog in car. NEW: The headlights flash (shown with light beams emanating).",
    196: "KEEP: all previous elements. NEW: The mechanic holds up a '200 Days' sign.",
    197: "KEEP: all previous elements. NEW: A giant red bow is placed on the roof of the car.",
    198: "KEEP: all previous elements, bow on car. CHANGE: The workshop lights are dimmed, only the car is lit by spotlight.",
    199: "KEEP: all previous elements. NEW: The car's engine is revving (large exhaust smoke cloud visible).",
    200: "KEEP: all previous elements. CHANGE: The car is driving off the edge of the platform, leaving tire tracks on the concrete, and the mechanic is waving goodbye.",
}


def get_prompt_for_day(day: int) -> str:
    """Generate the complete prompt for a given day."""
    description = DAY_DESCRIPTIONS.get(day, f"Day {day} of the restoration journey.")

    return f"""
{BASE_STYLE}

On the garage floor platform:
{description}

Day {day} of 200 - Vintage Porsche 356 restoration journey.
Claymation miniature diorama style. Keep all accumulated elements visible.
"""


def get_reference_day(day: int) -> int:
    """Get the best reference image day for consistency."""
    if day <= 1:
        return None

    # Use milestone-based references for stability
    # Phase boundaries: 1, 20, 40, 60, 80, 100, 120, 140, 160, 180
    milestones = [1, 20, 40, 60, 80, 100, 120, 140, 160, 180]

    for i, m in enumerate(milestones):
        if day <= m:
            if i == 0:
                return None
            return milestones[i-1]
    return 180  # For days 181-200


def generate_image(day: int, use_reference: bool = True) -> Path:
    """Generate a single day's image."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"  Day {day:3d}: exists, skipping")
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
                f"Use this image as reference for style, platform shape, and existing elements. This is Day {ref_day}. Now create Day {day}:\n\n" + prompt,
                ref_image
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
                image.save(filename)
                print("done")
                return filename

        print("failed (no image)")
        return None

    except Exception as e:
        print(f"failed ({e})")
        return None


def main():
    """Generate all 200 car restoration images."""
    print("=" * 60)
    print("V9: Complete 200-Day Car Restoration Journey")
    print("=" * 60)
    print()

    # First generate milestone days
    milestones = [1, 20, 40, 60, 80, 100, 120, 140, 160, 180]

    print("Phase 1: Generating milestone reference images...")
    for milestone in milestones:
        result = generate_image(milestone)
        if result is None:
            time.sleep(3)
            generate_image(milestone, use_reference=False)
        time.sleep(2)
    print()

    # Then generate all remaining days
    print("Phase 2: Generating all 200 days...")
    for day in range(1, 201):
        if day in milestones:
            continue  # Already generated
        result = generate_image(day)
        if result is None:
            time.sleep(3)
            generate_image(day, use_reference=False)
        time.sleep(2)

        # Progress update every 10 days
        if day % 10 == 0:
            print(f"  Progress: {day}/200 days complete")

    print()
    print("=" * 60)
    images = list(OUTPUT_DIR.glob("day-*.png"))
    print(f"Done! Generated {len(images)} images")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
