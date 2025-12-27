# Pre-Rendered Diorama Assets - Migration Plan

## Overview

Replace the current procedural Three.js plant generation with **200 pre-rendered images** generated using **Google Gemini (Nano Banana Pro)**. This gives you high-quality visuals without needing to learn Blender or 3D software.

---

## Asset Format: Static PNG Images

**One image per day (1-200), generated via Gemini API**

```
public/diorama/
├── day-001.png
├── day-002.png
├── ...
└── day-200.png
```

### Why PNG?
- Gemini outputs PNG natively
- Supports transparency (plant on transparent background)
- Can convert to WebP later for smaller sizes
- No rotation needed - static images are simpler and faster

### Recommended Settings
- **Resolution**: 1K (1024×1024) - good balance of quality and size
- **Aspect Ratio**: 1:1 (square, fits terrarium view)
- **Background**: Request transparent or include terrarium in prompt

---

## Gemini Image Generation Workflow

### Step 1: Set Up Environment

```bash
# Install Python package
pip install google-genai pillow

# Set API key
export GEMINI_API_KEY="your-api-key-here"
```

### Step 2: Base Generation Script

```python
# scripts/generate_diorama_images.py
import os
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

OUTPUT_DIR = Path("public/diorama")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_plant_image(day: int, prompt: str) -> None:
    """Generate a single plant image for a specific day."""
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
            filename = OUTPUT_DIR / f"day-{day:03d}.png"
            image.save(filename)
            print(f"Saved: {filename}")

# Example usage
generate_plant_image(1, "A tiny seed buried in rich brown soil inside a glass terrarium, claymation style, soft lighting, cozy aesthetic")
```

### Step 3: Batch Generation with Progressive Prompts

```python
# scripts/generate_all_plants.py
import os
from google import genai
from google.genai import types
from pathlib import Path
import time

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
OUTPUT_DIR = Path("public/diorama")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Base style to maintain consistency
BASE_STYLE = """
claymation style, miniature diorama inside a glass terrarium jar,
soft warm lighting, cozy aesthetic, highly detailed,
rich brown soil base, tiny decorative elements,
studio photography, shallow depth of field
"""

# Plant progression descriptions
PLANT_STAGES = {
    # Days 1-3: Seed
    (1, 3): "a small round seed partially buried in soil, slight crack forming",

    # Days 4-7: Sprouting
    (4, 5): "seed with tiny green sprout emerging, first sign of life",
    (6, 7): "small green sprout with seed shell still attached, reaching upward",

    # Days 8-14: Seedling
    (8, 10): "tiny seedling with two small round leaves (cotyledons)",
    (11, 14): "young seedling with first true leaves forming, delicate stem",

    # Days 15-21: Young Plant
    (15, 17): "small plant with 4-5 leaves, thickening stem",
    (18, 21): "young bushy plant with multiple leaf clusters",

    # Days 22-30: Maturing
    (22, 25): "healthy plant with full foliage, some leaves with detailed veins",
    (26, 30): "mature plant with dense leaves, small buds forming",

    # Days 31-50: Flowering
    (31, 35): "plant with first small flowers opening",
    (36, 40): "flowering plant with multiple colorful blooms",
    (41, 50): "lush flowering plant in full bloom, vibrant colors",

    # Days 51-75: Full Growth
    (51, 60): "magnificent plant with abundant flowers and foliage",
    (61, 75): "thriving garden plant, some flowers becoming seed pods",

    # Days 76-100: Ancient
    (76, 85): "ancient gnarled plant with thick woody stem, mystical appearance",
    (86, 100): "wise old plant with crystalline elements, magical glow",

    # Days 101-150: Mythic
    (101, 120): "mythical glowing plant with ethereal light, floating particles",
    (121, 150): "legendary tree with golden leaves, magical aura, tiny fairy lights",

    # Days 151-200: Transcendent
    (151, 175): "transcendent crystal tree, prismatic light effects, celestial beauty",
    (176, 200): "ultimate cosmic plant, star-like sparkles, universe within leaves",
}

def get_prompt_for_day(day: int) -> str:
    """Get the appropriate prompt for a specific day."""
    for (start, end), description in PLANT_STAGES.items():
        if start <= day <= end:
            # Add day-specific variation
            progress = (day - start) / (end - start) if end > start else 0
            growth_modifier = f"at {int(progress * 100)}% growth within this stage"
            return f"{description}, {growth_modifier}, {BASE_STYLE}"
    return f"mature plant, {BASE_STYLE}"

def generate_all_images(start_day: int = 1, end_day: int = 200):
    """Generate all plant images."""
    for day in range(start_day, end_day + 1):
        filename = OUTPUT_DIR / f"day-{day:03d}.png"

        # Skip if already exists
        if filename.exists():
            print(f"Skipping day {day} (already exists)")
            continue

        prompt = get_prompt_for_day(day)
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
                    print(f"  Saved: {filename}")
                    break

            # Rate limiting - be nice to the API
            time.sleep(2)

        except Exception as e:
            print(f"  Error on day {day}: {e}")
            time.sleep(5)  # Wait longer on error

if __name__ == "__main__":
    generate_all_images()
```

