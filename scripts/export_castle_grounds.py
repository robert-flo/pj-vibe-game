import os
import re
import shutil

BASE_C_DIR = "/home/omarchy/Projects/Render96ex/levels/castle_grounds/areas/1"
TEX_OUTSIDE_DIR = "/home/omarchy/Projects/RENDER96-HD-TEXTURE-PACK/gfx/textures/outside"
TEX_LEVEL_DIR = "/home/omarchy/Projects/RENDER96-HD-TEXTURE-PACK/gfx/levels/castle_grounds"
OUT_TEX_DIR = "/home/omarchy/Projects/pj-vibe-game/assets/textures/castle_grounds"
OUT_OBJ_PATH = "/home/omarchy/Projects/pj-vibe-game/assets/models/castle_grounds.obj"
OUT_MTL_PATH = "/home/omarchy/Projects/pj-vibe-game/assets/models/castle_grounds.mtl"

os.makedirs(OUT_TEX_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUT_OBJ_PATH), exist_ok=True)

# Texture symbol to HD texture filename and original (width, height)
TEX_MAP = {
    # Level textures
    "castle_grounds_seg7_texture_07000000": ("0.rgba16.png", TEX_LEVEL_DIR, 32, 64),
    "castle_grounds_seg7_texture_07001000": ("1.rgba16.png", TEX_LEVEL_DIR, 32, 64),
    "castle_grounds_seg7_texture_07002000": ("2.rgba16.png", TEX_LEVEL_DIR, 64, 32),
    "castle_grounds_seg7_texture_0700C9E8": ("3.rgba16.png", TEX_LEVEL_DIR, 32, 32),
    "castle_grounds_seg7_texture_0700D9E8": ("4.rgba16.png", TEX_LEVEL_DIR, 32, 32),
    "castle_grounds_seg7_us_texture_0700EAE8": ("5.ia8.png", TEX_LEVEL_DIR, 32, 32),

    # Outside generic textures
    "outside_09000000": ("castle_grounds_textures.00000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09000800": ("castle_grounds_textures.00800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09001000": ("castle_grounds_textures.01000.rgba16.png", TEX_OUTSIDE_DIR, 64, 32),
    "outside_09002000": ("castle_grounds_textures.02000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09003000": ("castle_grounds_textures.03000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09003800": ("castle_grounds_textures.03800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09004000": ("castle_grounds_textures.04000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09004800": ("castle_grounds_textures.04800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09005800": ("castle_grounds_textures.05800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09006000": ("castle_grounds_textures.06000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09006800": ("castle_grounds_textures.06800.rgba16.png", TEX_OUTSIDE_DIR, 64, 32),
    "outside_09007800": ("castle_grounds_textures.07800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09008000": ("castle_grounds_textures.08000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09008800": ("castle_grounds_textures.08800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09009000": ("castle_grounds_textures.09000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_09009800": ("castle_grounds_textures.09800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_0900A000": ("castle_grounds_textures.0A000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_0900A800": ("castle_grounds_textures.0A800.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_0900B000": ("castle_grounds_textures.0B000.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_0900B400": ("castle_grounds_textures.0B400.rgba16.png", TEX_OUTSIDE_DIR, 32, 32),
    "outside_0900BC00": ("castle_grounds_textures.0BC00.ia16.png", TEX_OUTSIDE_DIR, 32, 32),
}

# Copy textures to output directory
copied_textures = {}
for sym, (fname, src_dir, orig_w, orig_h) in TEX_MAP.items():
    src_file = os.path.join(src_dir, fname)
    dst_file = os.path.join(OUT_TEX_DIR, fname)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dst_file)
        copied_textures[sym] = (fname, orig_w, orig_h)
    else:
        print(f"Warning: Missing texture file {src_file}")

# Write MTL file
with open(OUT_MTL_PATH, "w") as mtl:
    for sym, (fname, orig_w, orig_h) in copied_textures.items():
        mtl.write(f"newmtl mat_{sym}\n")
        mtl.write("Ka 1.000 1.000 1.000\n")
        mtl.write("Kd 1.000 1.000 1.000\n")
        mtl.write("Ks 0.000 0.000 0.000\n")
        mtl.write("d 1.0\n")
        mtl.write("illum 2\n")
        rel_tex_path = os.path.relpath(os.path.join(OUT_TEX_DIR, fname), os.path.dirname(OUT_OBJ_PATH))
        mtl.write(f"map_Kd {rel_tex_path}\n\n")

print(f"MTL written with {len(copied_textures)} materials.")

# Process all model.inc.c files (areas 1 to 11)
all_v_lines = []
all_vt_lines = []
all_f_by_mat = {}

v_offset = 1
vt_offset = 1

# SM64 scale factor: 1 SM64 unit = 0.01 Three.js units (or 100 SM64 units = 1 meter)
SCALE = 0.01

# Solo las capas estáticas del nivel (geo.inc.c principal): 1,2,4,5,6,9,10
for area_idx in (1, 2, 4, 5, 6, 9, 10):
    mf = os.path.join(BASE_C_DIR, str(area_idx), "model.inc.c")
    if not os.path.exists(mf):
        continue

    with open(mf, "r") as f:
        text = f.read()

    # Luces (gdSPDefLights1): ambiente, color difuso y dirección (int8)
    lights = {}
    for lm in re.finditer(r'Lights1\s+(\w+)\s*=\s*gdSPDefLights1\(([^)]+)\)', text):
        n = [int(t.strip(), 0) for t in lm.group(2).replace('\n', ' ').split(',') if t.strip()]
        d = [(v - 256 if v > 127 else v) for v in n[6:9]]
        mag = max((d[0]**2 + d[1]**2 + d[2]**2) ** 0.5, 1e-6)
        lights[lm.group(1)] = (n[0:3], n[3:6], [c / mag for c in d])
    lit_file = 'gsSPLight' in text

    # Parse vertex arrays
    vtx_arrays = {}
    for m in re.finditer(r'static const Vtx\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
        arr_name = m.group(1)
        body = m.group(2)
        verts = []
        for vm in re.finditer(r'\{\{\{\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\},\s*0,\s*\{\s*(-?\d+),\s*(-?\d+)\},\s*\{\s*([^}]+)\}\}\}', body):
            x = float(vm.group(1)) * SCALE
            y = float(vm.group(2)) * SCALE
            z = float(vm.group(3)) * SCALE
            u_raw = float(vm.group(4))
            v_raw = float(vm.group(5))
            cols = [int(c.strip(), 0) for c in vm.group(6).split(',')]
            verts.append((x, y, z, u_raw, v_raw, cols[0], cols[1], cols[2]))
        vtx_arrays[arr_name] = verts

    # Parse display lists
    dl_matches = list(re.finditer(r'(?:static const Gfx|const Gfx)\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL))
    current_mat = "outside_09000000"
    cur_light = None  # persiste entre display lists (como el estado RSP)

    for dl in dl_matches:
        dl_body = dl.group(2)

        # Update texture if present
        tex_m = re.search(r'gsDPSetTextureImage\([^,]+,\s*[^,]+,\s*[^,]+,\s*(\w+)\)', dl_body)
        if tex_m:
            current_mat = tex_m.group(1)

        if current_mat not in all_f_by_mat:
            all_f_by_mat[current_mat] = []

        # Current vertex cache (indices 0..31)
        vcache = {}
        lines = dl_body.split("\n")

        # Get texture dimensions for normalized UVs
        if current_mat in copied_textures:
            _, orig_w, orig_h = copied_textures[current_mat]
        else:
            orig_w, orig_h = 32, 32

        for line in lines:
            # Check texture within line
            ltm = re.search(r'gsDPSetTextureImage\([^,]+,\s*[^,]+,\s*[^,]+,\s*(\w+)\)', line)
            if ltm:
                current_mat = ltm.group(1)
                if current_mat not in all_f_by_mat:
                    all_f_by_mat[current_mat] = []
                if current_mat in copied_textures:
                    _, orig_w, orig_h = copied_textures[current_mat]
                else:
                    orig_w, orig_h = 32, 32

            lgm = re.search(r'gsSPLight\(&(\w+)\.l,\s*1\)', line)
            if lgm:
                cur_light = lgm.group(1)

            # Check vertex load
            vm = re.search(r'gsSPVertex\((\w+),\s*(\d+),\s*(\d+)\)', line)
            if vm:
                varr = vm.group(1)
                count = int(vm.group(2))
                start = int(vm.group(3))
                if varr in vtx_arrays:
                    src_verts = vtx_arrays[varr]
                    for i in range(count):
                        if i < len(src_verts):
                            vx, vy, vz, ur, vr, cr, cg, cb = src_verts[i]
                            if lit_file and cur_light in lights:
                                amb, dif, ldir = lights[cur_light]
                                nx, ny, nz = [((c - 256) if c > 127 else c) / 127.0 for c in (cr, cg, cb)]
                                ndl = max(0.0, nx * ldir[0] + ny * ldir[1] + nz * ldir[2])
                                cr, cg, cb = [min(1.0, (amb[k] + dif[k] * ndl) / 255.0) for k in range(3)]
                            else:
                                cr, cg, cb = cr / 255.0, cg / 255.0, cb / 255.0
                            # Normalized UVs
                            u_norm = (ur / 32.0) / orig_w
                            # In OpenGL / OBJ UV space, V is inverted
                            v_norm = 1.0 - ((vr / 32.0) / orig_h)

                            all_v_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f} {cr:.4f} {cg:.4f} {cb:.4f}\n")
                            all_vt_lines.append(f"vt {u_norm:.6f} {v_norm:.6f}\n")

                            curr_idx = len(all_v_lines) # 1-based index in OBJ
                            vcache[start + i] = curr_idx

            # Triangles
            t1m = re.search(r'gsSP1Triangle\(\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t1m:
                i0 = int(t1m.group(1))
                i1 = int(t1m.group(2))
                i2 = int(t1m.group(3))
                if i0 in vcache and i1 in vcache and i2 in vcache:
                    v0 = vcache[i0]
                    v1 = vcache[i1]
                    v2 = vcache[i2]
                    all_f_by_mat[current_mat].append(f"f {v0}/{v0} {v1}/{v1} {v2}/{v2}\n")

            t2m = re.search(r'gsSP2Triangles\(\s*(\d+),\s*(\d+),\s*(\d+),\s*[^,]+,\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t2m:
                i0 = int(t2m.group(1))
                i1 = int(t2m.group(2))
                i2 = int(t2m.group(3))
                if i0 in vcache and i1 in vcache and i2 in vcache:
                    v0 = vcache[i0]
                    v1 = vcache[i1]
                    v2 = vcache[i2]
                    all_f_by_mat[current_mat].append(f"f {v0}/{v0} {v1}/{v1} {v2}/{v2}\n")

                i3 = int(t2m.group(4))
                i4 = int(t2m.group(5))
                i5 = int(t2m.group(6))
                if i3 in vcache and i4 in vcache and i5 in vcache:
                    v3 = vcache[i3]
                    v4 = vcache[i4]
                    v5 = vcache[i5]
                    all_f_by_mat[current_mat].append(f"f {v3}/{v3} {v4}/{v4} {v5}/{v5}\n")

# Write OBJ file
with open(OUT_OBJ_PATH, "w") as obj:
    obj.write(f"mtllib {os.path.basename(OUT_MTL_PATH)}\n")
    obj.write("o PeachCastleGrounds\n\n")

    for vl in all_v_lines:
        obj.write(vl)
    obj.write("\n")

    for vtl in all_vt_lines:
        obj.write(vtl)
    obj.write("\n")

    for mat, faces in all_f_by_mat.items():
        if faces:
            obj.write(f"usemtl mat_{mat}\n")
            obj.write("s 1\n")
            for f in faces:
                obj.write(f)
            obj.write("\n")

total_faces = sum(len(f) for f in all_f_by_mat.values())
print(f"OBJ Export Complete: {len(all_v_lines)} vertices, {total_faces} faces, saved to {OUT_OBJ_PATH}")
