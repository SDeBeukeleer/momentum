# Isometric Platform Plant Visuals - Design Plan

## Overview

Replace the current glass terrarium images with **isometric platform tiles** - square earth/soil platforms tilted at an angle to give 3D depth, with plants growing on top. No container, no conflicting background colors.

---

## Visual Concept

### Platform Design
- **Shape**: Square platform viewed at ~45° isometric angle
- **Material**: Rich dark soil/earth with moss, small stones, and organic details
- **Edge**: Visible layered earth cross-section (like a floating island chunk)
- **Background**: Transparent PNG - works on any app background
- **Style**: Same claymation/stop-motion aesthetic for consistency

### Example Visual
```
         🌱
       /    \
      /  🪴  \
     /________\    <- Tilted square platform
    |    ◯    |    <- Earth cross-section with layers
    |_________|
```

### Platform Progression
The platform itself could evolve:
- **Days 1-30**: Simple earth tile with basic moss
- **Days 31-75**: Richer soil, small decorative stones appear
- **Days 76-100**: Magical elements, crystals in the earth
- **Days 101-150**: Glowing elements, ethereal particles
- **Days 151-200**: Cosmic/celestial platform effects

---

## Gemini Prompt Template

### Base Style
```
isometric 3D view of a square earthen platform tile viewed from above at 45 degree angle,
the platform shows layered soil cross-section on the edges,
claymation stop-motion style, transparent background,
soft studio lighting with gentle shadows,
the platform floats with no container or enclosure
```

### Example Prompts

**Day 1 - Seed:**
```
isometric 3D view of a square earthen platform tile viewed from above at 45 degree angle,
a tiny seed half-buried in rich dark soil on top,
the platform shows layered soil cross-section on the edges with small pebbles,
claymation stop-motion style, transparent background (PNG),
soft studio lighting, subtle moss around the edges
```

**Day 30 - Young Plant:**
```
isometric 3D view of a square earthen platform tile viewed from above at 45 degree angle,
a healthy young plant with vibrant green leaves growing from the center,
the platform shows rich soil layers with decorative stones and moss,
claymation stop-motion style, transparent background (PNG),
soft warm studio lighting, the plant has a sturdy stem
```

**Day 100 - Magical Tree:**
```
isometric 3D view of a square earthen platform tile viewed from above at 45 degree angle,
an ancient magical bonsai tree with a gnarled trunk and crystalline leaves,
the platform shows mystical soil layers with embedded crystals and glowing moss,
claymation stop-motion style, transparent background (PNG),
ethereal lighting, tiny magical particles floating around
```

---

## Implementation Steps

### Phase 1: Test Generation (1-2 hours)
1. Generate 5 test images at key days (1, 7, 30, 75, 150)
2. Verify transparent background works
3. Validate isometric angle and style consistency
4. Test how it looks on dark background in the app

### Phase 2: Full Asset Generation
1. Update generation script with new prompts
2. Generate all 200 images
3. Review and regenerate inconsistent ones
4. Remove background if not transparent (rembg tool)

### Phase 3: Code Updates
1. Update DioramaDisplay component styling
   - Remove amber glow (was matching terrarium)
   - Add subtle green/teal glow to match botanical noir
2. Update loading skeleton colors
3. Test across all sizes (mini, medium, full)

### Phase 4: Clean Up
1. Delete old terrarium images
2. Update any amber/cream color references

---

## Color Adjustments for DioramaDisplay.tsx

```tsx
// Current (terrarium themed):
- bg-gradient-to-br from-amber-100 to-amber-200 // loading
- bg-amber-400 // glow

// New (botanical noir themed):
- bg-gradient-to-br from-primary/20 to-accent/20 // loading
- bg-primary // glow (green)
```

---

## Alternative Future Visuals

Once the platform system is in place, you could have different visual themes:
- **Garden**: Plants (current) - Jade plant with gnome, mushrooms, creatures
- **Crystal Cave**: Crystals growing from stone platforms - Miner gnome, geodes, glowing mushrooms
- **Ocean**: Coral growing on rock tiles - Mermaid, tropical fish, octopus, treasure
- **Space**: Rocket being built on moon base - Astronauts, rover, habitat dome, Earth in sky
- **Desert**: Cacti on sandy platforms - Explorer, gecko, scorpion, oasis
- **Car Restoration**: Vintage car being restored - Mechanic, tools, garage workshop

Each could be a theme users unlock or choose!

---

## Questions to Confirm

1. **Platform shape**: Square, hexagon, or circular?
2. **Edge detail**: Simple cut or visible earth layers?
3. **Glow effect**: Keep the subtle glow animation?
4. **Shadow**: Include drop shadow for depth?

---

## Cost Estimate

- Regenerating 200 images: ~$4-8 (Gemini API)
- Time: ~2-4 hours for generation + review
- Code changes: ~30 minutes

---

## Next Steps

1. Confirm design direction
2. Generate 5 test images
3. Review in app on dark background
4. If approved, generate full set
