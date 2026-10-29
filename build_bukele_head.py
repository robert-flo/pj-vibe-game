import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# -------------------------------------------------------------------------
# CARGAR TEXTURA DE ALTA DEFINICIÓN DE NAYIB BUKELE
# -------------------------------------------------------------------------
tex_path = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_face_tex.png"
img = bpy.data.images.load(tex_path)

# Material de la cara con la textura mapeada y especularidad N64
mat_face = bpy.data.materials.new(name="BukeleFaceMat")
mat_face.use_nodes = True
nodes = mat_face.node_tree.nodes
links = mat_face.node_tree.links
nodes.clear()

node_tex = nodes.new(type='ShaderNodeTexImage')
node_tex.image = img
node_tex.location = (-300, 0)

node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
node_bsdf.inputs['Roughness'].default_value = 0.32
node_bsdf.inputs['Metallic'].default_value = 0.05
node_bsdf.location = (0, 0)

node_out = nodes.new(type='ShaderNodeOutputMaterial')
node_out.location = (300, 0)

links.new(node_tex.outputs['Color'], node_bsdf.inputs['Base Color'])
links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

# Material negro para la parte posterior del cabello
mat_hair_back = bpy.data.materials.new(name="HairBackMat")
mat_hair_back.use_nodes = True
bsdf_hair = mat_hair_back.node_tree.nodes.get("Principled BSDF")
if bsdf_hair:
    bsdf_hair.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
    bsdf_hair.inputs['Roughness'].default_value = 0.5

# Material para el cuello ceremonial
mat_collar = bpy.data.materials.new(name="CollarMat")
mat_collar.use_nodes = True
bsdf_col = mat_collar.node_tree.nodes.get("Principled BSDF")
if bsdf_col:
    bsdf_col.inputs['Base Color'].default_value = (0.04, 0.04, 0.05, 1.0)
    bsdf_col.inputs['Roughness'].default_value = 0.4

# -------------------------------------------------------------------------
# MODELADO DE LA CABEZA 3D CON FORMA ANATÓMICA
# -------------------------------------------------------------------------
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=1.0, location=(0, 0, 0))
head = bpy.context.active_object
head.name = "BukeleHead"

head.scale = (0.92, 1.05, 1.18)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

head.data.materials.append(mat_face)

mesh = head.data
uv_layer = mesh.uv_layers.new(name="FaceUV")

for poly in mesh.polygons:
    for loop_idx in poly.loop_indices:
        vert_idx = mesh.loops[loop_idx].vertex_index
        vert = mesh.vertices[vert_idx].co
        u = 0.5 + (vert.x / 1.85)
        v = 0.48 + (vert.z / 2.1)
        
        if vert.y < 0:
            v_fade = max(0.0, vert.y / -1.0)
            u = 0.5 + (vert.x / 1.85) * (1.0 - v_fade * 0.4)
            
        uv_layer.data[loop_idx].uv = (u, v)

bpy.ops.object.shade_smooth()

# -------------------------------------------------------------------------
# CUELLO MANDARÍN CEREMONIAL Y VOLUMEN DE CABELLO POSTERIOR
# -------------------------------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(radius=0.58, depth=0.65, location=(0, -0.05, -1.05))
neck = bpy.context.active_object
neck.name = "NeckCollar"
neck.data.materials.append(mat_collar)
bpy.ops.object.shade_smooth()

bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=1.02, location=(0, -0.15, 0.12))
hair_back = bpy.context.active_object
hair_back.name = "HairBack"
hair_back.scale = (0.94, 0.96, 1.02)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
hair_back.data.materials.append(mat_hair_back)
bpy.ops.object.shade_smooth()

bpy.ops.object.select_all(action='DESELECT')
head.select_set(True)
neck.select_set(True)
hair_back.select_set(True)
bpy.context.view_layer.objects.active = head
bpy.ops.object.join()
bukele_bust = bpy.context.active_object
bukele_bust.name = "BukeleBust"

# -------------------------------------------------------------------------
# EXPORTACIÓN GLB
# -------------------------------------------------------------------------
output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/models"
os.makedirs(output_dir, exist_ok=True)
glb_path = os.path.join(output_dir, "bukele_head.glb")

bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_image_format='AUTO'
)
print(f"[OK] Cabeza realista bukele_head.glb exportada con exito en: {glb_path}")

# -------------------------------------------------------------------------
# TURNAROUND RENDERS
# -------------------------------------------------------------------------
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"
os.makedirs(stills_dir, exist_ok=True)

bpy.ops.object.camera_add(location=(0, 3.6, 0.0), rotation=(math.radians(90), 0, math.radians(180)))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(3, 4, 5))
sun = bpy.context.active_object
sun.data.energy = 4.2

bpy.ops.object.light_add(type='POINT', location=(-3, 2, 2))
fill = bpy.context.active_object
fill.data.energy = 160.0

scene = bpy.context.scene
scene.render.resolution_x = 720
scene.render.resolution_y = 720

# Frontal
bukele_bust.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-head-front.png")
bpy.ops.render.render(write_still=True)

# Perfil
bukele_bust.rotation_euler = (0, 0, math.radians(60))
scene.render.filepath = os.path.join(stills_dir, "turnaround-head-side.png")
bpy.ops.render.render(write_still=True)

print("[OK] Renders de turnaround completados.")
