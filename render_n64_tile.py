import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# -----------------------------------------------------------------------------
# 1. CARGAR FUENTE N64 OFICIAL
# -----------------------------------------------------------------------------
font_path = "/home/omarchy/Projects/pj-vibe-game/assets/fonts/TypefaceMario64.otf"
mario_font = bpy.data.fonts.load(font_path)

# -----------------------------------------------------------------------------
# 2. MATERIALES AUTÉNTICOS N64
# -----------------------------------------------------------------------------
# Fondo Azul Marino N64 con viñeta radial (centro más claro, bordes oscuros)
mat_tile_bg = bpy.data.materials.new(name="TileBG")
mat_tile_bg.use_nodes = True
nodes = mat_tile_bg.node_tree.nodes
links = mat_tile_bg.node_tree.links
bsdf = nodes.get("Principled BSDF")

tex_coord = nodes.new('ShaderNodeTexCoord')
v_dist = nodes.new('ShaderNodeVectorMath')
v_dist.operation = 'DISTANCE'
v_dist.inputs[1].default_value = (0.5, 0.5, 0.0)

ramp_vignette = nodes.new('ShaderNodeValToRGB')
ramp_vignette.color_ramp.elements[0].position = 0.0
# Centro azul cobalto N64 brillante
ramp_vignette.color_ramp.elements[0].color = (0.04, 0.11, 0.38, 1.0)
ramp_vignette.color_ramp.elements[1].position = 0.68
# Borde azul oscuro profundo
ramp_vignette.color_ramp.elements[1].color = (0.005, 0.012, 0.05, 1.0)

# Ruido sutil para textura de tela/denim N64
noise = nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 24.0
noise.inputs['Detail'].default_value = 3.0

mix_rgb = nodes.new('ShaderNodeMix')
mix_rgb.data_type = 'RGBA'
mix_rgb.inputs['Factor'].default_value = 0.18
links.new(ramp_vignette.outputs['Color'], mix_rgb.inputs['A'])
links.new(noise.outputs['Color'], mix_rgb.inputs['B'])
links.new(mix_rgb.outputs['Result'], bsdf.inputs['Base Color'])

links.new(tex_coord.outputs['UV'], v_dist.inputs[0])
links.new(v_dist.outputs['Value'], ramp_vignette.inputs['Fac'])
bsdf.inputs['Roughness'].default_value = 0.88

# Material para texto SUPER y BUKELE: Azul Hielo N64
mat_ice_face = bpy.data.materials.new(name="IceFace")
mat_ice_face.use_nodes = True
bsdf_if = mat_ice_face.node_tree.nodes.get("Principled BSDF")
# Color celeste hielo brillante N64
bsdf_if.inputs['Base Color'].default_value = (0.16, 0.44, 0.98, 1.0)
bsdf_if.inputs['Roughness'].default_value = 0.18
if 'Specular IOR Level' in bsdf_if.inputs:
    bsdf_if.inputs['Specular IOR Level'].default_value = 0.9

# Material para laterales/sombra de las letras
mat_ice_sides = bpy.data.materials.new(name="IceSides")
mat_ice_sides.use_nodes = True
bsdf_is = mat_ice_sides.node_tree.nodes.get("Principled BSDF")
bsdf_is.inputs['Base Color'].default_value = (0.008, 0.02, 0.09, 1.0)
bsdf_is.inputs['Roughness'].default_value = 0.65

# Material para el "64" rojo
mat_red_64 = bpy.data.materials.new(name="Red64")
mat_red_64.use_nodes = True
bsdf_r = mat_red_64.node_tree.nodes.get("Principled BSDF")
bsdf_r.inputs['Base Color'].default_value = (0.88, 0.02, 0.02, 1.0)
bsdf_r.inputs['Roughness'].default_value = 0.18
if 'Specular IOR Level' in bsdf_r.inputs:
    bsdf_r.inputs['Specular IOR Level'].default_value = 0.92

mat_red_sides = bpy.data.materials.new(name="RedSides")
mat_red_sides.use_nodes = True
bsdf_rs = mat_red_sides.node_tree.nodes.get("Principled BSDF")
bsdf_rs.inputs['Base Color'].default_value = (0.18, 0.004, 0.004, 1.0)

