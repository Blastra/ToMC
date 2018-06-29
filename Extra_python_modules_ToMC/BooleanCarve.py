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

#TODO: Add the union boolean option and the respective
#input from BGE side

def CreateAndBoolean(targName,
                     targVerts,
                     targFaces,                     
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

    #Activate edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    #(At this point a sample by CoDEmanX was used as a reference)
    #https://blenderartists.org/t/stay-in-edit-mode-when-adding-custom-primitive/569202/3

    #Generate a new object within edit mode
    ob = bpy.context.edit_object

    #Store the object's data into a local variable
    me = ob.data

    #Generate a mesh using Blender's internal bmesh module
    bm = bmesh.from_edit_mesh(me)

    #TODO: Remove repetitious code

    #A list to check whether a face has already
    #been added to the target-tool combination
    #omniFaceList = []

    

    #Create a list into which the tool faces can be stored
    toolFaceList = []

    toolVertexList = []

    

    #Iterate through the vertices in the input data
    for toolFaceNums in toolFaces:

        recToolList = []
        for toolFaceNum in toolFaceNums:
            #newToolVert = bm.verts.new((Ve(toolVerts[toolFaceNum])+Ve(toolPosition))*Eu(toolOrient,"XYZ").to_matrix())
            #newToolVert = bm.verts.new(Ve(toolVerts[toowwlFaceNum])*Eu(toolOrient,"XYZ").to_matrix()+Ve(toolPosition))
            #newToolVert = bm.verts.new((Ve(toolVerts[toolFaceNum])+Ve(toolPosition))*Eu(toolOrient,"XYZ").to_matrix())
            #newToolVert = bm.verts.new(Ve(toolVerts[toolFaceNum])*Eu(toolOrient,"XYZ").to_matrix()+Ve(toolPosition)*Eu(targOrient,"XYZ").to_matrix())
            newToolVert = bm.verts.new(Ve(toolVerts[toolFaceNum])*Eu(toolOrient,"XYZ").to_matrix().inverted()+Ve(toolPosition))
            
            recToolList.append(newToolVert)

            toolVertexList.append(newToolVert)
            
        #Form a new face now that the vertices form a connected loop

        #if recToolList not in omniFaceList:
        newToolFace = bm.faces.new(recToolList)
        #omniFaceList.append(recToolList)

        #Add the new face to the list of tool faces
        toolFaceList.append(newToolFace)

    print("toolVertexList length: "+str(len(toolVertexList)))

    

    #Merge any double vertices in the tool vertex list
    #bmesh.ops.remove_doubles(bm,verts = toolVertexList,dist = 0.00001)
    
    #Update the normals to avoid problems with collision
    #calculations
    bm.normal_update()

    #Update Blender on everything new that was set
    bmesh.update_edit_mesh(me, True, True)
    me.update()
    
    targFaceList = []

    targVertexList = []
    
    """
    
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')

    """

    #Remove vertex doubles to prevent interference with boolean
    #operations
    #bmesh.ops.remove_doubles(bm,verts = targVertexList,dist = 0.00001)
       
    
    

    #For some reason Blender takes along vertices of both tool and target
    #when storing the vertices of the tool
    
    

    
    #Cut tool reconstruction from here

    """
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')

    """

    #Remove vertex doubles to prevent interference with the boolean operation

    """
    #Deselect all target faces
    for targVert in targVertexList:
        try: 
            targVert.select = False
        except ReferenceError:
            pass
    """

    #Select each face in the tool face list
    #remainingToolFaces = []
    for toolFace in toolFaceList:
        try:
            toolFace.select = True
            #remainingToolFaces.append(toolFace)
        except ReferenceError:
            pass
    
    #bmesh.ops.reverse_faces(bm, faces=remainingToolFaces)

    bpy.ops.mesh.select_all(action="INVERT")

    bpy.ops.mesh.delete(type='FACE')


    #Iterate through the vertices in the input data

    
    
    for targFaceNums in targFaces:

        recTargList = []
        
        for targFaceNum in targFaceNums:

            #newTargVert = bm.verts.new(targVerts[targFaceNum]) #*Eu(toolOrient,"XYZ").to_matrix())
            newTargVert = bm.verts.new(Eu(targOrient,"XYZ").to_matrix()*Ve(targVerts[targFaceNum]))
            recTargList.append(newTargVert)

            targVertexList.append(newTargVert)

        #if recTargList not in omniFaceList:
            
        #Form a new face now that the vertices form a connected loop
        newTargFace = bm.faces.new(recTargList)

        #Add the new face to the list of target faces
        targFaceList.append(newTargFace)
        #omniFaceList.append(recTargList)

    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')

    """
    

    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    
    """
    
    #print(dir(toolVertex))

    for toolVertex in toolVertexList:
        try:
            toolVertex.select = True
            
            #del toolVertex
        except ReferenceError:
            pass
    
    #Update the normals to avoid problems with collision
    #calculations
    #bm.normal_update()

    #Update Blender on everything new that was set
    #bmesh.update_edit_mesh(me, True, True)
    #me.update()

    #Update the normals to avoid problems with collision
    #calculations
    bm.normal_update()

    #Update Blender on everything new that was set
    bmesh.update_edit_mesh(me, True, True)
    me.update()

    #bpy.context.scene.update()
    
    #Run the boolean operation
    bpy.ops.mesh.intersect_boolean(operation= boolType, use_swap=False, threshold=1e-06)
        
    #print("Raarpaapra "+str(laa))

    #Remove double vertices and recreate faces to iron out
    #escalating mesh bugs
    """
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent()

    bpy.ops.mesh.select_all(action='DESELECT')
    """
    #Add a remesh operation to the object to fix any breakage
 
    """
    bpy.ops.object.modifier_add(type='REMESH')
    bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
    bpy.context.object.modifiers["Remesh"].octree_depth = 5
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

    #Decimate the mesh to avoid trouble from unneeded mesh complexity
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
    """

    #Rename the object for further iterations
    bpy.data.objects[targName.replace(".blend","")].name = fiName.replace(".blend","")

    

#bpy.ops.mesh.normals_make_consistent()

#Remove the tool bmesh vertices, since they are no longer needed

#TODO: Separate into different objects by loose parts

#bpy.ops.mesh.separate(type='LOOSE')

#TODO: Copy logic bricks and game properties to the newly created loose parts

#TODO: Generate a name for each separated part

#TODO: Store each part of the shattered object as its own blend file

#TODO: Remove each loose part except for one from the scene

#fiName = os.path.split(saveName)[1].replace(".pickle",".blend")
#blendSavePath = os.path.join(objLibPath,fiName)

#Save the current open file
#bpy.ops.wm.save_as_mainfile(filepath=fiName, check_existing=False, filter_blender=True, filter_backup=False, filter_image=False, filter_movie=False, filter_python=False, filter_font=False, filter_sound=False, filter_text=False, filter_btx=False, filter_collada=False, filter_folder=True, filter_blenlib=False, filemode=8, display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', compress=False, relative_remap=True, copy=False, use_mesh_compat=False)

### TEST ENDS ###

#Finally return the object itself for further alterations 

#return obj

######## ENSURING THE INTENDED FUNCTIONALITY OF THE BOOLEAN OPERATION ENDS HERE ######

    

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
