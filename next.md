# Estado de Continuidad del Proyecto (`next.md`)

> **Propósito**: Bitácora viva en la raíz de `pj-vibe-game` para registrar el estado exacto del proyecto, entregables oficiales, cambios completados y enlaces de entrega académica.

**Última actualización**: 2026-11-01 10:35 (UTC-6)  
**Actividad**: Semana 2 — Vibecoding Guiado (AI FOR DEVS JR. 5 - Kodigo Academy)  
**Estudiante**: Roberto Carlos Flores Quintanilla  
**Instructor**: Ing. Ronald Mejia  
**Repositorio principal**: `/home/omarchy/Projects/pj-vibe-game` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game) | [Despliegue GitHub Pages](https://robert-flo.github.io/pj-vibe-game/))  
**Repositorio de documentación**: `/home/omarchy/Projects/pj-vibe-game-docs` ([Enlace GitHub](https://github.com/robert-flo/pj-vibe-game-docs) | [Sitio Jekyll en Vivo](https://robert-flo.github.io/pj-vibe-game-docs/))  
**PDF Oficial de Entrega**: `/home/omarchy/Desktop/RobertoFlores-Tarea02.pdf` (Documento A4 de 6 páginas con portada institucional Kodigo, resumen ejecutivo, tabla de 21 prompts, galería visual con capturas de Bukele Fortnite y cámara panorámica, 14 incidencias resueltas y respuestas a la rúbrica).

---

## 1. ¿Qué está completado y publicado (`origin/main`)?

1. **Héroe Jugable Nayib Bukele Estilo Fortnite (Mejora 1)**:
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
