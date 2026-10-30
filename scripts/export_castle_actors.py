import os
import re
import shutil
import subprocess

R96_ACTORS = "/home/omarchy/Projects/Render96ex/actors"
HD_ACTORS = "/home/omarchy/Projects/RENDER96-HD-TEXTURE-PACK/gfx/actors"
OUT_TEX_DIR = "/home/omarchy/Projects/pj-vibe-game/assets/textures/castle_grounds"
OUT_MODELS_DIR = "/home/omarchy/Projects/pj-vibe-game/assets/models"

os.makedirs(OUT_TEX_DIR, exist_ok=True)
os.makedirs(OUT_MODELS_DIR, exist_ok=True)

# Copy HD tree textures for runtime Y-billboard bubbly trees
for tname in ("tree_left_side.rgba16.png", "tree_right_side.rgba16.png"):
    shutil.copy2(os.path.join(HD_ACTORS, "tree", tname), os.path.join(OUT_TEX_DIR, tname))


def export_actor_to_glb(c_path, root_dls, tex_map, scale, out_name):
    with open(c_path, "r") as f:
        text = f.read()

    copied = {}
    for sym, (fname, subdir, ow, oh) in tex_map.items():
        src = os.path.join(HD_ACTORS, subdir, fname)
        dst = os.path.join(OUT_TEX_DIR, fname)
        shutil.copy2(src, dst)
        copied[sym] = (fname, ow, oh)

    obj_path = os.path.join("/tmp", f"{out_name}.obj")
    mtl_path = os.path.join("/tmp", f"{out_name}.mtl")
    glb_path = os.path.join(OUT_MODELS_DIR, f"{out_name}.glb")

    with open(mtl_path, "w") as mtl:
        mtl.write("newmtl mat_untextured_shade\nKa 1 1 1\nKd 1 1 1\nKs 0 0 0\nd 1\nillum 2\n\n")
        for sym, (fname, ow, oh) in copied.items():
            mtl.write(f"newmtl mat_{sym}\nKa 1 1 1\nKd 1 1 1\nKs 0 0 0\nd 1\nillum 2\n")
            rel_tex = os.path.relpath(os.path.join(OUT_TEX_DIR, fname), "/tmp")
            mtl.write(f"map_Kd {rel_tex}\n\n")

    lights = {}
    for lm in re.finditer(r'Lights1\s+(\w+)\s*=\s*gdSPDefLights1\(([^)]+)\)', text):
        n = [int(t.strip(), 0) for t in lm.group(2).replace('\n', ' ').split(',') if t.strip()]
        d = [(v - 256 if v > 127 else v) for v in n[6:9]]
        mag = max((d[0]**2 + d[1]**2 + d[2]**2) ** 0.5, 1e-6)
        lights[lm.group(1)] = (n[0:3], n[3:6], [c / mag for c in d])

    vtx_arrays = {}
    for m in re.finditer(r'static const Vtx\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
        verts = []
        for vm in re.finditer(r'\{\{\{\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\},\s*0,\s*\{\s*(-?\d+),\s*(-?\d+)\},\s*\{\s*([^}]+)\}\}\}', m.group(2)):
            x, y, z = float(vm.group(1)) * scale, float(vm.group(2)) * scale, float(vm.group(3)) * scale
            ur, vr = float(vm.group(4)), float(vm.group(5))
            cols = [int(c.strip(), 0) for c in vm.group(6).split(',')]
            verts.append((x, y, z, ur, vr, cols[0], cols[1], cols[2]))
        vtx_arrays[m.group(1)] = verts

    dl_dict = {}
    for dl in re.finditer(r'(?:static const Gfx|const Gfx)\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
        dl_dict[dl.group(1)] = dl.group(2)

    v_lines, vt_lines = [], []
    f_by_mat = {"untextured_shade": []}
    state = {"mat": "untextured_shade", "tex_on": False, "light": None, "vcache": {}}

    def run_dl(name):
        if name not in dl_dict:
            return
        for line in dl_dict[name].split("\n"):
            if "gsSPTexture(" in line:
                if "G_ON" in line:
                    state["tex_on"] = True
                elif "G_OFF" in line:
                    state["tex_on"] = False
                    state["mat"] = "untextured_shade"
            ltm = re.search(r'gsDPSetTextureImage\([^,]+,\s*[^,]+,\s*[^,]+,\s*(\w+)\)', line)
            if ltm:
                state["mat"] = ltm.group(1)
                f_by_mat.setdefault(state["mat"], [])
            lgm = re.search(r'gsSPLight\(&(\w+)\.l,\s*1\)', line)
            if lgm:
                state["light"] = lgm.group(1)
            subm = re.search(r'gsSP(?:Display|Branch)List\((\w+)\)', line)
            if subm:
                run_dl(subm.group(1))
                continue

            active_mat = state["mat"] if state["tex_on"] else "untextured_shade"
            f_by_mat.setdefault(active_mat, [])
            ow, oh = copied[active_mat][1:] if active_mat in copied else (32, 32)

            vm = re.search(r'gsSPVertex\((\w+),\s*(\d+),\s*(\d+)\)', line)
            if vm:
                varr, count, start = vm.group(1), int(vm.group(2)), int(vm.group(3))
                if varr in vtx_arrays:
                    for i in range(min(count, len(vtx_arrays[varr]))):
                        vx, vy, vz, ur, vr, cr, cg, cb = vtx_arrays[varr][i]
                        if state["light"] in lights:
                            amb, dif, ldir = lights[state["light"]]
                            nx, ny, nz = [((c - 256) if c > 127 else c) / 127.0 for c in (cr, cg, cb)]
                            ndl = max(0.0, nx * ldir[0] + ny * ldir[1] + nz * ldir[2])
                            cr, cg, cb = [min(1.0, (amb[k] + dif[k] * ndl) / 255.0) for k in range(3)]
                        else:
                            cr, cg, cb = cr / 255.0, cg / 255.0, cb / 255.0
                        u_norm = (ur / 32.0) / ow
                        v_norm = 1.0 - ((vr / 32.0) / oh)
                        v_lines.append(f"v {vx:.4f} {vy:.4f} {vz:.4f} {cr:.4f} {cg:.4f} {cb:.4f}\n")
                        vt_lines.append(f"vt {u_norm:.6f} {v_norm:.6f}\n")
                        state["vcache"][start + i] = len(v_lines)

            t1m = re.search(r'gsSP1Triangle\(\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t1m:
                i0, i1, i2 = int(t1m.group(1)), int(t1m.group(2)), int(t1m.group(3))
                vc = state["vcache"]
                if i0 in vc and i1 in vc and i2 in vc:
                    f_by_mat[active_mat].append(f"f {vc[i0]}/{vc[i0]} {vc[i1]}/{vc[i1]} {vc[i2]}/{vc[i2]}\n")

            t2m = re.search(r'gsSP2Triangles\(\s*(\d+),\s*(\d+),\s*(\d+),\s*[^,]+,\s*(\d+),\s*(\d+),\s*(\d+)', line)
            if t2m:
                vc = state["vcache"]
                for a, b, c in ((int(t2m.group(1)), int(t2m.group(2)), int(t2m.group(3))),
                                (int(t2m.group(4)), int(t2m.group(5)), int(t2m.group(6)))):
                    if a in vc and b in vc and c in vc:
                        f_by_mat[active_mat].append(f"f {vc[a]}/{vc[a]} {vc[b]}/{vc[b]} {vc[c]}/{vc[c]}\n")

    for rdl in root_dls:
        run_dl(rdl)

    with open(obj_path, "w") as obj:
        obj.write(f"mtllib {os.path.basename(mtl_path)}\no {out_name}\n\n")
        obj.writelines(v_lines)
        obj.writelines(vt_lines)
        for mat, faces in f_by_mat.items():
            if faces:
                obj.write(f"usemtl mat_{mat}\ns 1\n")
                obj.writelines(faces)

    bscript = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath={obj_path!r}, forward_axis='NEGATIVE_Z', up_axis='Y')
bpy.ops.export_scene.gltf(filepath={glb_path!r}, export_format='GLB', export_materials='EXPORT', export_vertex_color='ACTIVE')
"""
    subprocess.run(["blender", "-b", "--python-expr", bscript], check=True)
    print(f"Exported {glb_path} ({len(v_lines)} verts)")


# 1. Castle Front Door leaf (GEO_SCALE 0.25 * SM64_SCALE 0.01 = 0.0025) + Star Sign on both faces
export_actor_to_glb(
    os.path.join(R96_ACTORS, "door", "model.inc.c"),
    ["door_seg3_dl_03013E28", "door_seg3_dl_030142B0"],
    {
        "door_seg3_texture_03009D10": ("polished_wooden_door.rgba16.png", "door", 32, 64),
        "door_seg3_texture_0300AD10": ("polished_wooden_door_overlay.rgba16.png", "door", 32, 64),
        "door_seg3_texture_03012510": ("one_star_door_sign.rgba16.png", "door", 32, 32),
    },
    0.0025,
    "castle_door"
)

# 2. Wooden Signpost (GEO_SCALE 0.25 * SM64_SCALE 0.01 = 0.0025)
export_actor_to_glb(
    os.path.join(R96_ACTORS, "wooden_signpost", "model.inc.c"),
    ["wooden_signpost_seg3_dl_0302DA48", "wooden_signpost_seg3_dl_0302DD08"],
    {
        "wooden_signpost_seg3_texture_0302C9C8": ("wooden_signpost_back.rgba16.png", "wooden_signpost", 32, 32),
        "wooden_signpost_seg3_texture_0302D1C8": ("wooden_signpost_front.rgba16.png", "wooden_signpost", 32, 32),
    },
    0.0025,
    "wooden_signpost"
)
