# Estado de Continuidad del Proyecto (`next.md`)

> **Propósito**: Bitácora viva en la raíz de `pj-vibe-game` para registrar el estado exacto del proyecto, entregables oficiales, cambios completados y enlaces de entrega académica.

**Última actualización**: 2026-11-01 09:15 (UTC-6)  
**Actividad**: Semana 2 — Vibecoding Guiado (AI FOR DEVS JR. 5 - Kodigo Academy)  
**Estudiante**: Roberto Carlos Flores Quintanilla  
**Instructor**: Ing. Ronald Mejia  
**Repositorio principal**: `/home/omarchy/Projects/pj-vibe-game` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game) | [Despliegue GitHub Pages](https://robert-flo.github.io/pj-vibe-game/))  
**Repositorio de documentación**: `/home/omarchy/Projects/pj-vibe-game-docs` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game-docs) | [Sitio Jekyll en Vivo](https://robert-flo.github.io/pj-vibe-game-docs/))  
**PDF Oficial de Entrega**: `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf` (Documento A4 de 6 páginas con portada institucional Kodigo, resumen ejecutivo, tabla de 20 prompts, galería visual, casos de estudio y respuestas a la rúbrica).

---

## 1. ¿Qué está completado y publicado (`origin/main`)?

1. **Flujo Canónico Completo de 6 Escenas + Cierre de Victoria**:
   - **Escena 1 (`#scene-1-title`)**: Pantalla de título *SUPER BUKELE 64* con logotipo 3D biselado facetado en madera generado en Blender mediante `TypefaceMario64.otf` sobre mosaico azul acolchado N64.
   - **Escena 2 (`#scene-2-overlay`)**: Busto 3D interactivo de Nayib Bukele (`assets/models/bukele_head.glb`, optimizado a 4.8 MB en 2K) con seguimiento elástico del cursor y toque móvil.
   - **Escena 3 (`#scene-3-fileselect`)**: Tablero dorado *SELECT FILE* con 4 ranuras (`BUKELE A–D`), insignias retro NEW y cursor tridimensional de mano enguantada N64.
   - **Escena 4 (`#scene-letter`)**: Pergamino de la Primera Dama Gabriela invitando a Nayib al castillo, acompañado del arpegio musical de piano extraído de la ROM.
   - **Escena 5 (`#scene-cinematic`)**: Cinemática aérea de Lakitu calibrada a 720p 60fps (22.5s, corte en segundo 49.0 sobre la tubería verde).
   - **Escena 6 (`SCENE_6_GAMEPLAY`)**: Exteriores completos de *Peach's Castle Grounds* con listas de despliegue RSP (Fast3D) y texturas HD de RENDER96, 26 árboles en billboard sobre eje Y, cascada con flujo UV continuo, 4 banderas ondeantes, 4 carteles cómicos interactivos y 10 Bitcoins coleccionables.
   - **Cierre de Victoria (`SCENE_DOOR_OPENING` ➔ `SCENE_VICTORY`)**: Al llegar a `Z ≈ -29.5, Y > 7.2`, las dos puertas estelares se abren hacia el exterior con sonido clásico de SM64, Bukele entra sobre la alfombra roja, suena *"Here we go!"* + `star_fanfare.mp3` y se abre `#victory-modal` con conteo de Bitcoins (`X / 10`), tiempo (`MM:SS`) y reinicio.

2. **Soporte Móvil y Responsividad Táctil**:
   - D-Pad táctil virtual (movimiento omnidireccional en tiempo real) y botón de salto N64 ("A") en pantalla, activados automáticamente en pantallas táctiles y móviles sin estorbar en escritorio.

3. **Optimización de Activos Gráficos**:
   - Reducción de texturas embebidas en `bukele_head.glb` de 4K a 2K (Blender Python), reduciendo el peso del modelo en un 60% (de 12 MB a 4.8 MB) manteniendo fidelidad facial fotorrealista.

4. **Audio Auténtico Extraído de la ROM US de SM64**:
   - Secuencias `.m64` y muestras PCM `.aiff` sintetizadas con NumPy según `seqplayer.c`: `castle_grounds_bgm.mp3`, `star_fanfare.mp3`, `coin.mp3`, `door_open.mp3`, `mario_0C.mp3` y 5 voces clásicas de salto. *(La ROM se mantiene fuera del repositorio Git por higiene de derechos de autor).*

5. **Documentación Académica e Historial Completo (`pj-vibe-game-docs`)**:
   - Portal Jekyll completo compilado y desplegado con todo el registro histórico: 20 prompts cronológicos, 19 iteraciones detalladas, 9 bugs reales auditados con capturas antes/después y respuestas a la rúbrica de evaluación.

6. **Generación del Documento PDF Oficial de Entrega**:
   - `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf`: Maquetado con los estándares institucionales de Kodigo Academy (6 páginas exactas A4, vectoriales, con portada, logotipos oficiales, tablas de prompts, galería de 6 capturas clave y análisis crítico).

---

## 2. Estado Actual de la Tarea

- **Estado**: **100% COMPLETADO, VERIFICADO Y ENTREGABLE**.
- Todos los repositorios locales y remotos (`origin/main`) están limpios, sincronizados y probados.
- El PDF final para subir a la plataforma académica está listo en el escritorio del estudiante: `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf`.

---

## 3. Comandos Útiles

```bash
# Servidor local para jugar o probar en navegador
cd /home/omarchy/Projects/pj-vibe-game && python3 -m http.server 8080

# Servidor local de la documentación Jekyll
cd /home/omarchy/Projects/pj-vibe-game-docs && bundle exec jekyll serve --port 4000

# Inspección de PDF generado
pdftotext /home/omarchy/Desktop/RobertoFlores-Tarea02.pdf - | head -n 40
```