### Step 4: Maintain Visual Consistency (Multi-Turn Refinement)

For better consistency, use the chat API to refine images:

```python
def generate_with_reference(day: int, reference_image_path: str):
    """Generate a new day's image based on a reference."""
    from PIL import Image

    ref_image = Image.open(reference_image_path)

    prompt = f"""
    Create the next stage of growth for this plant.
    Day {day}: {get_prompt_for_day(day)}
    Keep the same terrarium, soil, and overall style.
    The plant should be slightly more grown than the reference.
    """

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt, ref_image],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",
                image_size="1K"
            ),
        ),
    )

    # Save result...
```

---

## Code Changes Required

### 1. New Simplified Component

```tsx
// src/components/diorama/DioramaDisplay.tsx
'use client';

import Image from 'next/image';
import { useState } from 'react';

interface DioramaDisplayProps {
  currentStreak: number;
  size?: 'mini' | 'full';
}

export function DioramaDisplay({ currentStreak, size = 'full' }: DioramaDisplayProps) {
  const [imageError, setImageError] = useState(false);

  // Clamp to available assets (1-200), fallback to day 1 if streak is 0
  const day = Math.min(Math.max(currentStreak || 1, 1), 200);
  const paddedDay = day.toString().padStart(3, '0');

  const dimensions = size === 'mini' ? 80 : 400;

  // Fallback to last available image if current doesn't exist
  const imageSrc = imageError
    ? '/diorama/day-001.png'
    : `/diorama/day-${paddedDay}.png`;

  return (
    <div className="relative flex items-center justify-center">
      <Image
        src={imageSrc}
        alt={`Plant growth - Day ${day}`}
        width={dimensions}
        height={dimensions}
        priority={size === 'full'}
        className="object-contain"
        onError={() => setImageError(true)}
      />
      {size === 'full' && (
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2
                        bg-black/50 text-white text-sm px-3 py-1 rounded-full">
          Day {day}
        </div>
      )}
    </div>
  );
}
```

### 2. Update Garden Page

```tsx
// In src/app/(dashboard)/garden/page.tsx
// Replace DioramaCanvas with DioramaDisplay

import { DioramaDisplay } from '@/components/diorama/DioramaDisplay';

// Instead of:
// <DioramaCanvas ... />

// Use:
<DioramaDisplay
  currentStreak={displayStreak}
  size="full"
/>
```

### 3. Files to Remove (After Migration)

Once all 200 images are generated and working:

```
src/components/diorama/
├── plant/           # DELETE entire folder
│   ├── stages/      # All 8 stage files
│   └── PlantSystem.tsx
├── Terrarium.tsx    # DELETE (included in generated images)
├── effects/         # DELETE entire folder
└── DioramaCanvas.tsx # REPLACE with DioramaDisplay.tsx
```

### 4. Optional: Remove Three.js Dependencies

```bash
npm uninstall three @react-three/fiber @react-three/drei @react-three/postprocessing @types/three
```

