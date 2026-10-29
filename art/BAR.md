# Visual Bar: Super Bukele 64

Locked Visual Bar criteria for *Super Bukele 64*. Every listed criterion must PASS for WIN.

| ID | Name | Tier | PASS Condition | FAIL Signs | Justifying Refs |
|---|---|---|---|---|---|
| **C1** | Materials and Lighting | Core | Lighting rig has directional key with cast shadows, soft ambient fill, and consistent light direction across hero, terrain, and props. | Flat unlit geometry, missing shadows, inverted normal maps, unshaded ground planes. | `ref-01`, `ref-03` |
| **C2** | Geometry and Silhouette Density | Core | Hero character has articulated proportions, limbs, head with hair/beard volume, and distinct garment geometry. Props read with natural low-poly silhouette. | Floating eye spheres, primitive-box mittens, unmodeled cylinder trunks, graybox stand-ins. | `ref-02`, `ref-03` |
| **C3** | SxS Blur Test | Core | Blurred game captures maintain the same value structure, color hierarchy, and focal contrast as the locked reference shots. | Washed out contrast, monochromatic mud, unreadable hero silhouette when blurred. | `ref-01`, `ref-02` |
| **C4** | Live Capture Provenance | Core | All captures are generated live from the running Three.js engine and Blender turnarounds. | Mockups, pre-rendered static fakes, concept drawings passed as engine output. | All |
| **C5** | Walkthrough Consistency | Core | 60 FPS smooth motion, responsive jump physics with natural parabola, and seamless camera tracking. | Jittery camera clipping, physics teleportation, infinite air-jumping. | `ref-01` |
| **C6** | Title Screen & N64 Typography | Game | Extruded 3D block letters with multi-color palette (red, blue, yellow, green), wood-carved bevel shadows, 3D tilted "64", and glowing cyan `©2026 Kodigo Academy`. | Flat 2D unstyled system fonts, missing wooden extrusion depth, incorrect copyright text. | `ref-01` |
| **C7** | Hero Ceremonial Regalia | Game | Nayib Bukele is authored in Blender and exported as GLB with high collar gold embroidery, blue-and-white presidential sash with center seal, and styled hair/beard. | Generic default mannequin, primitive boxes without clothing details, missing sash. | `ref-02`, `ref-04` |
