#Much help was found in:
#https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects

import bpy
import sys
import os
import time
import random
import pickle
import bmesh
from mathutils import Vector as Ve
from mathutils import Euler as Eu

bpy.ops.wm.addon_enable(module="object_boolean_tools")

#TODO: Add the union boolean option and the respective
#input from BGE side

def CreateAndBoolean(targName,
                     targVerts,
                     targFaces,
                     targPosition,
                     targOrient,
                     toolName,
                     toolVerts,
                     toolFaces,
                     toolPosition,
                     toolOrient,
                     boolType,
                     fiName):

    #Save name core comes from Blender as an argument
    saveNameFrame = targName

    #GENERATE THE CARVE TARGET FROM PYDATA

    #Add the mesh object to the scene at origin
    bpy.ops.object.add(
        type = 'MESH',
        enter_editmode=False,
        location=Ve(targPosition))     #position)

    #TODO: Rotate the target mesh accordingly
    
    #Store the object in the blender scene
    #for targeting
    carTargObj = bpy.context.object

    #Give the object its name as seen in Blender's
    #Properties window
    carTargObj.name = os.path.split(saveNameFrame)[-1].replace(".blend","")

    carTargName = str(carTargObj.name)
    

    #Store the object data for targeting
    me = carTargObj.data

    #Activate rigid body physics and apply collisions to the
    #object's visual shape

    bpy.data.objects[carTargObj.name].game.physics_type = "RIGID_BODY"
    bpy.data.objects[carTargObj.name].game.use_collision_bounds = True
    bpy.data.objects[carTargObj.name].game.collision_bounds_type = 'TRIANGLE_MESH'
    
    #TODO: Give the object the first material available in the blend file
    

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

    #if saveNameFrame+'Mesh' not in curObjs:
    if saveNameFrame not in curObjs:    
        me.name = os.path.split(saveNameFrame)[-1].replace(".blend","")
    else:
        me.name = os.path.split(saveNameFrame)[-1].replace(".blend","")+'AltMesh'

    #Keep the object name list up to date
    curObjs.append(me.name)

    #Apply the vertex and face data for the generation
    me.from_pydata(targVerts, [], targFaces)

    #Call update on the scene
    #NOTE: possibly not needed, obtained from the INFO window
    #of Blender in the first place
    me.update()

    bpy.ops.object.mode_set(mode='OBJECT')

    objs = bpy.data.objects

    #Select the modified mesh version
    bpy.data.objects[carTargObj.name].select = True

    #Activate edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    #Remove vertex duplicates
    bpy.ops.mesh.remove_doubles()

    #Convert all mesh faces to triangles
    bpy.ops.mesh.quads_convert_to_tris()    

    #Recalculate the normals of the mesh
    bpy.ops.mesh.normals_make_consistent()

    #Deactivate edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #If the object in question is the carve target, it's on the scene first
    if carTargObj.name+".001" in bpy.data.objects:
        
        #Select the object's unmodified duplicate
        #which contains all of the game logic
        objs[carTargObj.name+".001"].select = True
        
        bpy.context.scene.objects.active = bpy.data.objects[carTargObj.name+".001"]

        #Copy game properties
        #TODO: Copy all properties instead of only ObjID
        bpy.ops.object.game_property_copy(property='ObjID')
    
        #Copy the logic bricks from the .001 copy to the final object
        bpy.ops.object.logic_bricks_copy()

        #Remove the extra unaltered mesh object which is generated
        #NOTE: reason for this behavior is unknown

        objs[carTargObj.name+".001"].select = False

        #if obj.name+".001" in objs:
        objs.remove(objs[carTargObj.name+".001"],True)

    #Rotate the carve target

    carTargObj.rotation_euler = targOrient
    """
    ### GENERATING THE TOOL STARTS HERE
    
    #Add the mesh object to the scene at origin
    bpy.ops.object.add(
        type = 'MESH',
        enter_editmode=False,
        location= Ve(toolPosition))

    #TODO: Rotate the target mesh accordingly
    
    #Store the object in the blender scene
    #for targeting
    obj = bpy.context.object

    #Give the object its name as seen in Blender's
    #Properties window
    obj.name = "CarveTool&"

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

    if 'CarveTool&MeshMesh' not in curObjs:
        me.name = 'CarveTool&Mesh'
    else:
        me.name = 'CarveTool&MeshAltMesh'

    #Keep the object name list up to date
    curObjs.append(me.name)

    #Apply the vertex and face data for the generation
    me.from_pydata(toolVerts, [], toolFaces)

    obj.rotation_euler = toolOrient

    #Call update on the scene
    #NOTE: possibly not needed, obtained from the INFO window
    #of Blender in the first place
    me.update()

    #Remove doubles from the carve tool

    #Activate edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.select_all(action='DESELECT')

    #Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    #Remove vertex duplicates
    bpy.ops.mesh.remove_doubles()

    #Convert all mesh faces to triangles
    bpy.ops.mesh.quads_convert_to_tris()    

    #Recalculate the normals of the mesh
    bpy.ops.mesh.normals_make_consistent()

    #Deactivate edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    obj.rotation_euler = toolOrient

    #obj.location = toolPosition
    
    ### GENERATING THE TOOL ENDS HERE

    #Select the carve target

    objs["CarveTool&"].select = True
    """
    objs[carTargName].select = True

    bpy.context.scene.objects.active = objs[carTargName]
    
    #Move the carve tool to its correct position and orientation

    #Use the bool tool carve

    #bpy.ops.btool.auto_difference(solver='CARVE')

    #Return to edit mode, select all vertices and recalculate
    #normals after the carving operation is finished

    bpy.ops.object.mode_set(mode='EDIT')

    #NOTE: At this point the newly generated faces
    #are selected
    
    bpy.ops.mesh.select_all(action='DESELECT')

    #Select all faces
    bpy.ops.mesh.select_all(action='SELECT')

    #Remove edges with no length and faces with no area
    bpy.ops.mesh.dissolve_degenerate()

    #Remove vertex duplicates
    bpy.ops.mesh.remove_doubles()

    #Convert all mesh faces to triangles
    bpy.ops.mesh.quads_convert_to_tris()    

    #Recalculate the normals of the mesh
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')

    #Remesh and decimate
    
    bpy.ops.object.modifier_add(type='REMESH')
    bpy.context.object.modifiers["Remesh"].octree_depth = 7    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.data.objects[carTargName].modifiers["Decimate"].decimate_type = 'DISSOLVE'
    
    bpy.context.object.modifiers["Decimate"].angle_limit = 0.149066
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.mesh.select_all(action='DESELECT')

    #Select all faces
    bpy.ops.mesh.select_all(action='SELECT')

    #Remove vertex doubles and recalculate normals
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.object.mode_set(mode='OBJECT')

