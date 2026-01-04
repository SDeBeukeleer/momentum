#!/usr/bin/env python3
"""
V13: Auto-Anchor System
- Analyzes generated images every 5 days to create detailed anchors
- Tracks car orientation to prevent direction changes
- Maintains cumulative improvements list (never regresses)
- Combines with V12's quality preservation techniques
"""

import os
import time
import json
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v13-auto-anchor")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANCHOR_FILE = OUTPUT_DIR / "anchors.json"
CHECKPOINT_INTERVAL = 3  # Tighter quality control

BASE_STYLE = """
CRITICAL STYLE REQUIREMENTS:
- Floating isometric concrete garage floor platform (20x20cm square)
- Concrete surface with realistic cracks, oil stains, tire marks
- Plain solid bright blue background (#0000FF), completely flat
- Neutral white studio lighting only
- Claymation stop-motion style with MAXIMUM DETAIL
- Centered in frame, clean composition

⚠️ CRITICAL PLATFORM EDGE REQUIREMENTS (DO NOT CHANGE):
- Brick edges are INDIVIDUAL SEGMENTS placed at corners and edges
- NOT a continuous brick wall around the perimeter - NEVER make a full brick border
- Bricks should be scattered/grouped in clusters at corners, with gaps between them
- Some edges have NO bricks at all - just exposed concrete edge
- Match the brick placement from the reference image EXACTLY

CRITICAL CAR REQUIREMENTS:
- The car is a HOLLOW RUSTED SHELL - just the body, NO working parts
- NO wheels, NO tires, NO headlights, NO bumpers, NO chrome - unless explicitly stated
- The car has EMPTY wheel wells - you can see through them
- NO engine visible - the engine bay is EMPTY
- NO windows/glass - all window openings are EMPTY holes
- NO doors - door openings are EMPTY

⚠️ CRITICAL QUALITY REQUIREMENTS:
- Background MUST be perfectly flat blue (#0000FF) with ZERO texture, noise, or grain
- All surfaces must be SHARP and CRISP, not soft or blurry
- Concrete cracks must be clearly defined with sharp edges
- Rust texture on car must be detailed and varied, not uniform
- Match the quality level of the Day 1 reference image EXACTLY
"""

# Track state between runs
ANCHORS = {}
IMPROVEMENTS = []


def load_anchors():
    """Load saved anchors from file."""
    global ANCHORS, IMPROVEMENTS
    if ANCHOR_FILE.exists():
        data = json.loads(ANCHOR_FILE.read_text())
        ANCHORS = data.get("anchors", {})
        IMPROVEMENTS = data.get("improvements", [])


def save_anchors():
    """Save anchors to file."""
    ANCHOR_FILE.write_text(json.dumps({
        "anchors": ANCHORS,
        "improvements": IMPROVEMENTS
    }, indent=2))


