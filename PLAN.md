# Plan de Ejecución: Super Bukele 64 - Exterior del Castillo de Peach

**Objetivo**: Replicar fielmente el exterior completo del Castillo de Peach (Peach's Castle Grounds), con sus superficies y texturas HD de RENDER96, integrando al personaje 3D de Nayib Bukele estilizado según los renders de `Desktop/assets2`, culminando el juego cuando Bukele cruza las puertas del castillo.

---

## 1. Alcance Arquitectónico y Narrativo
* **Punto de Inicio**: Tubería verde N64 recién emergida en el terreno (relevo exacto del video cinemático).
* **Entorno**: Explanada exterior del Castillo de Peach:
  * Suelo de pradera verde y arena modelada.
  * Foso perimetral con canal de agua.
  * Puente central de piedra que cruza el foso.
  * Fachada monumental del castillo con columnas, torreones, vitral superior y las grandes puertas frontales de madera.
* **Personaje**: Nayib Bukele en 3D con traje azul marino formal oscuro, camiseta negra y barba estilizada (conforme a `Desktop/assets2`).
* **Condición de Victoria**: Cruzar las puertas frontales del castillo, activando la cinemática de apertura de puertas, fanfarria de triunfo N64 y pantalla final de victoria con estadísticas.

---

## 2. Fases de Ejecución

### Fase 1: Actualización de Artefactos de la Skill Game-Builder (Stage A)
- Actualizar `BRIEF.md` con el nuevo flujo y condición de victoria.
- Ampliar `art/BAR.md` con los criterios:
  - **C9 (Castle Grounds Architecture & Surfaces)**: Foso, puente, muros y texturas HD de RENDER96.
  - **C10 (Bukele Hero Model fidelity to assets2)**: Traje azul marino, camiseta negra y peinado.
- Actualizar `art/LEDGER.md` con los nuevos assets.

### Fase 2: Modelo 3D de Peach's Castle Grounds y Texturas RENDER96
- Obtener el modelo 3D optimizado (.glb) de los exteriores del castillo de Peach con UVs originales.
- Mapear las texturas HD de `RENDER96-HD-TEXTURE-PACK/gfx/levels/castle_grounds/`:
  - `0.rgba16.png` / `1.rgba16.png` (ladrillos de castillo, piedra, molduras).
  - `2.rgba16.png` (hierba/pradera exterior).
  - `3.rgba16.png` / `4.rgba16.png` (puente de piedra y barandillas).
  - Puertas de madera dobles con herrajes dorados.
- Optimizar la geometría y compresión GLB para Three.js.

### Fase 3: Modelo 3D de Nayib Bukele (Fidelidad a `Desktop/assets2`)
- Modificar los materiales y malla de `assets/models/bukele.glb` en Blender:
  - Traje formal azul marino oscuro con corte contemporáneo.
  - Camiseta interior negra lisa.
  - Barba perfilada y cabello castaño oscuro con volumen.
- Exportar versión final `assets/models/bukele.glb`.

### Fase 4: Integración en Three.js (`js/game.js`)
- Cargar `castle_grounds.glb` con sombras proyectadas y recibidas.
- Posicionar la tubería verde N64 en el punto de spawn idéntico al corte del video.
- Configurar colisionadores de terreno (suelo, foso, puente, muros y puertas).
- Incorporar Bitcoins coleccionables a lo largo del sendero y el puente.
- Añadir el tema musical de exteriores (`assets/audio/castle_grounds_bgm.mp3`).

### Fase 5: Cinemática de Victoria (Entrada al Castillo)
- Detectar cuando el jugador llega al umbral de las puertas del castillo.
- Animación de apertura de las puertas hacia el interior.
- Reproducción de la fanfarria de victoria triunfal de Super Mario 64.
- Despliegue de la pantalla de felicitaciones con tiempo de juego, monedas recolectadas y botón de reinicio.

### Fase 6: Pruebas y Control de Calidad Visual (Stage D)
- Verificación con navegador headless y captura de pantalla en `?scene=gameplay`.
- Inspección de iluminación, materiales y fidelidad contra las capturas de Mario 64.

### Fase 7: Documentación y Publicación en Git
- Actualizar `_docs/prompts.md` y `_docs/iteracion.md` en `pj-vibe-game-docs`.
- Commits y push en `pj-vibe-game` y `pj-vibe-game-docs`.
