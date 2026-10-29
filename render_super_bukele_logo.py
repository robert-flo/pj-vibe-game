import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# -----------------------------------------------------------------------------
# 1. FUENTE OFICIAL MARIO 64 Y MATERIALES
# -----------------------------------------------------------------------------
font_path = "/home/omarchy/Projects/pj-vibe-game/assets/fonts/TypefaceMario64.otf"
n64_font = bpy.data.fonts.load(font_path)

# Material de Madera Pino Clásica N64 con vetas de corte de madera
mat_wood = bpy.data.materials.new(name="N64PineWood")
mat_wood.use_nodes = True
nodes = mat_wood.node_tree.nodes
links = mat_wood.node_tree.links
tex_coord = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
mapping.inputs['Scale'].default_value = (0.2, 0.2, 5.0)
wave = nodes.new('ShaderNodeTexWave')
wave.wave_type = 'BANDS'
wave.inputs['Scale'].default_value = 5.5
wave.inputs['Distortion'].default_value = 1.6
ramp = nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = 0.0
ramp.color_ramp.elements[0].color = (0.75, 0.46, 0.22, 1.0) # Veta ámbar madera
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = (0.96, 0.76, 0.50, 1.0) # Tono pino cálido
bsdf_w = nodes.get("Principled BSDF")
if bsdf_w:
    bsdf_w.inputs['Roughness'].default_value = 0.52
links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
links.new(wave.outputs['Color'], ramp.inputs['Fac'])
links.new(ramp.outputs['Color'], bsdf_w.inputs['Base Color'])