def analyze_image(image_path: Path) -> str:
    """Use Gemini to analyze an image and extract detailed description."""
    print(f"  Analyzing {image_path.name}...", end=" ", flush=True)

    image = Image.open(image_path)

    analysis_prompt = """
Analyze this claymation diorama image in EXTREME detail. I need this for consistency in future image generation.

Describe PRECISELY:

1. CAR ORIENTATION:
   - Which direction is the car's front facing? (e.g., "toward bottom-left corner")
   - What angle is it at relative to the platform? (e.g., "45 degrees from front edge")
   - Which parts of the car are visible? (front, back, left side, right side)

2. CAR STATE:
   - Body condition (rusted/sanded/primed/painted)
   - Paint color and finish if any
   - What parts are installed vs missing (wheels, engine, doors, windows, etc.)

3. ACCESSORIES & POSITIONS:
   - List every object on the platform
   - Describe their EXACT positions (e.g., "red toolbox in back-left corner")

4. PLATFORM:
   - Brick edge appearance
   - Concrete surface details
   - Any markings or stains

Be EXTREMELY specific. This description will be used to maintain consistency.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[analysis_prompt, image],
        )
        print("done")
        return response.text
    except Exception as e:
        print(f"failed ({e})")
        return ""


def get_anchor_day(day: int) -> int:
    """Get which checkpoint day to use as anchor."""
    if day <= 1:
        return 0
    return ((day - 1) // CHECKPOINT_INTERVAL) * CHECKPOINT_INTERVAL or 1


def should_create_checkpoint(day: int) -> bool:
    """Check if this day should create a new anchor checkpoint."""
    return day > 0 and day % CHECKPOINT_INTERVAL == 0


def is_quality_reset_day(day: int) -> bool:
    """Checkpoint days get quality reset - Day 1 reference only (no previous day).
    This prevents cumulative quality degradation from image-to-image chaining.
    DISABLED for days > 109 because Day 1 shows rusted shell, not the race car."""
    return day > 1 and day <= 109 and day % CHECKPOINT_INTERVAL == 0


# Day descriptions for Days 1-20
DAYS = {
    1: {
        "elements": [
            "A rusted, hollow metal Porsche 356 car shell - DETAILED rust texture, no wheels, no engine, no doors, no glass"
        ],
        "action": "The bare rusted shell sits alone on the platform",
        "is_milestone": True
    },
    2: {
        "elements": [
            "The rusted Porsche 356 car shell (same position and orientation as Day 1)",
            "NEW: A small red metal toolbox with visible latches in the far left corner"
        ],
        "action": "A red toolbox has appeared",
        "is_milestone": True
    },
    3: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "NEW: A chrome metal wrench on the floor near the car"
        ],
        "action": "A wrench appears on the floor",
        "is_milestone": False
    },
    4: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "NEW: A scissor car jack near the rear of the car"
        ],
        "action": "A car jack is placed near the rear",
        "is_milestone": False
    },
    5: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "NEW: A bearded mechanic in blue overalls holding a clipboard, standing next to the car"
        ],
        "action": "The mechanic arrives with a clipboard",
        "is_milestone": True
    },
    6: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls, now holding a wire brush, scrubbing the car"
        ],
        "action": "Mechanic scrubs rust with wire brush",
        "is_milestone": False
    },
    7: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls",
            "NEW: A wooden workbench with detailed wood grain in the back corner"
        ],
        "action": "A wooden workbench appears",
        "is_milestone": True
    },
    8: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The bearded mechanic in blue overalls",
            "The wooden workbench in the back corner",
            "NEW: A desk lamp on the workbench, turned ON"
        ],
        "action": "A desk lamp is placed on the workbench",
        "is_milestone": True
    },
    9: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "The mechanic under the car - only his legs in blue overalls visible"
        ],
        "action": "Mechanic is under the car, only legs visible",
        "is_milestone": False
    },
    10: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "The bearded mechanic in blue overalls standing",
            "NEW: ONE rusted wheel rim leaning against the workbench"
        ],
        "action": "First wheel rim appears",
        "is_milestone": True
    },
    11: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "The bearded mechanic in blue overalls",
            "TWO rusted wheel rims leaning against the workbench"
        ],
        "action": "Second wheel rim appears",
        "is_milestone": False
    },
    12: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO wheel rims near the workbench",
            "The mechanic in blue overalls cleaning one wheel rim with a cloth"
        ],
        "action": "Mechanic cleaning the first wheel rim",
        "is_milestone": False
    },
    13: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "ONE SHINY CHROME wheel rim (polished)",
            "ONE rusted wheel rim next to it",
            "The bearded mechanic standing proudly"
        ],
        "action": "First wheel rim is now chrome!",
        "is_milestone": True,
        "improvement": "First wheel rim polished to chrome"
    },
    14: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims (both polished)",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Both wheel rims now chrome",
        "is_milestone": False,
        "improvement": "Second wheel rim polished to chrome"
    },
    15: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "TWO SHINY CHROME wheel rims",
            "TWO NEW RUSTED wheel rims (just arrived)",
            "The bearded mechanic examining the new rims"
        ],
        "action": "Two more rusted wheel rims arrive (4 total)",
        "is_milestone": True
    },
    16: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "FOUR wheel rims - 2 chrome, 2 rusted",
            "The mechanic polishing the third wheel rim"
        ],
        "action": "Mechanic polishing third wheel rim",
        "is_milestone": False
    },
    17: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "FOUR wheel rims - 3 chrome, 1 rusted",
            "The bearded mechanic in blue overalls",
            "NEW: An engine block (bare metal) placed on the workbench"
        ],
        "action": "Engine block appears on workbench",
        "is_milestone": True,
        "improvement": "Third wheel rim polished to chrome"
    },
    18: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp and engine block",
            "FOUR CHROME wheel rims (all polished now)",
            "The mechanic bolting a small part onto the engine"
        ],
        "action": "Mechanic working on engine, fourth rim polished",
        "is_milestone": False,
        "improvement": "Fourth wheel rim polished to chrome"
    },
    19: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The engine block with spark plug wires added",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Spark plug wires added to engine",
        "is_milestone": False
    },
    20: {
        "elements": [
            "The rusted Porsche 356 car shell (same position)",
            "The red metal toolbox in the far left corner",
            "The chrome wrench on the floor",
            "The scissor car jack near the rear",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The complete engine with fan belt and chrome cover",
            "NEW: A yellow engine hoist (crane) next to the car"
        ],
        "action": "Engine complete, engine hoist appears",
        "is_milestone": True,
        "improvement": "Engine fully assembled"
    },
    # Days 21-40: Shop Setup & Engine Installation Prep
    21: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims stacked",
            "The complete engine on a rolling cart",
            "The yellow engine hoist positioned over the engine bay",
            "The bearded mechanic guiding the engine with chains"
        ],
        "action": "Mechanic preparing to lift engine into car",
        "is_milestone": False
    },
    22: {
        "elements": [
            "The rusted Porsche 356 car shell",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The engine SUSPENDED from the hoist, hovering over the engine bay",
            "The bearded mechanic in blue overalls watching carefully"
        ],
        "action": "Engine suspended, being lowered into place",
        "is_milestone": False
    },
    23: {
        "elements": [
            "The rusted Porsche 356 car shell with ENGINE INSTALLED in the bay",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The yellow engine hoist moved to the side",
            "The bearded mechanic connecting wires under the hood"
        ],
        "action": "Engine installed! Mechanic connecting wires",
        "is_milestone": True,
        "improvement": "Engine installed in car"
    },
    24: {
        "elements": [
            "The rusted Porsche 356 car shell with ENGINE INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The yellow engine hoist",
            "The mechanic lying under the car, legs visible",
            "NEW: A creeper (rolling mechanic board) near the car"
        ],
        "action": "Mechanic under car connecting exhaust",
        "is_milestone": False
    },
    25: {
        "elements": [
            "The rusted Porsche 356 car shell with ENGINE INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The creeper near the car",
            "NEW: A small red fire extinguisher in the corner",
            "The bearded mechanic standing, wiping hands with rag"
        ],
        "action": "Fire extinguisher added for safety",
        "is_milestone": True
    },
    26: {
        "elements": [
            "The rusted Porsche 356 car shell with ENGINE INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher in corner",
            "NEW: An air compressor (red tank with hose) near workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Air compressor added to shop",
        "is_milestone": True
    },
    27: {
        "elements": [
            "The rusted Porsche 356 car shell with ENGINE INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The mechanic using a sanding block on the car's hood"
        ],
        "action": "Mechanic begins sanding the hood",
        "is_milestone": False
    },
    28: {
        "elements": [
            "The Porsche 356 car shell - HOOD NOW PARTIALLY SANDED (some bare metal showing)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The bearded mechanic sanding the front fender"
        ],
        "action": "Hood partially sanded, working on fender",
        "is_milestone": False,
        "improvement": "Hood partially sanded - bare metal showing"
    },
    29: {
        "elements": [
            "The Porsche 356 - FRONT HALF NOW SANDED (hood and fenders showing bare metal)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The mechanic taking a break, drinking from a thermos"
        ],
        "action": "Front half sanded, mechanic takes break",
        "is_milestone": False,
        "improvement": "Front half sanded to bare metal"
    },
    30: {
        "elements": [
            "The Porsche 356 - FRONT HALF SANDED (bare metal)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: A shop fan (standing fan) for ventilation",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Shop fan added, preparing for more sanding",
        "is_milestone": True
    },
    31: {
        "elements": [
            "The Porsche 356 - FRONT HALF SANDED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan running",
            "The mechanic sanding the rear quarter panel"
        ],
        "action": "Sanding the rear quarter panel",
        "is_milestone": False
    },
    32: {
        "elements": [
            "The Porsche 356 - 75% NOW SANDED (only rear deck still rusty)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic finishing the doors area"
        ],
        "action": "Almost fully sanded, just rear deck left",
        "is_milestone": False,
        "improvement": "75% of body sanded to bare metal"
    },
    33: {
        "elements": [
            "The Porsche 356 - FULLY SANDED TO BARE METAL (no rust visible)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The bearded mechanic standing proudly, hands on hips"
        ],
        "action": "CAR FULLY SANDED! All rust removed!",
        "is_milestone": True,
        "improvement": "Car fully sanded - all rust removed, bare metal"
    },
    34: {
        "elements": [
            "The Porsche 356 - BARE METAL (fully sanded, silver/grey)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Cans of body filler on the workbench",
            "The mechanic examining dents in the body"
        ],
        "action": "Body filler arrives, inspecting dents",
        "is_milestone": False
    },
    35: {
        "elements": [
            "The Porsche 356 - BARE METAL with BODY FILLER PATCHES (grey spots)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Body filler cans on workbench",
            "The mechanic applying filler to a dent"
        ],
        "action": "Applying body filler to dents",
        "is_milestone": True,
        "improvement": "Body filler applied to dents"
    },
    36: {
        "elements": [
            "The Porsche 356 - BARE METAL with FILLER PATCHES being sanded smooth",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Body filler cans",
            "The mechanic sanding the filler smooth"
        ],
        "action": "Sanding body filler smooth",
        "is_milestone": False
    },
    37: {
        "elements": [
            "The Porsche 356 - SMOOTH BARE METAL (filler sanded, ready for primer)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Cans of grey primer on the workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Body smooth, primer arrives!",
        "is_milestone": False,
        "improvement": "Body filler sanded smooth"
    },
    38: {
        "elements": [
            "The Porsche 356 - SMOOTH BARE METAL",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Primer cans on workbench",
            "NEW: The car is now MASKED with paper and tape around windows/openings",
            "The mechanic preparing spray gun"
        ],
        "action": "Car masked for painting, spray gun ready",
        "is_milestone": False
    },
    39: {
        "elements": [
            "The Porsche 356 - HOOD NOW PRIMER GREY",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan running",
            "The mechanic spraying primer on the fender"
        ],
        "action": "Spraying primer - hood done!",
        "is_milestone": False,
        "improvement": "Hood primed grey"
    },
    40: {
        "elements": [
            "The Porsche 356 - FULLY PRIMED GREY (entire car is now matte grey primer)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The bearded mechanic removing masking tape"
        ],
        "action": "CAR FULLY PRIMED! Phase 1 complete!",
        "is_milestone": True,
        "improvement": "Car fully primed grey"
    },
    # Days 41-60: Phase 2 - Painting the Car Red
    41: {
        "elements": [
            "The Porsche 356 - GREY PRIMER",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic wet sanding the primer with water and sandpaper"
        ],
        "action": "Wet sanding the primer for smooth finish",
        "is_milestone": False
    },
    42: {
        "elements": [
            "The Porsche 356 - GREY PRIMER (now smooth and dull from wet sanding)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Cans of RED paint on the workbench",
            "The bearded mechanic in blue overalls looking at paint cans"
        ],
        "action": "Red paint arrives! Inspecting the color",
        "is_milestone": False
    },
    43: {
        "elements": [
            "The Porsche 356 - GREY PRIMER, now MASKED with paper and tape",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Red paint cans on workbench",
            "The mechanic wearing a respirator mask, holding spray gun"
        ],
        "action": "Car masked, mechanic ready to paint",
        "is_milestone": False
    },
    44: {
        "elements": [
            "The Porsche 356 - HOOD NOW RED (rest still grey primer)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan running",
            "The mechanic spraying red paint on the fender"
        ],
        "action": "First red coat - hood done!",
        "is_milestone": False,
        "improvement": "Hood painted red"
    },
    45: {
        "elements": [
            "The Porsche 356 - FRONT HALF NOW RED (hood and fenders red, rear still grey)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic continuing to spray"
        ],
        "action": "Front half painted red",
        "is_milestone": True,
        "improvement": "Front half painted red"
    },
    46: {
        "elements": [
            "The Porsche 356 - 75% RED (only rear deck still grey)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic painting the doors area"
        ],
        "action": "Almost fully red, finishing sides",
        "is_milestone": False
    },
    47: {
        "elements": [
            "The Porsche 356 - FULLY RED (first coat complete, matte finish)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The bearded mechanic standing back admiring the red car"
        ],
        "action": "First coat complete! Car is fully red!",
        "is_milestone": True,
        "improvement": "Car fully painted red (first coat)"
    },
    48: {
        "elements": [
            "The Porsche 356 - MATTE RED (first coat)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic lightly sanding between coats"
        ],
        "action": "Light sanding between coats",
        "is_milestone": False
    },
    49: {
        "elements": [
            "The Porsche 356 - MATTE RED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic spraying second coat of red"
        ],
        "action": "Applying second coat of red",
        "is_milestone": False
    },
    50: {
        "elements": [
            "The Porsche 356 - DEEPER RED (second coat, richer color)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The bearded mechanic in blue overalls inspecting the finish"
        ],
        "action": "Second coat done - color is richer",
        "is_milestone": True,
        "improvement": "Second coat of red applied"
    },
    51: {
        "elements": [
            "The Porsche 356 - RICH RED (two coats)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Cans of CLEAR COAT on the workbench",
            "The mechanic preparing for clear coat"
        ],
        "action": "Clear coat arrives",
        "is_milestone": False
    },
    52: {
        "elements": [
            "The Porsche 356 - RED, now being sprayed with CLEAR COAT (wet glossy look)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The mechanic carefully spraying clear coat"
        ],
        "action": "Spraying clear coat",
        "is_milestone": False
    },
    53: {
        "elements": [
            "The Porsche 356 - GLOSSY RED (clear coat applied, shiny wet look)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "The shop fan",
            "The bearded mechanic admiring the glossy finish"
        ],
        "action": "Clear coat done! Car is GLOSSY!",
        "is_milestone": True,
        "improvement": "Clear coat applied - glossy finish"
    },
    54: {
        "elements": [
            "The Porsche 356 - GLOSSY RED (curing)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Heat lamps pointed at the car for curing",
            "The mechanic monitoring temperature"
        ],
        "action": "Paint curing under heat lamps",
        "is_milestone": False
    },
    55: {
        "elements": [
            "The Porsche 356 - GLOSSY RED (cured)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Heat lamps moved to side",
            "The mechanic carefully removing masking tape and paper"
        ],
        "action": "Removing masking - reveal time!",
        "is_milestone": True
    },
    56: {
        "elements": [
            "The Porsche 356 - GLOSSY RED (all masking removed, beautiful red car)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Polishing compound and microfiber cloths on workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Masking removed! Polishing supplies ready",
        "is_milestone": False
    },
    57: {
        "elements": [
            "The Porsche 356 - GLOSSY RED being POLISHED (mechanic buffing hood)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Polishing supplies on workbench",
            "The mechanic using a polishing buffer on the hood"
        ],
        "action": "Polishing the paint to mirror finish",
        "is_milestone": False
    },
    58: {
        "elements": [
            "The Porsche 356 - MIRROR-FINISH RED (highly reflective, polished)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Polishing supplies",
            "The mechanic standing proudly, hands on hips"
        ],
        "action": "Paint polished to mirror finish!",
        "is_milestone": True,
        "improvement": "Paint polished to mirror finish"
    },
    59: {
        "elements": [
            "The Porsche 356 - MIRROR-FINISH RED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "FOUR CHROME wheel rims next to the car",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Car is now on JACK STANDS (raised off ground)",
            "The mechanic preparing to install wheels"
        ],
        "action": "Car on jack stands, ready for wheels",
        "is_milestone": False
    },
    60: {
        "elements": [
            "The Porsche 356 - MIRROR-FINISH RED with FRONT WHEELS INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Two chrome wheel rims still waiting",
            "The fire extinguisher",
            "The air compressor",
            "Car on jack stands",
            "The bearded mechanic tightening wheel bolts"
        ],
        "action": "Front wheels installed! Phase 2 complete!",
        "is_milestone": True,
        "improvement": "Front wheels installed"
    },
    # Days 61-80: Phase 3 - Assembly (Wheels, Glass, Interior, Chrome)
    61: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with front wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Two chrome wheel rims",
            "The fire extinguisher",
            "The air compressor",
            "Car on jack stands",
            "The mechanic installing the rear left wheel"
        ],
        "action": "Installing rear left wheel",
        "is_milestone": False
    },
    62: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with THREE wheels installed",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "One chrome wheel rim remaining",
            "The fire extinguisher",
            "The air compressor",
            "Car on jack stands",
            "The mechanic installing the last wheel"
        ],
        "action": "Installing final wheel",
        "is_milestone": False
    },
    63: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS installed",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The air compressor",
            "Car LOWERED off jack stands - on its own wheels!",
            "The bearded mechanic standing proudly"
        ],
        "action": "ALL WHEELS ON! Car on the ground!",
        "is_milestone": True,
        "improvement": "All four wheels installed"
    },
    64: {
        "elements": [
            "The Porsche 356 - GLOSSY RED on all four wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The air compressor",
            "NEW: Chrome HUBCAPS next to the car",
            "The mechanic holding a hubcap"
        ],
        "action": "Chrome hubcaps arrive",
        "is_milestone": False
    },
    65: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS and CHROME HUBCAPS",
            "Car is ON THE GROUND on its wheels (not on jack stands)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The air compressor",
            "The bearded mechanic admiring the hubcaps"
        ],
        "action": "Hubcaps installed - wheels look complete!",
        "is_milestone": True,
        "improvement": "Chrome hubcaps installed"
    },
    66: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS and chrome hubcaps",
            "Car is ON THE GROUND on its wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: WINDSHIELD glass leaning against workbench",
            "The mechanic preparing rubber seal"
        ],
        "action": "Windshield glass arrives",
        "is_milestone": True
    },
    67: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS, WINDSHIELD being installed",
            "Car is ON THE GROUND on its wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The mechanic carefully fitting the windshield"
        ],
        "action": "Installing windshield",
        "is_milestone": False
    },
    68: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS and WINDSHIELD INSTALLED",
            "Car is ON THE GROUND on its wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Rear window glass on workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Windshield done! Rear window ready",
        "is_milestone": True,
        "improvement": "Windshield installed"
    },
    69: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS, windshield, and REAR WINDOW INSTALLED",
            "Car is ON THE GROUND on its wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Side window glass pieces on workbench",
            "The mechanic inspecting side windows"
        ],
        "action": "Rear window installed, side windows ready",
        "is_milestone": True,
        "improvement": "Rear window installed"
    },
    70: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ALL FOUR WHEELS and ALL GLASS (windshield, rear, sides)",
            "Car is ON THE GROUND on its wheels",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The bearded mechanic standing proudly"
        ],
        "action": "All glass installed!",
        "is_milestone": True,
        "improvement": "All windows installed"
    },
    71: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with all glass",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Chrome FRONT BUMPER on workbench",
            "The mechanic examining the bumper"
        ],
        "action": "Chrome front bumper arrives",
        "is_milestone": False
    },
    72: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with FRONT CHROME BUMPER INSTALLED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Chrome REAR BUMPER on workbench",
            "The mechanic preparing rear bumper"
        ],
        "action": "Front bumper installed, rear ready",
        "is_milestone": True,
        "improvement": "Front chrome bumper installed"
    },
    73: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with BOTH CHROME BUMPERS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The bearded mechanic polishing the rear bumper"
        ],
        "action": "Both bumpers installed!",
        "is_milestone": True,
        "improvement": "Rear chrome bumper installed"
    },
    74: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with bumpers",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Chrome DOOR HANDLES on workbench",
            "The mechanic installing driver door handle"
        ],
        "action": "Installing chrome door handles",
        "is_milestone": False
    },
    75: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with bumpers and CHROME DOOR HANDLES",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Chrome SIDE MIRRORS on workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Door handles installed, mirrors ready",
        "is_milestone": True,
        "improvement": "Chrome door handles installed"
    },
    76: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with CHROME SIDE MIRRORS installed",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The mechanic adjusting the driver side mirror"
        ],
        "action": "Side mirrors installed",
        "is_milestone": True,
        "improvement": "Chrome side mirrors installed"
    },
    77: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with all chrome trim",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: TAN LEATHER SEATS next to the car",
            "The mechanic preparing to install driver seat"
        ],
        "action": "Leather seats arrive!",
        "is_milestone": False
    },
    78: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with DRIVER SEAT installed (tan leather)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "Passenger seat waiting",
            "The mechanic installing passenger seat"
        ],
        "action": "Driver seat in, installing passenger seat",
        "is_milestone": True,
        "improvement": "Driver seat installed"
    },
    79: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with BOTH TAN LEATHER SEATS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "NEW: Wooden STEERING WHEEL on workbench",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Both seats in, steering wheel ready",
        "is_milestone": True,
        "improvement": "Both leather seats installed"
    },
    80: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with seats and WOODEN STEERING WHEEL",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The fire extinguisher",
            "The bearded mechanic sitting in driver seat, hands on wheel"
        ],
        "action": "Steering wheel installed! Phase 3 complete!",
        "is_milestone": True,
        "improvement": "Wooden steering wheel installed"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 4: FINAL DETAILS (Days 81-100)
    # Dashboard, gauges, final trim, first start
    # ═══════════════════════════════════════════════════════════════════════
    81: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with interior (seats, steering wheel)",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: Restored DASHBOARD on workbench (tan leather, chrome bezels)",
            "The bearded mechanic examining the dashboard"
        ],
        "action": "Restored dashboard arrives",
        "is_milestone": False
    },
    82: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with interior",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic installing dashboard into the car"
        ],
        "action": "Installing the dashboard",
        "is_milestone": False
    },
    83: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with TAN DASHBOARD installed",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: Chrome GAUGES on workbench (speedometer, tachometer)",
            "The bearded mechanic in blue overalls"
        ],
        "action": "Dashboard in, gauges ready",
        "is_milestone": True,
        "improvement": "Tan leather dashboard installed"
    },
    84: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with dashboard and CHROME GAUGES installed",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic connecting gauge wiring"
        ],
        "action": "Gauges installed and wired",
        "is_milestone": True,
        "improvement": "Chrome gauges installed"
    },
    85: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with complete dashboard",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: Vintage RADIO on workbench (chrome knobs)",
            "The mechanic preparing radio installation"
        ],
        "action": "Vintage radio arrives",
        "is_milestone": False
    },
    86: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with VINTAGE RADIO in dashboard",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic tuning the radio"
        ],
        "action": "Radio installed!",
        "is_milestone": True,
        "improvement": "Vintage radio installed"
    },
    87: {
        "elements": [
            "The Porsche 356 - GLOSSY RED complete interior",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: TAN CARPET pieces next to car",
            "The mechanic preparing floor carpets"
        ],
        "action": "Floor carpets arrive",
        "is_milestone": False
    },
    88: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with TAN FLOOR CARPETS installed",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic smoothing out the carpet"
        ],
        "action": "Floor carpets installed",
        "is_milestone": True,
        "improvement": "Tan floor carpets installed"
    },
    89: {
        "elements": [
            "The Porsche 356 - GLOSSY RED fully detailed interior",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: Chrome PORSCHE BADGE for hood",
            "The mechanic polishing the badge"
        ],
        "action": "Porsche badge ready",
        "is_milestone": False
    },
    90: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with CHROME PORSCHE BADGE on hood",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic standing proudly next to the car"
        ],
        "action": "Badge installed! Car looks complete!",
        "is_milestone": True,
        "improvement": "Chrome Porsche badge installed"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 5: FIRST START & CELEBRATION (Days 91-110)
    # License plates, first start, test drive, final touches
    # ═══════════════════════════════════════════════════════════════════════
    91: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, fully restored exterior",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: Vintage LICENSE PLATES on workbench",
            "The bearded mechanic examining the plates"
        ],
        "action": "License plates arrive",
        "is_milestone": False
    },
    92: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with FRONT LICENSE PLATE installed",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic installing the rear plate"
        ],
        "action": "Installing license plates",
        "is_milestone": False
    },
    93: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with BOTH LICENSE PLATES",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic polishing the car with a cloth"
        ],
        "action": "License plates installed, final polish",
        "is_milestone": True,
        "improvement": "License plates installed"
    },
    94: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, fully complete",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: GAS CAN next to car",
            "The mechanic preparing to add fuel"
        ],
        "action": "Adding fuel for first start",
        "is_milestone": False
    },
    95: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, fully complete",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic sitting in driver seat, hand on KEY in ignition"
        ],
        "action": "Moment of truth - key in ignition!",
        "is_milestone": False
    },
    96: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with ENGINE RUNNING (small exhaust smoke)",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic with arms raised in celebration"
        ],
        "action": "IT STARTS! First successful engine start!",
        "is_milestone": True,
        "improvement": "First successful engine start"
    },
    97: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with engine running",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Hood open, mechanic listening to engine"
        ],
        "action": "Listening to the engine purr",
        "is_milestone": False
    },
    98: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with hood open",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic adjusting engine with wrench"
        ],
        "action": "Fine-tuning the engine",
        "is_milestone": False
    },
    99: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, engine tuned perfectly",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic closing the hood"
        ],
        "action": "Engine tuned, closing hood",
        "is_milestone": True,
        "improvement": "Engine fine-tuned"
    },
    100: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, COMPLETE AND RUNNING",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The bearded mechanic standing proudly, arms crossed"
        ],
        "action": "DAY 100! Restoration complete!",
        "is_milestone": True,
        "improvement": "Day 100 milestone - restoration complete"
    },
    101: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, pristine condition",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: CHAMPAGNE BOTTLE on workbench",
            "The mechanic opening the champagne"
        ],
        "action": "Time to celebrate!",
        "is_milestone": False
    },
    102: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, pristine condition",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "CHAMPAGNE GLASSES on workbench",
            "The bearded mechanic raising a toast"
        ],
        "action": "Celebrating the completed restoration",
        "is_milestone": True,
        "improvement": "Celebration toast"
    },
    103: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, gleaming",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: CAMERA on tripod pointed at car",
            "The mechanic positioning the camera"
        ],
        "action": "Setting up for photo shoot",
        "is_milestone": False
    },
    104: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, photo-ready",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Camera on tripod, FLASH going off",
            "The mechanic posing next to car"
        ],
        "action": "Photo shoot in progress",
        "is_milestone": False
    },
    105: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, spotless",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: FRAMED PHOTO of restored car on workbench",
            "The mechanic admiring the photo"
        ],
        "action": "Photo printed and framed!",
        "is_milestone": True,
        "improvement": "Restoration photo framed"
    },
    106: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, showroom condition",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic doing final interior wipe-down"
        ],
        "action": "Final interior detailing",
        "is_milestone": False
    },
    107: {
        "elements": [
            "The Porsche 356 - GLOSSY RED, absolutely perfect",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: CAR COVER folded on workbench",
            "The mechanic preparing the cover"
        ],
        "action": "Preparing car cover",
        "is_milestone": False
    },
    108: {
        "elements": [
            "The Porsche 356 - GLOSSY RED with CAR COVER partially on",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic draping the cover"
        ],
        "action": "Covering the masterpiece",
        "is_milestone": True,
        "improvement": "Car cover ready"
    },
    109: {
        "elements": [
            "The Porsche 356 - mostly covered with fitted CAR COVER",
            "Only the front visible, GLOSSY RED",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic adjusting the cover"
        ],
        "action": "Almost fully covered",
        "is_milestone": False
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 6: RACE CAR TRANSFORMATION BEGINS (Days 110-125)
    # The mechanic decides to turn his restored classic into a race machine!
    # ═══════════════════════════════════════════════════════════════════════
    110: {
        "elements": [
            "The GLOSSY RED Porsche 356",
            "Car has ALL FOUR WHEELS with chrome hubcaps",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: RACING MAGAZINE open on workbench showing race cars",
            "The bearded mechanic reading magazine with excited expression"
        ],
        "action": "Inspiration strikes - time to build a race car!",
        "is_milestone": True,
        "improvement": "Race car dream begins"
    },
    111: {
        "elements": [
            "The GLOSSY RED Porsche 356",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: MASKING TAPE rolls and WHITE PAINT CAN on workbench",
            "The mechanic applying masking tape in stripe pattern on hood"
        ],
        "action": "Preparing for racing stripes!",
        "is_milestone": False
    },
    112: {
        "elements": [
            "The Porsche 356 - RED with TWO WHITE RACING STRIPES on hood",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Paint supplies on workbench",
            "The mechanic painting the stripes carefully"
        ],
        "action": "Racing stripes on hood!",
        "is_milestone": True,
        "improvement": "White racing stripes on hood"
    },
    113: {
        "elements": [
            "The Porsche 356 - RED with WHITE RACING STRIPES running full length (hood to trunk)",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic removing masking tape, revealing clean stripes"
        ],
        "action": "Full length racing stripes complete!",
        "is_milestone": True,
        "improvement": "Full length racing stripes"
    },
    114: {
        "elements": [
            "The Porsche 356 - RED with WHITE RACING STRIPES",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: LOWERING SPRINGS kit on workbench",
            "Car on JACK STANDS, mechanic underneath"
        ],
        "action": "Installing lowering springs",
        "is_milestone": False
    },
    115: {
        "elements": [
            "The Porsche 356 - RED with WHITE STRIPES, now VISIBLY LOWERED (2 inches lower)",
            "Car has ALL FOUR WHEELS, aggressive lowered stance",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic admiring the aggressive new stance"
        ],
        "action": "Car lowered - aggressive stance!",
        "is_milestone": True,
        "improvement": "Lowered suspension - aggressive stance"
    },
    116: {
        "elements": [
            "The LOWERED Porsche 356 - RED with WHITE STRIPES",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: BLACK FRONT SPLITTER/LIP on workbench",
            "The mechanic test-fitting the splitter under front bumper"
        ],
        "action": "Front splitter arrives",
        "is_milestone": False
    },
    117: {
        "elements": [
            "The LOWERED Porsche 356 - RED with WHITE STRIPES and BLACK FRONT SPLITTER installed",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic tightening bolts on the splitter"
        ],
        "action": "Front splitter installed - more downforce!",
        "is_milestone": True,
        "improvement": "Black front splitter installed"
    },
    118: {
        "elements": [
            "The LOWERED Porsche 356 with STRIPES and FRONT SPLITTER",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: BLACK REAR SPOILER/DUCKTAIL on workbench",
            "The mechanic holding spoiler up to rear of car"
        ],
        "action": "Rear spoiler fitting",
        "is_milestone": False
    },
    119: {
        "elements": [
            "The LOWERED Porsche 356 - RED with WHITE STRIPES, FRONT SPLITTER, and BLACK DUCKTAIL REAR SPOILER",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic stepping back to admire the sporty look"
        ],
        "action": "Ducktail spoiler installed!",
        "is_milestone": True,
        "improvement": "Black ducktail rear spoiler"
    },
    120: {
        "elements": [
            "The LOWERED Porsche 356 with STRIPES, SPLITTER, and SPOILER",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: WIDE FENDER FLARES (fiberglass, unpainted) on workbench",
            "The mechanic examining the front fender flares"
        ],
        "action": "Wide body kit arrives!",
        "is_milestone": False
    },
    121: {
        "elements": [
            "The LOWERED Porsche 356 - now with WIDE FRONT FENDER FLARES (painted red to match)",
            "Car has WHITE STRIPES, SPLITTER, SPOILER",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic bolting on the front flares"
        ],
        "action": "Front fender flares installed!",
        "is_milestone": True,
        "improvement": "Wide front fender flares"
    },
    122: {
        "elements": [
            "The LOWERED Porsche 356 - WIDE FRONT AND REAR FENDER FLARES (full wide body)",
            "Car has WHITE STRIPES, SPLITTER, SPOILER",
            "Car has ALL FOUR WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic finishing rear flare installation"
        ],
        "action": "Full wide body complete!",
        "is_milestone": True,
        "improvement": "Full wide body kit installed"
    },
    123: {
        "elements": [
            "The WIDE BODY Porsche 356 with all aero mods",
            "Car has ALL FOUR WHEELS (now look small in wide arches)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: SET OF WIDE RACING WHEELS (gold BBS style) on workbench",
            "The mechanic examining the new wheels excitedly"
        ],
        "action": "Wide racing wheels arrive!",
        "is_milestone": False
    },
    124: {
        "elements": [
            "The WIDE BODY Porsche 356 - now with GOLD BBS RACING WHEELS (wide, filling the fenders)",
            "Car has WHITE STRIPES, SPLITTER, SPOILER, WIDE BODY",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic torquing the wheel bolts"
        ],
        "action": "Gold racing wheels installed!",
        "is_milestone": True,
        "improvement": "Gold BBS racing wheels"
    },
    125: {
        "elements": [
            "The WIDE BODY Porsche 356 with GOLD WHEELS",
            "Car has all aero mods, aggressive stance",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: SLICK RACING TIRES mounted on workbench",
            "The mechanic mounting racing slicks on the gold wheels"
        ],
        "action": "Racing slicks going on!",
        "is_milestone": True,
        "improvement": "Racing slick tires"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 7: ENGINE & PERFORMANCE (Days 126-140)
    # Serious power upgrades!
    # ═══════════════════════════════════════════════════════════════════════
    126: {
        "elements": [
            "The WIDE BODY race Porsche 356 with GOLD WHEELS and SLICKS",
            "Hood OPEN showing engine bay",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: TURBOCHARGER KIT on workbench",
            "The mechanic studying turbo installation manual"
        ],
        "action": "Turbo kit arrives!",
        "is_milestone": False
    },
    127: {
        "elements": [
            "The WIDE BODY race Porsche 356",
            "Hood OPEN - TURBOCHARGER now visible in engine bay (shiny metal turbo)",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic connecting turbo piping"
        ],
        "action": "Turbo installed!",
        "is_milestone": True,
        "improvement": "Turbocharger installed"
    },
    128: {
        "elements": [
            "The TURBOCHARGED WIDE BODY Porsche 356",
            "Hood OPEN showing turbo",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: INTERCOOLER on workbench",
            "The mechanic mounting intercooler behind front grille"
        ],
        "action": "Front mount intercooler",
        "is_milestone": False
    },
    129: {
        "elements": [
            "The TURBOCHARGED Porsche 356 - INTERCOOLER visible through front grille",
            "WIDE BODY, GOLD WHEELS, all aero mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic admiring the aggressive front end"
        ],
        "action": "Intercooler visible - mean look!",
        "is_milestone": True,
        "improvement": "Front mount intercooler visible"
    },
    130: {
        "elements": [
            "The TURBOCHARGED Porsche 356 with INTERCOOLER",
            "WIDE BODY, GOLD WHEELS, all aero mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: HOOD with SCOOP/VENTS on workbench",
            "The mechanic removing stock hood"
        ],
        "action": "Vented hood swap!",
        "is_milestone": False
    },
    131: {
        "elements": [
            "The Porsche 356 - now with VENTED HOOD (black hood scoop and heat vents)",
            "TURBOCHARGED, WIDE BODY, GOLD WHEELS, INTERCOOLER",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic securing the new hood"
        ],
        "action": "Vented hood installed!",
        "is_milestone": True,
        "improvement": "Vented hood with scoop"
    },
    132: {
        "elements": [
            "The race Porsche 356 with VENTED HOOD",
            "All previous mods visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: SIDE EXIT EXHAUST PIPES on workbench",
            "The mechanic measuring exhaust routing"
        ],
        "action": "Side exit exhaust prep",
        "is_milestone": False
    },
    133: {
        "elements": [
            "The race Porsche 356 - CHROME SIDE EXIT EXHAUST PIPES visible (exiting just behind doors)",
            "All previous mods: VENTED HOOD, TURBO, WIDE BODY, GOLD WHEELS",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic tightening exhaust clamps"
        ],
        "action": "Side exit exhausts installed!",
        "is_milestone": True,
        "improvement": "Chrome side exit exhausts"
    },
    134: {
        "elements": [
            "The race Porsche 356 with SIDE EXHAUSTS",
            "Engine running - FLAMES shooting from side exhausts!",
            "All previous mods visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic grinning at the flames"
        ],
        "action": "Testing exhaust - FLAMES!",
        "is_milestone": True,
        "improvement": "Exhaust shoots flames"
    },
    135: {
        "elements": [
            "The race Porsche 356 with all mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: OIL COOLER kit on workbench",
            "The mechanic installing oil cooler behind front grille"
        ],
        "action": "Oil cooler for track duty",
        "is_milestone": False
    },
    136: {
        "elements": [
            "The race Porsche 356 - OIL COOLER visible next to intercooler",
            "BRAIDED OIL LINES visible",
            "All previous mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic checking for leaks"
        ],
        "action": "Oil cooler installed!",
        "is_milestone": True,
        "improvement": "Oil cooler with braided lines"
    },
    137: {
        "elements": [
            "The race Porsche 356 with all mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: BIG BRAKE KIT (red calipers, drilled rotors) on workbench",
            "The mechanic removing stock brakes"
        ],
        "action": "Big brake kit upgrade!",
        "is_milestone": False
    },
    138: {
        "elements": [
            "The race Porsche 356 - RED 6-PISTON BRAKE CALIPERS visible through gold wheels",
            "DRILLED ROTORS visible",
            "All previous mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic bleeding the brakes"
        ],
        "action": "Big brakes installed!",
        "is_milestone": True,
        "improvement": "Red big brake kit"
    },
    139: {
        "elements": [
            "The race Porsche 356 with BIG BRAKES",
            "All previous mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: NITROUS OXIDE BOTTLE (blue) on workbench",
            "The mechanic holding the NOS bottle"
        ],
        "action": "NITROUS system arrives!",
        "is_milestone": False
    },
    140: {
        "elements": [
            "The race Porsche 356 - NITROUS BOTTLE visible mounted in rear",
            "NOS PURGE NOZZLE visible near front",
            "All previous mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic activating purge - WHITE CLOUD spraying"
        ],
        "action": "NOS installed - PURGE TEST!",
        "is_milestone": True,
        "improvement": "Nitrous oxide system"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 8: RACE INTERIOR (Days 141-155)
    # Full race cockpit transformation!
    # ═══════════════════════════════════════════════════════════════════════
    141: {
        "elements": [
            "The race Porsche 356 - door open showing interior",
            "Stock interior still visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: BUCKET RACING SEAT (red with harness slots) on workbench"
        ],
        "action": "Racing seat arrives!",
        "is_milestone": False
    },
    142: {
        "elements": [
            "The race Porsche 356 - RED BUCKET RACING SEAT installed (driver side)",
            "Stock passenger seat still there",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic bolting in the racing seat"
        ],
        "action": "Racing driver seat installed!",
        "is_milestone": True,
        "improvement": "Racing bucket seat"
    },
    143: {
        "elements": [
            "The race Porsche 356 - TWO RED BUCKET RACING SEATS installed",
            "Interior looking more race-like",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic adjusting seat positions"
        ],
        "action": "Both racing seats in!",
        "is_milestone": True,
        "improvement": "Matching racing seats"
    },
    144: {
        "elements": [
            "The race Porsche 356 with RACING SEATS",
            "Interior visible through open door",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: RACING HARNESSES (red 4-point) on workbench"
        ],
        "action": "Racing harnesses arrive!",
        "is_milestone": False
    },
    145: {
        "elements": [
            "The race Porsche 356 - RED 4-POINT RACING HARNESSES installed on both seats",
            "Harness buckles visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic testing harness tension"
        ],
        "action": "Racing harnesses installed!",
        "is_milestone": True,
        "improvement": "4-point racing harnesses"
    },
    146: {
        "elements": [
            "The race Porsche 356 with SEATS and HARNESSES",
            "Interior visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: ROLL CAGE TUBES (chrome-moly steel) on workbench"
        ],
        "action": "Roll cage kit arrives!",
        "is_milestone": False
    },
    147: {
        "elements": [
            "The race Porsche 356 - ROLL CAGE MAIN HOOP installed (visible behind seats)",
            "Chrome-moly steel tubes",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic welding the cage"
        ],
        "action": "Main hoop installed!",
        "is_milestone": True,
        "improvement": "Roll cage main hoop"
    },
    148: {
        "elements": [
            "The race Porsche 356 - FULL ROLL CAGE visible (door bars, A-pillar bars)",
            "Complete safety cage structure",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic finishing welds"
        ],
        "action": "Full roll cage complete!",
        "is_milestone": True,
        "improvement": "Full roll cage installed"
    },
    149: {
        "elements": [
            "The race Porsche 356 with FULL ROLL CAGE",
            "Interior visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: SUEDE RACING STEERING WHEEL (with buttons) on workbench"
        ],
        "action": "Racing wheel arrives!",
        "is_milestone": False
    },
    150: {
        "elements": [
            "The race Porsche 356 - SUEDE RACING STEERING WHEEL installed (flat bottom, with NOS button)",
            "Roll cage, racing seats visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic checking steering alignment"
        ],
        "action": "Racing steering wheel!",
        "is_milestone": True,
        "improvement": "Suede racing wheel with NOS button"
    },
    151: {
        "elements": [
            "The race Porsche 356 with RACING WHEEL",
            "Interior visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: DIGITAL RACING DASH DISPLAY on workbench"
        ],
        "action": "Digital dash arrives!",
        "is_milestone": False
    },
    152: {
        "elements": [
            "The race Porsche 356 - DIGITAL RACING DASH replacing stock gauges",
            "LCD display showing RPM, speed, temps",
            "Full race interior visible",
            "All exterior mods",
            "The red metal toolbox",
            "The mechanic programming the dash"
        ],
        "action": "Digital dash installed!",
        "is_milestone": True,
        "improvement": "Digital racing dashboard"
    },
    153: {
        "elements": [
            "The race Porsche 356 with DIGITAL DASH",
            "Interior visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: FIRE EXTINGUISHER SYSTEM (red bottle, nozzles) on workbench"
        ],
        "action": "Fire suppression system!",
        "is_milestone": False
    },
    154: {
        "elements": [
            "The race Porsche 356 - FIRE EXTINGUISHER mounted beside driver seat",
            "FIRE NOZZLES visible in engine bay",
            "Full race interior",
            "All exterior mods",
            "The red metal toolbox",
            "The mechanic testing the system"
        ],
        "action": "Fire system installed - safety first!",
        "is_milestone": True,
        "improvement": "Fire suppression system"
    },
    155: {
        "elements": [
            "The race Porsche 356 with all safety equipment",
            "Interior visible showing complete race cockpit",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: QUICK RELEASE STEERING HUB on workbench"
        ],
        "action": "Quick release hub",
        "is_milestone": True,
        "improvement": "Quick release steering hub"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 9: LIVERY & RACE PREP (Days 156-175)
    # Race car livery and final touches!
    # ═══════════════════════════════════════════════════════════════════════
    156: {
        "elements": [
            "The race Porsche 356 - all mods visible",
            "Full race spec now",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: RACING NUMBER DECALS (number 56) on workbench",
            "The mechanic planning decal placement"
        ],
        "action": "Race number decals arrive!",
        "is_milestone": False
    },
    157: {
        "elements": [
            "The race Porsche 356 - LARGE WHITE NUMBER 56 on doors (both sides)",
            "Racing number circles visible",
            "All exterior mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic smoothing out the decals"
        ],
        "action": "Race number 56 applied!",
        "is_milestone": True,
        "improvement": "Race number 56 on doors"
    },
    158: {
        "elements": [
            "The race Porsche 356 with NUMBER 56",
            "All mods visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: SPONSOR DECALS (various racing brands) on workbench",
            "The mechanic selecting decals"
        ],
        "action": "Sponsor decals arrive!",
        "is_milestone": False
    },
    159: {
        "elements": [
            "The race Porsche 356 - SPONSOR DECALS on fenders and bumpers",
            "Logos visible: oil, tires, parts brands",
            "NUMBER 56 on doors",
            "All mods visible",
            "The red metal toolbox",
            "The mechanic applying hood decals"
        ],
        "action": "Sponsors going on!",
        "is_milestone": True,
        "improvement": "Sponsor decals applied"
    },
    160: {
        "elements": [
            "The race Porsche 356 - fully decorated with DECALS everywhere",
            "Professional race car livery look",
            "All mods visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic admiring the full livery"
        ],
        "action": "Full race livery complete!",
        "is_milestone": True,
        "improvement": "Full race livery"
    },
    161: {
        "elements": [
            "The race Porsche 356 with FULL LIVERY",
            "All mods visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: TOWING EYE HOOKS (front and rear, neon yellow) on workbench",
            "The mechanic examining the hooks"
        ],
        "action": "Tow hooks arrive!",
        "is_milestone": False
    },
    162: {
        "elements": [
            "The race Porsche 356 - NEON YELLOW TOW HOOKS installed (front and rear)",
            "Race requirement visible",
            "Full livery, all mods",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic tightening tow hooks"
        ],
        "action": "Tow hooks installed!",
        "is_milestone": True,
        "improvement": "Neon yellow tow hooks"
    },
    163: {
        "elements": [
            "The race Porsche 356 with TOW HOOKS",
            "Full race spec",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: WINDOW NET (driver side) on workbench",
            "The mechanic measuring window opening"
        ],
        "action": "Window net prep",
        "is_milestone": False
    },
    164: {
        "elements": [
            "The race Porsche 356 - RED WINDOW NET installed on driver side",
            "Full race safety equipment now",
            "All exterior mods and livery",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic testing net release"
        ],
        "action": "Window net installed!",
        "is_milestone": True,
        "improvement": "Driver window net"
    },
    165: {
        "elements": [
            "The race Porsche 356 - full race spec",
            "All safety equipment visible",
            "All exterior mods and livery",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: LED LIGHT BAR (for rain racing) on workbench"
        ],
        "action": "Rain lights arrive!",
        "is_milestone": False
    },
    166: {
        "elements": [
            "The race Porsche 356 - REAR LED RAIN LIGHT installed (red, flashing)",
            "Full race spec",
            "All exterior mods and livery",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic testing the rain light - it's ON and bright"
        ],
        "action": "Rain light installed!",
        "is_milestone": True,
        "improvement": "LED rain light"
    },
    167: {
        "elements": [
            "The race Porsche 356 with RAIN LIGHT",
            "Full race spec",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: HOOD PINS (aluminum, silver) on workbench",
            "The mechanic drilling hood for pins"
        ],
        "action": "Hood pins prep",
        "is_milestone": False
    },
    168: {
        "elements": [
            "The race Porsche 356 - ALUMINUM HOOD PINS installed (4 pins visible)",
            "Hood secured race-style",
            "Full race spec, all livery",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic latching the pins"
        ],
        "action": "Hood pins installed!",
        "is_milestone": True,
        "improvement": "Aluminum hood pins"
    },
    169: {
        "elements": [
            "The race Porsche 356 with HOOD PINS",
            "Full race spec",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: CARBON FIBER MIRROR CAPS on workbench",
            "The mechanic removing stock mirror covers"
        ],
        "action": "Carbon mirrors",
        "is_milestone": False
    },
    170: {
        "elements": [
            "The race Porsche 356 - CARBON FIBER MIRROR CAPS installed",
            "Carbon weave pattern visible",
            "Full race spec, all livery",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "The mechanic polishing the carbon"
        ],
        "action": "Carbon mirrors installed!",
        "is_milestone": False,
        "improvement": "Carbon fiber mirrors"
    },
    171: {
        "elements": [
            "The race Porsche 356 with CARBON MIRRORS",
            "Full race spec",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: RACING HELMET (red with visor) and RACING SUIT (red) on workbench",
            "The mechanic holding helmet proudly"
        ],
        "action": "Racing gear arrives!",
        "is_milestone": False,
        "improvement": "Racing helmet and suit"
    },
    172: {
        "elements": [
            "The race Porsche 356 - full race spec",
            "The mechanic WEARING RED RACING SUIT standing next to car",
            "Racing helmet on workbench",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Ready for action"
        ],
        "action": "Driver suited up!",
        "is_milestone": True,
        "improvement": "Driver in racing suit"
    },
    173: {
        "elements": [
            "The race Porsche 356 - full race spec",
            "The mechanic in RACING SUIT, HELMET ON, sitting in car",
            "Full race cockpit visible",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Ready for race day"
        ],
        "action": "Race ready!",
        "is_milestone": True,
        "improvement": "Driver fully equipped"
    },
    174: {
        "elements": [
            "The race Porsche 356 - ENGINE RUNNING, small exhaust flames",
            "Driver in full gear in car",
            "Warming up",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Smoke from exhaust"
        ],
        "action": "Final warm-up!",
        "is_milestone": False
    },
    175: {
        "elements": [
            "The race Porsche 356 - full race spec, all mods visible",
            "Driver in gear, engine running",
            "NOS PURGE firing - white cloud",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "Final systems check"
        ],
        "action": "NOS purge - ALL SYSTEMS GO!",
        "is_milestone": True,
        "improvement": "All race systems operational"
    },
    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 10: RACE DAY & GLORY (Days 176-200)
    # Track action and championship victory!
    # ═══════════════════════════════════════════════════════════════════════
    176: {
        "elements": [
            "The race Porsche 356 - full race spec",
            "CHECKERED FLAGS decorating the garage",
            "The red metal toolbox",
            "The wooden workbench with desk lamp",
            "NEW: RACE TRACK BANNER 'Race Day' on wall",
            "The mechanic in racing suit celebrating"
        ],
        "action": "RACE DAY IS HERE!",
        "is_milestone": True,
        "improvement": "Race day arrives"
    },
    177: {
        "elements": [
            "The race Porsche 356 - ON TRAILER (car hauler visible)",
            "Strapped down for transport",
            "Full race spec visible",
            "The red metal toolbox packed",
            "The mechanic securing the last strap"
        ],
        "action": "Loading for the track!",
        "is_milestone": False
    },
    178: {
        "elements": [
            "The race Porsche 356 - back in garage after qualifying",
            "POLE POSITION sign on windshield",
            "Trophy for pole on workbench",
            "The mechanic pumping fist in celebration"
        ],
        "action": "POLE POSITION!",
        "is_milestone": True,
        "improvement": "Qualified on pole"
    },
    179: {
        "elements": [
            "The race Porsche 356 - driver in car, engine running",
            "GREEN FLAG on workbench",
            "Exhaust flames visible",
            "The mechanic giving thumbs up"
        ],
        "action": "GREEN FLAG - GO GO GO!",
        "is_milestone": False
    },
    180: {
        "elements": [
            "The race Porsche 356 - slightly dirty from racing (dust, rubber marks)",
            "NUMBER 56 clearly visible",
            "LEADING THE RACE - #1 sign on workbench",
            "The mechanic watching intensely"
        ],
        "action": "LEADING THE RACE!",
        "is_milestone": True,
        "improvement": "Leading the race"
    },
    181: {
        "elements": [
            "The race Porsche 356 - battle scarred (minor contact marks)",
            "Racing hard visible evidence",
            "HALFWAY flag on workbench",
            "The mechanic biting nails nervously"
        ],
        "action": "Halfway point - still leading!",
        "is_milestone": False
    },
    182: {
        "elements": [
            "The race Porsche 356 - driver in car, pit stop",
            "TIRE CHANGE in progress - mechanic with impact wrench",
            "Fresh slicks waiting",
            "Quick pit stop action"
        ],
        "action": "PIT STOP!",
        "is_milestone": True,
        "improvement": "Perfect pit stop"
    },
    183: {
        "elements": [
            "The race Porsche 356 - TIRES SMOKING from hot restart",
            "Fresh slicks mounted",
            "Back on track",
            "The mechanic waving go-go-go"
        ],
        "action": "Back in action!",
        "is_milestone": False
    },
    184: {
        "elements": [
            "The race Porsche 356 - final laps",
            "LAST LAP flag on workbench",
            "Tension high",
            "The mechanic crossing fingers"
        ],
        "action": "FINAL LAP!",
        "is_milestone": False
    },
    185: {
        "elements": [
            "The race Porsche 356 - CROSSING FINISH LINE",
            "CHECKERED FLAG waving",
            "WINNER WINNER WINNER",
            "The mechanic jumping with joy"
        ],
        "action": "CHECKERED FLAG - WE WON!!!",
        "is_milestone": True,
        "improvement": "Won the race"
    },
    186: {
        "elements": [
            "The race Porsche 356 - victory burnout",
            "MASSIVE TIRE SMOKE cloud",
            "Winner circle",
            "Celebration everywhere"
        ],
        "action": "VICTORY BURNOUT!",
        "is_milestone": True,
        "improvement": "Victory celebration burnout"
    },
    187: {
        "elements": [
            "The race Porsche 356 - on VICTORY PODIUM",
            "GIANT TROPHY (1st place) next to car",
            "CHAMPAGNE spraying",
            "The mechanic on podium celebrating"
        ],
        "action": "PODIUM CELEBRATION!",
        "is_milestone": True,
        "improvement": "First place podium"
    },
    188: {
        "elements": [
            "The race Porsche 356 - back in garage",
            "GIANT WINNER TROPHY on workbench",
            "WINNER BANNER behind car",
            "The mechanic hugging the trophy"
        ],
        "action": "Trophy comes home!",
        "is_milestone": True,
        "improvement": "Winner trophy home"
    },
    189: {
        "elements": [
            "The race Porsche 356 - getting cleaned after race",
            "Battle damage being assessed",
            "Trophy on display",
            "The mechanic washing car lovingly"
        ],
        "action": "Post-race cleanup",
        "is_milestone": False
    },
    190: {
        "elements": [
            "The race Porsche 356 - minor repairs",
            "Fixing small dents from racing",
            "Trophy on workbench",
            "The mechanic doing bodywork"
        ],
        "action": "Race damage repair",
        "is_milestone": False
    },
    191: {
        "elements": [
            "The race Porsche 356 - ALL FIXED, gleaming again",
            "Like new condition",
            "Trophy prominent",
            "The mechanic polishing car"
        ],
        "action": "Good as new!",
        "is_milestone": True,
        "improvement": "Fully restored after race"
    },
    192: {
        "elements": [
            "The race Porsche 356 - CHAMPIONSHIP BANNER added to garage wall",
            "Multiple trophies on shelf now",
            "The mechanic hanging banner"
        ],
        "action": "Championship memorabilia",
        "is_milestone": True,
        "improvement": "Championship banner"
    },
    193: {
        "elements": [
            "The race Porsche 356 with all racing mods",
            "NEW: GOLD CHAMPIONSHIP WRAP being applied (chrome gold accents)",
            "Winner's upgrade",
            "The mechanic applying gold details"
        ],
        "action": "Champion's gold trim!",
        "is_milestone": True,
        "improvement": "Gold champion accents"
    },
    194: {
        "elements": [
            "The race Porsche 356 - GOLD ACCENTS complete (stripes, mirrors, wheels painted gold)",
            "Champion edition",
            "Multiple trophies on shelf",
            "The mechanic standing proud"
        ],
        "action": "Gold champion livery!",
        "is_milestone": True,
        "improvement": "Full gold champion livery"
    },
    195: {
        "elements": [
            "The GOLD CHAMPION Porsche 356",
            "Professional PHOTOSHOOT setup (lights, camera on tripod)",
            "Trophies arranged",
            "The mechanic posing with car"
        ],
        "action": "Champion photoshoot!",
        "is_milestone": False
    },
    196: {
        "elements": [
            "The GOLD CHAMPION Porsche 356",
            "MAGAZINE COVER FRAMED on wall (featuring the car)",
            "Multiple trophies",
            "The mechanic admiring magazine"
        ],
        "action": "Magazine cover star!",
        "is_milestone": True,
        "improvement": "Featured on magazine cover"
    },
    197: {
        "elements": [
            "The GOLD CHAMPION Porsche 356",
            "TROPHY SHELF full (10+ trophies)",
            "Championship banners on wall",
            "Magazine covers framed",
            "The mechanic organizing trophies"
        ],
        "action": "Trophy collection grows!",
        "is_milestone": True,
        "improvement": "Full trophy collection"
    },
    198: {
        "elements": [
            "The GOLD CHAMPION Porsche 356 - MUSEUM QUALITY display",
            "Velvet ropes around car",
            "Spotlight on car",
            "Ultimate showpiece",
            "The mechanic in suit admiring"
        ],
        "action": "Museum display setup!",
        "is_milestone": True,
        "improvement": "Museum quality display"
    },
    199: {
        "elements": [
            "The GOLD CHAMPION Porsche 356",
            "HALL OF FAME plaque being mounted",
            "Full championship display",
            "Life achievement moment",
            "The mechanic emotional, hand on heart"
        ],
        "action": "Hall of Fame moment!",
        "is_milestone": True,
        "improvement": "Hall of Fame induction"
    },
    200: {
        "elements": [
            "The LEGENDARY GOLD CHAMPION Porsche 356 - ultimate final form",
            "ALL TROPHIES displayed (championship wall)",
            "HALL OF FAME plaque",
            "MAGAZINE COVERS framed",
            "The bearded mechanic sitting in car, helmet on, giving thumbs up",
            "PERFECT ENDING - LEGEND STATUS ACHIEVED"
        ],
        "action": "DAY 200 - LEGEND COMPLETE!!!",
        "is_milestone": True,
        "improvement": "LEGEND STATUS - Journey Complete"
    },
}


def get_prompt_for_day(day: int) -> str:
    """Generate prompt with anchor information."""
    if day not in DAYS:
        return None

    day_data = DAYS[day]
    elements = day_data["elements"]
    action = day_data["action"]
    elements_list = "\n".join(f"  • {e}" for e in elements)

    # Get anchor description if available
    anchor_day = get_anchor_day(day)
    anchor_section = ""
    if str(anchor_day) in ANCHORS and anchor_day > 0:
        anchor_section = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️  MANDATORY ORIENTATION LOCK - COPY EXACTLY FROM DAY {anchor_day}  ⚠️           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

The following description is from Day {anchor_day}. You MUST reproduce the EXACT SAME:
- Car position and angle on the platform
- Car orientation (which direction the front faces)
- Platform appearance and brick placement
- Position of ALL accessories (toolbox, jack, wrench locations)

ANCHOR DESCRIPTION:
{ANCHORS[str(anchor_day)]}

════════════════════════════════════════════════════════════════════════════════
"""

    # Build improvements section
    improvements_section = ""
    if IMPROVEMENTS:
        improvements_section = f"""
CUMULATIVE IMPROVEMENTS (MUST ALL BE VISIBLE - cannot be undone):
{chr(10).join(f'  ✓ {imp}' for imp in IMPROVEMENTS)}

"""

    # Build "DO NOT" section based on what shouldn't exist yet
    do_not_section = ""
    if day <= 15:  # Before wheel rims become chrome
        do_not_section = """
⛔ DO NOT ADD THESE (they don't exist yet):
- NO wheels or tires on the car
- NO headlights or taillights
- NO bumpers
- NO chrome parts
- NO engine (engine bay is empty)
- NO glass/windows
- NO doors
The car is just a HOLLOW RUSTED SHELL with empty openings!
"""

    return f"""
{BASE_STYLE}
{anchor_section}
{improvements_section}
═══════════════════════════════════════════════════════════
DAY {day} OF 200 - PORSCHE 356 RESTORATION
═══════════════════════════════════════════════════════════

SCENE ELEMENTS (all must be visible):
{elements_list}

TODAY'S ACTION: {action}
{do_not_section}
STRICT RULES:
1. ⚠️ CAR ORIENTATION: Must be IDENTICAL to the reference image - front facing bottom-left corner
2. ⚠️ CAR STATE: Hollow rusted shell ONLY - no parts that aren't explicitly listed
3. ⚠️ ACCESSORIES: Keep in SAME positions as reference image
4. Platform brick segments must match reference
5. Every element must be sharp and detailed
"""


