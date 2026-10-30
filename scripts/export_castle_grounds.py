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
    "castle_grounds_seg7_texture_0700C9E8": ("3.rgba16.png", TEX_LEVEL_DIR, 32, 64),
    "castle_grounds_seg7_texture_0700D9E8": ("4.rgba16.png", TEX_LEVEL_DIR, 32, 64),
    "castle_grounds_seg7_us_texture_0700EAE8": ("5.ia8.png", TEX_LEVEL_DIR, 64, 32),

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

copied_textures = {}
for sym, (fname, src_dir, orig_w, orig_h) in TEX_MAP.items():
    src_file = os.path.join(src_dir, fname)
    dst_file = os.path.join(OUT_TEX_DIR, fname)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dst_file)
        copied_textures[sym] = (fname, orig_w, orig_h)
    else:
        print(f"Warning: Missing texture file {src_file}")

with open(OUT_MTL_PATH, "w") as mtl:
    mtl.write("newmtl mat_untextured_shade\n")
    mtl.write("Ka 1.000 1.000 1.000\n")
    mtl.write("Kd 1.000 1.000 1.000\n")
    mtl.write("Ks 0.000 0.000 0.000\n")
    mtl.write("d 1.0\n")
    mtl.write("illum 2\n\n")
    for sym, (fname, orig_w, orig_h) in copied_textures.items():
        mtl.write(f"newmtl mat_{sym}\n")
        mtl.write("Ka 1.000 1.000 1.000\n")
        mtl.write("Kd 1.000 1.000 1.000\n")
        mtl.write("Ks 0.000 0.000 0.000\n")
        mtl.write("d 1.0\n")
        mtl.write("illum 2\n")
        rel_tex_path = os.path.relpath(os.path.join(OUT_TEX_DIR, fname), os.path.dirname(OUT_OBJ_PATH))
        mtl.write(f"map_Kd {rel_tex_path}\n\n")

print(f"MTL written with {len(copied_textures) + 1} materials.")

all_v_lines = []
all_vt_lines = []
all_f_by_mat = {"untextured_shade": []}

SCALE = 0.01

# Static level layers + special_level_geo_03 (central castle spire at 0, 2867, -3924) + moat/cannon grills (7, 8)
AREA_PLACEMENTS = [
    (1, (0.0, 0.0, 0.0)),
    (2, (0.0, 0.0, 0.0)),
    (3, (0.0, 2867.0, -3924.0)),
    (4, (0.0, 0.0, 0.0)),
    (5, (0.0, 0.0, 0.0)),
    (6, (0.0, 0.0, 0.0)),
    (7, (0.0, 0.0, 0.0)),
    (8, (0.0, 0.0, 0.0)),
    (9, (0.0, 0.0, 0.0)),
    (10, (0.0, 0.0, 0.0)),
]

