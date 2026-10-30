# Estado de Continuidad del Proyecto (`next.md`)

> **Propósito**: Bitácora viva en la raíz de `pj-vibe-game` para retomar el desarrollo de inmediato en caso de corte de sesión o límite de cuota. Se actualiza junto con cada avance relevante.

**Última actualización**: 2026-10-29 21:56 (UTC-6)  
**Repositorio principal**: `/home/omarchy/Projects/pj-vibe-game` (`https://robert-flo.github.io/pj-vibe-game/`)  
**Repositorio de documentación**: `/home/omarchy/Projects/pj-vibe-game-docs` (`https://robert-flo.github.io/pj-vibe-game-docs/`)

---

## 1. ¿Qué ya está completado y publicado (`origin/main`)?

1. **Flujo Completo de 6 Escenas + Victoria**:
   - **Escena 1 (`#scene-1-title`)**: Pantalla de título *SUPER BUKELE 64* con logotipo 3D en tipografía oficial y mosaico N64.
   - **Escena 2 (`#scene-2-overlay`)**: Busto 3D interactivo de Nayib Bukele (`assets/models/bukele_head.glb`) con seguimiento de ratón y arrastre elástico.
   - **Escena 3 (`#scene-3-fileselect`)**: Tablero dorado *SELECT FILE* con 4 ranuras (`BUKELE A–D`) y cursor de mano enguantada 3D (`assets/img/n64_hand_cursor.png`).
   - **Escena 4 (`#scene-letter`)**: Pergamino de la Primera Dama Gabriela con música original (`assets/audio/letter_bgm.mp3`).
   - **Escena 5 (`#scene-cinematic`)**: Vuelo de Lakitu calibrado (`assets/video/lakitu_castle_flight.mp4`, 22.50s, corte exacto en el segundo 49.0 sobre la tubería verde antes de que aparezca Mario).
   - **Escena 6 (`SCENE_6_GAMEPLAY`)**: Exteriores completos del Castillo de Peach (*Castle Grounds*, Área 1).
   - **Cierre (`SCENE_DOOR_OPENING` ➔ `SCENE_VICTORY`)**: Al llegar a `Z ≈ -29.5, Y > 7.2`, las dos puertas estelares se abren hacia el pórtico (`±1.62 rad`), suena `door_open.mp3`, Bukele entra sobre la alfombra roja, suena *"Here we go!"* + `star_fanfare.mp3` y se abre `#victory-modal` con Bitcoins (`X / 10`), tiempo (`MM:SS`) y reinicio.

2. **Arquitectura 3D y Texturas HD (`RENDER96-HD-TEXTURE-PACK`)**:
   - `assets/models/castle_grounds.glb` exportado con `scripts/export_castle_grounds.py`: terreno, puente de piedra, foso, fachada con vitral de Peach, torreones laterales, torre central alta con asta (`areas/1/3`), sombras circulares alfa (`0900BC00`) y rejillas (`areas/1/7`, `8`).
   - `assets/models/castle_door.glb` y `assets/models/wooden_signpost.glb` exportados con `scripts/export_castle_actors.py` (emblema estelar simétrico sin número `zero_star_door_sign.rgba16.png`).
   - 26 árboles HD en billboard sobre eje Y (`special_bubble_tree`) con colisión de tronco, cascada animada (`movtext.inc.c`), agua de foso/laguna animada, 4 banderas rojas ondeando en las torres y 4 carteles cómicos con cuadro de diálogo contextual (`#sign-dialog`).
   - 10 Bitcoins giratorios con símbolo `₿` derecho en ambas caras a lo largo del sendero hasta el castillo.

3. **Personaje Jugable 3D (`Desktop/assets2`) y Física**:
   - Cuerpo articulado `assets/models/bukele_body.glb` (`scripts/build_bukele_hero.py`: saco formal azul marino oscuro, camiseta negra, pantalón azul marino y zapatos cafés) + clon de `bukele_head.glb` asentado sobre el cuello con recorte por shader (`onBeforeCompile`).
   - Raycasting de suelo (`sampleGround`) y paredes (`wallAhead`) con transformación de normales a espacio de mundo (`transformDirection(matrixWorld)`) y bloqueo de gravedad previo a `castleLoaded`.

