import bpy
import bmesh
import math
import os

# Clean slate
bpy.ops.wm.read_factory_settings(use_empty=True)

# -----------------------------------------------------------------------------
# PALETA DE MATERIALES ESTILIZADOS N64 (PBR LIMPIO, SIN FOTOS ESTIRADAS)
# -----------------------------------------------------------------------------
def make_material(name, base_color, roughness=0.4, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
    return mat

# Piel cálida salvadoreña N64
mat_skin = make_material("BukeleSkin", (0.76, 0.53, 0.42, 1.0), roughness=0.36)

# Piel mejillas con rubor suave
mat_cheeks = make_material("BukeleCheeks", (0.80, 0.50, 0.42, 1.0), roughness=0.38)

# Cabello y barba negro azabache / castaño oscuro muy profundo
mat_hair = make_material("BukeleHair", (0.05, 0.04, 0.04, 1.0), roughness=0.45, metallic=0.08)

# Esclera de los ojos (blanco marfil)
mat_eye_white = make_material("EyeWhite", (0.95, 0.95, 0.95, 1.0), roughness=0.2)

# Iris castaño oscuro Bukele
mat_eye_iris = make_material("EyeIris", (0.22, 0.12, 0.07, 1.0), roughness=0.15)

# Pupila negra con brillo
mat_eye_pupil = make_material("EyePupil", (0.01, 0.01, 0.01, 1.0), roughness=0.1)

# Brillo especular del ojo (destello blanco N64)
mat_eye_glint = make_material("EyeGlint", (1.0, 1.0, 1.0, 1.0), roughness=0.05)

# Labios y dientes
mat_lips = make_material("BukeleLips", (0.62, 0.36, 0.32, 1.0), roughness=0.35)
mat_teeth = make_material("BukeleTeeth", (0.92, 0.92, 0.90, 1.0), roughness=0.25)

# Traje presidencial (negro medianoche)
mat_suit = make_material("SuitBlack", (0.03, 0.03, 0.04, 1.0), roughness=0.5)

# Bordado dorado ceremonial (oro reflectante N64)
mat_gold = make_material("GoldTrim", (0.96, 0.76, 0.15, 1.0), roughness=0.22, metallic=0.95)

# Banda presidencial: Azul cobalto y blanco
mat_sash_blue = make_material("SashBlue", (0.04, 0.30, 0.82, 1.0), roughness=0.32)
mat_sash_white = make_material("SashWhite", (0.92, 0.94, 0.96, 1.0), roughness=0.32)

all_parts = []

# -----------------------------------------------------------------------------
# 1. CRÁNEO Y MANDÍBULA BASE (FORMA HUMANA REAL, NO ESFERA / HUEVO)
# -----------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=1.0, location=(0, 0, 0))
head = bpy.context.active_object
head.name = "HeadBase"

# Esculpido poligonal de cabeza humana estilizada
for v in head.data.vertices:
    x, y, z = v.co.x, v.co.y, v.co.z
    # Proporciones humanas
    x *= 0.82
    y *= 0.92
    z *= 1.08

    # Aplanar y estrechar mandíbula hacia la barbilla
    if z < -0.1:
        t = min(1.0, (-z - 0.1) / 0.75)
        x *= (1.0 - t * 0.30)
        # Mentón Bukele: ligeramente cuadrado y prominente
        if y > 0:
            chin_w = max(0.0, 1.0 - abs(x) / 0.32) * max(0.0, 1.0 - abs(z + 0.6) / 0.35)
            y += chin_w * 0.14
            
    # Cavidades para los ojos (Z ~ 0.15 a 0.35, X ~ 0.25 a 0.55)
    if y > 0.3 and 0.12 < z < 0.38:
        dist_eye_l = math.hypot(x - 0.35, z - 0.24)
        dist_eye_r = math.hypot(x + 0.35, z - 0.24)
        if dist_eye_l < 0.22:
            y -= (0.22 - dist_eye_l) * 0.35
        if dist_eye_r < 0.22:
            y -= (0.22 - dist_eye_r) * 0.35

    # Frente amplia y curvada
    if z > 0.4:
        y -= (z - 0.4) * 0.12

    v.co.x, v.co.y, v.co.z = x, y, z

head.data.update()
head.data.materials.append(mat_skin)
bpy.ops.object.shade_smooth()
all_parts.append(head)

# Pómulos estilizados
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.28, location=(side * 0.46, 0.48, 0.05))
    cheek = bpy.context.active_object
    cheek.scale = (0.9, 0.6, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    cheek.data.materials.append(mat_cheeks)
    bpy.ops.object.shade_smooth()
    all_parts.append(cheek)

# -----------------------------------------------------------------------------
# 2. NARIZ 3D REAL (TABIQUE RECTO, PUNTA Y ALETAS NASALES)
# -----------------------------------------------------------------------------
# Puente nasal
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.34, location=(0, 0.72, 0.22))
nose_bridge = bpy.context.active_object
nose_bridge.rotation_euler = (math.radians(-22), 0, 0)
nose_bridge.scale = (0.9, 1.4, 1.0)
bpy.ops.object.transform_apply(scale=True, rotation=True)
nose_bridge.data.materials.append(mat_skin)
bpy.ops.object.shade_smooth()
all_parts.append(nose_bridge)

