import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Importar el modelo descomprimido de Tripo3D
input_glb = '/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_tripo_decompressed.glb'
bpy.ops.import_scene.gltf(filepath=input_glb)

mesh_objs = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if not mesh_objs:
    raise RuntimeError("No se encontro ningun objeto MESH en el GLB importado.")

bukele_bust = mesh_objs[0]
bukele_bust.name = "BukeleHeroBust"

bpy.ops.object.select_all(action='DESELECT')
bukele_bust.select_set(True)
bpy.context.view_layer.objects.active = bukele_bust

# Centrar pivote geométricamente
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bukele_bust.location = (0, 0, 0)
bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

# Escala normalizada (1.6 unidades de alto)
current_height = bukele_bust.dimensions.z
if current_height > 0:
    target_scale = 1.6 / current_height
    bukele_bust.scale = (target_scale, target_scale, target_scale)
    bpy.ops.object.transform_apply(scale=True)

# Decimación suave a 65,000 polígonos para preservar detalles finos de sonrisa y ojos
poly_count = len(bukele_bust.data.polygons)
if poly_count > 70000:
    decimate_ratio = 65000 / poly_count
    mod = bukele_bust.modifiers.new(name="DecimateSmooth", type='DECIMATE')
    mod.ratio = decimate_ratio
    bpy.ops.object.modifier_apply(modifier="DecimateSmooth")

# IMPORTANTE: APLICAR SMOOTH SHADING TOTAL PARA ELIMINAR FACETAS
bpy.ops.object.shade_smooth()
bukele_bust.data.polygons.foreach_set('use_smooth', [True] * len(bukele_bust.data.polygons))

# Configuración de Material PBR Cálido
for mat_slot in bukele_bust.material_slots:
    if mat_slot.material and mat_slot.material.use_nodes:
        bsdf = mat_slot.material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Piel suave natural, no plástico brillante
            bsdf.inputs['Roughness'].default_value = 0.55
            bsdf.inputs['Metallic'].default_value = 0.0

# -----------------------------------------------------------------------------
# EXPORTACIÓN GLB
# -----------------------------------------------------------------------------
output_glb = "/home/omarchy/Projects/pj-vibe-game/assets/models/bukele_head.glb"
bpy.ops.object.select_all(action='DESELECT')
bukele_bust.select_set(True)
bpy.context.view_layer.objects.active = bukele_bust

bpy.ops.export_scene.gltf(
    filepath=output_glb,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_image_format='AUTO'
)
print(f"[EXITO] bukele_head.glb generado: {output_glb} ({os.path.getsize(output_glb)} bytes)")