# -----------------------------------------------------------------------------
# 3. BALDOSA BASE Y LÍNEAS DE JUNTA (4.0 x 4.0)
# -----------------------------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0, 0, 0))
plane = bpy.context.active_object
plane.name = "TilePlane"
plane.data.materials.append(mat_tile_bg)

# Líneas sutiles de costura perimetral en los bordes para la cuadrícula
mat_seam = bpy.data.materials.new(name="Seam")
mat_seam.use_nodes = True
bsdf_seam = mat_seam.node_tree.nodes.get("Principled BSDF")
bsdf_seam.inputs['Base Color'].default_value = (0.002, 0.005, 0.02, 1.0)
bsdf_seam.inputs['Roughness'].default_value = 1.0

def make_seam_border(loc, scale):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    b = bpy.context.active_object
    b.scale = scale
    b.data.materials.append(mat_seam)

seam_w = 0.035
make_seam_border((0, 2.0 - seam_w/2, 0.005), (4.0, seam_w, 0.01))
make_seam_border((0, -2.0 + seam_w/2, 0.005), (4.0, seam_w, 0.01))
make_seam_border((-2.0 + seam_w/2, 0, 0.005), (seam_w, 4.0, 0.01))
make_seam_border((2.0 - seam_w/2, 0, 0.005), (seam_w, 4.0, 0.01))

# -----------------------------------------------------------------------------
# 4. TEXTOS CON RELIEVE Y BISEL N64
# -----------------------------------------------------------------------------
def make_tile_text(body, loc, size, mat_front, mat_side, extrude=0.09, bevel=0.022):
    bpy.ops.object.text_add(location=loc)
    t = bpy.context.active_object
    t.data.body = body
    t.data.font = mario_font
    t.data.size = size
    t.data.extrude = extrude
    t.data.bevel_depth = bevel
    t.data.bevel_resolution = 2
    t.data.align_x = 'CENTER'
    t.data.align_y = 'CENTER'
    bpy.ops.object.convert(target='MESH')
    t.data.materials.append(mat_front)
    t.data.materials.append(mat_side)
    for p in t.data.polygons:
        if p.normal.z > 0.4:
            p.material_index = 0
        else:
            p.material_index = 1
    return t

# "SUPER"
make_tile_text("SUPER", (-0.32, 0.94, 0.02), size=1.14, mat_front=mat_ice_face, mat_side=mat_ice_sides)

# "BUKELE"
make_tile_text("BUKELE", (-0.18, -0.88, 0.02), size=0.95, mat_front=mat_ice_face, mat_side=mat_ice_sides)

# "64" (en rojo intenso entre SUPER y BUKELE a la derecha)
make_tile_text("64", (1.26, 0.05, 0.03), size=0.92, mat_front=mat_red_64, mat_side=mat_red_sides, extrude=0.11, bevel=0.025)

# -----------------------------------------------------------------------------
# 5. CÁMARA ORTOGRÁFICA E ILUMINACIÓN
# -----------------------------------------------------------------------------
bpy.ops.object.camera_add(location=(0, 0, 6.0), rotation=(0, 0, 0))
cam = bpy.context.active_object
cam.data.type = 'ORTHO'
cam.data.ortho_scale = 4.0
bpy.context.scene.camera = cam

# Luces
bpy.ops.object.light_add(type='SUN', location=(-5, 5, 8), rotation=(math.radians(38), math.radians(-32), 0))
sun = bpy.context.active_object
sun.data.energy = 3.9

bpy.ops.object.light_add(type='POINT', location=(0, 0, 3.5))
fill = bpy.context.active_object
fill.data.energy = 100.0
fill.data.color = (0.5, 0.7, 1.0)

world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg_w = world.node_tree.nodes.get("Background")
if bg_w:
    bg_w.inputs['Color'].default_value = (0.01, 0.02, 0.08, 1.0)
    bg_w.inputs['Strength'].default_value = 0.5

# Render settings: 512x512
scene = bpy.context.scene
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.image_settings.color_mode = 'RGB'

output_dir = "/home/omarchy/Projects/pj-vibe-game/assets/img"
os.makedirs(output_dir, exist_ok=True)
tile_png_path = os.path.join(output_dir, "n64_bg_tile.png")
scene.render.filepath = tile_png_path

bpy.ops.render.render(write_still=True)
print(f"[OK] Baldosa N64 v5 finalizada: {tile_png_path}")
