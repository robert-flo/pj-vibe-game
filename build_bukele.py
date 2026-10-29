import bpy
import math
import os

# Limpiar escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# -------------------------------------------------------------------------
# 1. MATERIALES PBR
# -------------------------------------------------------------------------
def create_mat(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
    return mat

mat_black_suit = create_mat("CeremonialBlack", (0.04, 0.04, 0.05, 1.0), 0.0, 0.45)
mat_gold = create_mat("GoldEmbroidery", (0.95, 0.74, 0.15, 1.0), 0.88, 0.22)
mat_skin = create_mat("SkinTone", (0.84, 0.61, 0.42, 1.0), 0.0, 0.55)
mat_hair = create_mat("HairAndBeard", (0.04, 0.04, 0.04, 1.0), 0.0, 0.6)
mat_sash_blue = create_mat("SashBlue", (0.08, 0.25, 0.85, 1.0), 0.0, 0.4)
mat_sash_white = create_mat("SashWhite", (0.96, 0.96, 0.98, 1.0), 0.0, 0.35)
mat_shoes = create_mat("PolishedShoes", (0.01, 0.01, 0.01, 1.0), 0.1, 0.18)

# -------------------------------------------------------------------------
# 2. CONSTRUCCIÓN DEL MODELO NAYIB BUKELE
# -------------------------------------------------------------------------
character_objects = []

# Helper para agregar cubos/cilindros con material y transformaciones
def add_part(name, geom_type, size, loc, rot=(0,0,0), mat=mat_black_suit):
    if geom_type == "cube":
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
        obj = bpy.context.active_object
        obj.scale = size
    elif geom_type == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=size[0], depth=size[1], location=loc, rotation=rot)
        obj = bpy.context.active_object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    character_objects.append(obj)
    return obj

# Torso principal (chaquetilla de gala)
torso = add_part("Torso", "cube", (0.75, 0.48, 0.95), (0, 0, 1.35), mat=mat_black_suit)

# Faldón inferior del chaquetón
skirt = add_part("CoatSkirt", "cube", (0.78, 0.50, 0.35), (0, 0, 0.85), mat=mat_black_suit)

# Cuello alto mandarín
collar = add_part("MandarinCollar", "cylinder", (0.24, 0.20), (0, 0, 1.88), mat=mat_black_suit)
collar_gold = add_part("CollarEmbroidery", "cylinder", (0.25, 0.08), (0, 0, 1.92), mat=mat_gold)

# Banda Presidencial (Azul, Blanco, Azul) diagonal sobre el pecho
sash_blue_l = add_part("SashBlueL", "cube", (0.07, 0.51, 1.05), (-0.08, 0, 1.35), rot=(0, 0, -0.42), mat=mat_sash_blue)
sash_white_m = add_part("SashWhiteM", "cube", (0.07, 0.51, 1.05), (0, 0, 1.35), rot=(0, 0, -0.42), mat=mat_sash_white)
sash_blue_r = add_part("SashBlueR", "cube", (0.07, 0.51, 1.05), (0.08, 0, 1.35), rot=(0, 0, -0.42), mat=mat_sash_blue)

# Escudo dorado central en la banda
sash_seal = add_part("SashSeal", "cylinder", (0.08, 0.53), (0, 0.01, 1.35), rot=(math.pi/2, 0, 0), mat=mat_gold)

# Cabeza
head = add_part("Head", "cube", (0.50, 0.52, 0.55), (0, 0, 2.22), mat=mat_skin)

# Cabello peinado hacia atrás (volumen superior y posterior)
hair_top = add_part("HairTop", "cube", (0.52, 0.54, 0.20), (0, -0.01, 2.52), mat=mat_hair)
hair_back = add_part("HairBack", "cube", (0.52, 0.16, 0.42), (0, -0.24, 2.26), mat=mat_hair)

# Barba recortada y bigote
beard_jaw = add_part("BeardJaw", "cube", (0.52, 0.36, 0.22), (0, 0.11, 2.06), mat=mat_hair)
mustache = add_part("Mustache", "cube", (0.34, 0.12, 0.08), (0, 0.26, 2.18), mat=mat_hair)

