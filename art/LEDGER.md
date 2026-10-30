# Asset Ledger: Super Bukele 64

| Asset ID | Type | Source | Target Ref | Status | Notes |
|---|---|---|---|---|---|
| `hero_bukele_head` | 3D Character Bust (GLB) | Tripo3D + Blender Pipeline | `ref-05`, `ref-07` | final | High-fidelity 3D PBR bust of Nayib Bukele (`assets/models/bukele_head.glb`, 12 MB) |
| `hero_bukele_gameplay` | 3D Character (GLB) | Blender Pipeline (`scripts/build_bukele_hero.py`) + Shader Neck Crop | `Desktop/assets2` | final | Formal dark navy blazer, black tee, dark navy pants, brown shoes, articulated `ArmL`/`ArmR`/`LegL`/`LegR` (`assets/models/bukele_body.glb`, 181 KB) + real head |
| `title_logo_super_bukele_64` | 3D Typographic Block | Blender Render (`assets/img/super_bukele_64_logo.png`) | `ref-01` | final | Classic N64 multi-color extruded logo |
| `prop_warp_pipe` | 3D Prop | Procedural Three.js Mesh | `ref-01-castle-wide` | final | Green N64 warp pipe with sand base at exact SM64 intro spawn `(-13.28, 2.60, 46.64)` |
| `env_castle_grounds` | 3D Level (GLB) | Extracted from `Render96ex/levels/castle_grounds/areas/1/{1..10}` + `RENDER96-HD-TEXTURE-PACK` | `ref-01-castle-wide`, `ref-03-bridge-env` | final | Complete Peach's Castle Grounds geometry with central spire, moat/cannon grills, N64 vertex lighting, and 27 HD textures (`assets/models/castle_grounds.glb`, 3.0 MB) |
| `env_ocean_sky_water` | Skybox & Water | `ocean_sky.jpg` + `water.png` + `movtext.inc.c` Waterfall | `ref-01-castle-wide` | final | Authentic ocean sky dome, animated moat/lake water boxes, and scrolling cliff waterfall |
| `env_bubbly_trees` | 3D Y-Billboard Props | `RENDER96-HD-TEXTURE-PACK/gfx/actors/tree/` (26 instances) | `ref-01-castle-wide`, `ref-02-grounds-action` | final | All 26 exact `special_bubble_tree` placements from `collision.inc.c` with trunk collision |
| `env_castle_flags` | 3D Animated Props | Procedural Ribbon + Pole at `script.c` tower coords | `ref-01-castle-wide` | final | 4 waving red tower flags (`bhvCastleFlagWaving`) |
| `prop_castle_doors` | 3D Animated Actor (GLB) | `Render96ex/actors/door/` + `RENDER96-HD` (`scripts/export_castle_actors.py`) | `ref-01-castle-wide`, `ref-03-bridge-env` | final | Double wooden Star-emblem doors (`assets/models/castle_door.glb`) at `(-1.53/+1.54, 8.03, -31.55)` with outward porch opening animation |
| `prop_wooden_signpost` | 3D Interactive Actor (GLB) | `Render96ex/actors/wooden_signpost/` + `RENDER96-HD` | `ref-02-grounds-action` | final | Classic wooden signposts (`assets/models/wooden_signpost.glb`) with proximity N64 comical dialogue banners |
| `prop_bitcoin` | 3D Collectable | Three.js Cylinder + Torus + Procedural `₿` Emblem Texture | `ref-02-grounds-action` | final | 10 rotating golden Bitcoins guiding from warp pipe across stone bridge to castle doors |
| `audio_castle_grounds_bgm` | Music Track (MP3) | Rendered from user US ROM `03_level_grass.m64` + Bank `22` (`scripts/render_sm64_audio.py`) | `ref-01` | final | Authentic 73.7s Koji Kondo outdoor theme (`assets/audio/sm64/castle_grounds_bgm.mp3`) |
| `audio_star_fanfare` | Victory Fanfare (MP3) | Rendered from user US ROM `01_cutscene_collect_star.m64` + Bank `22` | `ref-01` | final | Authentic 4.96s Star Collect victory fanfare (`assets/audio/sm64/star_fanfare.mp3`) |
| `audio_sm64_sfx_voices` | SFX & Voices (MP3) | Extracted from user US ROM (`sfx_mario`, `sfx_mario_peach`, `sfx_5`, `sfx_9`) | `ref-01` | final | Jump voices (`Wah!`, `Hoo!`, `Yah!`, `Hoo-hoo!`, `Yahoo!`), `Here we go!`, coin chime (`coin.mp3`), and wooden castle door open (`door_open.mp3`) |
