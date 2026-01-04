#!/usr/bin/env python3
"""
V14: Spaceship/Moonbase Theme - Auto-Anchor System
- Based on V13 architecture with all the same quality controls
- 200 days of building a spaceship and moonbase on the moon
- 30% smaller resolution for mobile display (720px instead of 1024px)
- Phases: Foundation → Rocket Assembly → Moonbase Expansion → Futuristic Upgrade
"""

import os
import time
import json
from pathlib import Path
from PIL import Image

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama/v14-spaceship")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANCHOR_FILE = OUTPUT_DIR / "anchors.json"
CHECKPOINT_INTERVAL = 3  # Create checkpoint every 3 days for tighter quality control

# 30% smaller than 1K (1024) = ~716px, using 720px for clean number
IMAGE_SIZE = 720

BASE_STYLE = """
CRITICAL STYLE REQUIREMENTS:
- Isometric 3D claymation/stop-motion style diorama
- Square moon-soil tile platform (grey lunar regolith surface)
- Cross-section visible on edges showing layered geology: grey dust on top, then tan/brown rock layers, then darker rock at bottom
- Plain solid BRIGHT GREEN chroma key background (#00FF00) - completely flat, for easy background removal
- Earth visible floating in the top-right corner of the scene
- Consistent soft studio lighting with tilt-shift miniature effect
- Centered in frame, clean composition
- Maximum detail on all elements - this is a high-quality miniature diorama

⚠️ CRITICAL PLATFORM REQUIREMENTS:
- The platform is a square chunk of moon surface, isometric angle
- Top surface: grey lunar dust with subtle craters, footprints, and texture
- Edge cross-section layers: grey dust → tan/beige rock → brown rock → dark rock at bottom
- Platform floats against white background

⚠️ CRITICAL ROCKET DESIGN (when present):
- Silver/metallic body with rivets and panel lines
- RED fins/landing legs at the bottom
- RED horizontal stripe around the middle section
- Round BLUE porthole windows
- Open hatch panel showing COLORFUL wiring (rainbow cables) inside
- Silver pointed nose cone with small antenna on top

⚠️ CRITICAL QUALITY REQUIREMENTS:
- Background MUST be perfectly flat BRIGHT GREEN (#00FF00) with ZERO texture, noise, or grain
- All surfaces must be SHARP and CRISP, not soft or blurry
- Moon dust texture must be detailed and realistic with visible footprints
- Metal surfaces should have appropriate reflections and weathering
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
Analyze this claymation moonbase diorama image in EXTREME detail. I need this for consistency in future image generation.

Describe PRECISELY:

1. PLATFORM ORIENTATION:
   - How is the moon-soil tile angled?
   - Which corner is closest to the viewer?

2. STRUCTURES & POSITIONS:
   - List EVERY structure (rocket, domes, scaffolding, etc.)
   - Describe their EXACT positions (e.g., "rocket in center", "dome in back-left")
   - Note any connections between structures (walkways, cables)

3. OBJECTS & ACCESSORIES:
   - List every small object (crates, barrels, rover, tripod, etc.)
   - Describe their EXACT positions
   - Note quantities and arrangements

4. CHARACTERS:
   - How many astronauts?
   - What are they doing?
   - Where are they positioned?

5. CURRENT STATE:
   - What phase of construction is visible?
   - What elements are complete vs in-progress?

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
    DISABLED for days > 75 because Day 1 shows empty moon tile, not the moonbase."""
    return day > 1 and day <= 75 and day % CHECKPOINT_INTERVAL == 0