def generate_image(day: int) -> Path:
    """Generate image with auto-anchor system."""
    filename = OUTPUT_DIR / f"day-{day:03d}.png"

    if filename.exists():
        print(f"Day {day:3d}: exists, skipping")
        return filename

    prompt = get_prompt_for_day(day)
    if not prompt:
        print(f"Day {day:3d}: no prompt defined")
        return None

    day_data = DAYS.get(day, {})
    is_milestone = day_data.get("is_milestone", False)

    print(f"Day {day:3d}: generating", end="")
    if is_milestone:
        print(" [MILESTONE]", end="")
    if is_quality_reset_day(day):
        print(" [QUALITY RESET]", end="")
    print("...", end=" ", flush=True)

    # Build reference images - TRIPLE REFERENCE SYSTEM with QUALITY RESET
    day1_path = OUTPUT_DIR / "day-001.png"
    prev_path = OUTPUT_DIR / f"day-{(day-1):03d}.png" if day > 1 else None  # Previous day for layout
    anchor_day = get_anchor_day(day)

    try:
        if day == 1:
            contents = [prompt]
        elif is_quality_reset_day(day) and day1_path.exists():
            # QUALITY RESET: Only Day 1 reference (no previous day)
            # This prevents cumulative quality degradation from image-to-image chaining
            day1_image = Image.open(day1_path)
            contents = [
                "⚠️ QUALITY RESET - Match this quality level EXACTLY:",
                "Copy the detail level, background flatness (pure blue, no noise), and sharpness from this reference:",
                day1_image,
                f"\nCreate Day {day} with MAXIMUM QUALITY - sharp details, flat blue background:\n" + prompt
            ]
        elif day1_path.exists() and prev_path and prev_path.exists():
            # TRIPLE REFERENCE: Day 1 (quality) + Previous day (layout) + Anchor text (in prompt)
            day1_image = Image.open(day1_path)
            prev_image = Image.open(prev_path)
            contents = [
                "QUALITY REFERENCE (match detail level):",
                day1_image,
                f"\n⚠️ LAYOUT REFERENCE (Day {day-1}) - COPY THIS EXACTLY:",
                "Match the EXACT car position, car orientation, brick edge style, and composition from this image:",
                prev_image,
                f"\nNow create Day {day} - add ONLY the new element, keep everything else identical:\n" + prompt
            ]
        elif day1_path.exists():
            day1_image = Image.open(day1_path)
            contents = [
                "Match this quality level and car orientation:",
                day1_image,
                f"\nCreate Day {day}:\n" + prompt
            ]
        else:
            contents = [prompt]

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
                part.as_image().save(filename)
                print("done")

                # Track improvements
                if "improvement" in day_data:
                    if day_data["improvement"] not in IMPROVEMENTS:
                        IMPROVEMENTS.append(day_data["improvement"])
                        save_anchors()

                return filename

        print("failed (no image)")
        return None

    except Exception as e:
        print(f"failed ({e})")
        return None


def main():
    """Generate images with auto-anchor system."""
    global ANCHORS, IMPROVEMENTS

    print("=" * 60)
    print("V13: Auto-Anchor System")
    print("=" * 60)
    print()
    print(f"Checkpoint interval: Every {CHECKPOINT_INTERVAL} days")
    print("Quality resets every 3 days for tighter control")
    print()

    load_anchors()

    for day in range(1, 201):
        # Generate the image
        result = generate_image(day)

        if result is None:
            time.sleep(3)
            result = generate_image(day)

        # Create checkpoint if needed
        if result and should_create_checkpoint(day):
            print(f"\n  >>> Creating checkpoint for Day {day}")
            anchor_desc = analyze_image(result)
            if anchor_desc:
                ANCHORS[str(day)] = anchor_desc
                save_anchors()
                print(f"  >>> Checkpoint saved\n")

        time.sleep(2)

    print()
    print("=" * 60)
    images = list(OUTPUT_DIR.glob("day-*.png"))
    print(f"Done! Generated {len(images)} images")
    print(f"Checkpoints created: {list(ANCHORS.keys())}")
    print(f"Improvements tracked: {IMPROVEMENTS}")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
