import bpy
import bmesh
import math
import os

# Clean slate
bpy.ops.wm.read_factory_settings(use_empty=True)

# -----------------------------------------------------------------------------
# 1. TEXTURAS Y MATERIALES (ALTA FIDELIDAD REF-07)
# -----------------------------------------------------------------------------
tex_face_path = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_face_crop_clean.png"
img_face = bpy.data.images.load(tex_face_path)

# Material Principal del Rostro (PBR realista estilo N64 SGI)
mat_face = bpy.data.materials.new(name="BukeleRealisticFace")
mat_face.use_nodes = True
nodes = mat_face.node_tree.nodes
links = mat_face.node_tree.links
nodes.clear()

node_tex = nodes.new(type='ShaderNodeTexImage')
node_tex.image = img_face
node_tex.location = (-400, 0)

node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
node_bsdf.inputs['Roughness'].default_value = 0.35
node_bsdf.inputs['Metallic'].default_value = 0.02
node_bsdf.location = (0, 0)

node_out = nodes.new(type='ShaderNodeOutputMaterial')
node_out.location = (300, 0)

links.new(node_tex.outputs['Color'], node_bsdf.inputs['Base Color'])
links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

# Material Cabello Oscuro
mat_hair = bpy.data.materials.new(name="BukeleHairMat")
mat_hair.use_nodes = True
bsdf_h = mat_hair.node_tree.nodes.get("Principled BSDF")
if bsdf_h:
    bsdf_h.inputs['Base Color'].default_value = (0.04, 0.035, 0.03, 1.0)
    bsdf_h.inputs['Roughness'].default_value = 0.45
    bsdf_h.inputs['Metallic'].default_value = 0.05

# Material Cuello Mandarín Negro
mat_suit = bpy.data.materials.new(name="MandarinSuitMat")
mat_suit.use_nodes = True
bsdf_s = mat_suit.node_tree.nodes.get("Principled BSDF")
if bsdf_s:
    bsdf_s.inputs['Base Color'].default_value = (0.03, 0.03, 0.04, 1.0)
    bsdf_s.inputs['Roughness'].default_value = 0.5

# Material Oro Ceremonial
mat_gold = bpy.data.materials.new(name="GoldEmbroideryMat")
mat_gold.use_nodes = True
bsdf_g = mat_gold.node_tree.nodes.get("Principled BSDF")
if bsdf_g:
    bsdf_g.inputs['Base Color'].default_value = (0.95, 0.78, 0.18, 1.0)
    bsdf_g.inputs['Roughness'].default_value = 0.25
    bsdf_g.inputs['Metallic'].default_value = 0.95

# -----------------------------------------------------------------------------
# 2. ESCULPIDO ANATÓMICO DETALLADO DE NAYIB BUKELE
# -----------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=36, radius=1.0, location=(0, 0, 0))
head = bpy.context.active_object
head.name = "BukeleHead"

# Deformación de vértices para esculpir proporciones exactas:
# - Mandíbula afilada con barba
# - Pómulos y cuencas
# - Nariz 3D con tabique recto y alas nasales
mesh = head.data
for v in mesh.vertices:
    x, y, z = v.co.x, v.co.y, v.co.z
    
    # Proporción craneal humana
    x *= 0.88
    y *= 0.95
    z *= 1.14
    
    # Mandíbula y mentón (Z < -0.1)
    if z < -0.1:
        t = min(1.0, (-z - 0.1) / 0.8)
        x *= (1.0 - t * 0.25)
        # Mentón Bukele
        if y > 0 and z < -0.4:
            chin_t = max(0.0, 1.0 - abs(x) / 0.35) * max(0.0, 1.0 - abs(z + 0.62) / 0.35)
            y += chin_t * 0.20
            
    # Nariz 3D pronunciada (+Y)
    if y > 0.2 and -0.22 < z < 0.25:
        dist_x = abs(x)
        if dist_x < 0.26:
            nose_profile = math.exp(-(dist_x**2) / (2 * 0.07**2))
            nose_z_weight = math.exp(-((z - 0.02)**2) / (2 * 0.14**2))
            nose_extrude = nose_profile * nose_z_weight * 0.35
            y += nose_extrude
            
    # Pómulos y sonrisa (Z ~ 0.0 a 0.3)
    if y > 0.1 and 0.0 < z < 0.32:
        cheek_weight = math.exp(-((abs(x) - 0.48)**2) / 0.05) * math.exp(-(z**2) / 0.07)
        y += cheek_weight * 0.09
        x += math.copysign(cheek_weight * 0.04, x)

    # Frente amplia
    if z > 0.35:
        forehead_t = (z - 0.35) / 0.75
        y -= forehead_t * 0.10

    v.co.x = x
    v.co.y = y
    v.co.z = z

mesh.update()
bpy.ops.object.shade_smooth()

# -----------------------------------------------------------------------------
# 3. UV MAPPING ALINEADO AL ROSTRO REAL DE BUKELE
# -----------------------------------------------------------------------------
head.data.materials.append(mat_face)
uv_layer = mesh.uv_layers.new(name="BukeleFaceUV")

for poly in mesh.polygons:
    for loop_idx in poly.loop_indices:
        vert_idx = mesh.loops[loop_idx].vertex_index
        vert = mesh.vertices[vert_idx].co
        
        # Mapeo frontal exacto para bukele_face_crop_clean.png
        # Centrado en X=0 -> U=0.50
        # Ojos/Nariz en Z=0.0 -> V=0.55
        u = 0.50 + (vert.x / 1.62)
        v = 0.55 + (vert.z / 1.95)
        
        # Conexión suave hacia el cabello posterior
        if vert.y < -0.05:
            depth_factor = min(1.0, (-vert.y - 0.05) / 0.75)
            v = min(0.96, v + depth_factor * 0.32)
            u = 0.5 + (u - 0.5) * (1.0 - depth_factor * 0.65)
            
        uv_layer.data[loop_idx].uv = (u, v)

