import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# -----------------------------------------------------------------------------
# 1. MATERIALES DEL GUANTE BLANCO N64
# -----------------------------------------------------------------------------
mat_glove = bpy.data.materials.new(name="WhiteGlove")
mat_glove.use_nodes = True
bsdf = mat_glove.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.96, 0.96, 0.98, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.4
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.6

mat_cuff = bpy.data.materials.new(name="GloveCuff")
mat_cuff.use_nodes = True
bsdf_c = mat_cuff.node_tree.nodes.get("Principled BSDF")
if bsdf_c:
    bsdf_c.inputs['Base Color'].default_value = (0.92, 0.92, 0.94, 1.0)
    bsdf_c.inputs['Roughness'].default_value = 0.45

mat_stitch = bpy.data.materials.new(name="BlackStitch")
mat_stitch.use_nodes = True
bsdf_s = mat_stitch.node_tree.nodes.get("Principled BSDF")
if bsdf_s:
    bsdf_s.inputs['Base Color'].default_value = (0.05, 0.05, 0.08, 1.0)
    bsdf_s.inputs['Roughness'].default_value = 0.8

# -----------------------------------------------------------------------------
# 2. MODELADO 3D DE LA MANO GUANTE DE MARIO 64
# -----------------------------------------------------------------------------
# Palma (esfera aplanada)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.7, location=(0, 0, 0))
palm = bpy.context.active_object
palm.scale = (1.0, 0.55, 0.95)
palm.data.materials.append(mat_glove)
bpy.ops.object.shade_smooth()

# Dedo Índice (apuntando hacia arriba-izquierda, a ~45 grados)
bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.1, location=(-0.55, 0.05, 0.85))
index_finger = bpy.context.active_object
index_finger.rotation_euler = (0, math.radians(-38), 0)
index_finger.data.materials.append(mat_glove)
bpy.ops.object.shade_smooth()

# Punta del dedo índice (esfera)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(-0.88, 0.05, 1.28))
index_tip = bpy.context.active_object
index_tip.data.materials.append(mat_glove)
bpy.ops.object.shade_smooth()

# Pulgar (curvado hacia abajo / lateral)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32, location=(0.6, 0.15, 0.1))
thumb = bpy.context.active_object
thumb.scale = (0.9, 0.8, 1.1)
thumb.rotation_euler = (0, math.radians(20), math.radians(15))
thumb.data.materials.append(mat_glove)
bpy.ops.object.shade_smooth()

# Nudillos / dedos doblados en puño (3 esferas suaves)
knuckle_coords = [
    (-0.15, 0.1, 0.55), # Dedo medio doblado
    (0.20, 0.1, 0.45),  # Dedo anular doblado
    (0.50, 0.08, 0.30), # Meñique doblado
]
for idx, (kx, ky, kz) in enumerate(knuckle_coords):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.26, location=(kx, ky, kz))
    k = bpy.context.active_object
    k.scale = (0.9, 0.85, 0.9)
    k.data.materials.append(mat_glove)
    bpy.ops.object.shade_smooth()

# Puño del guante (toro / anillo en la muñeca)
bpy.ops.mesh.primitive_torus_add(major_radius=0.6, minor_radius=0.18, location=(0.4, -0.05, -0.7))
cuff = bpy.context.active_object
cuff.rotation_euler = (math.radians(15), math.radians(45), 0)
cuff.data.materials.append(mat_cuff)
bpy.ops.object.shade_smooth()

# Tres costuras negras del dorso del guante N64
stitch_coords = [
    ((-0.1, 0.28, 0.1), (-0.15, 0.28, -0.2)),
    ((0.12, 0.28, 0.05), (0.08, 0.28, -0.25)),
    ((0.32, 0.26, -0.05), (0.28, 0.26, -0.32))
]
for p1, p2 in stitch_coords:
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    mz = (p1[2] + p2[2]) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.35, location=(mx, my, mz))
    st = bpy.context.active_object
    st.rotation_euler = (math.radians(-10), math.radians(12), 0)
    st.data.materials.append(mat_stitch)

# -----------------------------------------------------------------------------
# 3. CÁMARA E ILUMINACIÓN
# -----------------------------------------------------------------------------
# La cámara mira de frente a la mano con perspectiva sutil
bpy.ops.object.camera_add(location=(0, -4.2, 0.2), rotation=(math.radians(90), 0, 0))
cam = bpy.context.active_object
cam.data.lens = 55
bpy.context.scene.camera = cam

# Luces para crear volumen en el guante blanco
bpy.ops.object.light_add(type='SUN', location=(-4, -8, 6), rotation=(math.radians(40), math.radians(-30), 0))
sun = bpy.context.active_object
sun.data.energy = 3.8

bpy.ops.object.light_add(type='POINT', location=(3, -4, -1))
fill = bpy.context.active_object
fill.data.energy = 80.0
fill.data.color = (0.85, 0.90, 1.0) # Sombra azulada suave

# Render transparente RGBA (256x256 para puntero perfecto)
scene = bpy.context.scene
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.film_transparent = True
scene.render.image_settings.color_mode = 'RGBA'

output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/img"
os.makedirs(output_dir, exist_ok=True)
cursor_path = os.path.join(output_dir, "n64_hand_cursor.png")
scene.render.filepath = cursor_path

bpy.ops.render.render(write_still=True)
print(f"[OK] Cursor de mano 3D N64 generado en: {cursor_path}")