# Materiales de caras frontales estilo N64 con alto brillo de juguete 3D
def make_face_mat(name, hex_color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    r = (int(hex_color[1:3], 16) / 255.0) ** 2.2
    g = (int(hex_color[3:5], 16) / 255.0) ** 2.2
    b = (int(hex_color[5:7], 16) / 255.0) ** 2.2
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.12
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = 0.85
    return mat

mat_red = make_face_mat("N64Red", "#e52521")
mat_blue = make_face_mat("N64Blue", "#2251e6")
mat_yellow = make_face_mat("N64Yellow", "#facc15")
mat_green = make_face_mat("N64Green", "#059639")
mat_gold = make_face_mat("N64Gold", "#fde047")
mat_white = make_face_mat("N64White", "#f8fafc")

def create_block_letter(char, mat_face, loc, size=1.0, extrude=0.6, bevel=0.035, tilt_x=12, tilt_z=0):
    rot = (math.radians(90 - tilt_x), 0, math.radians(tilt_z))
    bpy.ops.object.text_add(location=loc, rotation=rot)
    t = bpy.context.active_object
    t.name = f"Char_{char}"
    t.data.body = char
    t.data.font = n64_font
    t.data.size = size
    t.data.extrude = extrude
    t.data.bevel_depth = bevel
    t.data.bevel_resolution = 2
    t.data.align_x = 'CENTER'
    t.data.align_y = 'CENTER'
    
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.transform_apply(rotation=True)
    
    mesh_obj = bpy.context.active_object
    mesh_obj.data.materials.append(mat_face) # index 0: Cara frontal
    mesh_obj.data.materials.append(mat_wood) # index 1: Bloque de madera
    
    for poly in mesh_obj.data.polygons:
        if poly.normal.y < -0.32:
            poly.material_index = 0
        else:
            poly.material_index = 1
            
    return mesh_obj

# -----------------------------------------------------------------------------
# 2. DISPOSICIÓN EXACTA AUTÉNTICA SM64 (Letras gruesas, compactas, unificadas)
# -----------------------------------------------------------------------------

# "SUPER" (Con la tipografía oficial Typeface Mario 64)
# S(Rojo), U(Azul), P(Amarillo), E(Azul), R(Verde)
super_letters = [
    ('S', mat_red, -2.4, 1.5, 1.05, 14, -6),
    ('U', mat_blue, -1.2, 1.5, 1.18, 12, -2),
    ('P', mat_yellow, 0.0, 1.5, 1.22, 11, 0),
    ('E', mat_blue, 1.2, 1.5, 1.18, 12, 2),
    ('R', mat_green, 2.4, 1.5, 1.05, 14, 6),
]

for char, mat, x, sz, z, tx, tz in super_letters:
    create_block_letter(char, mat, (x, 0.05, z), size=sz, extrude=0.48, bevel=0.03, tilt_x=tx, tilt_z=tz)

# "64" (Con la tipografía oficial Typeface Mario 64)
bpy.ops.object.text_add(location=(3.95, -0.15, 1.1), rotation=(math.radians(76), 0, math.radians(-15)))
num64 = bpy.context.active_object
num64.name = "Logo_64"
num64.data.body = "64"
num64.data.font = n64_font
num64.data.size = 1.85
num64.data.extrude = 0.62
num64.data.bevel_depth = 0.04
num64.data.bevel_resolution = 2
num64.data.align_x = 'CENTER'
num64.data.align_y = 'CENTER'
bpy.ops.object.convert(target='MESH')
bpy.ops.object.transform_apply(rotation=True)
num64.data.materials.append(mat_red)
num64.data.materials.append(mat_gold)
for poly in num64.data.polygons:
    if poly.normal.y < -0.3:
        poly.material_index = 0
    else:
        poly.material_index = 1

# "TM"
bpy.ops.object.text_add(location=(5.2, -0.25, 2.05), rotation=(math.radians(82), 0, 0))
tm = bpy.context.active_object
tm.name = "Logo_TM"
tm.data.body = "TM"
tm.data.font = n64_font
tm.data.size = 0.48
tm.data.extrude = 0.12
tm.data.align_x = 'CENTER'
tm.data.align_y = 'CENTER'
bpy.ops.object.convert(target='MESH')
tm.data.materials.append(mat_white)

# "BUKELE" (Fila inferior dominante con la tipografía oficial Typeface Mario 64)
# B(Azul), U(Verde), K(Amarillo), E(Rojo), L(Verde), E(Azul)
bukele_letters = [
    ('B', mat_blue, -3.75, 2.35, -0.75, 14, -6),
    ('U', mat_green, -2.25, 2.4, -0.65, 13, -3),
    ('K', mat_yellow, -0.75, 2.45, -0.6, 12, 0),
    ('E', mat_red, 0.75, 2.45, -0.6, 12, 1),
    ('L', mat_green, 2.25, 2.4, -0.65, 13, 3),
    ('E', mat_blue, 3.75, 2.35, -0.75, 14, 6),
]

for char, mat, x, sz, z, tx, tz in bukele_letters:
    create_block_letter(char, mat, (x, -0.15, z), size=sz, extrude=0.72, bevel=0.04, tilt_x=tx, tilt_z=tz)

# -----------------------------------------------------------------------------
# 3. CÁMARA E ILUMINACIÓN DE ESTUDIO N64
# -----------------------------------------------------------------------------
bpy.ops.object.camera_add(
    location=(0.4, -16.2, 0.35),
    rotation=(math.radians(91), 0, 0)
)
cam = bpy.context.active_object
cam.data.lens = 52
bpy.context.scene.camera = cam

# Luces
bpy.ops.object.light_add(type='SUN', location=(-8, -12, 12), rotation=(math.radians(45), math.radians(-32), 0))
sun = bpy.context.active_object
sun.data.energy = 4.4

bpy.ops.object.light_add(type='POINT', location=(4, -8, 2))
fill = bpy.context.active_object
fill.data.energy = 280.0
fill.data.color = (1.0, 0.96, 0.90)

bpy.ops.object.light_add(type='POINT', location=(0, -6, -3.5))
bottom_light = bpy.context.active_object
bottom_light.data.energy = 220.0
bottom_light.data.color = (1.0, 0.88, 0.72)

world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.28, 0.28, 0.28, 1.0)
    bg.inputs['Strength'].default_value = 0.9

# Configuración de Render RGBA
scene = bpy.context.scene
scene.render.resolution_x = 1800
scene.render.resolution_y = 800
scene.render.film_transparent = True
scene.render.image_settings.color_mode = 'RGBA'

output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/img"
os.makedirs(output_dir, exist_ok=True)
logo_png_path = os.path.join(output_dir, "super_bukele_64_logo.png")
scene.render.filepath = logo_png_path

bpy.ops.render.render(write_still=True)
print(f"[OK] Render logo oficial Mario 64 finalizado: {logo_png_path}")