# Punta de la nariz redondeada
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.10, location=(0, 0.84, 0.08))
nose_tip = bpy.context.active_object
nose_tip.scale = (1.1, 1.2, 0.9)
bpy.ops.object.transform_apply(scale=True)
nose_tip.data.materials.append(mat_skin)
bpy.ops.object.shade_smooth()
all_parts.append(nose_tip)

# Aletas nasales (izquierda y derecha)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=10, radius=0.065, location=(side * 0.10, 0.79, 0.06))
    nostril = bpy.context.active_object
    nostril.scale = (1.0, 1.1, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    nostril.data.materials.append(mat_skin)
    bpy.ops.object.shade_smooth()
    all_parts.append(nostril)

# -----------------------------------------------------------------------------
# 3. OJOS ESTILIZADOS N64 (ESCLERA, IRIS CASTAÑO, PUPILA Y DESTELLO)
# -----------------------------------------------------------------------------
for side in [-1, 1]:
    # Esclera blanca
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=16, radius=0.15, location=(side * 0.32, 0.62, 0.24))
    eye_white = bpy.context.active_object
    eye_white.scale = (1.15, 0.85, 0.95)
    eye_white.rotation_euler = (0, math.radians(side * 8), 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    eye_white.data.materials.append(mat_eye_white)
    bpy.ops.object.shade_smooth()
    all_parts.append(eye_white)

    # Iris castaño
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.04, location=(side * 0.32, 0.74, 0.24))
    iris = bpy.context.active_object
    iris.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    iris.data.materials.append(mat_eye_iris)
    bpy.ops.object.shade_smooth()
    all_parts.append(iris)

    # Pupila negra
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.042, location=(side * 0.32, 0.745, 0.24))
    pupil = bpy.context.active_object
    pupil.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    pupil.data.materials.append(mat_eye_pupil)
    bpy.ops.object.shade_smooth()
    all_parts.append(pupil)

    # Destello de brillo estilo Mario 64 (Eye Glint)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=0.022, location=(side * 0.30, 0.76, 0.27))
    glint = bpy.context.active_object
    glint.data.materials.append(mat_eye_glint)
    bpy.ops.object.shade_smooth()
    all_parts.append(glint)

    # Ceja arqueada Bukele
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.28, location=(side * 0.33, 0.66, 0.41))
    brow = bpy.context.active_object
    brow.rotation_euler = (math.radians(-10), math.radians(side * 18), math.radians(side * 8))
    brow.scale = (1.4, 0.6, 0.8)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    brow.data.materials.append(mat_hair)
    bpy.ops.object.shade_smooth()
    all_parts.append(brow)