for area_idx, (ox, oy, oz) in AREA_PLACEMENTS:
    mf = os.path.join(BASE_C_DIR, str(area_idx), "model.inc.c")
    if not os.path.exists(mf):
        continue

    with open(mf, "r") as f:
        text = f.read()

    lights = {}
    for lm in re.finditer(r'Lights1\s+(\w+)\s*=\s*gdSPDefLights1\(([^)]+)\)', text):
        n = [int(t.strip(), 0) for t in lm.group(2).replace('\n', ' ').split(',') if t.strip()]
        d = [(v - 256 if v > 127 else v) for v in n[6:9]]
        mag = max((d[0]**2 + d[1]**2 + d[2]**2) ** 0.5, 1e-6)
        lights[lm.group(1)] = (n[0:3], n[3:6], [c / mag for c in d])
    lit_file = 'gsSPLight' in text

    vtx_arrays = {}
    for m in re.finditer(r'static const Vtx\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
        arr_name = m.group(1)
        body = m.group(2)
        verts = []
        for vm in re.finditer(r'\{\{\{\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\},\s*0,\s*\{\s*(-?\d+),\s*(-?\d+)\},\s*\{\s*([^}]+)\}\}\}', body):
            x = (float(vm.group(1)) + ox) * SCALE
            y = (float(vm.group(2)) + oy) * SCALE
            z = (float(vm.group(3)) + oz) * SCALE
            u_raw = float(vm.group(4))
            v_raw = float(vm.group(5))
            cols = [int(c.strip(), 0) for c in vm.group(6).split(',')]
            verts.append((x, y, z, u_raw, v_raw, cols[0], cols[1], cols[2]))
        vtx_arrays[arr_name] = verts

    dl_dict = {}
    root_dl = None
    for dl in re.finditer(r'(static const Gfx|const Gfx)\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
        qual, name, body = dl.group(1), dl.group(2), dl.group(3)
        dl_dict[name] = body
        if qual == "const Gfx":
            root_dl = name

    state = {
        "mat": "untextured_shade",
        "tex_on": False,
        "light": None,
        "vcache": {},
    }

    def run_dl(dl_name):
        if dl_name not in dl_dict:
            return
        for line in dl_dict[dl_name].split("\n"):
            if "gsSPTexture(" in line:
                if "G_ON" in line:
                    state["tex_on"] = True
                elif "G_OFF" in line:
                    state["tex_on"] = False
                    state["mat"] = "untextured_shade"

            ltm = re.search(r'gsDPSetTextureImage\([^,]+,\s*[^,]+,\s*[^,]+,\s*(\w+)\)', line)
            if ltm:
                state["mat"] = ltm.group(1)
                all_f_by_mat.setdefault(state["mat"], [])

            lgm = re.search(r'gsSPLight\(&(\w+)\.l,\s*1\)', line)
            if lgm:
                state["light"] = lgm.group(1)

            subm = re.search(r'gsSP(?:Display|Branch)List\((\w+)\)', line)
            if subm:
                run_dl(subm.group(1))
                continue

            active_mat = state["mat"] if state["tex_on"] else "untextured_shade"
            all_f_by_mat.setdefault(active_mat, [])
            if active_mat in copied_textures:
                _, orig_w, orig_h = copied_textures[active_mat]
            else:
                orig_w, orig_h = 32, 32

            vm = re.search(r'gsSPVertex\((\w+),\s*(\d+),\s*(\d+)\)', line)
            if vm:
                varr, count, start = vm.group(1), int(vm.group(2)), int(vm.group(3))
                if varr in vtx_arrays:
                    src_verts = vtx_arrays[varr]
                    for i in range(count):
                        if i < len(src_verts):
                            vx, vy, vz, ur, vr, cr, cg, cb = src_verts[i]
                            if lit_file and state["light"] in lights:
                                amb, dif, ldir = lights[state["light"]]
                                nx, ny, nz = [((c - 256) if c > 127 else c) / 127.0 for c in (cr, cg, cb)]
                                ndl = max(0.0, nx * ldir[0] + ny * ldir[1] + nz * ldir[2])
                                cr, cg, cb = [min(1.0, (amb[k] + dif[k] * ndl) / 255.0) for k in range(3)]
                            else:
                                cr, cg, cb = cr / 255.0, cg / 255.0, cb / 255.0
                            u_norm = (ur / 32.0) / orig_w
                            v_norm = 1.0 - ((vr / 32.0) / orig_h)
                            all_v_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f} {cr:.4f} {cg:.4f} {cb:.4f}\n")
                            all_vt_lines.append(f"vt {u_norm:.6f} {v_norm:.6f}\n")
                            state["vcache"][start + i] = len(all_v_lines)

            t1m = re.search(r'gsSP1Triangle\(\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t1m:
                i0, i1, i2 = int(t1m.group(1)), int(t1m.group(2)), int(t1m.group(3))
                vc = state["vcache"]
                if i0 in vc and i1 in vc and i2 in vc:
                    all_f_by_mat[active_mat].append(f"f {vc[i0]}/{vc[i0]} {vc[i1]}/{vc[i1]} {vc[i2]}/{vc[i2]}\n")

            t2m = re.search(r'gsSP2Triangles\(\s*(\d+),\s*(\d+),\s*(\d+),\s*[^,]+,\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t2m:
                vc = state["vcache"]
                for a, b, c in ((int(t2m.group(1)), int(t2m.group(2)), int(t2m.group(3))),
                                (int(t2m.group(4)), int(t2m.group(5)), int(t2m.group(6)))):
                    if a in vc and b in vc and c in vc:
                        all_f_by_mat[active_mat].append(f"f {vc[a]}/{vc[a]} {vc[b]}/{vc[b]} {vc[c]}/{vc[c]}\n")

    if root_dl:
        run_dl(root_dl)

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