4. **Audio Auténtico Extraído de la ROM US del Usuario**:
   - Secuencias `.m64` y muestras `.aiff` sintetizadas con `scripts/render_sm64_audio.py` hacia `assets/audio/sm64/`: `castle_grounds_bgm.mp3`, `star_fanfare.mp3`, `coin.mp3`, `door_open.mp3`, `mario_0C.mp3` y 5 voces clásicas de salto. *(La ROM original se mantiene fuera de Git en `/home/omarchy/Projects/rom/`).*

5. **Documentación Académica e Historial Completo para Evaluación (`pj-vibe-game-docs`)**:
   - `scripts/shot.sh` configurado con Chromium headless + SwiftShader WebGL (~6s por captura).
   - `PLAN.md`, `art/BAR.md`, `art/LEDGER.md` al día en `pj-vibe-game`.
   - Sitio Jekyll completo actualizado y compilado (`bundle exec jekyll build` en 0.38s sin errores) en `pj-vibe-game-docs`, preservando **todo el proceso histórico** desde el prototipo inicial hasta la versión final:
     - `index.md`, `README.md` y `_docs/introduccion.md` (evolución desde el *Vertical Slice* hasta *Castle Grounds* HD).
     - `_docs/arquitectura.md` (máquina de 8 estados, pipelines Blender/Python, shader GLSL `onBeforeCompile` y audio híbrido).
     - `_docs/prompts.md` (los 19 prompts cronológicos íntegros).
     - `_docs/iteracion.md` (las 18 iteraciones + galería visual comparativa *Antes/Después* con 7 capturas históricas en `assets/images/proceso/`).
     - `_docs/validacion.md` (los 9 bugs reales diagnosticados y resueltos con código y capturas de los fallos intermedios).
     - `_docs/reflexion.md` y `_docs/demo.md` actualizados y sincronizados en `origin/main`.

---

## 2. ¿En qué estamos trabajando ahora mismo?

- **Estado actual**: **Hito principal completado, verificado visualmente y desplegado en `origin/main`**. No quedan errores bloqueantes ni cambios sin commitear.
- Esperando validación del usuario tras probar la experiencia completa en vivo (`https://robert-flo.github.io/pj-vibe-game/` o servidor local) para aplicar cualquier ajuste fino estético, sonoro o jugable que solicite.

---

## 3. Pasos siguientes pensados / Mejoras listas para abordar si se desea continuar

Si se retoma el trabajo en una siguiente sesión, este es el orden recomendado de mejoras opcionales o de pulido:

1. **Revisión de experiencia en navegador real con el usuario**:
   - Confirmar volumen relativo entre `castle_grounds_bgm.mp3` (`0.42`), voces de salto (`0.72`) y fanfarria final (`0.72`).
   - Ajustar velocidad de movimiento (`SPEED = 9.0`), fuerza de salto (`JUMP_FORCE = 13.5`) o sensibilidad de cámara si el usuario lo prefiere más rápido/lento.
2. **Optimización de peso de carga inicial (`bukele_head.glb`)**:
   - Actualmente `assets/models/bukele_head.glb` pesa ~12 MB (se carga una sola vez y se clona para Escena 2 y Gameplay). Si se busca carga instantánea en redes móviles, se puede comprimir la textura embebida a WebP/JPEG de alta calidad o aplicar compresión Draco manteniendo intacta la fidelidad facial.
3. **Detalles adicionales opcionales de *Castle Grounds***:
   - Mariposas o pájaros ambientales cerca de los árboles de la pradera, salpicadura visual/sonora al caer al agua del foso o controles táctiles en pantalla (joystick virtual + botón de salto) para dispositivos móviles.
4. **Reglas operativas que deben mantenerse siempre**:
   - Hacer **commit atómico de cada cambio por pequeño que sea** y `git push origin main`.
   - Mantener **actualizado este archivo `next.md`** en cada paso.
   - Sincronizar cualquier nueva iteración en `/home/omarchy/Projects/pj-vibe-game-docs` (`_docs/prompts.md` e `_docs/iteracion.md`).
   - Nunca versionar archivos binarios de ROM dentro de los repositorios Git.

---

## 4. Comandos rápidos para retomar en otra sesión

```bash
# 1. Revisar estado e historial reciente
cd /home/omarchy/Projects/pj-vibe-game && git status && git log -n 5 --oneline

# 2. Levantar servidor local para probar en navegador
cd /home/omarchy/Projects/pj-vibe-game && python3 -m http.server 8080

# 3. Tomar captura rápida de verificación WebGL (~6s)
./scripts/shot.sh "scene=6&cam=-13.3,8.5,51.5,-2.5,14.5,-28.0" /tmp/check.png 2400
```