########## INPUT VALUE REFERENCE STARTS ############

"""
0: gD["blenderPath"],           #path to blender
1: str(tarFilePath),            #Full file path of the pickle file
                                #(verts, faces)
2: "-b",                        #backround mode of Blender
3: "--python",                  #Use Python to drive Blender
4: str(scriptPath),             #Full path of the Python script to run
5: str(carveTarget.name),       #Name of the carve target
6: str(carveTool.name),         #Name of the carving tool
7: str(gD['ObjLibraryFolder']), #Full path of the storage folder
8: saveName]                    #Name of the save file

"""

boolType = 'DIFFERENCE'

########### INPUT VALUE REFERENCE ENDS ##############



##### RUNNING THE FUNCTIONS STARTS HERE ########

carveTarName = os.path.split(str(sys.argv[5]))[-1]
carveToolName = os.path.split(str(sys.argv[6]))[-1]

objLibPath = str(sys.argv[7])
saveName = str(sys.argv[8])

print("objLibPath + saveName: "+str(objLibPath+saveName))

tarObjPath = os.path.join(objLibPath,carveTarName+".blend")
toolPath = os.path.join(objLibPath,carveToolName+".blend")

#for i in sys.argv:
#    print("sys.argv["+str(sys.argv.index(i))+"]: "+str(i))

picklePath = os.path.join(str(sys.argv[7]),"GeneratedPickles",str(sys.argv[8]))
#picklePath = sys.argv[8]


print("picklePath: "+str(picklePath))

#Take the target file name and target object name and open a corresponding pickle file
with open(picklePath,"rb") as handle:
    #Load the pickled contents
    loadedObj = pickle.load(handle)
    handle.close()

#print(loadedObj)

#Retrieve the vertices and faces of the target object from the pickle file
targVerts = loadedObj["targVerts"]
targFaces = loadedObj["targFaces"]

#targVerts = []
#targFaces = []


#Retrieve the vertices and faces of the tool object from the pickle file
toolVerts = loadedObj["toolVerts"]
toolFaces = loadedObj["toolFaces"]

#Retrieve the orientation of the target object and the carve tool object
targPos = loadedObj["targetPosition"]
targOrient = loadedObj["targetOrientation"]
toolOrient = loadedObj["toolOrientation"]

#print("TOOL ORIENTATION: "+str(toolOrient))

toolPos = loadedObj["toolDistance"]


#Locally store the arguments according to the input given by BooleanCarve.py

fiName = os.path.split(saveName)[1].replace(".pickle",".blend")
blendSavePath = os.path.join(objLibPath,fiName)

CreateAndBoolean(carveTarName,
                 targVerts,
                 targFaces,
                 targPos,
                 targOrient,
                 carveToolName,
                 toolVerts,
                 toolFaces,
                 toolPos,
                 toolOrient,
                 boolType,
                 fiName)

#Save the current open file
bpy.ops.wm.save_as_mainfile(filepath=blendSavePath, check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Remove the pickle file from ObjectLibrary
#os.remove(picklePath)

#Shut down the backround Blender
bpy.ops.wm.quit_blender()

#Communicate to BGE that the carved object is ready to be imported

##### RUNNING THE FUNCTIONS ENDS HERE ########
