import bpy
import sys

print("sys.argv[2:] "+str(sys.argv[0:]))

#From the list of arguments mesh vertices passed from BGE can be parsed

verts = sys.argv[5]

#From the list of arguments mesh faces passed from BGE can be parsed

faces = sys.argv[6]

#destFilePath = "/home/arad/Desktop/TestiSTLPalkki.stl"

#bpy.ops.export_mesh.stl(filepath=destFilePath,check_existing=True,axis_forward="Y",axis_up="Z",filter_glob="*.stl",use_selection=False,global_scale=1.0,use_scene_unit=False,ascii=False,use_mesh_modifiers=True,batch_mode="OFF")

bpy.ops.wm.quit_blender()