# Ojos
eye_l = add_part("EyeL", "cube", (0.08, 0.05, 0.06), (-0.14, 0.26, 2.30), mat=mat_hair)
eye_r = add_part("EyeR", "cube", (0.08, 0.05, 0.06), (0.14, 0.26, 2.30), mat=mat_hair)

# Piernas y pantalones
leg_l = add_part("LegL", "cube", (0.28, 0.32, 0.70), (-0.20, 0, 0.52), mat=mat_black_suit)
leg_r = add_part("LegR", "cube", (0.28, 0.32, 0.70), (0.20, 0, 0.52), mat=mat_black_suit)

# Zapatos de gala negros
shoe_l = add_part("ShoeL", "cube", (0.30, 0.44, 0.18), (-0.20, 0.05, 0.10), mat=mat_shoes)
shoe_r = add_part("ShoeR", "cube", (0.30, 0.44, 0.18), (0.20, 0.05, 0.10), mat=mat_shoes)

# Brazos ceremoniales con puños bordados
arm_l = add_part("ArmL", "cube", (0.22, 0.26, 0.72), (-0.48, 0, 1.35), mat=mat_black_suit)
cuff_gold_l = add_part("CuffL", "cube", (0.24, 0.28, 0.16), (-0.48, 0, 1.06), mat=mat_gold)
hand_l = add_part("HandL", "cube", (0.18, 0.20, 0.16), (-0.48, 0, 0.92), mat=mat_skin)

arm_r = add_part("ArmR", "cube", (0.22, 0.26, 0.72), (0.48, 0, 1.35), mat=mat_black_suit)
cuff_gold_r = add_part("CuffR", "cube", (0.24, 0.28, 0.16), (0.48, 0, 1.06), mat=mat_gold)
hand_r = add_part("HandR", "cube", (0.18, 0.20, 0.16), (0.48, 0, 0.92), mat=mat_skin)

# Unir todas las partes en una sola malla limpia del personaje
bpy.ops.object.select_all(action='DESELECT')
for obj in character_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = torso
bpy.ops.object.join()
bukele_mesh = bpy.context.active_object
bukele_mesh.name = "BukeleHero"

# -------------------------------------------------------------------------
# 3. EXPORTAR GLB OFICIAL (glTF 2.0)
# -------------------------------------------------------------------------
output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/models"
os.makedirs(output_dir, exist_ok=True)
glb_path = os.path.join(output_dir, "bukele.glb")

bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True
)
print(f"[OK] GLB exportado con exito en: {glb_path}")

# -------------------------------------------------------------------------
# 4. TURNAROUND GATE: RENDER DE VISTAS (Frontal, Lateral y Posterior)
# -------------------------------------------------------------------------
stills_dir = "/home/omarchy/Projects/pj-vibe-game/artifacts/stills"
os.makedirs(stills_dir, exist_ok=True)

# Crear cámara y luces de estudio
bpy.ops.object.camera_add(location=(0, -4.5, 1.5), rotation=(math.radians(82), 0, 0))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='SUN', location=(4, -4, 6))
sun = bpy.context.active_object
sun.data.energy = 3.5

bpy.ops.object.light_add(type='POINT', location=(-3, 3, 4))
fill = bpy.context.active_object
fill.data.energy = 150.0

scene = bpy.context.scene
scene.render.resolution_x = 720
scene.render.resolution_y = 960
scene.render.image_settings.file_format = 'PNG'

# Render Frontal
bukele_mesh.rotation_euler = (0, 0, 0)
scene.render.filepath = os.path.join(stills_dir, "turnaround-front.png")
bpy.ops.render.render(write_still=True)

# Render Lateral (Perfil)
bukele_mesh.rotation_euler = (0, 0, math.radians(90))
scene.render.filepath = os.path.join(stills_dir, "turnaround-side.png")
bpy.ops.render.render(write_still=True)

# Render Posterior (Espalda)
bukele_mesh.rotation_euler = (0, 0, math.radians(180))
scene.render.filepath = os.path.join(stills_dir, "turnaround-back.png")
bpy.ops.render.render(write_still=True)

print("[OK] Turnaround renders completados en artifacts/stills/")