# =============================================================================
# PHASE 1: LOGISTICS & FOUNDATION (Days 1-50)
# =============================================================================
DAYS = {
    1: {
        "elements": [
            "Empty grey square moon-soil tile platform",
            "Cross-section showing layered lunar geology (grey dust → tan rock → brown rock → dark rock)",
            "Earth visible floating in top-right corner of scene",
            "Subtle crater marks and footprint-ready dust on surface"
        ],
        "action": "Empty moon platform - the beginning",
        "is_milestone": True
    },
    2: {
        "elements": [
            "Grey moon-soil tile with layered cross-section",
            "Earth in top-right corner",
            "A small orange 'X' landing marker painted in the center of the tile",
        ],
        "action": "Landing marker painted",
        "is_milestone": True,
        "improvement": "Orange X landing marker painted"
    },
    3: {
        "elements": [
            "Moon-soil tile with orange X in center, Earth in sky",
            "NEW: One wooden supply crate in the back-left area"
        ],
        "action": "First supply crate arrives",
        "is_milestone": False
    },
    4: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "TWO wooden crates stacked in back-left area"
        ],
        "action": "Second crate stacked",
        "is_milestone": False
    },
    5: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "Two wooden crates in back-left",
            "NEW: One metal barrel (grey/blue) next to the crates"
        ],
        "action": "Metal barrel delivered",
        "is_milestone": True,
        "improvement": "Supply area established"
    },
    6: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "Two wooden crates and one metal barrel in back-left",
            "NEW: Second metal barrel added to supply area"
        ],
        "action": "Second barrel arrives",
        "is_milestone": False
    },
    7: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "Two wooden crates and two metal barrels in back-left",
            "NEW: Third wooden crate added"
        ],
        "action": "Third crate arrives",
        "is_milestone": False
    },
    8: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "THREE wooden crates and TWO metal barrels forming supply pile in back-left"
        ],
        "action": "Supply pile growing",
        "is_milestone": False
    },
    9: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "Supply pile (3 crates, 2 barrels) in back-left",
            "NEW: Small white rover with cargo bed entering from bottom edge"
        ],
        "action": "Rover arrives!",
        "is_milestone": True,
        "improvement": "Rover deployed"
    },
    10: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky",
            "Supply pile in back-left",
            "Rover parked in front-center area with cargo"
        ],
        "action": "Rover parked and ready",
        "is_milestone": True
    },
    11: {
        "elements": [
            "Moon-soil tile with orange X, Earth in sky, supplies, rover",
            "NEW: Small beige habitat dome base being placed in back-right area"
        ],
        "action": "Habitat dome base placed",
        "is_milestone": True,
        "improvement": "Habitat dome construction begun"
    },
    12: {
        "elements": [
            "Moon-soil tile with all previous elements",
            "Habitat dome 25% built - base and first wall section"
        ],
        "action": "Dome walls rising",
        "is_milestone": False
    },
    13: {
        "elements": [
            "Moon-soil tile with all previous elements",
            "Habitat dome 50% built"
        ],
        "action": "Dome half complete",
        "is_milestone": False
    },
    14: {
        "elements": [
            "Moon-soil tile with all previous elements",
            "Habitat dome 75% built"
        ],
        "action": "Dome nearly complete",
        "is_milestone": False
    },
    15: {
        "elements": [
            "Moon-soil tile with supplies, rover, Earth in sky",
            "COMPLETE beige habitat dome with round blue window in back-right"
        ],
        "action": "Habitat dome complete!",
        "is_milestone": True,
        "improvement": "Habitat dome finished with blue window"
    },
    16: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome, Earth in sky",
            "NEW: Small satellite dish being placed on habitat dome roof"
        ],
        "action": "Satellite dish installation",
        "is_milestone": False
    },
    17: {
        "elements": [
            "Moon-soil tile with supplies, rover, Earth in sky",
            "Habitat dome with satellite dish mounted on roof"
        ],
        "action": "Satellite dish mounted",
        "is_milestone": True,
        "improvement": "Satellite dish on habitat"
    },
    18: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome with dish, Earth in sky",
            "NEW: Solar panel frame placed next to habitat dome"
        ],
        "action": "Solar panel frame placed",
        "is_milestone": False
    },
    19: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome with dish, Earth in sky",
            "Solar panel partially unfolded (50%)"
        ],
        "action": "Solar panel unfolding",
        "is_milestone": False
    },
    20: {
        "elements": [
            "Moon-soil tile with supplies, rover, Earth in sky",
            "Habitat dome with satellite dish",
            "COMPLETE blue solar panel array next to dome"
        ],
        "action": "Solar panel operational!",
        "is_milestone": True,
        "improvement": "Solar panel array deployed"
    },
    21: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome with dish, solar panel, Earth in sky",
            "NEW: ONE astronaut in white spacesuit appears, holding clipboard/tablet"
        ],
        "action": "First astronaut arrives!",
        "is_milestone": True,
        "improvement": "First astronaut on site"
    },
    22: {
        "elements": [
            "All previous elements",
            "Astronaut walking toward the orange X landing marker"
        ],
        "action": "Astronaut surveying site",
        "is_milestone": False
    },
    23: {
        "elements": [
            "All previous elements",
            "Astronaut standing at orange X, checking tablet"
        ],
        "action": "Astronaut at landing site",
        "is_milestone": False
    },
    24: {
        "elements": [
            "All previous elements",
            "NEW: Metal launch platform base being placed at orange X"
        ],
        "action": "Launch platform arrives",
        "is_milestone": False
    },
    25: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome, solar panel, Earth in sky",
            "Astronaut with tablet",
            "Metal launch platform base installed at center"
        ],
        "action": "Launch platform installed!",
        "is_milestone": True,
        "improvement": "Launch platform base installed"
    },
    26: {
        "elements": [
            "All previous elements",
            "NEW: First vertical scaffolding pole erected at launch platform"
        ],
        "action": "First scaffolding pole",
        "is_milestone": False
    },
    27: {
        "elements": [
            "All previous elements",
            "TWO scaffolding poles erected"
        ],
        "action": "Second scaffolding pole",
        "is_milestone": False
    },
    28: {
        "elements": [
            "All previous elements",
            "THREE scaffolding poles erected"
        ],
        "action": "Third scaffolding pole",
        "is_milestone": False
    },
    29: {
        "elements": [
            "All previous elements",
            "FOUR scaffolding poles erected - corners complete"
        ],
        "action": "Four corner poles up",
        "is_milestone": False
    },
    30: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat, solar panel, astronaut, Earth",
            "Basic scaffolding frame (4 poles with horizontal connectors)"
        ],
        "action": "Basic scaffolding frame!",
        "is_milestone": True,
        "improvement": "Basic scaffolding erected"
    },
    31: {
        "elements": [
            "All previous elements",
            "Scaffolding with first platform level added"
        ],
        "action": "Scaffolding platform 1",
        "is_milestone": False
    },
    32: {
        "elements": [
            "All previous elements",
            "Scaffolding with second platform level"
        ],
        "action": "Scaffolding platform 2",
        "is_milestone": False
    },
    33: {
        "elements": [
            "All previous elements",
            "Scaffolding with third platform level"
        ],
        "action": "Scaffolding platform 3",
        "is_milestone": False
    },
    34: {
        "elements": [
            "All previous elements",
            "Scaffolding taller - fourth level"
        ],
        "action": "Scaffolding taller",
        "is_milestone": False
    },
    35: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat, solar panel, astronaut, Earth",
            "TALL multi-level metal scaffolding structure at center (5 levels)"
        ],
        "action": "Full scaffolding complete!",
        "is_milestone": True,
        "improvement": "Full scaffolding tower built"
    },
    36: {
        "elements": [
            "All previous elements",
            "NEW: Second astronaut appears on the tile"
        ],
        "action": "Second astronaut arrives!",
        "is_milestone": True,
        "improvement": "Second astronaut joins crew"
    },
    37: {
        "elements": [
            "All previous elements",
            "Both astronauts examining the scaffolding"
        ],
        "action": "Crew planning",
        "is_milestone": False
    },
    38: {
        "elements": [
            "All previous elements",
            "One astronaut on scaffolding platform, one on ground with tablet"
        ],
        "action": "Astronaut climbs scaffolding",
        "is_milestone": False
    },
    39: {
        "elements": [
            "All previous elements",
            "Astronauts preparing for rocket delivery"
        ],
        "action": "Preparing for rocket",
        "is_milestone": False
    },
    40: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat dome with dish, solar panel, Earth",
            "Two astronauts",
            "Complete scaffolding tower",
            "Everything ready for rocket assembly"
        ],
        "action": "Phase 1 Complete - Ready for rocket!",
        "is_milestone": True,
        "improvement": "Foundation phase complete"
    },
    41: {
        "elements": [
            "All previous elements",
            "NEW: RED rocket landing legs/fins placed at base of scaffolding"
        ],
        "action": "Rocket legs arrive!",
        "is_milestone": True,
        "improvement": "Red rocket legs installed"
    },
    42: {
        "elements": [
            "All previous elements with red rocket legs",
            "Astronaut attaching leg to platform"
        ],
        "action": "Attaching rocket legs",
        "is_milestone": False
    },
    43: {
        "elements": [
            "All previous elements",
            "All RED rocket legs secured to platform"
        ],
        "action": "All legs secured",
        "is_milestone": False
    },
    44: {
        "elements": [
            "All previous elements",
            "NEW: First silver rocket hull section placed on legs"
        ],
        "action": "First hull section!",
        "is_milestone": False
    },
    45: {
        "elements": [
            "Moon-soil tile with all base elements",
            "Red rocket legs with first silver hull section",
            "Scaffolding surrounding rocket"
        ],
        "action": "Rocket base taking shape!",
        "is_milestone": True,
        "improvement": "Rocket hull assembly begun"
    },
    46: {
        "elements": [
            "All previous elements",
            "Second silver hull section stacked"
        ],
        "action": "Second hull section",
        "is_milestone": False
    },
    47: {
        "elements": [
            "All previous elements",
            "Third silver hull section - rocket getting taller"
        ],
        "action": "Third hull section",
        "is_milestone": False
    },
    48: {
        "elements": [
            "All previous elements",
            "Fourth silver hull section"
        ],
        "action": "Fourth hull section",
        "is_milestone": False
    },
    49: {
        "elements": [
            "All previous elements",
            "Fifth silver hull section with RED horizontal stripe painted"
        ],
        "action": "Red stripe painted!",
        "is_milestone": False
    },
    50: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "Two astronauts working",
            "Scaffolding with SILVER ROCKET (lower half) - red legs, red stripe",
            "Phase 1 complete!"
        ],
        "action": "Lower rocket hull complete!",
        "is_milestone": True,
        "improvement": "Lower rocket hull with red stripe"
    },

    # =========================================================================
    # PHASE 2: ROCKET ASSEMBLY (Days 51-100)
    # =========================================================================
    51: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "Two astronauts",
            "Scaffolding with lower rocket (red legs, silver hull, red stripe)",
            "NEW: Sixth silver hull section added"
        ],
        "action": "Sixth hull section",
        "is_milestone": False
    },
    52: {
        "elements": [
            "All previous elements",
            "Seventh silver hull section - rocket growing taller"
        ],
        "action": "Seventh hull section",
        "is_milestone": False
    },
    53: {
        "elements": [
            "All previous elements",
            "NEW: Round BLUE porthole window installed on hull"
        ],
        "action": "Porthole window installed!",
        "is_milestone": True,
        "improvement": "Blue porthole window added"
    },
    54: {
        "elements": [
            "All previous elements with porthole",
            "Eighth silver hull section added"
        ],
        "action": "Eighth hull section",
        "is_milestone": False
    },
    55: {
        "elements": [
            "Moon-soil tile with all base elements",
            "Silver rocket with red legs, red stripe, blue porthole",
            "Scaffolding surrounding rocket",
            "Main hull body complete"
        ],
        "action": "Main hull body complete!",
        "is_milestone": True,
        "improvement": "Main rocket hull complete"
    },
    56: {
        "elements": [
            "All previous elements",
            "NEW: Open rectangular HATCH panel on upper hull showing EMPTY interior"
        ],
        "action": "Hatch panel opened",
        "is_milestone": False
    },
    57: {
        "elements": [
            "All previous elements with open hatch",
            "First wiring bundle visible inside hatch"
        ],
        "action": "First wiring installed",
        "is_milestone": False
    },
    58: {
        "elements": [
            "All previous elements",
            "More COLORFUL wiring (red, blue, yellow cables) visible in hatch"
        ],
        "action": "Colorful wiring added",
        "is_milestone": False
    },
    59: {
        "elements": [
            "All previous elements",
            "Complex rainbow wiring and circuit boards visible in open hatch"
        ],
        "action": "Electronics installed",
        "is_milestone": False
    },
    60: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "Two astronauts",
            "Silver rocket with red legs, red stripe, blue porthole, OPEN HATCH showing colorful wiring",
            "Scaffolding surrounding rocket"
        ],
        "action": "Internal wiring complete!",
        "is_milestone": True,
        "improvement": "Colorful internal wiring visible through hatch"
    },
    61: {
        "elements": [
            "All previous elements",
            "NEW: Second blue porthole window being installed"
        ],
        "action": "Second porthole",
        "is_milestone": False
    },
    62: {
        "elements": [
            "All previous elements",
            "TWO blue porthole windows on rocket hull"
        ],
        "action": "Both portholes installed",
        "is_milestone": False
    },
    63: {
        "elements": [
            "All previous elements",
            "Astronaut on scaffolding platform working on rocket with tool"
        ],
        "action": "Astronaut working on scaffolding",
        "is_milestone": False
    },
    64: {
        "elements": [
            "All previous elements",
            "One astronaut on scaffolding with BLUE TOOL, one below with clipboard"
        ],
        "action": "Team working on rocket",
        "is_milestone": False
    },
    65: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "Silver rocket (red legs, red stripe, blue portholes, open hatch with rainbow wiring)",
            "Scaffolding around rocket",
            "Two astronauts - one on scaffolding with tool, one with clipboard"
        ],
        "action": "Assembly in progress!",
        "is_milestone": True,
        "improvement": "Active construction scene"
    },
    66: {
        "elements": [
            "All previous elements",
            "Upper hull section being added above the hatch"
        ],
        "action": "Upper hull section",
        "is_milestone": False
    },
    67: {
        "elements": [
            "All previous elements",
            "Rocket hull nearly complete - just needs nose cone"
        ],
        "action": "Hull nearly complete",
        "is_milestone": False
    },
    68: {
        "elements": [
            "All previous elements",
            "NEW: Silver pointed nose cone being prepared nearby"
        ],
        "action": "Nose cone arrives",
        "is_milestone": False
    },
    69: {
        "elements": [
            "All previous elements",
            "Nose cone being lifted by astronaut on top scaffolding platform"
        ],
        "action": "Lifting nose cone",
        "is_milestone": False
    },
    70: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "COMPLETE silver rocket with nose cone, red legs, red stripe, blue portholes, open hatch with wiring",
            "Scaffolding still around rocket",
            "Two astronauts"
        ],
        "action": "Nose cone installed!",
        "is_milestone": True,
        "improvement": "Silver nose cone with antenna installed"
    },
    71: {
        "elements": [
            "All previous elements",
            "Antenna being attached to tip of nose cone"
        ],
        "action": "Antenna installation",
        "is_milestone": False
    },
    72: {
        "elements": [
            "All previous elements",
            "Antenna complete on nose cone tip"
        ],
        "action": "Antenna complete",
        "is_milestone": False
    },
    73: {
        "elements": [
            "All previous elements",
            "Astronaut inspecting the rocket from scaffolding"
        ],
        "action": "Quality inspection",
        "is_milestone": False
    },
    74: {
        "elements": [
            "All previous elements",
            "Both astronauts checking different parts of the rocket"
        ],
        "action": "Final inspection",
        "is_milestone": False
    },
    75: {
        "elements": [
            "Moon-soil tile with layered cross-section (grey → tan → brown → dark rock)",
            "Supply pile (wooden crates + metal barrels) in back-left",
            "White rover with cargo in front-center, footprints in dust",
            "Beige habitat dome with blue window, satellite dish on roof, in back-right",
            "Blue solar panel array next to habitat",
            "COMPLETE silver rocket at center: red fins/legs, red stripe, TWO blue portholes, OPEN HATCH showing COLORFUL RAINBOW WIRING",
            "Silver nose cone with small antenna on top",
            "Metal scaffolding structure surrounding the rocket",
            "TWO astronauts: one on scaffolding with BLUE TOOL working on rocket, one on ground with CLIPBOARD",
            "Earth floating in top-right corner",
            "Visible footprints in the lunar dust"
        ],
        "action": "ROCKET ASSEMBLY PEAK - Reference scene!",
        "is_milestone": True,
        "improvement": "Full assembly scene with active astronauts"
    },
    76: {
        "elements": [
            "All Day 75 elements",
            "Astronaut beginning to close the hatch panel (10% closed)"
        ],
        "action": "Hatch closing begins",
        "is_milestone": False
    },
    77: {
        "elements": [
            "All previous elements",
            "Hatch panel 25% closed - some wiring still visible"
        ],
        "action": "Hatch 25% closed",
        "is_milestone": False
    },
    78: {
        "elements": [
            "All previous elements",
            "Hatch panel 50% closed"
        ],
        "action": "Hatch 50% closed",
        "is_milestone": False
    },
    79: {
        "elements": [
            "All previous elements",
            "Hatch panel 75% closed - almost sealed"
        ],
        "action": "Hatch 75% closed",
        "is_milestone": False
    },
    80: {
        "elements": [
            "All base elements",
            "Complete rocket with HATCH NOW FULLY CLOSED - smooth hull",
            "Scaffolding still around rocket",
            "Two astronauts"
        ],
        "action": "Hatch sealed!",
        "is_milestone": True,
        "improvement": "Rocket hatch sealed"
    },
    81: {
        "elements": [
            "All previous elements",
            "Astronauts beginning to dismantle scaffolding - one section removed"
        ],
        "action": "Scaffolding removal begins",
        "is_milestone": False
    },
    82: {
        "elements": [
            "All previous elements",
            "25% of scaffolding removed"
        ],
        "action": "Scaffolding 25% removed",
        "is_milestone": False
    },
    83: {
        "elements": [
            "All previous elements",
            "50% of scaffolding removed - rocket more visible"
        ],
        "action": "Scaffolding 50% removed",
        "is_milestone": False
    },
    84: {
        "elements": [
            "All previous elements",
            "75% of scaffolding removed"
        ],
        "action": "Scaffolding 75% removed",
        "is_milestone": False
    },
    85: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat, solar panel, Earth",
            "COMPLETE rocket standing FREELY - no scaffolding!",
            "Silver body, red legs, red stripe, blue portholes, closed hatch, nose cone with antenna",
            "Two astronauts standing proudly"
        ],
        "action": "Scaffolding removed - rocket revealed!",
        "is_milestone": True,
        "improvement": "Scaffolding completely removed"
    },
    86: {
        "elements": [
            "All previous elements",
            "Scaffolding materials stacked to the side"
        ],
        "action": "Cleanup continues",
        "is_milestone": False
    },
    87: {
        "elements": [
            "All previous elements",
            "Astronauts inspecting the complete rocket"
        ],
        "action": "Final rocket inspection",
        "is_milestone": False
    },
    88: {
        "elements": [
            "All previous elements",
            "One astronaut pointing at rocket while other takes notes"
        ],
        "action": "Documentation",
        "is_milestone": False
    },
    89: {
        "elements": [
            "All previous elements",
            "Astronauts giving thumbs up"
        ],
        "action": "Rocket approved!",
        "is_milestone": False
    },
    90: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "COMPLETE freestanding rocket - silver with red legs, red stripe, blue portholes, nose cone",
            "Two astronauts celebrating"
        ],
        "action": "Phase 2 Complete - Rocket finished!",
        "is_milestone": True,
        "improvement": "Rocket construction complete"
    },
    91: {
        "elements": [
            "All previous elements",
            "Astronaut polishing the rocket hull"
        ],
        "action": "Polishing rocket",
        "is_milestone": False
    },
    92: {
        "elements": [
            "All previous elements",
            "Rocket hull gleaming after polish"
        ],
        "action": "Rocket gleaming",
        "is_milestone": False
    },
    93: {
        "elements": [
            "All previous elements",
            "NEW: Control panel/console being set up near rocket base"
        ],
        "action": "Control panel setup",
        "is_milestone": False
    },
    94: {
        "elements": [
            "All previous elements",
            "Control panel installed with blinking lights"
        ],
        "action": "Control panel active",
        "is_milestone": False
    },
    95: {
        "elements": [
            "All previous elements with control panel",
            "Cables connecting control panel to rocket"
        ],
        "action": "Systems connected!",
        "is_milestone": True,
        "improvement": "Launch control panel installed"
    },
    96: {
        "elements": [
            "All previous elements",
            "Astronaut at control panel running diagnostics"
        ],
        "action": "Running diagnostics",
        "is_milestone": False
    },
    97: {
        "elements": [
            "All previous elements",
            "Green lights on control panel - systems OK"
        ],
        "action": "Systems check passed",
        "is_milestone": False
    },
    98: {
        "elements": [
            "All previous elements",
            "Second astronaut inspecting fuel connections"
        ],
        "action": "Fuel system check",
        "is_milestone": False
    },
    99: {
        "elements": [
            "All previous elements",
            "Both astronauts at control panel, all green lights"
        ],
        "action": "All systems go!",
        "is_milestone": False
    },
    100: {
        "elements": [
            "Moon-soil tile with supplies, rover, habitat with dish, solar panel, Earth",
            "Complete rocket with control panel nearby",
            "Two astronauts - one at controls, one monitoring rocket",
            "All systems operational"
        ],
        "action": "Phase 2 Complete - Ready for base expansion!",
        "is_milestone": True,
        "improvement": "Rocket systems online"
    },

    # =========================================================================
    # PHASE 3: MOONBASE EXPANSION (Days 101-150)
    # =========================================================================
    101: {
        "elements": [
            "All Phase 2 elements (rocket, habitat with dish, etc.)",
            "NEW: First segment of glass walkway built from rocket"
        ],
        "action": "Glass walkway begun",
        "is_milestone": True
    },
    102: {
        "elements": [
            "All previous elements",
            "TWO segments of glass walkway"
        ],
        "action": "Second walkway segment",
        "is_milestone": False
    },
    103: {
        "elements": [
            "All previous elements",
            "THREE segments of glass walkway"
        ],
        "action": "Third walkway segment",
        "is_milestone": False
    },
    104: {
        "elements": [
            "All previous elements",
            "FOUR segments of glass walkway"
        ],
        "action": "Fourth walkway segment",
        "is_milestone": False
    },
    105: {
        "elements": [
            "All previous elements",
            "FIVE segments of glass walkway"
        ],
        "action": "Fifth walkway segment",
        "is_milestone": True
    },
    106: {
        "elements": [
            "All previous elements",
            "SIX segments of glass walkway"
        ],
        "action": "Sixth walkway segment",
        "is_milestone": False
    },
    107: {
        "elements": [
            "All previous elements",
            "SEVEN segments of glass walkway"
        ],
        "action": "Seventh walkway segment",
        "is_milestone": False
    },
    108: {
        "elements": [
            "All previous elements",
            "EIGHT segments of glass walkway"
        ],
        "action": "Eighth walkway segment",
        "is_milestone": False
    },
    109: {
        "elements": [
            "All previous elements",
            "NINE segments of glass walkway"
        ],
        "action": "Ninth walkway segment",
        "is_milestone": False
    },
    110: {
        "elements": [
            "Glass walkway CONNECTS rocket to habitat hut",
            "All other elements"
        ],
        "action": "Walkway complete!",
        "is_milestone": True,
        "improvement": "Glass walkway connects rocket to habitat"
    },
    111: {
        "elements": [
            "All previous elements",
            "NEW: Construction begins on second Habitat Dome"
        ],
        "action": "Second dome started",
        "is_milestone": True
    },
    112: {
        "elements": [
            "All previous elements",
            "Base of second dome laid"
        ],
        "action": "Dome base laid",
        "is_milestone": False
    },
    113: {
        "elements": [
            "All previous elements",
            "First tier of second dome built"
        ],
        "action": "Dome tier 1",
        "is_milestone": False
    },
    114: {
        "elements": [
            "All previous elements",
            "Second tier of dome built"
        ],
        "action": "Dome tier 2",
        "is_milestone": False
    },
    115: {
        "elements": [
            "All previous elements",
            "Third tier of dome built"
        ],
        "action": "Dome tier 3",
        "is_milestone": True
    },
    116: {
        "elements": [
            "All previous elements",
            "Fourth tier of dome built"
        ],
        "action": "Dome tier 4",
        "is_milestone": False
    },
    117: {
        "elements": [
            "All previous elements",
            "Fifth tier of dome built"
        ],
        "action": "Dome tier 5",
        "is_milestone": False
    },
    118: {
        "elements": [
            "All previous elements",
            "Dome frame completed"
        ],
        "action": "Dome frame complete",
        "is_milestone": False
    },
    119: {
        "elements": [
            "All previous elements",
            "Exterior panels added to second dome"
        ],
        "action": "Dome panels added",
        "is_milestone": False
    },
    120: {
        "elements": [
            "Complete second Habitat Dome",
            "Glass walkway, rocket, first habitat with dish"
        ],
        "action": "Second dome complete!",
        "is_milestone": True,
        "improvement": "Second habitat dome finished"
    },
    121: {
        "elements": [
            "All previous elements",
            "NEW: First solar panel unfolded behind the base"
        ],
        "action": "First solar panel deployed",
        "is_milestone": True
    },
    122: {
        "elements": [
            "All previous elements",
            "TWO solar panels unfolded"
        ],
        "action": "Second solar panel",
        "is_milestone": False
    },
    123: {
        "elements": [
            "All previous elements",
            "THREE solar panels unfolded"
        ],
        "action": "Third solar panel",
        "is_milestone": False
    },
    124: {
        "elements": [
            "All previous elements",
            "FOUR solar panels unfolded"
        ],
        "action": "Fourth solar panel",
        "is_milestone": False
    },
    125: {
        "elements": [
            "All previous elements",
            "FIVE solar panels fully deployed"
        ],
        "action": "Solar array complete!",
        "is_milestone": True,
        "improvement": "Five solar panels deployed"
    },
    126: {
        "elements": [
            "All previous elements",
            "NEW: Small Moon Garden glass box appears"
        ],
        "action": "Moon garden box placed",
        "is_milestone": True,
        "improvement": "Moon garden greenhouse added"
    },
    127: {
        "elements": [
            "All previous elements",
            "Tiny green sprout appears in the garden box"
        ],
        "action": "First sprout!",
        "is_milestone": False
    },
    128: {
        "elements": [
            "All previous elements",
            "Plant grows its first leaf"
        ],
        "action": "First leaf grows",
        "is_milestone": False
    },
    129: {
        "elements": [
            "All previous elements",
            "Plant has TWO leaves"
        ],
        "action": "Second leaf",
        "is_milestone": False
    },
    130: {
        "elements": [
            "All previous elements",
            "Plant has THREE leaves"
        ],
        "action": "Third leaf",
        "is_milestone": True
    },
    131: {
        "elements": [
            "All previous elements",
            "Plant has FOUR leaves"
        ],
        "action": "Fourth leaf",
        "is_milestone": False
    },
    132: {
        "elements": [
            "All previous elements",
            "Plant has FIVE leaves"
        ],
        "action": "Fifth leaf",
        "is_milestone": False
    },
    133: {
        "elements": [
            "All previous elements",
            "Plant has SIX leaves"
        ],
        "action": "Sixth leaf",
        "is_milestone": False
    },
    134: {
        "elements": [
            "All previous elements",
            "Plant has SEVEN leaves"
        ],
        "action": "Seventh leaf",
        "is_milestone": False
    },
    135: {
        "elements": [
            "All previous elements",
            "Plant has EIGHT leaves - thriving!"
        ],
        "action": "Moon plant thriving!",
        "is_milestone": True,
        "improvement": "Moon plant fully grown (8 leaves)"
    },
    136: {
        "elements": [
            "All previous elements",
            "NEW: Flag pole erected in the soil"
        ],
        "action": "Flag pole planted",
        "is_milestone": True
    },
    137: {
        "elements": [
            "All previous elements",
            "Flag begins to unfurl (20%)"
        ],
        "action": "Flag unfurling - 20%",
        "is_milestone": False
    },
    138: {
        "elements": [
            "All previous elements",
            "Flag 40% unfurled"
        ],
        "action": "Flag unfurling - 40%",
        "is_milestone": False
    },
    139: {
        "elements": [
            "All previous elements",
            "Flag 60% unfurled"
        ],
        "action": "Flag unfurling - 60%",
        "is_milestone": False
    },
    140: {
        "elements": [
            "All previous elements",
            "Flag FULLY unfurled and waving"
        ],
        "action": "Flag flying!",
        "is_milestone": True,
        "improvement": "Flag fully unfurled"
    },
    141: {
        "elements": [
            "All previous elements",
            "NEW: Second astronaut appears on the tile"
        ],
        "action": "Second astronaut arrives!",
        "is_milestone": True,
        "improvement": "Second astronaut joins crew"
    },
    142: {
        "elements": [
            "All previous elements",
            "Second astronaut walking toward the habitat"
        ],
        "action": "Astronaut approaching habitat",
        "is_milestone": False
    },
    143: {
        "elements": [
            "All previous elements",
            "Second astronaut preparing to wave"
        ],
        "action": "Astronaut preparing greeting",
        "is_milestone": False
    },
    144: {
        "elements": [
            "All previous elements",
            "Second astronaut starting to wave"
        ],
        "action": "Astronaut waving",
        "is_milestone": False
    },
    145: {
        "elements": [
            "All previous elements",
            "Both astronauts visible, waving at each other"
        ],
        "action": "Crew greeting!",
        "is_milestone": True
    },
    146: {
        "elements": [
            "All previous elements",
            "NEW: ONE string of LED lights hung between structures"
        ],
        "action": "First LED string",
        "is_milestone": False
    },
    147: {
        "elements": [
            "All previous elements",
            "TWO strings of LED lights"
        ],
        "action": "Second LED string",
        "is_milestone": False
    },
    148: {
        "elements": [
            "All previous elements",
            "THREE strings of LED lights"
        ],
        "action": "Third LED string",
        "is_milestone": False
    },
    149: {
        "elements": [
            "All previous elements",
            "FOUR strings of LED lights"
        ],
        "action": "Fourth LED string",
        "is_milestone": False
    },
    150: {
        "elements": [
            "Complete moonbase with rocket, two domes, walkway, solar panels, garden, flag",
            "Two astronauts",
            "LED lights strung between rocket and domes - festive!"
        ],
        "action": "Phase 3 Complete - Moonbase celebration!",
        "is_milestone": True,
        "improvement": "LED lights decorated throughout base"
    },

    # =========================================================================
    # PHASE 4: FUTURISTIC UPGRADE (Days 151-200)
    # =========================================================================
    151: {
        "elements": [
            "All Phase 3 elements",
            "ONE wooden crate replaced by white carbon-fiber canister"
        ],
        "action": "Upgrading supplies - 1",
        "is_milestone": True
    },
    152: {
        "elements": [
            "All previous elements",
            "TWO crates replaced by white canisters"
        ],
        "action": "Upgrading supplies - 2",
        "is_milestone": False
    },
    153: {
        "elements": [
            "All previous elements",
            "THREE crates replaced"
        ],
        "action": "Upgrading supplies - 3",
        "is_milestone": False
    },
    154: {
        "elements": [
            "All previous elements",
            "FOUR crates replaced"
        ],
        "action": "Upgrading supplies - 4",
        "is_milestone": False
    },
    155: {
        "elements": [
            "All previous elements",
            "FIVE crates replaced"
        ],
        "action": "Upgrading supplies - 5",
        "is_milestone": True
    },
    156: {
        "elements": [
            "All previous elements",
            "SIX crates replaced"
        ],
        "action": "Upgrading supplies - 6",
        "is_milestone": False
    },
    157: {
        "elements": [
            "All previous elements",
            "SEVEN crates replaced"
        ],
        "action": "Upgrading supplies - 7",
        "is_milestone": False
    },
    158: {
        "elements": [
            "All previous elements",
            "EIGHT crates replaced"
        ],
        "action": "Upgrading supplies - 8",
        "is_milestone": False
    },
    159: {
        "elements": [
            "All previous elements",
            "NINE crates replaced"
        ],
        "action": "Upgrading supplies - 9",
        "is_milestone": False
    },
    160: {
        "elements": [
            "ALL wooden crates replaced by sleek white carbon-fiber canisters"
        ],
        "action": "Supply upgrade complete!",
        "is_milestone": True,
        "improvement": "All crates upgraded to carbon-fiber canisters"
    },
    161: {
        "elements": [
            "All previous elements",
            "ONE Ion Drive ring replacing engine component"
        ],
        "action": "Ion drive upgrade - 1",
        "is_milestone": True
    },
    162: {
        "elements": [
            "All previous elements",
            "TWO Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 2",
        "is_milestone": False
    },
    163: {
        "elements": [
            "All previous elements",
            "THREE Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 3",
        "is_milestone": False
    },
    164: {
        "elements": [
            "All previous elements",
            "FOUR Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 4",
        "is_milestone": False
    },
    165: {
        "elements": [
            "All previous elements",
            "FIVE Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 5",
        "is_milestone": True
    },
    166: {
        "elements": [
            "All previous elements",
            "SIX Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 6",
        "is_milestone": False
    },
    167: {
        "elements": [
            "All previous elements",
            "SEVEN Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 7",
        "is_milestone": False
    },
    168: {
        "elements": [
            "All previous elements",
            "EIGHT Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 8",
        "is_milestone": False
    },
    169: {
        "elements": [
            "All previous elements",
            "NINE Ion Drive rings"
        ],
        "action": "Ion drive upgrade - 9",
        "is_milestone": False
    },
    170: {
        "elements": [
            "Rocket engines fully replaced by GLOWING BLUE ION DRIVE rings"
        ],
        "action": "Ion drive complete!",
        "is_milestone": True,
        "improvement": "Engines replaced with glowing blue Ion Drive"
    },
    171: {
        "elements": [
            "All previous elements",
            "ONE hexagonal power-floor tile laid"
        ],
        "action": "Power floor - 1",
        "is_milestone": False
    },
    172: {
        "elements": [
            "All previous elements",
            "TWO hexagonal power-floor tiles"
        ],
        "action": "Power floor - 2",
        "is_milestone": False
    },
    173: {
        "elements": [
            "All previous elements",
            "THREE hexagonal power-floor tiles"
        ],
        "action": "Power floor - 3",
        "is_milestone": False
    },
    174: {
        "elements": [
            "All previous elements",
            "FOUR hexagonal power-floor tiles"
        ],
        "action": "Power floor - 4",
        "is_milestone": False
    },
    175: {
        "elements": [
            "All previous elements",
            "FIVE hexagonal power-floor tiles"
        ],
        "action": "Power floor - 5",
        "is_milestone": True
    },
    176: {
        "elements": [
            "All previous elements",
            "SIX hexagonal power-floor tiles"
        ],
        "action": "Power floor - 6",
        "is_milestone": False
    },
    177: {
        "elements": [
            "All previous elements",
            "SEVEN hexagonal power-floor tiles"
        ],
        "action": "Power floor - 7",
        "is_milestone": False
    },
    178: {
        "elements": [
            "All previous elements",
            "EIGHT hexagonal power-floor tiles"
        ],
        "action": "Power floor - 8",
        "is_milestone": False
    },
    179: {
        "elements": [
            "All previous elements",
            "NINE hexagonal power-floor tiles"
        ],
        "action": "Power floor - 9",
        "is_milestone": False
    },
    180: {
        "elements": [
            "Grey moon soil covered with HIGH-TECH HEXAGONAL POWER-FLOOR tiles"
        ],
        "action": "Power floor complete!",
        "is_milestone": True,
        "improvement": "Hexagonal power-floor tiles cover platform"
    },
    181: {
        "elements": [
            "All previous elements",
            "NEW: Hologram projector base appears"
        ],
        "action": "Hologram projector base",
        "is_milestone": True
    },
    182: {
        "elements": [
            "All previous elements",
            "Hologram projector emits a light beam"
        ],
        "action": "Hologram light beam",
        "is_milestone": False
    },
    183: {
        "elements": [
            "All previous elements",
            "Hologram starts forming a map"
        ],
        "action": "Hologram map forming",
        "is_milestone": False
    },
    184: {
        "elements": [
            "All previous elements",
            "Hologram shows stars"
        ],
        "action": "Hologram shows stars",
        "is_milestone": False
    },
    185: {
        "elements": [
            "HOLOGRAM PROJECTOR showing map of the solar system"
        ],
        "action": "Solar system hologram!",
        "is_milestone": True,
        "improvement": "Hologram projector showing solar system map"
    },
    186: {
        "elements": [
            "All previous elements",
            "Astronauts' suits get GOLD-TINTED VISORS"
        ],
        "action": "Gold visors upgrade",
        "is_milestone": True,
        "improvement": "Astronaut suits upgraded with gold visors"
    },
    187: {
        "elements": [
            "All previous elements",
            "BLUE GLOWING ACCENTS added to astronaut suits"
        ],
        "action": "Blue suit accents",
        "is_milestone": False
    },
    188: {
        "elements": [
            "All previous elements",
            "Suits polished to high-tech finish"
        ],
        "action": "Suits polished",
        "is_milestone": False
    },
    189: {
        "elements": [
            "All previous elements",
            "Glow intensity on suits increased"
        ],
        "action": "Suit glow intensified",
        "is_milestone": False
    },
    190: {
        "elements": [
            "Astronauts in FULLY UPGRADED SUITS - gold visors, blue glowing accents"
        ],
        "action": "Suit upgrades complete!",
        "is_milestone": True,
        "improvement": "Astronaut suits fully upgraded"
    },
    191: {
        "elements": [
            "All previous elements",
            "ONE small drone hovering"
        ],
        "action": "First drone appears",
        "is_milestone": False
    },
    192: {
        "elements": [
            "All previous elements",
            "TWO small drones hovering"
        ],
        "action": "Second drone",
        "is_milestone": False
    },
    193: {
        "elements": [
            "All previous elements",
            "THREE small drones hovering"
        ],
        "action": "Third drone",
        "is_milestone": False
    },
    194: {
        "elements": [
            "All previous elements",
            "FOUR small drones hovering"
        ],
        "action": "Fourth drone",
        "is_milestone": False
    },
    195: {
        "elements": [
            "FIVE small drone robots hovering around the rocket"
        ],
        "action": "Drone fleet active!",
        "is_milestone": True,
        "improvement": "Five helper drones deployed"
    },
    196: {
        "elements": [
            "All previous elements",
            "NEW: Launch Countdown digital screen showing: 05"
        ],
        "action": "Countdown: 5",
        "is_milestone": True,
        "improvement": "Launch countdown initiated"
    },
    197: {
        "elements": [
            "All previous elements",
            "Countdown screen: 04"
        ],
        "action": "Countdown: 4",
        "is_milestone": False
    },
    198: {
        "elements": [
            "All previous elements",
            "Countdown screen: 03"
        ],
        "action": "Countdown: 3",
        "is_milestone": False
    },
    199: {
        "elements": [
            "All previous elements",
            "Countdown screen: 02",
            "BLUE STEAM starts venting from the rocket base"
        ],
        "action": "Countdown: 2 - Steam venting!",
        "is_milestone": False
    },
    200: {
        "elements": [
            "Countdown screen: 01",
            "Rocket LIFTING 1 INCH off the ground",
            "Engines GLOWING BRIGHT BLUE",
            "Both astronauts SALUTING",
            "Complete futuristic moonbase below"
        ],
        "action": "LIFTOFF! Mission complete!",
        "is_milestone": True,
        "improvement": "ROCKET LAUNCHING - MISSION SUCCESS!"
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
║  ⚠️  MANDATORY LAYOUT LOCK - COPY EXACTLY FROM DAY {anchor_day}  ⚠️                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

The following description is from Day {anchor_day}. You MUST reproduce the EXACT SAME:
- Platform position and angle
- Positions of ALL structures (rocket, domes, etc.)
- Positions of ALL accessories (crates, rover, fuel barrels, etc.)
- Astronaut positions (if present)

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

    return f"""
{BASE_STYLE}
{anchor_section}
{improvements_section}
═══════════════════════════════════════════════════════════
DAY {day} OF 200 - MOONBASE & SPACESHIP CONSTRUCTION
═══════════════════════════════════════════════════════════

SCENE ELEMENTS (all must be visible):
{elements_list}

TODAY'S ACTION: {action}

STRICT RULES:
1. ⚠️ PLATFORM: Grey lunar soil tile with layered cross-section (grey → tan → brown → dark)
2. ⚠️ BACKGROUND: Plain solid BRIGHT GREEN (#00FF00) - completely flat, no texture
3. ⚠️ EARTH: Small Earth visible floating in top-right corner
4. ⚠️ STYLE: Claymation/stop-motion diorama with tilt-shift miniature effect
5. ⚠️ CONSISTENCY: Keep all previous elements in same positions
6. Every element must be sharp and detailed
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

    # Build reference images
    day1_path = OUTPUT_DIR / "day-001.png"
    prev_path = OUTPUT_DIR / f"day-{(day-1):03d}.png" if day > 1 else None

    try:
        if day == 1:
            contents = [prompt]
        elif is_quality_reset_day(day) and day1_path.exists():
            # QUALITY RESET: Only Day 1 reference
            day1_image = Image.open(day1_path)
            contents = [
                "⚠️ QUALITY RESET - Match this quality level EXACTLY:",
                "Copy the detail level, background flatness, and sharpness from this reference:",
                day1_image,
                f"\nCreate Day {day} with MAXIMUM QUALITY:\n" + prompt
            ]
        elif day1_path.exists() and prev_path and prev_path.exists():
            # DUAL REFERENCE: Day 1 (quality) + Previous day (layout)
            day1_image = Image.open(day1_path)
            prev_image = Image.open(prev_path)
            contents = [
                "QUALITY REFERENCE (match detail level):",
                day1_image,
                f"\n⚠️ LAYOUT REFERENCE (Day {day-1}) - COPY THIS EXACTLY:",
                "Match the EXACT positions of all elements from this image:",
                prev_image,
                f"\nNow create Day {day} - add ONLY the new element, keep everything else identical:\n" + prompt
            ]
        elif day1_path.exists():
            day1_image = Image.open(day1_path)
            contents = [
                "Match this quality level:",
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
                    # Note: Gemini may not support custom sizes, using default
                    # Post-process resize to 720px if needed
                ),
            ),
        )

        for part in response.parts:
            if part.inline_data:
                # Save the generated image first
                part.as_image().save(filename)

                # Reopen with PIL and resize to 720px (30% smaller than 1024)
                pil_image = Image.open(filename)
                if pil_image.width != IMAGE_SIZE or pil_image.height != IMAGE_SIZE:
                    pil_image = pil_image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
                    pil_image.save(filename)

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
    print("V14: Spaceship/Moonbase Theme - Auto-Anchor System")
    print("=" * 60)
    print()
    print(f"Output: {OUTPUT_DIR}")
    print(f"Image size: {IMAGE_SIZE}x{IMAGE_SIZE}px (30% smaller for mobile)")
    print(f"Checkpoint interval: Every {CHECKPOINT_INTERVAL} days")
    print(f"Total days: {len(DAYS)}")
    print()

    load_anchors()

    for day in range(1, 201):  # Days 1-200 (existing will be skipped)
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
    print(f"Improvements tracked: {len(IMPROVEMENTS)}")
    print(f"Saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
