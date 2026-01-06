# V13 Auto-Anchor System - Resume Instructions

## Current Status (January 2, 2026)

### Completed
- Days 1-5 generated successfully
- Day 5 checkpoint created with detailed anchor description
- Day 6 deleted (needs regeneration with improved prompts)

### Files
- **Script**: `scripts/generate_v13_auto_anchor.py`
- **Output folder**: `public/diorama/v13-auto-anchor/`
- **Anchors file**: `public/diorama/v13-auto-anchor/anchors.json`

### What was fixed
The script was updated with stronger orientation locking to fix the Day 6 drift issue:

1. **BASE_STYLE now includes CRITICAL CAR REQUIREMENTS**:
   - Explicitly states what the car should NOT have (wheels, headlights, bumpers, etc.)
   - Makes it clear the car is a "HOLLOW RUSTED SHELL"

2. **Stronger anchor prompts**:
   - Added "MANDATORY ORIENTATION LOCK" section with visual emphasis
   - Requires exact reproduction of car position, angle, orientation, and accessory positions

3. **DO NOT section**:
   - Lists all parts that should NOT appear yet
   - Prevents Gemini from adding wheels, headlights, etc. prematurely

## To Resume Tomorrow

Run the following command when the API quota resets:

```bash
cd /Users/stevendebeukeleer/Claude\ Code\ Projects/momentum
export GEMINI_API_KEY=your-api-key-here
python scripts/generate_v13_auto_anchor.py
```

### Expected behavior:
1. Days 1-5 will be skipped (already exist)
2. Day 6 will be regenerated with improved prompts
3. Days 7-10 will be generated
4. Day 10 checkpoint will be created
5. Days 11-15 will be generated
6. Day 15 checkpoint will be created
7. Days 16-20 will be generated
8. Day 20 checkpoint will be created

### What to verify:
- [ ] Day 6 car orientation matches Day 5 anchor
- [ ] Car remains a hollow shell (no wheels, headlights)
- [ ] Accessories stay in same positions across checkpoints
- [ ] Quality stays consistent throughout
- [ ] Checkpoints at Day 10, 15, 20 are created

## Day 5 Anchor Description (saved)

The anchor for Day 5 contains detailed descriptions of:
- Car orientation (front toward bottom-left corner, ~30 degrees)
- Car state (hollow rusted shell, empty wheel wells)
- Accessories: toolbox (back-left), wrench (near car), jack (back-right), mechanic (right side)
- Platform with brick segments on edges

## If Day 6 still drifts

Options to try:
1. Increase reference image influence in the prompt
2. Use Day 5 as BOTH quality and scene reference
3. Add even more explicit constraints to the prompt
4. Consider using a different model if available

## Full 200-Day Plan

Once the 20-day test validates the approach:
1. Expand DAYS dictionary to all 200 days
2. Keep checkpoint interval at 5 days
3. Track all improvements in the IMPROVEMENTS list
4. Key state changes to watch:
   - Day 50: Car sanded smooth
   - Day 62: Car primed grey
   - Day 73: Car painted red
   - Day 80: Car polished glossy
   - Day 117: Wheels installed
   - Day 120: Engine running
