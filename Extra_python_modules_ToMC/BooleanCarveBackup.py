#Much help was found in:
#https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects

import bpy
import sys
import os
import time
import random
import pickle


"""
#Go through the polygon strings
for fa in faces:
    #Remove the rest of the unnecessary characters and turn
    #the end result into a list
    fa = fa.replace("(","").replace(")","").replace(" ","").strip("'").split(",")

    #Turn the lists into tuples which contain integers
    finalFaces.append(tuple(map(int,fa)))
"""

def CreateObjectOnScene(objName,objVerts,objFaces,position,orient):

    print("objName: "+str(objName))
    print("objVerts: "+str(objVerts))
    print("objFaces: "+str(objFaces))
    print("position: "+str(position))
    print("orient: "+str(orient))


    #Save name core comes from Blender as an argument
    saveNameFrame = objName

    

    #Add the mesh object to the scene at origin
    bpy.ops.object.add(
        type = 'MESH',
        enter_editmode=False,
        location=position)

    #TODO: Rotate the target mesh accordingly
    
    #Store the object in the blender scene
    #for targeting
    obj = bpy.context.object

    #Give the object its name as seen in Blender's
    #Properties window
    obj.name = os.path.split(saveNameFrame)[-1].replace(".blend","")

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
        me.name = os.path.split(saveNameFrame)[-1].replace(".blend","")+'Mesh'        
    else:
        me.name = os.path.split(saveNameFrame)[-1].replace(".blend","")+'AltMesh'

    #Keep the object name list up to date
    curObjs.append(me.name)

    #Apply the vertex and face data for the generation
    me.from_pydata(objVerts, [], objFaces)

    #Call update on the scene
    #NOTE: possibly not needed, obtained from the INFO window
    #of Blender in the first place
    me.update()

    bpy.ops.object.mode_set(mode='OBJECT')

    #Destination file path of the object library folder to the file path and change the suffix to blend
    #destFilePath = os.path.join(objName.replace(".pickle",".blend"))
    
    #extra = bpy.data.objects[saveName+str(".001")]

    objs = bpy.data.objects

    #Select the modified mesh version
    bpy.data.objects[obj.name].select = True

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
    if obj.name+".001" in bpy.data.objects:

        """

        ###TEST COPY REMOVAL BEGINS HERE###

        #Select the object's unmodified duplicate
        #which contains all of the game logic
        objs[obj.name+".001"].select = False
        objs[obj.name].select = True
        objs[obj.name+".001"].select = True

        #Copy game properties
        #TODO: Copy all properties instead of only ObjID
        bpy.ops.object.game_property_copy(property='ObjID')

        #Copy the logic bricks from the .001 copy to the final object
        bpy.ops.object.logic_bricks_copy()

        #Deselect all objects
        bpy.context.scene.objects.active = None
        bpy.ops.object.select_all(action='TOGGLE')
        
        ###TEST COPY REMOVAL ENDS HERE###

        """

        #Select the object's unmodified duplicate
        #which contains all of the game logic
        objs[obj.name+".001"].select = True
        
        bpy.context.scene.objects.active = bpy.data.objects[obj.name+".001"]

        #Copy game properties
        #TODO: Copy all properties instead of only ObjID
        bpy.ops.object.game_property_copy(property='ObjID')
    
        #Copy the logic bricks from the .001 copy to the final object
        bpy.ops.object.logic_bricks_copy()

        #Remove the extra unaltered mesh object which is generated
        #NOTE: reason for this behavior is unknown

        objs[obj.name+".001"].select = False

        #if obj.name+".001" in objs:
        objs.remove(objs[obj.name+".001"],True)

    #Finally return the object itself for further alterations 

    return obj