# -----------------------------------------------------------------------------
# 4. BOCA Y SONRISA CÁLIDA (LABIOS Y DIENTES ESTILIZADOS)
# -----------------------------------------------------------------------------
# Labio superior e inferior en sonrisa
bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.035, location=(0, 0.69, -0.15))
mouth = bpy.context.active_object
mouth.rotation_euler = (math.radians(82), 0, 0)
mouth.scale = (1.1, 0.7, 0.8)
bpy.ops.object.transform_apply(scale=True, rotation=True)
mouth.data.materials.append(mat_lips)
bpy.ops.object.shade_smooth()
all_parts.append(mouth)

# Dientes blancos sonrientes
bpy.ops.mesh.primitive_cube_add(size=0.14, location=(0, 0.70, -0.15))
teeth = bpy.context.active_object
teeth.scale = (1.2, 0.2, 0.35)
bpy.ops.object.transform_apply(scale=True)
teeth.data.materials.append(mat_teeth)
bpy.ops.object.shade_smooth()
all_parts.append(teeth)

# -----------------------------------------------------------------------------
# 5. BARBA Y BIGOTE 3D REAL (EL RASGO MÁS ICÓNICO DE BUKELE)
# -----------------------------------------------------------------------------
# Bigote recortado sobre el labio
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.18, location=(side * 0.10, 0.76, -0.05))
    mustache = bpy.context.active_object
    mustache.rotation_euler = (math.radians(15), math.radians(side * 28), math.radians(side * -14))
    mustache.scale = (1.2, 0.6, 0.9)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    mustache.data.materials.append(mat_hair)
    bpy.ops.object.shade_smooth()
    all_parts.append(mustache)

# Barba de la mandíbula y mentón (Torus y cilindros que abrazan el mentón)
bpy.ops.mesh.primitive_torus_add(major_radius=0.48, minor_radius=0.09, location=(0, 0.18, -0.42))
beard_jaw = bpy.context.active_object
beard_jaw.rotation_euler = (math.radians(28), 0, 0)
beard_jaw.scale = (0.86, 0.92, 0.95)
bpy.ops.object.transform_apply(scale=True, rotation=True)
beard_jaw.data.materials.append(mat_hair)
bpy.ops.object.shade_smooth()
all_parts.append(beard_jaw)

# Barba de mentón / candado frontal
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.19, location=(0, 0.64, -0.38))
beard_chin = bpy.context.active_object
beard_chin.scale = (0.9, 0.8, 1.1)
bpy.ops.object.transform_apply(scale=True)
beard_chin.data.materials.append(mat_hair)
bpy.ops.object.shade_smooth()
all_parts.append(beard_chin)

# Patillas que unen el cabello con la barba
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(side * 0.69, 0.05, -0.08))
    sideburn = bpy.context.active_object
    sideburn.scale = (0.4, 0.9, 2.2)
    bpy.ops.object.transform_apply(scale=True)
    sideburn.data.materials.append(mat_hair)
    bpy.ops.object.shade_smooth()
    all_parts.append(sideburn)

# -----------------------------------------------------------------------------
# 6. CABELLO 3D ESTILIZADO (PEINADO POMPADOUR VOLUMÉTRICO HACIA ATRÁS)
# -----------------------------------------------------------------------------
# Corona principal del cabello con volumen elevado
bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.92, location=(0, -0.10, 0.42))
hair_main = bpy.context.active_object
hair_main.scale = (0.88, 1.05, 0.92)
bpy.ops.object.transform_apply(scale=True)
hair_main.data.materials.append(mat_hair)
bpy.ops.object.shade_smooth()
all_parts.append(hair_main)

# Copete frontal peinado hacia atrás (mechón característico de Bukele)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=16, radius=0.45, location=(0, 0.32, 0.72))
hair_front = bpy.context.active_object
hair_front.scale = (1.2, 0.9, 0.65)
hair_front.rotation_euler = (math.radians(-18), 0, 0)
bpy.ops.object.transform_apply(scale=True, rotation=True)
hair_front.data.materials.append(mat_hair)
bpy.ops.object.shade_smooth()
all_parts.append(hair_front)