# -----------------------------------------------------------------------------
# 4. ELEMENTOS 3D SECUNDARIOS
# -----------------------------------------------------------------------------
# Oreja Izquierda
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.22, location=(-0.78, -0.05, 0.02))
ear_l = bpy.context.active_object
ear_l.scale = (0.35, 0.75, 1.3)
bpy.ops.object.transform_apply(scale=True)
ear_l.data.materials.append(mat_face)
bpy.ops.object.shade_smooth()

# Oreja Derecha
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.22, location=(0.78, -0.05, 0.02))
ear_r = bpy.context.active_object
ear_r.scale = (0.35, 0.75, 1.3)
bpy.ops.object.transform_apply(scale=True)
ear_r.data.materials.append(mat_face)
bpy.ops.object.shade_smooth()

# Cabello con volumen peinado hacia atrás
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.96, location=(0, -0.20, 0.32))
hair = bpy.context.active_object
hair.scale = (0.86, 1.05, 0.95)
bpy.ops.object.transform_apply(scale=True)
hair.data.materials.append(mat_hair)
bpy.ops.object.shade_smooth()

# -----------------------------------------------------------------------------
# 5. CUELLO MANDARÍN CEREMONIAL Y HOMBROS
# -----------------------------------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(radius=0.52, depth=0.55, location=(0, -0.04, -0.92))
neck = bpy.context.active_object
neck.data.materials.append(mat_face)
bpy.ops.object.shade_smooth()

# Cuello de traje mandarín con reborde
bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.08, location=(0, -0.04, -0.98))
collar_rim = bpy.context.active_object
collar_rim.scale = (1.0, 1.08, 0.8)
bpy.ops.object.transform_apply(scale=True)
collar_rim.data.materials.append(mat_suit)
bpy.ops.object.shade_smooth()

# Bordado dorado ceremonial en el cuello
bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.035, location=(0, -0.04, -0.96))
gold_rim = bpy.context.active_object
gold_rim.scale = (1.0, 1.08, 0.8)
bpy.ops.object.transform_apply(scale=True)
gold_rim.data.materials.append(mat_gold)
bpy.ops.object.shade_smooth()

# Base de Hombros
bpy.ops.mesh.primitive_cylinder_add(radius=1.35, depth=0.45, location=(0, -0.06, -1.35))
torso_base = bpy.context.active_object
torso_base.scale = (1.2, 0.75, 1.0)
bpy.ops.object.transform_apply(scale=True)
torso_base.data.materials.append(mat_suit)
bpy.ops.object.shade_smooth()

# Banda Presidencial Azul y Blanco sobre el hombro
bpy.ops.mesh.primitive_cylinder_add(radius=1.38, depth=0.18, location=(-0.12, -0.06, -1.32))
sash = bpy.context.active_object
sash.rotation_euler = (0, math.radians(22), 0)
sash.scale = (1.18, 0.76, 0.9)
bpy.ops.object.transform_apply(scale=True, rotation=True)
mat_sash = bpy.data.materials.new(name="PresSashMat")
mat_sash.use_nodes = True
bsdf_sash = mat_sash.node_tree.nodes.get("Principled BSDF")
if bsdf_sash:
    bsdf_sash.inputs['Base Color'].default_value = (0.05, 0.28, 0.75, 1.0)
    bsdf_sash.inputs['Roughness'].default_value = 0.3
sash.data.materials.append(mat_sash)
bpy.ops.object.shade_smooth()

# -----------------------------------------------------------------------------
# 6. UNIR EN UN SOLO OBJETO Y CENTRAR PIVOTE
# -----------------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
for obj in [head, ear_l, ear_r, hair, neck, collar_rim, gold_rim, torso_base, sash]:
    obj.select_set(True)

bpy.context.view_layer.objects.active = head
bpy.ops.object.join()
bukele_bust = bpy.context.active_object
bukele_bust.name = "BukeleHD"
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

# -----------------------------------------------------------------------------
# 7. EXPORTACIÓN GLB (ANTES DE RENDERS PARA EVITAR PÉRDIDA DE SELECCIÓN)
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
    export_apply=True,
    export_image_format='AUTO'
)
print(f"[EXPORT GLB] bukele_head.glb exportado: {glb_path} ({os.path.getsize(glb_path)} bytes)")

# -----------------------------------------------------------------------------
# 8. RENDERS DE TURNAROUND
# -----------------------------------------------------------------------------
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"
os.makedirs(stills_dir, exist_ok=True)

bpy.ops.object.camera_add(location=(0, 3.4, 0.0), rotation=(math.radians(90), 0, math.radians(180)))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(2.5, 3.5, 4.0))
sun = bpy.context.active_object
sun.data.energy = 4.5

bpy.ops.object.light_add(type='POINT', location=(-3.0, 2.0, 1.5))
fill = bpy.context.active_object
fill.data.energy = 140.0
fill.data.color = (0.7, 0.85, 1.0)

scene = bpy.context.scene
scene.render.resolution_x = 768
scene.render.resolution_y = 768

# Vista Frontal
bukele_bust.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-v2-front.png")
bpy.ops.render.render(write_still=True)

# Vista 3/4
bukele_bust.rotation_euler = (0, 0, math.radians(35))
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-v2-threequarter.png")
bpy.ops.render.render(write_still=True)

print("[OK] Renders de turnaround finalizados.")
