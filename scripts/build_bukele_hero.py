"""Generador del cuerpo de Bukele estilo Fortnite / Atleta Estilizado (7.5 cabezas).
Blazer azul marino oscuro con V-taper, camiseta negra, cinturón con hebilla,
brazos articulados con codos y piernas articuladas con rodillas y zapatillas 3D.
Convención: Z arriba, mira hacia +X.
Jerarquía exportada:
  - Torso
  - ArmL -> ForearmL
  - ArmR -> ForearmR
  - LegL -> ShinL
  - LegR -> ShinR
"""
import bpy, math

OUT = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_body.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)

# ----------------- Materiales -----------------
def mat(name, rgb, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m

BLAZER    = mat("blazer_navy", (0.015, 0.032, 0.085), 0.72)
LAPEL     = mat("blazer_lapel", (0.010, 0.022, 0.060), 0.60)
TEE       = mat("tee_black", (0.010, 0.010, 0.012), 0.88)
PANTS     = mat("pants_navy", (0.012, 0.024, 0.055), 0.75)
BELT      = mat("belt_black", (0.008, 0.008, 0.009), 0.40)
BUCKLE    = mat("buckle_gold", (0.85, 0.68, 0.18), 0.25, 0.85)
WATCH     = mat("watch_gold", (0.90, 0.72, 0.20), 0.20, 0.90)
SKIN      = mat("skin", (0.710, 0.440, 0.310), 0.65)
SNEAKER_W = mat("sneaker_white", (0.86, 0.87, 0.89), 0.55)
SNEAKER_B = mat("sneaker_blue", (0.02, 0.12, 0.40), 0.60)
SNEAKER_S = mat("sneaker_sole", (0.16, 0.16, 0.18), 0.80)

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

def sph(name, r, loc, scale=(1, 1, 1), m=SKIN, segs=20, rings=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=rings, radius=r, location=loc)
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
    if bevel > 0:
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

# ==============================================================================
# 1. TORSO ATLÉTICO (V-Taper estilo Fortnite, pecho atlético, cintura y cuello)
# ==============================================================================
t = []

# Pecho con volumen atlético tridimensional (profundidad 0.32m, ancho 0.44m)
t.append(box("t_pecs", (0.32, 0.42, 0.28), (0.04, 0, 1.39), (0, math.radians(7), 0), BLAZER, bevel=0.045))
# Espalda en V con grosor muscular (trapecio y dorsales)
t.append(box("t_upper_back", (0.28, 0.44, 0.30), (-0.05, 0, 1.40), (0, math.radians(-5), 0), BLAZER, bevel=0.045))
# Caja torácica media
t.append(box("t_ribcage", (0.28, 0.37, 0.22), (0.0, 0, 1.24), (0, 0, 0), BLAZER, bevel=0.035))
# Cintura atlética estilizada
t.append(box("t_waist", (0.25, 0.33, 0.18), (0.0, 0, 1.10), (0, 0, 0), BLAZER, bevel=0.030))

# Cinturón negro y hebilla dorada
t.append(box("t_belt", (0.265, 0.34, 0.055), (0.0, 0, 1.02), (0, 0, 0), BELT, bevel=0.008))
t.append(box("t_buckle", (0.04, 0.09, 0.065), (0.135, 0, 1.02), (0, 0, 0), BUCKLE, bevel=0.006))

# Pelvis / caderas con faldón del blazer
t.append(box("t_hips", (0.26, 0.35, 0.14), (0.0, 0, 0.95), (0, 0, 0), PANTS, bevel=0.035))
t.append(box("t_blazer_skirtL", (0.27, 0.045, 0.15), (0.0, 0.175, 0.96), (0, 0, math.radians(4)), BLAZER, bevel=0.015))
t.append(box("t_blazer_skirtR", (0.27, 0.045, 0.15), (0.0, -0.175, 0.96), (0, 0, math.radians(-4)), BLAZER, bevel=0.015))
t.append(box("t_blazer_skirtB", (0.045, 0.35, 0.15), (-0.135, 0, 0.96), (0, 0, 0), BLAZER, bevel=0.015))

# Hombros deltoides atléticos
t.append(sph("t_shoulderL", 0.095, (0.0, 0.25, 1.48), (1.15, 1.05, 1.15), BLAZER))
t.append(sph("t_shoulderR", 0.095, (0.0, -0.25, 1.48), (1.15, 1.05, 1.15), BLAZER))

# Cuello ergonómico con piel natural que empalma con la cabeza
t.append(cyl("t_neck_skin", 0.076, 0.16, (0.01, 0, 1.57), (1.15, 1.0, 1.0), SKIN, verts=20))
# Solapas del blazer y cuello de la camiseta
t.append(box("t_lapelL", (0.04, 0.075, 0.32), (0.165, 0.10, 1.37), (math.radians(10), 0, math.radians(-6)), LAPEL, bevel=0.012))
t.append(box("t_lapelR", (0.04, 0.075, 0.32), (0.165, -0.10, 1.37), (math.radians(-10), 0, math.radians(6)), LAPEL, bevel=0.012))
t.append(box("t_tee", (0.03, 0.12, 0.30), (0.160, 0, 1.37), (0, 0, 0), TEE, bevel=0.005))
# Bolsillo superior de pecho con pañuelo blanco
t.append(box("t_pocket", (0.018, 0.07, 0.016), (0.178, 0.13, 1.38), (0, 0, math.radians(-8)), LAPEL, bevel=0.003))
t.append(box("t_hanky", (0.020, 0.04, 0.022), (0.182, 0.13, 1.40), (0, 0, math.radians(-8)), SNEAKER_W, bevel=0.002))

torso = join(t, "Torso", (0, 0, 1.15))

# ==============================================================================
# 2. BRAZOS ARTICULADOS (Upper Arm -> Forearm con codos y manos atléticas)
# ==============================================================================
def create_arm(side):
    s = 1 if side == "L" else -1
    shoulder_pos = (0, s * 0.25, 1.48)
    elbow_pos = (0, s * 0.27, 1.18)

    # --- Upper Arm (Hombro a Codo) ---
    ua = []
    # Bíceps/Tríceps en blazer
    ua.append(cyl(f"a_upper_{side}", 0.065, 0.30, (0, 0, -0.15), (1.05, 0.95, 1.0), BLAZER, verts=16))
    ua.append(sph(f"a_deltoid_{side}", 0.072, (0, 0, -0.04), (1.0, 1.0, 1.1), BLAZER))
    # Codo redondeado
    ua.append(sph(f"a_elbow_{side}", 0.055, (0, 0, -0.30), (1.0, 1.0, 1.0), BLAZER))
    arm_upper = join(ua, f"Arm{side}", (0, 0, 0))
    arm_upper.location = shoulder_pos

    # --- Forearm (Codo a Muñeca) ---
    fa = []
    # Antebrazo cónico
    fa.append(cyl(f"a_fore_{side}", 0.052, 0.26, (0, 0, -0.13), (1.0, 0.92, 1.0), BLAZER, verts=16))
    # Puño de manga
    fa.append(cyl(f"a_cuff_{side}", 0.054, 0.04, (0, 0, -0.25), (1.0, 1.0, 1.0), LAPEL, verts=16))
    if side == "L":
        # Reloj dorado en muñeca izquierda
        fa.append(cyl("a_watch", 0.057, 0.025, (0, 0, -0.26), (1.0, 1.0, 1.0), WATCH, verts=16))
    # Mano atlética cerrada en puño / dedos estilizados
    fa.append(sph(f"a_hand_{side}", 0.052, (0.015, 0, -0.32), (1.3, 0.85, 1.1), SKIN))
    fa.append(box(f"a_thumb_{side}", (0.035, 0.025, 0.03), (0.035, s * 0.02, -0.31), (0, 0, math.radians(s * 15)), SKIN, bevel=0.005))

    arm_fore = join(fa, f"Forearm{side}", (0, 0, 0))
    arm_fore.location = (0, s * 0.02, -0.30)
    arm_fore.parent = arm_upper

    return arm_upper

create_arm("L")
create_arm("R")

# ==============================================================================
# 3. PIERNAS ARTICULADAS (Thigh -> Shin con rodillas y zapatillas 3D)
# ==============================================================================
def create_leg(side):
    s = 1 if side == "L" else -1
    hip_pos = (0, s * 0.115, 0.94)

    # --- Thigh (Muslo: Cadera a Rodilla) ---
    th = []
    # Cuádriceps atlético
    th.append(cyl(f"l_thigh_{side}", 0.092, 0.42, (0.015, 0, -0.21), (1.18, 1.05, 1.0), PANTS, verts=18))
    # Articulación de rodilla
    th.append(sph(f"l_knee_{side}", 0.078, (0.02, 0, -0.42), (1.15, 1.0, 1.0), PANTS))
    leg_upper = join(th, f"Leg{side}", (0, 0, 0))
    leg_upper.location = hip_pos

    # --- Shin (Pantorrilla: Rodilla a Tobillo + Zapatilla) ---
    sh = []
    # Pantorrilla cónica
    sh.append(cyl(f"l_calf_{side}", 0.076, 0.38, (0.01, 0, -0.19), (1.15, 1.0, 1.0), PANTS, verts=18))
    # Tobillo
    sh.append(cyl(f"l_ankle_{side}", 0.060, 0.08, (0, 0, -0.36), (1.0, 1.0, 1.0), PANTS, verts=16))

    # --- Zapatilla Deportiva Moderna (Sneaker estilo Fortnite) ---
    # Suela de goma negra con dibujo
    sh.append(box(f"s_sole_{side}", (0.26, 0.12, 0.038), (0.055, 0, -0.42), (0, 0, 0), SNEAKER_S, bevel=0.008))
    # Cuerpo principal blanco
    sh.append(box(f"s_body_{side}", (0.24, 0.108, 0.072), (0.05, 0, -0.375), (0, math.radians(-3), 0), SNEAKER_W, bevel=0.015))
    # Puntera estilizada curvada hacia arriba
    sh.append(box(f"s_toe_{side}", (0.09, 0.102, 0.050), (0.145, 0, -0.380), (0, math.radians(14), 0), SNEAKER_B, bevel=0.01))
    # Detalle lateral azul marino
    sh.append(box(f"s_stripe_{side}", (0.16, 0.114, 0.028), (0.045, 0, -0.370), (0, 0, 0), SNEAKER_B, bevel=0.004))

    leg_shin = join(sh, f"Shin{side}", (0, 0, 0))
    leg_shin.location = (0, 0, -0.42)
    leg_shin.parent = leg_upper

    return leg_upper

create_leg("L")
create_leg("R")

# ==============================================================================
# EXPORTACIÓN GLTF CON JERARQUÍA COMPLETA
# ==============================================================================
bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format="GLB",
    export_materials="EXPORT",
    export_apply=False  # Mantener transformaciones relativas de jerarquía de padres/hijos
)
print("EXPORTED SUCCESSFUL:", OUT)