# Ondas laterales del peinado
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.85, location=(side * 0.52, -0.05, 0.62))
    hair_wave = bpy.context.active_object
    hair_wave.rotation_euler = (math.radians(72), math.radians(side * -15), math.radians(side * 10))
    bpy.ops.object.transform_apply(rotation=True)
    hair_wave.data.materials.append(mat_hair)
    bpy.ops.object.shade_smooth()
    all_parts.append(hair_wave)

# Orejas modeladas en 3D
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, radius=0.18, location=(side * 0.72, -0.06, 0.08))
    ear = bpy.context.active_object
    ear.scale = (0.35, 0.70, 1.25)
    ear.rotation_euler = (0, math.radians(side * -12), 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    ear.data.materials.append(mat_skin)
    bpy.ops.object.shade_smooth()
    all_parts.append(ear)

# -----------------------------------------------------------------------------
# 7. CUELLO MANDARÍN CEREMONIAL, ORO Y BANDA PRESIDENCIAL
# -----------------------------------------------------------------------------
# Cuello humano
bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.55, location=(0, -0.05, -0.85))
neck = bpy.context.active_object
neck.data.materials.append(mat_skin)
bpy.ops.object.shade_smooth()
all_parts.append(neck)

# Cuello alto mandarín (negro rígido ceremonial)
bpy.ops.mesh.primitive_cylinder_add(radius=0.52, depth=0.38, location=(0, -0.05, -0.98))
mandarin_collar = bpy.context.active_object
mandarin_collar.scale = (0.95, 1.05, 1.0)
bpy.ops.object.transform_apply(scale=True)
mandarin_collar.data.materials.append(mat_suit)
bpy.ops.object.shade_smooth()
all_parts.append(mandarin_collar)

# Bordado dorado superior del cuello
bpy.ops.mesh.primitive_torus_add(major_radius=0.53, minor_radius=0.035, location=(0, -0.05, -0.84))
gold_top = bpy.context.active_object
gold_top.scale = (0.95, 1.05, 1.0)
bpy.ops.object.transform_apply(scale=True)
gold_top.data.materials.append(mat_gold)
bpy.ops.object.shade_smooth()
all_parts.append(gold_top)

# Bordado dorado inferior del cuello
bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.035, location=(0, -0.05, -1.14))
gold_bot = bpy.context.active_object
gold_bot.scale = (0.95, 1.05, 1.0)
bpy.ops.object.transform_apply(scale=True)
gold_bot.data.materials.append(mat_gold)
bpy.ops.object.shade_smooth()
all_parts.append(gold_bot)

# Base de Hombros y Pecho Ceremonial
bpy.ops.mesh.primitive_cylinder_add(radius=1.35, depth=0.48, location=(0, -0.08, -1.45))
shoulders = bpy.context.active_object
shoulders.scale = (1.25, 0.78, 1.0)
bpy.ops.object.transform_apply(scale=True)
shoulders.data.materials.append(mat_suit)
bpy.ops.object.shade_smooth()
all_parts.append(shoulders)

# Banda Presidencial: Franja Azul Superior
bpy.ops.mesh.primitive_cylinder_add(radius=1.38, depth=0.10, location=(-0.16, -0.08, -1.36))
sash_b1 = bpy.context.active_object
sash_b1.rotation_euler = (0, math.radians(24), 0)
sash_b1.scale = (1.24, 0.80, 1.0)
bpy.ops.object.transform_apply(scale=True, rotation=True)
sash_b1.data.materials.append(mat_sash_blue)
bpy.ops.object.shade_smooth()
all_parts.append(sash_b1)

# Banda Presidencial: Franja Blanca Central
bpy.ops.mesh.primitive_cylinder_add(radius=1.385, depth=0.09, location=(-0.11, -0.08, -1.44))
sash_w = bpy.context.active_object
sash_w.rotation_euler = (0, math.radians(24), 0)
sash_w.scale = (1.24, 0.80, 1.0)
bpy.ops.object.transform_apply(scale=True, rotation=True)
sash_w.data.materials.append(mat_sash_white)
bpy.ops.object.shade_smooth()
all_parts.append(sash_w)