This saves ~500KB from your bundle!

---

## Asset Hosting Strategy

### Option A: Public Folder (Start Here)
```
public/diorama/
├── day-001.png
├── day-002.png
└── ...
```
- Simple, works immediately
- ~200MB for 200 images at 1K resolution
- Git will be slower with large binary files

### Option B: Convert to WebP (Recommended)
After generating PNGs, convert to WebP for 50-70% size reduction:

```bash
# Using cwebp (install via homebrew: brew install webp)
for f in public/diorama/*.png; do
  cwebp -q 85 "$f" -o "${f%.png}.webp"
done
```

### Option C: Use Cloudinary or Vercel Blob (Future)
Move images to CDN once you have many users.

---

## Implementation Phases

### Phase 1: Proof of Concept
1. Generate 10 key images manually (days 1, 7, 14, 30, 50, 100)
2. Create `DioramaDisplay` component
3. Test in garden page
4. Validate visual style and consistency

### Phase 2: Full Asset Generation
1. Run batch script to generate all 200 images
2. Review and regenerate any inconsistent images
3. Convert to WebP
4. Place in public folder

### Phase 3: Code Migration
1. Replace `DioramaCanvas` with `DioramaDisplay`
2. Update all usages (garden page, habit cards)
3. Remove Three.js code and dependencies
4. Test thoroughly

### Phase 4: Polish
1. Add CSS animations (gentle float, glow on milestones)
2. Add loading skeleton/placeholder
3. Preload nearby images for garden scrubber

---

## Prompt Engineering Tips

### For Consistent Style
Always include these elements in your prompts:
- "claymation style" or "stop-motion aesthetic"
- "glass terrarium jar" or "miniature diorama"
- "soft warm lighting"
- "studio photography"
- Specific soil/pot description

### For Progressive Growth
Describe specific growth features:
- Day 1-3: "seed", "buried", "crack forming"
- Day 4-10: "sprout", "emerging", "cotyledons"
- Day 11-30: "leaves", "stem thickening", "bushy"
- Day 31-75: "flowers", "blooms", "vibrant"
- Day 76-100: "ancient", "gnarled", "mystical"
- Day 100+: "magical", "glowing", "ethereal"

### Example Prompts

**Day 1:**
```
A tiny brown seed half-buried in rich dark soil inside a small glass terrarium jar,
claymation stop-motion style, soft warm studio lighting, miniature diorama aesthetic,
the seed has a slight crack starting to form, highly detailed macro photography
```

**Day 30:**
```
A healthy young plant with vibrant green leaves and small flower buds forming,
inside a glass terrarium jar, claymation stop-motion style, soft warm lighting,
the plant has a sturdy stem and full foliage, miniature diorama aesthetic,
some tiny decorative pebbles around the base
```

**Day 100:**
```
An ancient magical bonsai tree with a thick gnarled trunk and crystalline leaves,
soft ethereal glow emanating from within, inside a glass terrarium jar,
claymation stop-motion style, mystical atmosphere, tiny fairy lights floating nearby,
the tree appears wise and powerful, miniature diorama aesthetic
```

---

## Cost Estimate

Gemini API pricing (as of 2024):
- Image generation: ~$0.02-0.04 per image
- 200 images: ~$4-8 total
- Regenerations for consistency: ~$2-4 extra

**Total estimated cost: $6-12**

---

## Questions Resolved

| Question | Decision |
|----------|----------|
| Format | Static PNG images |
| Resolution | 1K (1024×1024) |
| Terrarium | Include in each generated image |
| Habit colors | Single green/natural palette (CSS filters can tint later) |
| Asset hosting | Public folder initially |
| Tool | Gemini API (Nano Banana Pro) |

---

## Next Steps

1. **Get Gemini API key** from [Google AI Studio](https://aistudio.google.com/)
2. **Generate 10 test images** to validate the style
3. **Create DioramaDisplay component**
4. **Iterate on prompts** until visuals are perfect
5. **Batch generate all 200** images
6. **Migrate code** from Three.js to images

Would you like me to help you start generating the first batch of test images?
