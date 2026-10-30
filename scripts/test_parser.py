import re, os

filepath = "/home/omarchy/Projects/Render96ex/levels/castle_grounds/areas/1/1/model.inc.c"
with open(filepath, 'r') as f:
    text = f.read()

# 1. Parse vertex arrays
# static const Vtx array_name[] = { ... };
vtx_arrays = {}
for m in re.finditer(r'static const Vtx\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL):
    arr_name = m.group(1)
    body = m.group(2)
    verts = []
    # {{{ x, y, z }, 0, { u, v }, { r, g, b, a }}}
    for vm in re.finditer(r'\{\{\{\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\},\s*0,\s*\{\s*(-?\d+),\s*(-?\d+)\},\s*\{\s*([^}]+)\}\}\}', body):
        x = float(vm.group(1))
        y = float(vm.group(2))
        z = float(vm.group(3))
        u = float(vm.group(4))
        v = float(vm.group(5))
        verts.append((x, y, z, u, v))
    vtx_arrays[arr_name] = verts

print(f"Parsed {len(vtx_arrays)} vertex arrays from 1/model.inc.c.")

# 2. Parse display lists and triangles
# Each sub-DL has:
# gsDPSetTextureImage(..., texture_name)
# gsSPVertex(array_name, count, start_index)
# gsSP1Triangle(v0, v1, v2, 0x0)
# gsSP2Triangles(v0, v1, v2, 0x0, v3, v4, v5, 0x0)

dl_matches = list(re.finditer(r'static const Gfx\s+(\w+)\s*\[\]\s*=\s*\{([^;]+)\};', text, re.DOTALL))
print(f"Parsed {len(dl_matches)} sub display lists.")

current_tex = "default"
total_tris = 0
for dl in dl_matches:
    dl_name = dl.group(1)
    dl_body = dl.group(2)
    
    # Check texture
    tex_m = re.search(r'gsDPSetTextureImage\([^,]+,\s*[^,]+,\s*[^,]+,\s*(\w+)\)', dl_body)
    if tex_m:
        current_tex = tex_m.group(1)
        
    vcache = {}
    lines = dl_body.split('\n')
    for line in lines:
        vm = re.search(r'gsSPVertex\((\w+),\s*(\d+),\s*(\d+)\)', line)
        if vm:
            varr = vm.group(1)
            count = int(vm.group(2))
            start = int(vm.group(3))
            if varr in vtx_arrays:
                src_verts = vtx_arrays[varr]
                for i in range(count):
                    if i < len(src_verts):
                        vcache[start + i] = src_verts[i]
        
        t1m = re.search(r'gsSP1Triangle\(\s*(\d+),\s*(\d+),\s*(\d+)', line)
        if t1m:
            total_tris += 1
            
        t2m = re.search(r'gsSP2Triangles\(\s*(\d+),\s*(\d+),\s*(\d+),\s*[^,]+,\s*(\d+),\s*(\d+),\s*(\d+)', line)
        if t2m:
            total_tris += 2

print(f"Total triangles resolved in 1/model.inc.c: {total_tris}")
