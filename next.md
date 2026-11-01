# Estado de Continuidad del Proyecto (`next.md`)

> **Propósito**: Bitácora viva en la raíz de `pj-vibe-game` para registrar el estado exacto del proyecto, entregables oficiales, cambios completados y enlaces de entrega académica.

**Última actualización**: 2026-11-01 12:15 (UTC-6)  
**Actividad**: Semana 2 — Vibecoding Guiado (AI FOR DEVS JR. 5 - Kodigo Academy)  
**Estudiante**: Roberto Carlos Flores Quintanilla  
**Instructor**: Ing. Ronald Mejia  
**Repositorio principal**: `/home/omarchy/Projects/pj-vibe-game` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game) | [Despliegue GitHub Pages](https://robert-flo.github.io/pj-vibe-game/))  
**Repositorio de documentación**: `/home/omarchy/Projects/pj-vibe-game-docs` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game-docs) | [Sitio Jekyll en Vivo](https://robert-flo.github.io/pj-vibe-game-docs/))  
**PDF Oficial de Entrega**: `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf` (Documento A4 v7 con portada institucional Kodigo, botón hero destacado de acceso al juego, Tabla 1.1 formal académica de repositorios técnicos, resumen ejecutivo, bitácora de prompts, galería visual, matriz de incidencias resueltas y rúbrica).

---

## 1. ¿Qué está completado y publicado (`origin/main`)?

0. **README Oficial del Motor con Gameplay HD, Enlaces Prominentes y Ficha Técnica**:
   - Integración de la captura real de gameplay (`assets/screenshots/super_bukele_64_gameplay.jpg`) con el nivel Peach's Castle Grounds HD, vitral de Gabriela de Bukele, puente pavimentado, Bitcoin coleccionable y carteles del MOP 64.
   - Enlace hero destacado al juego en vivo (`robert-flo.github.io/pj-vibe-game`), enlace a la documentación web Jekyll (`robert-flo.github.io/pj-vibe-game-docs`) y al repositorio de documentación (`github.com/robert-flo/pj-vibe-game-docs`).
   - Tabla formal de enlaces, desglose del flujo de 6 escenas, guía completa de controles para PC/Móvil y ficha técnica institucional.

1. **Corrección de GitHub Pages para el Portal de Documentación (Incidencia 18)**:
   - Diagnóstico: En `.github/workflows/deploy.yml`, el paso de compilación utilizaba `--baseurl "${{ steps.pages.base_path }}"`, la cual devolvía una cadena vacía `""`, sobreescribiendo el `baseurl: "/pj-vibe-game-docs"` de `_config.yml` y provocando errores HTTP 404 en las hojas de estilo CSS (`vitepress-core.css`, etc.) y scripts Turbo.
   - Solución: Se fijó `--baseurl "/pj-vibe-game-docs"` explícitamente en el workflow de despliegue. Despliegue verificado con código HTTP 200 en todos los recursos estáticos y renderizado completo.

1. **Jerarquía Visual y Tabla Académica de Repositorios en el Documento PDF Oficial (`RobertoFlores-Tarea02.pdf` v7)**:
   - **Portada (Página 1)**: Tarjeta interactiva con gradiente azul (`#0284c7` a `#1e40af`) y llamado a la acción directo: `🎮 DEMO INTERACTIVA EN LÍNEA • ▶ CLIC AQUÍ PARA JUGAR: SUPER BUKELE 64`.
   - **Resumen Ejecutivo (Página 2)**:
     - *Hero Card* gaming con fondo oscuro estilizado, botón dorado con relieve (`#fbbf24`), enlace directo en tipografía monospace cian y badges de compatibilidad (100% navegador, PC y móvil, sin emuladores, audio N64 auténtico).
     - **Tabla 1.1 Formal Académica**: Se reemplazó el formato informal por una tabla técnica estandarizada (*Recurso / Entregable*, *Descripción del Contenido*, *Enlace Permanente URI*) que documenta con rigor académico el portal Jekyll, el repositorio del motor Three.js y el repositorio de documentación histórica.
   - **Conclusión (Página 6)**: Botón verde esmeralda de llamado a la acción final para garantizar acceso directo inmediato tanto al abrir el documento como al finalizar su lectura.
   - Verificado rigurosamente en **6 páginas A4** sin desbordamiento.

1. **Animación Orgánica y Fluida de Caminata/Carrera de Bukele (FK de 3 Huesos con Tobillos Articulados)**:
   - Diagnóstico: La pierna delantera se proyectaba recta a 45° como una estaca rígida con la zapatilla apuntando hacia el cielo, la rodilla trasera se doblaba en exceso (~58°), el torso se inclinaba hacia atrás (`+0.08` rad) y el rebote vertical vibraba al doble de frecuencia.
   - Solución:
     - Jerarquía FK extendida en Blender (`Leg -> Shin -> Foot`): se crearon los nodos `FootL` y `FootR` para articular las zapatillas 3D en el tobillo.
     - Nivelación automática de pies en `animateLimbs()`: las zapatillas contrarrestan el ángulo de la pierna y se mantienen paralelas al suelo al pisar.
     - Flexión suave y natural de rodilla en el avance y recogida trasera amortiguada.
     - Inclinación atlética hacia adelante (`pitch = -0.10` rad) hacia la dirección de avance.
     - Cadencia de trote natural (`walkCycle += delta * 9.5`) y rebote vertical suave de un solo pulso por paso (`Math.abs(Math.sin(walkCycle)) * 0.045`).

2. **Corrección de la Pantalla SELECT FILE (Escena 3 - Desbloqueo y Debounce Guard)**:
   - Diagnóstico: Al pulsar "PRESS START" en la Escena 2, el evento `pointerdown` transicionaba a la Escena 3 pero el subsecuente evento `mousedown`/`click` en el mismo ciclo era capturado por el listener global de ventana, saltándose la pantalla en 0 ms directo a la Carta de Gabriela.
   - Solución: Se implementó un guardián de tiempo (`scene3EnterTime = performance.now()`) con una ventana de protección de 450 ms que absorbe cualquier clic residual. La pantalla dorada SELECT FILE ahora permanece activa y permite interactuar con el cursor de mano 3D sobre los slots `BUKELE A, B, C, D`.

2. **Vitral Oficial de Gabriela de Bukele en el Castillo**:
   - Integración del retrato oficial de la Primera Dama Gabriela de Bukele (`images.jpeg`) adaptado al marco ovalado del castillo (`stained_glass_gabriela.png`).
   - Composición con bisel dorado de plomo, bandera nacional de El Salvador y transparencia en el arco exterior superior para integrarse perfectamente a la mampostería 3D del castillo.

3. **Banda Sonora Oficial Completa (OST Original SM64)**:
   - Integradas las pistas oficiales del usuario desde `~/Desktop/assets4`:
     - Pista `01`: Saludo de inicio clásico *"It's-a Me, Mario!"* al arrancar el juego.
     - Pista `02`: Tema principal de alta fidelidad *Title Theme* (3:34 min) para Escenas 1 y 2.
     - Pista `03`: Tema oficial de selección *File Select* (46 s) para la Escena 3.

4. **Vitral de Peach Corregido y Sistema de Vitral Personalizable**:
   - Diagnóstico de UVs: `castle_grounds_seg7_texture_07001000` (`1.rgba16.png`) tenía dimensiones `(32, 64)` invertidas en `scripts/export_castle_grounds.py` en lugar de `(64, 32)`, lo que causaba que la mitad inferior de Peach se dividiera verticalmente y se duplicara a los lados.
   - Corregida la relación de aspecto en el exportador y re-exportado `assets/models/castle_grounds.glb` con Blender 5.2.2. Vitral ovalado de Peach ahora completamente continuo, unificado y en alta definición.
   - Sistema de personalización dinámica habilitado en `js/game.js`: permite cambiar el vitral por cualquier imagen personalizada mediante el parámetro URL `?glass=ruta/imagen.png` o mediante la función de consola `window.setCastleStainedGlass(url)`.

2. **Héroe Jugable Nayib Bukele Estilo Fortnite (Mejora 1)**:
   - Proporciones humanas estilizadas de 7.5 cabezas (`HS = 0.52`).
   - Torso atlético con volumen pectoral de 0.32m de profundidad, silueta en V (*V-taper*), saco entallado con pañuelo blanco en bolsillo, cinturón con hebilla de oro, reloj en la muñeca izquierda y zapatillas 3D con suela y puntera.
   - Jerarquía cinemática FK de 2 tramos por extremidad (`LegL/R -> ShinL/R`, `ArmL/R -> ForearmL/R`).
   - Animación orgánica: flexión de rodilla hacia atrás en la pierna retrasada (`Math.abs(swing) * 1.35`), braceo atlético con codos doblados (35° a 60°), balanceo vertical de cadera, inclinación de avance al correr (`lean`) y ciclo de respiración en reposo (*Idle*).

2. **Banda Sonora Original en Menús de Inicio (Mejora 2)**:
   - Síntesis directa desde secuencias de la ROM de SM64 de `title_screen_bgm.mp3` (`02_menu_title_screen.m64`, Bank 11) para Escenas 1 y 2.
   - Síntesis de `file_select_bgm.mp3` (`21_menu_file_select.m64`, Bank 24) para la Escena 3 (Select File).
   - Activación fluida con el primer clic o toque y cross-fade entre pantallas.

3. **Jugabilidad Móvil Completa y Desbloqueo Táctil (Mejora 3)**:
   - Corregido el bloqueo de eventos táctiles en la Escena 2 (Cabeza 3D) mediante `pointerdown` y detección de toque con umbral de 800 ms.
   - D-Pad virtual y botón de salto N64 ("A") activos en cualquier dispositivo táctil.
   - Aviso elegante de orientación móvil: `📱 Gira tu dispositivo a horizontal (Landscape) para vista panorámica`.

4. **Flujo Descendente Natural de la Cascada (Mejora 4)**:
   - Corregido el desplazamiento UV (`waterfallTex.offset.y += delta * 1.35`), logrando que la corriente baje de forma natural hacia el foso y la laguna.

5. **Inclinación Vertical de Cámara (*Pitch*) para Ver el Castillo (Mejora 5)**:
   - Rango de elevación de [-0.35, 0.72] rad controlado mediante teclas **R / F**, **PageUp / PageDown** o arrastre vertical con ratón o dedo táctil, permitiendo alzar la vista hacia el cielo para contemplar el vitral de Peach, las torres y las banderas ondeando.

6. **Flujo Canónico Completo de 6 Escenas + Cierre de Victoria**:
   - Secuencia completa: Título 3D ➔ Busto elástico 3D ➔ Tablero dorado Select File ➔ Carta de Gabriela ➔ Cinemática aérea de Lakitu (corte s49.0) ➔ Castillo de Peach HD (10 Bitcoins, 26 árboles, carteles) ➔ Puertas estelares abriéndose y pantalla de victoria.

7. **Documentación Académica y PDF Oficial v2**:
   - `pj-vibe-game-docs` con Prompt 21, Iteración 20, 14 incidencias resueltas y capturas actualizadas.
   - PDF de 6 páginas A4 generado e instalado en `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf` y descargable desde el portal web.

---

## 2. Estado Actual de la Tarea

- **Estado**: **100% COMPLETADO, VERIFICADO Y ENTREGABLE**.
- Todos los repositorios locales y remotos (`origin/main`) están limpios, sincronizados y probados.

---

## 3. Comandos Útiles

```bash
# Servidor local para jugar o probar en navegador
cd /home/omarchy/Projects/pj-vibe-game && python3 -m http.server 8080

# Servidor local de la documentación Jekyll
cd /home/omarchy/Projects/pj-vibe-game-docs && bundle exec jekyll serve --port 4000
```
