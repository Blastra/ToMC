#Much help was found in:
#https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects

import bpy
import sys
import os
import time
import random
import pickle

for i in sys.argv:
    print("sys.argv["+str(sys.argv.index(i))+"]: "+str(i))

picklePath = os.path.join(sys.argv[6],sys.argv[7])

print("picklePath: "+str(picklePath))

#Take the target file name and target object name and open a corresponding pickle file
with open(picklePath,"rb") as handle:
    #Load the pickled contents
    loadedObj = pickle.load(handle)
    handle.close()

#print(loadedObj)

#Retrieve the vertices from the pickle file
finalVerts = loadedObj["Vertices"]

#Prepare a list to store the final faces
finalFaces = loadedObj["Faces"]

"""
#Go through the polygon strings
for fa in faces:
    #Remove the rest of the unnecessary characters and turn
    #the end result into a list
    fa = fa.replace("(","").replace(")","").replace(" ","").strip("'").split(",")

    #Turn the lists into tuples which contain integers
    finalFaces.append(tuple(map(int,fa)))
"""
#print("Final version of faces: "+str(finalFaces))

def CreateObjectOnScene(objName,objVerts,objFaces,position,orient):

    #Save name core comes from Blender as an argument
    saveNameFrame = objName

    
    #saveName = os.path.join(sys.argv[6],sys.argv[5]+".blend")

    #Add the mesh object to the scene at origin
    bpy.ops.object.add(
        type = 'MESH',
        enter_editmode=False,
        location=position)

    #Store the object in the blender scene
    #for targeting
    obj = bpy.context.object

    #Give the object its name as seen in Blender's
    #Properties window
    obj.name = saveNameFrame

    #Store the object data for targeting
    me = obj.data

    #Store the current scene to access
    #the object names
    sce = bpy.context.scene

    curObjs = []
    #Store the names of the scene's objects
    #for comparison
    for obNameIter in sce.objects:
        curObjs.append(obNameIter.name)

    #Change the name of the target mesh
    #within the scene, check that duplicate names
    #are not created

    if saveNameFrame+'Mesh' not in curObjs:
        me.name = saveNameFrame+'Mesh'        
    else:
        me.name = saveNameFrame+'AltMesh'

    #Keep the object name list up to date
    curObjs.append(me.name)

    #Apply the vertex and face data for the generation
    me.from_pydata(finalVerts, [], finalFaces)

    #Call update on the scene
    #NOTE: possibly not needed, obtained from the INFO window
    #of Blender in the first place
    me.update()

    bpy.ops.object.mode_set(mode='OBJECT')

    #Destination file path of the STL file is stored, add the STL folder to the file path and change the suffix to stl
    destFilePath = os.path.join(sys.argv[7].replace(sys.argv[6],os.path.join(sys.argv[6],"STL")).replace(".pickle",".stl"))
    
    #extra = bpy.data.objects[saveName+str(".001")]

    objs = bpy.data.objects

    #Remove the extra unaltered mesh object which is generated
    #NOTE: reason for this behavior is unknown
    if saveNameFrame+".001" in objs:
        objs.remove(objs[saveNameFrame+".001"],True)

    #Finally return the object itself for further alterations 

    return obj


#Carve target is always created at 0,0,0
def CarveBoolean(resultName,
                 carveTarget,
                 targetOrient,
                 carverTool,
                 toolPos,
                 toolOrient):
    
    #Open the modifier menu
    bpy.context.space_data.context = 'MODIFIER'

    #Create a boolean modifier to the carveTarget object
    bpy.ops.object.modifier_add(type='BOOLEAN')

    #Choose the boolean type to remove the intersecting volume of
    #carvertool from carveTarget
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'

    #Apply the role of the carverTool in the operation
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[carverTool]
    
    #Change the boolean solver to Carve
    bpy.context.object.modifiers["Boolean"].solver = 'CARVE'

    #Apply the boolean modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

    #Obtain the current scene

    #Select the carverTool object
    bpy.context.object = sce.objects

    #Remove the carverTool
    bpy.ops.object.delete(use_global=False)

    #Return the carve target object

    return carveTarget


##### RUNNING THE FUNCTIONS STARTS HERE ########

#Create the carve target object at origo
carTarg = CreateObjectOnScene(carveTarget,objVerts,objFaces,(0,0,0),orient)

#Create the carver 
carver = CreateObjectOnScene(carverTool,objVerts,objFaces,toolPos,toolOrient)

#Perform the boolean carve
carvedObject = CarveBoolean("TestCarve",carTarg,carver)

#Save the current open file
bpy.ops.wm.save_as_mainfile("TestCarveFile.blend", check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)
#bpy.ops.wm.save_as_mainfile(filepath=sys.argv[7].replace(".pickle",".blend"), check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Shut down the backround Blender
bpy.ops.wm.quit_blender()

##### RUNNING THE FUNCTIONS ENDS HERE ########


#### OLD SCRIPT STARTS HERE ######################

"""

#Save name core comes from Blender as an argument
saveNameFrame = sys.argv[5]

saveName = os.path.join(sys.argv[6],sys.argv[5]+".blend")

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
obj.name = saveNameFrame

#Store the object data for targeting
me = obj.data

me.name = saveNameFrame+'Mesh'

#Apply the vertex and face data for the generation
me.from_pydata(finalVerts, [], finalFaces)

#Call update on the scene
#NOTE: possibly not needed, obtained from the INFO window
#of Blender in the first place
me.update()

bpy.ops.object.mode_set(mode='OBJECT')

#Destination file path of the STL file is stored, add the STL folder to the file path and change the suffix to stl
destFilePath = os.path.join(sys.argv[7].replace(sys.argv[6],os.path.join(sys.argv[6],"STL")).replace(".pickle",".stl"))

scene = bpy.context.scene

#extra = bpy.data.objects[saveName+str(".001")]

objs = bpy.data.objects

#Remove the extra unaltered mesh object which is generated
#NOTE: reason for this behavior is unknown
if saveNameFrame+".001" in objs:
    objs.remove(objs[saveNameFrame+".001"],True)

#Save the blend file
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[7].replace(".pickle",".blend"), check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Save the STL file
#bpy.ops.export_mesh.stl(filepath=destFilePath,check_existing=True,axis_forward="Y",axis_up="Z",filter_glob="*.stl",use_selection=False,global_scale=1.0,use_scene_unit=False,ascii=False,use_mesh_modifiers=True,batch_mode="OFF")

#Shut down the backround blender
bpy.ops.wm.quit_blender()

"""
