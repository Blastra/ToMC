
#STL-tiedoston generoinnin info alkaa tästä

#The command to start a blender instance
#just add "-b" to the list to run it in the backround
#and 

taustaBlender = subprocess.Popen(["blender"])

#Template for the Python command which must be run inside blender to export
#the current blender scene as an stl file:

bpy.ops.export_mesh.stl(filepath="/home/blastra/Desktop/TestiSTLPutkilo.stl",
                       check_existing=True,
                       axis_forward='Y',
                       axis_up='Z',
                       filter_glob="*.stl",
                       use_selection=False,
                       global_scale=1.0,
                       use_scene_unit=False,
                       ascii=False,
                       use_mesh_modifiers=True,
                       batch_mode='OFF')

taustaBlender.kill()
print("Finished")

#Ainakin Linuxilla toimiva komentorimpsu
blender -b /home/blastra/ModifyTargetBlend.blend --python-expr 'import bpy; bpy.ops.export_mesh.stl(filepath="/home/blastra/Desktop/TestiSTLPalkki.stl",check_existing=True,axis_forward="Y",axis_up="Z",filter_glob="*.stl",use_selection=False,global_scale=1.0,use_scene_unit=False,ascii=False,use_mesh_modifiers=True,batch_mode="OFF"); bpy.ops.wm.quit_blender();'

#STL-tiedoston generoinnin info päättyy tähän


#Blend-tiedoston generoinnin info alkaa tästä

#http://blender.stackexchange.com/questions/2407/how-to-create-a-mesh-programmatically-without-bmesh

import bpy  

verts = [
    (-0.285437,-0.744976,-0.471429),
    (-0.285437,-0.744976,-2.471429),
    (1.714563,-0.744976,-2.471429),
    (1.714563,-0.744976,-0.471429),
    (-0.285437,1.255024,-0.471429),
    (-0.285437,1.255024,-2.471429),
    (1.714563,1.255024,-2.471429),
    (1.714563,1.255024,-0.471429)
]

faces =  [
    (4,5,1), (5,6,2), (6,7,3), (4,0,7),
    (0,1,2), (7,6,5), (0,4,1), (1,5,2),
    (2,6,3), (7,0,3), (3,0,2), (4,7,5)
]

mesh_data = bpy.data.meshes.new("cube_mesh_data")
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()

obj = bpy.data.objects.new("My_Object", mesh_data)

scene = bpy.context.scene
scene.objects.link(obj)
obj.select = True

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

bpy.ops.wm.save_as_mainfile(filepath="/home/blastra/Desktop/DataGeneroituPalikka.blend", check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Blend-tiedoston generoinnin info päättyy tähän