#Carve target is always created at 0,0,0
def CarveBoolean(resultName,
                 carveTarget,
                 targetOrient,
                 carverTool,
                 toolPos,
                 toolOrient):

    #NOTE: Two objects of the same type cause errors due
    #to removal of extra copies
    cTar = bpy.data.objects[0]
    cTool = bpy.data.objects[1]

    #Causes tool to 
    cTool.rotation_euler = toolOrient

    ######## ENSURING THE INTENDED FUNCTIONALITY OF THE BOOLEAN OPERATION BEGINS HERE ######
        
    #Select the carve target as active
    carveTarget.select = True    

    #Activate edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    #Convert all mesh faces to triangles
    bpy.ops.mesh.quads_convert_to_tris()

    #Activate vertex selection
    bpy.ops.mesh.select_mode(type="VERT")

    #Select all faces of the carve target mesh
    bpy.ops.mesh.select_all(action='TOGGLE')

    #Recalculate normals of the carve target
    bpy.ops.mesh.normals_make_consistent()

    #Deactivate edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #Select the carve tool
    carverTool.select = True
    carveTarget.select = False

    #Activate edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")

    #Select all faces of the carve target mesh
    bpy.ops.mesh.select_all(action='TOGGLE')
    
    #Recalculate normals of the carve tool
    bpy.ops.mesh.normals_make_consistent()  

    #Deactivate edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #Select both objects
    carveTarget.select = True
    carverTool.select = True           

    ######## ENSURING THE INTENDED FUNCTIONALITY OF THE BOOLEAN OPERATION ENDS HERE ######
    
    #Create a new boolean modifier named Boolean
    carvBool = cTar.modifiers.new("Boolean","BOOLEAN")

    #Choose the boolean type to remove the intersecting volume of
    #carvertool from carveTarget
    
    carvBool.operation = 'DIFFERENCE'
    
    #Apply the role of the carverTool in the operation
    carvBool.object = cTool #str(carveTool)
        
    #Change the boolean solver to Carve    
    carvBool.solver = 'CARVE'

    #Explicitly select the carveTarget for applying the boolean modifier
    bpy.context.scene.objects.active = carveTarget

    #carverTool.select = False
    #carveTarget.select = True

    #Apply the boolean modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
    #carvBool.modifier_apply(apply_as='DATA', modifier="Boolean")

    #Setup rigid body physics
    bpy.context.object.game.physics_type = 'RIGID_BODY'

    #Activate collision bounds
    bpy.context.object.game.use_collision_bounds = True

    #Use triangle mesh
    bpy.context.object.game.collision_bounds_type = 'TRIANGLE_MESH'
    
    print("Applied boolean modified with carveTarget at "+str(carveTarget.location)+" and carve tool at "+str(carverTool.location))

    #Select the carverTool object    
    carverTool.select = True

    #Deselect carve target
    carveTarget.select = False

    #Remove the carverTool
    bpy.ops.object.delete(use_global=False)

    

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

#Retrieve the vertices and faces of the tool object from the pickle file
toolVerts = loadedObj["toolVerts"]
toolFaces = loadedObj["toolFaces"]

#Retrieve the orientation of the target object and the carve tool object
targOrient = loadedObj["targetOrientation"]
toolOrient = loadedObj["toolOrientation"]

#print("TOOL ORIENTATION: "+str(toolOrient))

toolPos = loadedObj["toolDistance"]

#Locally store the arguments according to the input given by BooleanCarve.py

#Create the carve target object at origo
carTarg = CreateObjectOnScene(tarObjPath,targVerts,targFaces,(0,0,0),targOrient)
#carTarg = CreateObjectOnScene(sys.argv[5],targVerts,targFaces,(0,0,0),targOrient)

#Create the carver
carver = CreateObjectOnScene(toolPath,toolVerts,toolFaces,toolPos,toolOrient)
#carver = CreateObjectOnScene(sys.argv[6],toolVerts,toolFaces,(0.5,0,0),toolOrient)


carvedObject = CarveBoolean(saveName,
                            carTarg,
                            targOrient,
                            carver,
                            toolPos,
                            toolOrient)

fiName = os.path.split(saveName)[1].replace(".pickle",".blend")
blendSavePath = os.path.join(objLibPath,fiName)

#Save the current open file
bpy.ops.wm.save_as_mainfile(filepath=blendSavePath, check_existing=True, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

#Remove the pickle file from ObjectLibrary
#os.remove(picklePath)

#Shut down the backround Blender
bpy.ops.wm.quit_blender()

#Communicate to BGE that the carved object is ready to be imported

##### RUNNING THE FUNCTIONS ENDS HERE ########
