import bpy
import sys

objects = bpy.context.scene.collection.children[0].objects

for obj in objects:
    if obj.hide_get():
        continue
    bpy.context.view_layer.objects.active = obj
    for modifier in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=modifier.name)

bpy.ops.export_scene.gltf(filepath=sys.argv[-1],
    check_existing=False,
    use_visible=True,
    export_cameras=False,
    use_renderable=True
)
