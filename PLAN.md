# Plan de Ejecución: Super Bukele 64 — Exterior Completo del Castillo de Peach

**Objetivo**: Replicar fielmente el exterior completo del Castillo de Peach (*Castle Grounds* de *Super Mario 64*), con su geometría original de decompilación y texturas HD de `RENDER96-HD-TEXTURE-PACK`, integrando al personaje 3D de Nayib Bukele diseñado según los renders de `Desktop/assets2`, la música y voces originales extraídas de la ROM US de *Super Mario 64*, y culminando la partida cuando Bukele abre y cruza las puertas estelares del castillo.

---

## 1. Alcance Arquitectónico, Sonoro y Narrativo
* **Punto de Inicio**: Tubería verde N64 recién emergida en `(-13.28, 2.60, 46.64)` (relevo exacto del corte en el segundo 49.0 de la cinemática de Lakitu).
* **Entorno Completo (*Castle Grounds*, Área 1)**:
  * Suelo de pradera verde, senderos de arena, acantilados rocosos y sombras circulares con canal alfa (`0900BC00`).
  * Foso perimetral y laguna lateral con agua animada, rejillas sumergidas (`areas/1/7` y `8`) y cascada con desplazamiento UV continuo (`movtext.inc.c`).
  * Puente central de piedra que cruza el foso hacia el pórtico real.
  * Fachada monumental del castillo con torreones laterales, **torre central alta con asta (`areas/1/3`, `special_level_geo_03`)**, vitral de la Princesa Peach y 4 banderas rojas ondeando al viento (`bhvCastleFlagWaving`).
  * **26 árboles oficiales con textura HD (`special_bubble_tree`)** en billboard sobre eje Y y colisión cilíndrica de tronco.
  * **4 carteles cómicos de madera (`wooden_signpost.glb`)** con cuadro de diálogo contextual N64 (`#sign-dialog`).
  * **Puertas dobles estelares (`castle_door.glb`)** articuladas en el arco frontal (`Z = -31.55, Y = 8.03`).
* **Personaje**: Nayib Bukele en 3D (`assets/models/bukele_body.glb` + `assets/models/bukele_head.glb` con recorte limpio de cuello por shader), vistiendo saco formal azul marino oscuro, camiseta negra lisa, pantalón azul marino y zapatos cafés conforme a `Desktop/assets2`.
* **Audio Original SM64**: Sintetizado directamente desde las secuencias `.m64`, bancos de instrumentos JSON y muestras `.aiff` extraídas de la ROM original US provista por el usuario (`castle_grounds_bgm.mp3`, `star_fanfare.mp3`, `coin.mp3`, `door_open.mp3`, `mario_0C.mp3` y voces de salto).
* **Condición de Victoria**: Al llegar al umbral del pórtico (`Z ≈ -29.5`), las dos puertas estelares se abren hacia afuera (`±1.62 rad`) con su sonido clásico de madera (`door_open.mp3`), Bukele camina hacia el interior del castillo, suena *"Here we go!"* seguido de la fanfarria clásica de estrella (`star_fanfare.mp3`) y se despliega `#victory-modal` con Bitcoins recolectados (`X / 10`), tiempo transcurrido (`MM:SS`) y botón de reinicio.

---

## 2. Fases Ejecutadas y Verificadas

### Fase 1: Artefactos de Diseño y Barra Visual (`PLAN.md`, `art/BAR.md`, `art/LEDGER.md`)
- Definición de criterios arquitectónicos, materiales HD, personaje `assets2`, audio auténtico y secuencia de victoria.

### Fase 2: Geometría Completa de *Castle Grounds* y Actores 3D (`scripts/export_castle_grounds.py`, `scripts/export_castle_actors.py`)
- Recorrido exacto de listas de despliegue RSP (`gsSPDisplayList`) incluyendo terreno, fachada, torre central alta (`areas/1/3`) y rejillas (`areas/1/7`, `8`), iluminación direccional `gdSPDefLights1` y soporte de superficies `G_CC_SHADE` (`assets/models/castle_grounds.glb`).
- Exportación de `assets/models/castle_door.glb` (madera pulida, pomo dorado y emblema estelar `one_star_door_sign.rgba16.png`) y `assets/models/wooden_signpost.glb`, más texturas HD de follaje (`tree_left_side.rgba16.png`, `tree_right_side.rgba16.png`).

### Fase 3: Personaje 3D de Nayib Bukele (`scripts/build_bukele_hero.py`)
- Construcción de cuerpo articulado (`Torso`, `ArmL`, `ArmR`, `LegL`, `LegR`) fiel a `Desktop/assets2` en `assets/models/bukele_body.glb` ensamblado con el busto de alta resolución `assets/models/bukele_head.glb` recortado limpiamente en cuello y nuca mediante `onBeforeCompile`.

### Fase 4: Síntesis de Música y Efectos Originales SM64 (`scripts/render_sm64_audio.py`)
- Decodificación de secuencias `.m64` (`03_level_grass` para exteriores y `01_cutscene_collect_star` para victoria) con articulación exacta `noteDuration` de `seqplayer.c` y muestras PCM `.aiff` del banco `22`, más efectos originales de moneda, puertas de madera y voces.

### Fase 5: Integración en Three.js y Secuencia de Victoria (`js/game.js`, `index.html`, `css/style.css`)
- Integración de los 26 árboles HD, cascada animada, foso y laguna, 4 banderas ondeantes, 4 carteles interactivos, 10 Bitcoins con símbolo `₿` en relieve sobre el sendero real y cinemática `SCENE_DOOR_OPENING` ➔ `SCENE_VICTORY`.

### Fase 6: Verificación Visual Headless (`scripts/shot.sh`)
- Captura e inspección visual con Chromium WebGL (SwiftShader) de vista panorámica del castillo, primer plano de Bukele junto a cartel interactivo, puente con Bitcoins frente a las puertas estelares y cinemática de apertura de puertas + pantalla de victoria.

### Fase 7: Documentación y Commits Granulares (`pj-vibe-game` y `pj-vibe-game-docs`)
- Commits atómicos de cada cambio y actualización completa de `_docs/prompts.md` e `_docs/iteracion.md`.
