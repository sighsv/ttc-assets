import bpy
import sys

bpy.ops.export_scene.gltf(filepath=sys.argv[-1],
    check_existing=False,
    use_visible=True,
    export_cameras=False, 
    use_renderable=True
)
