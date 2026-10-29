import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Importar el modelo descomprimido de Tripo3D
input_glb = '/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_tripo_decompressed.glb'
bpy.ops.import_scene.gltf(filepath=input_glb)

# Buscar el objeto principal
mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not mesh_objs:
    raise RuntimeError("No se encontro ningun objeto MESH en el GLB importado.")

bukele_bust = mesh_objs[0]
bukele_bust.name = "BukeleHeroBust"
print(f"[BLENDER] Objeto cargado: {bukele_bust.name}, dim: {bukele_bust.dimensions}")

# Asegurarse de que esté seleccionado y activo
bpy.ops.object.select_all(action='DESELECT')
bukele_bust.select_set(True)
bpy.context.view_layer.objects.active = bukele_bust

# Centrar pivote geométricamente
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bukele_bust.location = (0, 0, 0)
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

# Normalizar escala si es necesario (que la altura Z sea ~1.8 unidades para Three.js)
current_height = bukele_bust.dimensions.z
if current_height > 0:
    target_scale = 1.6 / current_height
    bukele_bust.scale = (target_scale, target_scale, target_scale)
    bpy.ops.object.transform_apply(scale=True)
    print(f"[BLENDER] Escala normalizada a dimensiones: {bukele_bust.dimensions}")

# Reducir levemente polígonos si está sobre 80k para rendimiento web
poly_count = len(bukele_bust.data.polygons)
print(f"[BLENDER] Polígonos originales: {poly_count}")
if poly_count > 40000:
    decimate_ratio = 35000 / poly_count
    mod = bukele_bust.modifiers.new(name="DecimateWeb", type='DECIMATE')
    mod.ratio = decimate_ratio
    bpy.ops.object.modifier_apply(modifier="DecimateWeb")
    print(f"[BLENDER] Polígonos optimizados para WebGL: {len(bukele_bust.data.polygons)}")

# Comprobar materiales e imágenes
for mat_slot in bukele_bust.material_slots:
    if mat_slot.material and mat_slot.material.use_nodes:
        bsdf = mat_slot.material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Ligera especularidad clásica N64
            bsdf.inputs['Roughness'].default_value = 0.42

# -----------------------------------------------------------------------------
# TURNAROUND RENDERS DE ESTUDIO
# -----------------------------------------------------------------------------
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"
os.makedirs(stills_dir, exist_ok=True)

# Cámara frontal
bpy.ops.object.camera_add(location=(0, 2.5, 0.0), rotation=(math.radians(90), 0, math.radians(180)))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# Luces de estudio
bpy.ops.object.light_add(type='SUN', location=(3.0, 4.0, 5.0))
sun = bpy.context.active_object
sun.data.energy = 4.0

bpy.ops.object.light_add(type='POINT', location=(-3.0, 2.5, 2.0))
fill = bpy.context.active_object
fill.data.energy = 160.0
fill.data.color = (0.8, 0.9, 1.0)

bpy.ops.object.light_add(type='POINT', location=(0.0, -2.5, 2.0))
rim = bpy.context.active_object
rim.data.energy = 180.0

scene = bpy.context.scene
scene.render.resolution_x = 768
scene.render.resolution_y = 768

# Render Frente
bukele_bust.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-tripo-front.png")
bpy.ops.render.render(write_still=True)

# Render 3/4
bukele_bust.rotation_euler = (0, 0, math.radians(35))
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-tripo-threequarter.png")
bpy.ops.render.render(write_still=True)

# Render Perfil
bukele_bust.rotation_euler = (0, 0, math.radians(75))
scene.render.filepath = os.path.join(stills_dir, "turnaround-bukele-tripo-profile.png")
bpy.ops.render.render(write_still=True)

# Restablecer rotación
bukele_bust.rotation_euler = (0, 0, 0)

# -----------------------------------------------------------------------------
# EXPORTACIÓN GLB FINAL LISTA PARA THREE.JS
# -----------------------------------------------------------------------------
output_glb = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_head.glb"
bpy.ops.object.select_all(action='DESELECT')
bukele_bust.select_set(True)
bpy.context.view_layer.objects.active = bukele_bust

bpy.ops.export_scene.gltf(
    filepath=output_glb,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_image_format='AUTO'
)
print(f"[EXITO] bukele_head.glb generado: {output_glb} ({os.path.getsize(output_glb)} bytes)")
