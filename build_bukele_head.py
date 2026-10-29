import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# -------------------------------------------------------------------------
# MATERIALES PBR ESTILO N64 (Con especularidad clásica)
# -------------------------------------------------------------------------
def create_mat(name, color, roughness=0.35, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
    return mat

mat_skin = create_mat("Skin_N64", (0.90, 0.68, 0.48, 1.0), roughness=0.32) # Piel con brillo retro
mat_hair = create_mat("Hair_Beard", (0.05, 0.05, 0.06, 1.0), roughness=0.45)
mat_eye_white = create_mat("Eye_White", (0.96, 0.96, 0.98, 1.0), roughness=0.15)
mat_eye_iris = create_mat("Eye_Iris", (0.12, 0.42, 0.88, 1.0), roughness=0.15)
mat_eye_pupil = create_mat("Eye_Pupil", (0.02, 0.02, 0.02, 1.0), roughness=0.1)
mat_mouth_inner = create_mat("Mouth_Inner", (0.68, 0.12, 0.15, 1.0), roughness=0.4)
mat_teeth = create_mat("Teeth", (0.95, 0.95, 0.95, 1.0), roughness=0.2)
mat_collar = create_mat("Collar_Black", (0.04, 0.04, 0.05, 1.0), roughness=0.4)
mat_gold = create_mat("Gold_Embroidery", (0.96, 0.76, 0.15, 1.0), roughness=0.25, metallic=0.85)

head_parts = []

def add_mesh(name, primitive_func, kwargs, loc=(0,0,0), rot=(0,0,0), scale=(1,1,1), mat=mat_skin):
    primitive_func(**kwargs, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    if mat:
        obj.data.materials.append(mat)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    head_parts.append(obj)
    return obj

# 1. Base Craneal (Forma de cabeza N64 estilizada)
head_base = add_mesh("HeadBase", bpy.ops.mesh.primitive_uv_sphere_add, 
                     {"segments": 24, "ring_count": 16, "radius": 1.0},
                     loc=(0, 0, 0), scale=(0.95, 1.05, 1.15), mat=mat_skin)

# 2. Mandíbula y Mentón estilizado
jaw = add_mesh("Jaw", bpy.ops.mesh.primitive_uv_sphere_add,
               {"segments": 20, "ring_count": 14, "radius": 0.65},
               loc=(0, 0.35, -0.55), scale=(0.9, 0.9, 0.8), mat=mat_skin)

# 3. Nariz prominente tipo N64
nose = add_mesh("Nose", bpy.ops.mesh.primitive_uv_sphere_add,
                {"segments": 16, "ring_count": 12, "radius": 0.28},
                loc=(0, 0.98, -0.05), scale=(0.8, 1.1, 0.9), mat=mat_skin)

# 4. Ojos (Esclera blanca + Iris azul + Pupila + Brillo)
for side, sign in [("L", -1), ("R", 1)]:
    # Esclera
    add_mesh(f"Sclera_{side}", bpy.ops.mesh.primitive_uv_sphere_add,
             {"segments": 16, "ring_count": 12, "radius": 0.24},
             loc=(sign * 0.38, 0.82, 0.22), scale=(0.75, 0.8, 1.1), mat=mat_eye_white)
    # Iris
    add_mesh(f"Iris_{side}", bpy.ops.mesh.primitive_cylinder_add,
             {"radius": 0.12, "depth": 0.06},
             loc=(sign * 0.38, 0.98, 0.22), rot=(math.radians(90), 0, 0), mat=mat_eye_iris)
    # Pupila
    add_mesh(f"Pupil_{side}", bpy.ops.mesh.primitive_cylinder_add,
             {"radius": 0.06, "depth": 0.08},
             loc=(sign * 0.38, 0.99, 0.22), rot=(math.radians(90), 0, 0), mat=mat_eye_pupil)
    # Ceja arqueada
    add_mesh(f"Eyebrow_{side}", bpy.ops.mesh.primitive_cube_add,
             {"size": 1.0},
             loc=(sign * 0.40, 0.85, 0.48), rot=(0, sign * math.radians(12), sign * math.radians(-8)),
             scale=(0.32, 0.10, 0.08), mat=mat_hair)

# 5. Boca sonriente y dientes
mouth = add_mesh("Mouth", bpy.ops.mesh.primitive_cube_add,
                 {"size": 1.0},
                 loc=(0, 0.82, -0.42), scale=(0.42, 0.15, 0.16), mat=mat_mouth_inner)
teeth = add_mesh("Teeth", bpy.ops.mesh.primitive_cube_add,
                 {"size": 1.0},
                 loc=(0, 0.86, -0.38), scale=(0.34, 0.08, 0.07), mat=mat_teeth)

# 6. Bigote característico curvado
mustache = add_mesh("Mustache", bpy.ops.mesh.primitive_cube_add,
                    {"size": 1.0},
                    loc=(0, 0.92, -0.22), rot=(0, 0, 0),
                    scale=(0.62, 0.18, 0.14), mat=mat_hair)

# 7. Barba delineada a lo largo de la mandíbula
beard_chin = add_mesh("BeardChin", bpy.ops.mesh.primitive_uv_sphere_add,
                      {"segments": 16, "ring_count": 12, "radius": 0.52},
                      loc=(0, 0.42, -0.65), scale=(0.95, 0.85, 0.65), mat=mat_hair)

for side, sign in [("L", -1), ("R", 1)]:
    add_mesh(f"BeardJaw_{side}", bpy.ops.mesh.primitive_cube_add,
             {"size": 1.0},
             loc=(sign * 0.62, 0.18, -0.42), rot=(math.radians(22), sign * math.radians(-15), sign * math.radians(12)),
             scale=(0.22, 0.65, 0.28), mat=mat_hair)
    # Orejas
    add_mesh(f"Ear_{side}", bpy.ops.mesh.primitive_uv_sphere_add,
             {"segments": 14, "ring_count": 10, "radius": 0.26},
             loc=(sign * 0.94, -0.05, 0.05), scale=(0.4, 0.7, 1.0), mat=mat_skin)

# 8. Cabello peinado hacia atrás (Volumen icónico)
hair_dome = add_mesh("HairDome", bpy.ops.mesh.primitive_uv_sphere_add,
                     {"segments": 22, "ring_count": 16, "radius": 1.04},
                     loc=(0, -0.12, 0.22), scale=(0.96, 1.04, 1.02), mat=mat_hair)
hair_slick = add_mesh("HairSlickBack", bpy.ops.mesh.primitive_cube_add,
                      {"size": 1.0},
                      loc=(0, -0.72, 0.15), rot=(math.radians(-25), 0, 0),
                      scale=(0.88, 0.55, 0.92), mat=mat_hair)

# 9. Cuello y Cuello Mandarín con bordado dorado (Base de la cabeza)
neck = add_mesh("Neck", bpy.ops.mesh.primitive_cylinder_add,
                {"radius": 0.55, "depth": 0.6},
                loc=(0, -0.05, -1.0), mat=mat_collar)
collar_gold_ring = add_mesh("CollarGold", bpy.ops.mesh.primitive_torus_add,
                            {"major_radius": 0.56, "minor_radius": 0.06, "major_segments": 24, "minor_segments": 10},
                            loc=(0, -0.05, -0.95), mat=mat_gold)

# Unir todas las partes en un objeto único bukele_head
bpy.ops.object.select_all(action='DESELECT')
for p in head_parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = head_base
bpy.ops.object.join()
bukele_head = bpy.context.active_object
bukele_head.name = "BukeleHeadN64"

# Aplicar Smooth Shading estilo N64
bpy.ops.object.shade_smooth()

# Exportar GLB
output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/models"
glb_path = os.path.join(output_dir, "bukele_head.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True
)
print(f"[OK] Cabeza N64 exportada en: {glb_path}")

# Renders de Turnaround para la compuerta de calidad
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"

bpy.ops.object.camera_add(location=(0, 3.8, 0.1), rotation=(math.radians(90), 0, math.radians(180)))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(3, 4, 5))
sun = bpy.context.active_object
sun.data.energy = 4.0

bpy.ops.object.light_add(type='POINT', location=(-3, 2, 2))
fill = bpy.context.active_object
fill.data.energy = 180.0

scene = bpy.context.scene
scene.render.resolution_x = 720
scene.render.resolution_y = 720

# Frontal
bukele_head.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-head-front.png")
bpy.ops.render.render(write_still=True)

# Perfil
bukele_head.rotation_euler = (0, 0, math.radians(90))
scene.render.filepath = os.path.join(stills_dir, "turnaround-head-side.png")
bpy.ops.render.render(write_still=True)

print("[OK] Turnaround de cabeza N64 guardado exitosamente.")
