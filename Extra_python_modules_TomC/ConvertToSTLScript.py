import bpy

destFilePath = "/home/arad/Desktop/TestiSTLPalkki.stl"

bpy.ops.export_mesh.stl(filepath=destFilePath,check_existing=True,axis_forward="Y",axis_up="Z",filter_glob="*.stl",use_selection=False,global_scale=1.0,use_scene_unit=False,ascii=False,use_mesh_modifiers=True,batch_mode="OFF")

bpy.ops.wm.quit_blender()
