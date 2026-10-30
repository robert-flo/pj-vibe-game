"""Cuerpo del Bukele jugable (sin cabeza) segun Desktop/assets2:
blazer azul marino, camiseta negra, pantalon azul oscuro, zapatos cafes.
Convencion: Z arriba, el personaje mira hacia +X (igual que bukele_head.glb).
Nodos exportados: Torso, ArmL, ArmR, LegL, LegR (pivotes en hombro/cadera)
para animarlos desde Three.js. La cabeza se carga aparte (bukele_head.glb).
"""
import bpy, math

OUT = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_body.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, rgb, rough=0.8):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    return m


BLAZER = mat("blazer_navy", (0.020, 0.045, 0.110))
TEE = mat("tee_black", (0.012, 0.012, 0.014))
PANTS = mat("pants_navy", (0.014, 0.024, 0.055))
SHOE = mat("shoe_brown", (0.140, 0.055, 0.020), 0.55)
SKIN = mat("skin", (0.690, 0.410, 0.290), 0.6)
BUTTON = mat("button", (0.01, 0.01, 0.012), 0.3)


def finish(o, m, smooth=True):
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if smooth:
        bpy.ops.object.shade_smooth()
    o.data.materials.clear()
    o.data.materials.append(m)
    o.select_set(False)
    return o


def cyl(name, r, h, loc, scale=(1, 1, 1), m=BLAZER, verts=20, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    return finish(o, m)


def sph(name, r, loc, scale=(1, 1, 1), m=SKIN):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    return finish(o, m)


def box(name, size, loc, rot=(0, 0, 0), m=BLAZER, bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = o.modifiers.new("b", "BEVEL")
    mod.width = bevel
    mod.segments = 2
    bpy.ops.object.modifier_apply(modifier="b")
    return finish(o, m)


def join(parts, name, origin):
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.active_object
    o.name = name
    bpy.context.scene.cursor.location = origin
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    return o


# ---------------- Torso (cadera z=0.95 -> cuello z=1.55) ----------------
t = []
t.append(cyl("t_chest", 0.30, 0.62, (0, 0, 1.25), (0.72, 1.12, 1.0), BLAZER))      # pecho/espalda
t.append(cyl("t_hips", 0.27, 0.22, (0, 0, 1.00), (0.70, 1.08, 1.0), BLAZER))        # faldon del blazer
t.append(sph("t_shoulderL", 0.15, (0, 0.31, 1.49), (0.9, 1, 0.9), BLAZER))
t.append(sph("t_shoulderR", 0.15, (0, -0.31, 1.49), (0.9, 1, 0.9), BLAZER))
t.append(cyl("t_neck", 0.085, 0.16, (0.0, 0, 1.60), (1, 1, 1), SKIN, verts=16))
# camiseta negra (V frontal) y solapas
t.append(box("t_tee", (0.03, 0.14, 0.52), (0.215, 0, 1.30), (0, 0, 0), TEE, 0.01))
t.append(box("t_lapelL", (0.035, 0.07, 0.40), (0.216, 0.10, 1.34), (math.radians(8), 0, math.radians(-3)), BLAZER))
t.append(box("t_lapelR", (0.035, 0.07, 0.40), (0.216, -0.10, 1.34), (math.radians(-8), 0, math.radians(3)), BLAZER))
t.append(box("t_collar", (0.10, 0.27, 0.05), (0.0, 0, 1.55), (0, 0, 0), BLAZER))
t.append(sph("t_btn1", 0.018, (0.232, 0.0, 1.10), (1, 1, 1), BUTTON))
t.append(sph("t_btn2", 0.018, (0.232, 0.0, 0.99), (1, 1, 1), BUTTON))
t.append(box("t_pocket", (0.02, 0.10, 0.03), (0.232, -0.15, 1.04), (0, 0, 0), BUTTON, 0.005))
torso = join(t, "Torso", (0, 0, 1.25))

# ---------------- Brazos (pivote en hombro) ----------------
def arm(side):
    s = 1 if side == "L" else -1
    p = []
    p.append(cyl("a_upper", 0.095, 0.40, (0, 0, -0.20), (1, 1, 1), BLAZER, verts=16))
    p.append(cyl("a_lower", 0.085, 0.36, (0.02, 0, -0.56), (1, 1, 1), BLAZER, verts=16))
    p.append(sph("a_cuff", 0.088, (0.02, 0, -0.74), (1, 1, 0.5), BLAZER))
    p.append(sph("a_hand", 0.082, (0.025, 0, -0.84), (0.9, 0.8, 1.15), SKIN))
    a = join(p, "Arm" + side, (0, 0, 0))
    a.location = (0, s * 0.335, 1.49)
    a.rotation_euler = (math.radians(-s * 6), 0, 0)
    return a


arm("L"); arm("R")

# ---------------- Piernas (pivote en cadera) ----------------
def leg(side):
    s = 1 if side == "L" else -1
    p = []
    p.append(cyl("l_upper", 0.115, 0.50, (0, 0, -0.25), (1, 1, 1), PANTS, verts=16))
    p.append(cyl("l_lower", 0.098, 0.46, (0, 0, -0.69), (1, 1, 1), PANTS, verts=16))
    p.append(sph("l_shoe", 0.10, (0.07, 0, -0.88), (1.65, 0.95, 0.75), SHOE))
    l = join(p, "Leg" + side, (0, 0, 0))
    l.location = (0, s * 0.14, 0.97)
    return l


leg("L"); leg("R")

# ---------------- Exportar ----------------
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_materials="EXPORT", export_apply=True)
print("EXPORTED", OUT)