# Banda Presidencial: Franja Azul Inferior
bpy.ops.mesh.primitive_cylinder_add(radius=1.39, depth=0.10, location=(-0.06, -0.08, -1.52))
sash_b2 = bpy.context.active_object
sash_b2.rotation_euler = (0, math.radians(24), 0)
sash_b2.scale = (1.24, 0.80, 1.0)
bpy.ops.object.transform_apply(scale=True, rotation=True)
sash_b2.data.materials.append(mat_sash_blue)
bpy.ops.object.shade_smooth()
all_parts.append(sash_b2)

# Escudo Dorado Presidencial en el centro de la banda
bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.05, location=(-0.18, 0.52, -1.38))
gold_seal = bpy.context.active_object
gold_seal.rotation_euler = (math.radians(72), math.radians(-18), 0)
bpy.ops.object.transform_apply(rotation=True)
gold_seal.data.materials.append(mat_gold)
bpy.ops.object.shade_smooth()
all_parts.append(gold_seal)

# -----------------------------------------------------------------------------
# 8. UNIFICACIÓN DEL MODELO Y CENTRADO DE PIVOTE
# -----------------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
for p in all_parts:
    p.select_set(True)

bpy.context.view_layer.objects.active = head
bpy.ops.object.join()
bukele_bust = bpy.context.active_object
bukele_bust.name = "BukeleStylizedN64"

# Centrar el origen en el centro de la cabeza para que los giros con el ratón sean perfectos
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

print(f"[OK] Modelo estilizado N64 creado: {len(bukele_bust.data.vertices)} vertices, {len(bukele_bust.data.polygons)} poligonos.")

# -----------------------------------------------------------------------------
# 9. EXPORTACIÓN GLB (GLTF 2.0)
# -----------------------------------------------------------------------------
output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/models"
os.makedirs(output_dir, exist_ok=True)
glb_path = os.path.join(output_dir, "bukele_head.glb")

bpy.ops.object.select_all(action='DESELECT')
bukele_bust.select_set(True)
bpy.context.view_layer.objects.active = bukele_bust

bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True
)
print(f"[OK] GLB exportado con exito en: {glb_path} ({os.path.getsize(glb_path)} bytes)")

# -----------------------------------------------------------------------------
# 10. TURNAROUND GATE (RENDERS OBLIGATORIOS PARA EL ORCHESTRATOR)
# -----------------------------------------------------------------------------
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"
os.makedirs(stills_dir, exist_ok=True)

# Cámara de estudio frontal
bpy.ops.object.camera_add(location=(0, 3.8, 0.0), rotation=(math.radians(90), 0, math.radians(180)))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# Luces N64 estilo Silicon Graphics (Key, Fill, Rim)
bpy.ops.object.light_add(type='SUN', location=(3.0, 4.0, 5.0))
sun = bpy.context.active_object
sun.data.energy = 4.0

bpy.ops.object.light_add(type='POINT', location=(-3.0, 2.5, 2.0))
fill = bpy.context.active_object
fill.data.energy = 180.0
fill.data.color = (0.75, 0.88, 1.0)

bpy.ops.object.light_add(type='POINT', location=(0.0, -3.0, 3.0))
rim = bpy.context.active_object
rim.data.energy = 220.0
rim.data.color = (1.0, 0.95, 0.85)

scene = bpy.context.scene
scene.render.resolution_x = 768
scene.render.resolution_y = 768

# 1. Frente
bukele_bust.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-stylized-front.png")
bpy.ops.render.render(write_still=True)

# 2. Tres cuartos (3/4)
bukele_bust.rotation_euler = (0, 0, math.radians(35))
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-stylized-threequarter.png")
bpy.ops.render.render(write_still=True)

# 3. Perfil (90 grados)
bukele_bust.rotation_euler = (0, 0, math.radians(80))
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-stylized-profile.png")
bpy.ops.render.render(write_still=True)

# Dejar rotación frontal en reposo
bukele_bust.rotation_euler = (0, 0, 0)
print("[OK] Turnaround gate renders completados.")
