import bpy
import os

obj_path = "/home/omarchy/Projects/pj-vibe-game/assets/models/castle_grounds.obj"
glb_path = "/home/omarchy/Projects/pj-vibe-game/assets/models/castle_grounds.glb"

# Clear all objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ
bpy.ops.wm.obj_import(filepath=obj_path)

# Verify objects
objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
print(f"Imported {len(objs)} mesh objects.")

# Adjust materials for optimal WebGL PBR rendering
for mat in bpy.data.materials:
    if mat.use_nodes:
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Roughness'].default_value = 0.65
            bsdf.inputs['Metallic'].default_value = 0.0

# Export GLB with embedded textures
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=False,
    export_materials='EXPORT',
    export_image_format='AUTO',
    export_vertex_color='ACTIVE'
)

print(f"GLB Exported successfully to: {glb_path}")
