# Game Brief: Super Bukele 64

**Publish: LOCKED**

## Overview
* **Working Title**: Super Bukele 64
* **Genre**: 3D Platformer Homage (inspired by Super Mario 64, N64 era)
* **Target Audience**: University Coursework / Vibecoding Demonstration
* **Session Length**: 2–4 minutes (Vertical Slice / 1-Star Demo)
* **Platform**: Modern Web Browsers via WebGL (Three.js)

## Narrative & Scope
* **Protagonist**: Nayib Bukele, modeled in Blender as a tailored low-poly 3D character in ceremonial dark uniform with gold embroidery and the blue-and-white presidential sash.
* **Objective**: Bowser has kidnapped First Lady Gabriela and fortified the mountain summit. Bukele must collect 5 Bitcoin tokens and reach the golden Power Star at the summit to dispel Bowser's barrier.
* **Win Condition**: Reaching and touching the golden Power Star at the mountain peak.
* **Fail Condition**: Falling off the boundary triggers a safe respawn at the origin point.

## Scene Progression
1. **Scene 1 (Title Screen)**: Pitch-black backdrop, 3D extruded polygonal wooden block letters "SUPER BUKELE 64", cyan glowing license notice `©2026 Kodigo Academy`, and animated "PRESS START".
2. **Scene 2 (Meadow & Mountain)**: 3D third-person exploration with WASD/jump controls, collectable Bitcoins, tiered terrain, and floating platforms.
3. **Scene 3 (Victory Celebration)**: Zoom on Bukele performing the victory salute, synthesized celebratory fanfare, and victory modal.

## Technical Stack & Constraints
* **Renderer**: Three.js (WebGL) with PCF soft shadows, directional sun, hemisphere ambient, and Web Audio API synthesizer.
* **Hero Asset Pipeline**: Authored in Blender via headless Python, exported as glTF/GLB (`assets/models/bukele.glb`), bound to Three.js with skeletal/joint animation.
* **No Non-Original Assets**: Strictly homage-only. All models, code, and synthesized sounds are original.

## Non-Goals
* Full multi-world game scope (focus strictly on a pristine 1-Star vertical slice).
* Pre-recorded heavy MP3 audio assets (all sound is synthesized in real time via Web Audio API).
