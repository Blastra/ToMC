#Much help was found in:
#https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects

import bpy
import sys
import os
import time
import random

for i in sys.argv:
    print("sys.argv["+str(sys.argv.index(i))+"]: "+str(i))

#From the list of arguments mesh vertices passed from BGE can be parsed

#Split the input string containing vertices
#into the tuples in string form, the result is a
#list of strings in which the first and last item
#have extra parentheses
verts = sys.argv[5].strip("[]").split("), (")

#Prepare a list to contain the cleaned-up tuples
finalVerts = []

#Go through the items in the verts list 
for ve in verts:
    #Turn the strings into lists without parentheses
    ve = ve.replace(" ","").replace("'","").strip("(").strip(")").split(",")

    #Turn the lists into tuples which contain floats
    finalVerts.append(tuple(map(float,ve)))

#print("Final version of verts: "+str(finalVerts))

#From the list of arguments mesh faces passed from BGE can be parsed

#Remove brackets and split the string into a list
faces = sys.argv[6].strip("[]").split("), (")

#Prepare a list to store the final faces
finalFaces = []

#Go through the polygon strings
for fa in faces:
    #Remove the rest of the unnecessary characters and turn
    #the end result into a list
    fa = fa.replace("(","").replace(")","").replace(" ","").strip("'").split(",")

    #Turn the lists into tuples which contain integers
    finalFaces.append(tuple(map(int,fa)))

#print("Final version of faces: "+str(finalFaces))

#Save name core comes from Blender as an argument
saveNameFrame = sys.argv[7]

#TODO: Obtain the name from the input command + year,month,day,hour,minute,second+random from 10000
saveName = saveNameFrame+str(time.localtime().tm_year)+str(time.localtime().tm_yday)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)+str(random.randint(1,9999))

#Add the mesh object to the scene at origin
bpy.ops.object.add(
    type = 'MESH',
    enter_editmode=False,
    location=(0,0,0))

#Store the object in the blender scene
#for targeting
obj = bpy.context.object

#Give the object its name as seen in Blender's
#Properties window
obj.name = saveName

#Store the object data for targeting
me = obj.data

me.name = saveName+'Mesh'

#Apply the vertex and face data for the generation
me.from_pydata(finalVerts, [], finalFaces)

#Call update on the scene
#NOTE: possibly not needed, obtained from the INFO window
#of Blender in the first place
me.update()

bpy.ops.object.mode_set(mode='OBJECT')

#Destination file path of the STL file is stored
destFilePath = os.path.join(sys.argv[9],saveName+".stl")

scene = bpy.context.scene

print("Presumed blend file storage path: "+str(sys.argv[8]))

print("Presumed stl file storage path: "+str(sys.argv[9]))

"""
#extra = bpy.data.objects[saveName+str(".001")]

objs = bpy.data.objects

objs.remove(objs[saveNameFrame+".001"],True)

#Save the blend file
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(sys.argv[8],saveName+".blend"), check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Save the STL file
bpy.ops.export_mesh.stl(filepath=destFilePath,check_existing=True,axis_forward="Y",axis_up="Z",filter_glob="*.stl",use_selection=False,global_scale=1.0,use_scene_unit=False,ascii=False,use_mesh_modifiers=True,batch_mode="OFF")

#Shut down the backround blender
bpy.ops.wm.quit_blender()
"""

