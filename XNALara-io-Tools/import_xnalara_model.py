import copy
import operator
import os
import re

import bpy
from mathutils import Vector

from . import (import_xnalara_pose, material_creator, read_ascii_xps,
               read_bin_xps, xps_types)
from .armature_tools.xnal_armature_utilities import (XnaL_AddRegisterBoneName,
                                                     Xnal_CreateArmatureObject,
                                                     XnaL_CreateBoneCollection,
                                                     XnaL_GetBoneNameByIndex,
                                                     XnaL_ShowHideBones)

# imported XPS directory
rootDir = ''
MIN_BONE_LENGHT = 0.005


def coordTransform(coords):
    x, y, z = coords
    z = -z
    return (x, z, y)


def faceTransform(face):
    return [face[0], face[2], face[1]]


def faceTransformList(faces):
    return map(faceTransform, faces)


def uvTransform(uv):
    u = uv[0] + xpsSettings.uvDisplX
    v = 1 + xpsSettings.uvDisplY - uv[1]
    return [u, v]


def rangeFloatToByte(float):
    return int(float * 255) % 256


def rangeByteToFloat(byte):
    return byte / 255


def uvTransformLayers(uvLayers):
    return list(map(uvTransform, uvLayers))


# profile
def getInputFilename(xpsSettingsAux):
    global xpsSettings
    xpsSettings = xpsSettingsAux

    blenderImportSetup()
    status = xpsImport()
    blenderImportFinalize()
    return status


def blenderImportSetup():
    # switch to object mode and deselect all
    objectMode()
    bpy.ops.object.select_all(action='DESELECT')


def blenderImportFinalize():
    # switch to object mode
    objectMode()


def objectMode():
    current_mode = bpy.context.mode
    if bpy.context.view_layer.objects.active and current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def loadXpsFile(filename):
    dirpath, file = os.path.split(filename)
    basename, ext = os.path.splitext(file)
    if ext.lower() in ('.mesh', '.xps'):
        xpsData = read_bin_xps.readXpsModel(filename)
    elif ext.lower() in ('.ascii'):
        xpsData = read_ascii_xps.readXpsModel(filename)
    else:
        xpsData = None

    return xpsData


def makeMesh(meshFullName):
    mesh_data = bpy.data.meshes.new(meshFullName)
    mesh_object = bpy.data.objects.new(mesh_data.name, mesh_data)
    print(f"Created Mesh: {meshFullName}")
    print(f"New Mesh = {mesh_data.name}")
    # bpy.context.scene.update()
    # mesh_da.update()
    return mesh_object


def linkToCollection(collection, obj):
    # Link Object to collection
    collection.objects.link(obj)


def xpsImport():
    global rootDir
    global xpsData

    print("------------------------------------------------------------")
    print("---------------EXECUTING XPS PYTHON IMPORTER----------------")
    print("------------------------------------------------------------")
    print("Importing file: ", xpsSettings.filename)

    rootDir, file = os.path.split(xpsSettings.filename)
    print('rootDir: {}'.format(rootDir))

    xpsData = loadXpsFile(xpsSettings.filename)
    if not xpsData:
        return '{NONE}'

    # Create New Collection
    fname, fext = os.path.splitext(file)
    import_target_collection = bpy.data.collections.new(fname)
    view_layer = bpy.context.view_layer
    scene_collection = view_layer.layer_collection
    scene_collection.children.link(import_target_collection)
    optional_objects_collection = bpy.data.collections.new(f"{fname} | OPTIONAL")
    import_target_collection.children.link(optional_objects_collection)

    # imports the armature
    armature_object = Xnal_CreateArmatureObject()
    if armature_object is not None:
        linkToCollection(import_target_collection, armature_object)
        XnaL_ImportModelBones(bpy.context, armature_object)
        armature_object.select_set(True)

    # imports all the meshes
    meshes_obs = importMeshesList(armature_object)

    if (xpsSettings.separate_optional_objects):
        for mesh_object in meshes_obs:
            object_name = re.split(r"[1234567890]+_", mesh_object.name, 1)[1]
            if (object_name[0] in ["+", "-"]):
                if ("|" in mesh_object.name):
                    optional_collection_name = re.split(r"(\|)(?!.*\1)", object_name[1:])[0]
                    if (optional_collection_name not in bpy.data.collections.keys()):
                        op_col = bpy.data.collections.new(optional_collection_name)
                        optional_objects_collection.children.link(op_col)

                    linkToCollection(bpy.data.collections[optional_collection_name], mesh_object)
                else:
                    linkToCollection(optional_objects_collection, mesh_object)
            linkToCollection(import_target_collection, mesh_object)
            mesh_object.select_set(True)
    else:
        for mesh_object in meshes_obs:
            linkToCollection(import_target_collection, mesh_object)
            mesh_object.select_set(True)

    if armature_object:
        armature_object.pose.use_auto_ik = xpsSettings.autoIk
        hideUnusedBones([armature_object])
        # set tail to Children Middle Point
        boneTailMiddleObject(armature_object, xpsSettings.connectBones)

    # Import default pose
    if (xpsSettings.importDefaultPose and armature_object):
        if (xpsData.header and xpsData.header.pose):
            import_xnalara_pose.setXpsPose(armature_object, xpsData.header.pose)
    return '{FINISHED}'


def setMinimumLenght(bone):
    default_length = MIN_BONE_LENGHT
    if bone.length == 0:
        bone.tail = bone.head - Vector((0, .001, 0))
    if bone.length < default_length:
        bone.length = default_length


def boneTailMiddleObject(armature_ob, connectBones):
    bpy.context.view_layer.objects.active = armature_ob

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    editBones = armature_ob.data.edit_bones
    boneTailMiddle(editBones, connectBones)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def setBoneConnect(connectBones):
    currMode = bpy.context.mode
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    editBones = bpy.context.view_layer.objects.active.data.edit_bones
    connectEditBones(editBones, connectBones)
    bpy.ops.object.mode_set(mode=currMode, toggle=False)


def connectEditBones(editBones, connectBones):
    for bone in editBones:
        if bone.parent:
            if bone.head == bone.parent.tail:
                bone.use_connect = connectBones


def hideBonesByName(armature_objs):
    """Hide bones that do not affect any mesh."""
    for armature in armature_objs:
        for bone in armature.data.bones:
            if bone.name.lower().startswith('unused'):
                XnaL_ShowHideBones([bone], False)


def hideBonesByVertexGroup(armature_objs):
    """Hide bones that do not affect any mesh."""
    for armature in armature_objs:
        objs = [obj for obj in armature.children
                if obj.type == 'MESH' and obj.modifiers and [
                    modif for modif in obj.modifiers if modif
                    and modif.type == 'ARMATURE' and modif.object == armature]]

        # cycle objects and get all vertex groups
        vertexgroups = set(
            [vg.name for obj in objs if obj.type == 'MESH'
                for vg in obj.vertex_groups])

        bones = armature.data.bones
        # leafBones = [bone for bone in bones if not bone.children]
        rootBones = [bone for bone in bones if not bone.parent]

        for bone in rootBones:
            recurBones(bone, vertexgroups, '')


def recurBones(bone, vertexgroups, name):
    visibleChild = False
    for childBone in bone.children:
        aux = recurBones(childBone, vertexgroups, '{} '.format(name))
        visibleChild = visibleChild or aux

    visibleChain = bone.name in vertexgroups or visibleChild
    if not visibleChain:
        XnaL_ShowHideBones([bone], False)
    return visibleChain


def hideUnusedBones(armature_objs):
    hideBonesByVertexGroup(armature_objs)
    hideBonesByName(armature_objs)


def boneDictRename(filepath, armatureObj):
    boneDictDataRename, boneDictDataRestore = read_ascii_xps.readBoneDict(filepath)
    renameBonesUsingDict(armatureObj, boneDictDataRename)


def boneDictRestore(filepath, armatureObj):
    boneDictDataRename, boneDictDataRestore = read_ascii_xps.readBoneDict(filepath)
    renameBonesUsingDict(armatureObj, boneDictDataRestore)


def renameBonesUsingDict(armatureObj, boneDict):
    getbone = armatureObj.data.bones.get
    for key, value in boneDict.items():
        boneRenamed = getbone(import_xnalara_pose.renameBoneToBlender(key))
        if boneRenamed:
            boneRenamed.name = value
        else:
            boneOriginal = getbone(key)
            if boneOriginal:
                boneOriginal.name = value


def XnaL_ImportModelBones(context: bpy.types.Context, armature_object: bpy.types.Object):
    xps_bones = xpsData.bones

    if (armature_object is not None) and (armature_object.data is not None) and (armature_object.type == "ARMATURE"):
        armature: bpy.types.Armature = armature_object.data

        context.view_layer.objects.active = armature_object
        bpy.ops.object.mode_set(mode='EDIT')

        xps_bone: xps_types.XpsBone
        for xps_bone in xps_bones:
            editBone = armature.edit_bones.new(xps_bone.name)
            XnaL_AddRegisterBoneName(editBone.name)

            transformedBone = coordTransform(xps_bone.co)
            editBone.head = Vector(transformedBone)
            editBone.tail = Vector(editBone.head) + Vector((0, 0, -.1))
            setMinimumLenght(editBone)

        for xps_bone in xps_bones:
            editBone: bpy.types.EditBone = armature.edit_bones[xps_bone.id]
            editBone.parent = armature.edit_bones[xps_bone.parentId]

        context.view_layer.objects.active = armature_object
        bpy.ops.object.mode_set(mode='OBJECT')
    return armature_object


def boneTailMiddle(editBones, connectBones):
    """Move bone tail to children middle point."""
    twistboneRegex = r'\b(hip)?(twist|ctr|root|adj)\d*\b'
    for bone in editBones:
        if (bone.name.lower() == "root ground" or not bone.parent):
            bone.tail = bone.head.xyz + Vector((0, -.5, 0))
        # elif (bone.name.lower() == "root hips"):
        #    bone.tail = bone.head.xyz + Vector((0, .2, 0))
        else:
            childBones = [childBone for childBone in bone.children
                          if not (re.search(twistboneRegex, childBone.name))]

            if childBones:
                # Set tail to children middle
                bone.tail = Vector(map(sum, zip(*(childBone.head.xyz for childBone in childBones)))) / len(childBones)
            else:
                # if no child, set tail acording to parent
                if bone.parent is not None:
                    if bone.head.xyz != bone.parent.tail.xyz:
                        # Tail to diference between bone and parent
                        delta = bone.head.xyz - bone.parent.tail.xyz
                    else:
                        # Tail to same lenght/direction than parent
                        delta = bone.parent.tail.xyz - bone.parent.head.xyz
                    bone.tail = bone.head.xyz + delta

    # Set minimum bone length
    for bone in editBones:
        setMinimumLenght(bone)

    # Connect Bones to parent
    connectEditBones(editBones, connectBones)


def makeUvs(mesh_da, faces, uvData, vertColors):
    # Create UVLayers
    for i in range(len(uvData[0])):
        mesh_da.uv_layers.new(name="UV{}".format(str(i + 1)))
    if xpsSettings.vColors:
        mesh_da.vertex_colors.new()

    # Assign UVCoords
    for faceId, face in enumerate(faces):
        for vertId, faceVert in enumerate(face):
            loopdId = (faceId * 3) + vertId
            if xpsSettings.vColors:
                mesh_da.vertex_colors[0].data[loopdId].color = vertColors[faceVert]
            for layerIdx, uvLayer in enumerate(mesh_da.uv_layers):
                uvCoor = uvData[faceVert][layerIdx]
                uvLayer.data[loopdId].uv = Vector(uvCoor)


def createJoinedMeshes():
    meshPartRegex = re.compile(r'(!.*)*([\d]+nPart)*!')
    sortedMeshesList = sorted(xpsData.meshes, key=operator.attrgetter('name'))
    joinedMeshesNames = list(
        {meshPartRegex.sub('', mesh.name, 0) for mesh in sortedMeshesList})
    joinedMeshesNames.sort()
    newMeshes = []
    for joinedMeshName in joinedMeshesNames:
        # for each joinedMeshName generate a list of meshes to join
        meshesToJoin = [mesh for mesh in sortedMeshesList if meshPartRegex.sub(
            '', mesh.name, 0) == joinedMeshName]

        totalVertexCount = 0
        vertexCount = 0
        meshCount = 0

        meshName = None
        textures = None
        vertex = None
        faces = None

        # new name for the unified mesh
        meshName = meshPartRegex.sub('', meshesToJoin[0].name, 0)
        # all the meshses share the same textures
        textures = meshesToJoin[0].textures
        # all the meshses share the uv layers count
        uvCount = meshesToJoin[0].uvCount
        # all the new joined mesh names
        vertex = []
        faces = []
        for mesh in meshesToJoin:
            vertexCount = 0
            meshCount = meshCount + 1

            if len(meshesToJoin) > 1 or meshesToJoin[0] not in sortedMeshesList:
                # unify vertex
                for vert in mesh.vertices:
                    vertexCount = vertexCount + 1
                    newVertice = xps_types.XpsVertex(
                        vert.id + totalVertexCount, vert.co, vert.norm, vert.vColor, vert.uv, vert.boneWeights)
                    vertex.append(newVertice)
                # unify faces
                for face in mesh.faces:
                    newFace = [face[0] + totalVertexCount, face[1]
                               + totalVertexCount, face[2] + totalVertexCount]
                    faces.append(newFace)
            else:
                vertex = mesh.vertices
                faces = mesh.faces
            totalVertexCount = totalVertexCount + vertexCount

        # Creates the nuw unified mesh
        xpsMesh = xps_types.XpsMesh(meshName, textures, vertex, faces, uvCount)
        newMeshes.append(xpsMesh)
    return newMeshes


def importMeshesList(armature_ob):
    if xpsSettings.joinMeshParts:
        newMeshes = createJoinedMeshes()
    else:
        newMeshes = xpsData.meshes
    importedMeshes = [importMesh(armature_ob, meshInfo)
                      for meshInfo in newMeshes]
    return [mesh for mesh in importedMeshes if mesh]


def generateVertexKey(vertex):
    if xpsSettings.joinMeshRips:
        key = str(vertex.co) + str(vertex.norm)
    else:
        key = str(vertex.id) + str(vertex.co) + str(vertex.norm)
    return key


def getVertexId(vertex, mapVertexKeys, mergedVertList):
    vertexKey = generateVertexKey(vertex)
    vertexID = mapVertexKeys.get(vertexKey)
    if vertexID is None:
        vertexID = len(mergedVertList)
        mapVertexKeys[vertexKey] = vertexID
        newVert = copy.copy(vertex)
        newVert.id = vertexID
        mergedVertList.append(newVert)
    else:
        mergedVertList[vertexID].merged = True
    return vertexID


def makeVertexDict(vertexDict, mergedVertList, uvLayers, vertColor, vertices):
    mapVertexKeys = {}
    uvLayerAppend = uvLayers.append
    vertColorAppend = vertColor.append
    vertexDictAppend = vertexDict.append

    for vertex in vertices:
        vColor = vertex.vColor
        uvLayerAppend(list(map(uvTransform, vertex.uv)))
        vertColorAppend(list(map(rangeByteToFloat, vColor)))
        vertexID = getVertexId(vertex, mapVertexKeys, mergedVertList)
        # old ID to new ID
        vertexDictAppend(vertexID)


def importMesh(armature_object, meshInfo):
    # boneCount = len(xpsData.bones)
    useSeams = xpsSettings.markSeams
    # Create Mesh
    meshFullName = meshInfo.name
    print()
    print('---*** Importing Mesh {} ***---'.format(meshFullName))

    # Load UV Layers Count
    uvLayerCount = meshInfo.uvCount
    print('UV Layer Count: {}'.format(str(uvLayerCount)))

    # Load Textures Count
    textureCount = len(meshInfo.textures)
    print('Texture Count: {}'.format(str(textureCount)))

    mesh_object = None
    vertCount = len(meshInfo.vertices)
    if vertCount >= 3:
        vertexDict = []
        mergedVertList = []
        uvLayers = []
        vertColors = []
        makeVertexDict(vertexDict, mergedVertList, uvLayers, vertColors, meshInfo.vertices)

        # new ID to riginal ID
        vertexOrig = [[] for x in range(len(mergedVertList))]
        for vertId, vert in enumerate(vertexDict):
            vertexOrig[vert].append(vertId)

        mergedVertices = {}
        seamEdgesDict = {}
        facesData = []
        for face in meshInfo.faces:
            v1Old = face[0]
            v2Old = face[1]
            v3Old = face[2]
            v1New = vertexDict[v1Old]
            v2New = vertexDict[v2Old]
            v3New = vertexDict[v3Old]
            oldFace = ((v1Old, v2Old, v3Old))
            facesData.append((v1New, v2New, v3New))

            if (useSeams):
                if (mergedVertList[v1New].merged
                        or mergedVertList[v2New].merged
                        or mergedVertList[v3New].merged):

                    findMergedEdges(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace)

        # merge Vertices of same coord and normal?
        mergeByNormal = True
        if mergeByNormal:
            vertices = mergedVertList
            facesList = facesData
        else:
            vertices = meshInfo.vertices
            facesList = meshInfo.faces

        # Create Mesh
        mesh_object = makeMesh(meshFullName)
        mesh_da: bpy.types.Mesh = mesh_object.data

        coords = []
        normals = []
        # vrtxList = []
        # nbVrtx = []

        for vertex in vertices:
            unitnormal = Vector(vertex.norm).normalized()
            coords.append(coordTransform(vertex.co))
            normals.append(coordTransform(unitnormal))
            # vertColors.append(vertex.vColor)
            # uvLayers.append(uvTransformLayers(vertex.uv))

        # Create Faces
        faces = list(faceTransformList(facesList))
        mesh_da.from_pydata(coords, [], faces)
        mesh_da.polygons.foreach_set(
            "use_smooth", [True] * len(mesh_da.polygons))

        # speedup!!!!
        if xpsSettings.markSeams:
            markSeams(mesh_da, seamEdgesDict)

        # Make UVLayers
        origFaces = faceTransformList(meshInfo.faces)
        makeUvs(mesh_da, origFaces, uvLayers, vertColors)

        if (xpsData.header):
            flags = xpsData.header.flags
        else:
            flags = read_bin_xps.flagsDefault()

        # Make Material
        material_creator.makeMaterial(xpsSettings, rootDir, mesh_da, meshInfo, flags)

        if (armature_object is not None) and (mesh_object is not None):
            setArmatureModifier(armature_object, mesh_object)
            setParent(armature_object, mesh_object)

        makeVertexGroups(mesh_object, vertices)

        if (armature_object is not None) and (mesh_object is not None):
            XnaL_CreateBoneCollection(armature_object, mesh_object)

        # import custom normals
        verts_nor = xpsSettings.importNormals
        use_edges = True
        # unique_smooth_groups = True

        if verts_nor:
            meshCorrected = mesh_da.validate(clean_customdata=False)  # *Very* important to not remove nors!
            mesh_da.update(calc_edges=use_edges)
            mesh_da.normals_split_custom_set_from_vertices(normals)
            if (bpy.app.version[:2] in [(4, 0), (3, 6), (3, 3)]):
                mesh_da.use_auto_smooth = True
        else:
            meshCorrected = mesh_da.validate()

        print("Geometry Corrected:", meshCorrected)

    return mesh_object


def markSeams(mesh_da, seamEdgesDict):
    # use Dict to speedup search
    edge_keys = {val: index for index, val in enumerate(mesh_da.edge_keys)}
    # mesh_da.show_edge_seams = True
    for vert1, list in seamEdgesDict.items():
        for vert2 in list:
            edgeIdx = None
            if vert1 < vert2:
                edgeIdx = edge_keys[(vert1, vert2)]
            elif vert2 < vert1:
                edgeIdx = edge_keys[(vert2, vert1)]
            if edgeIdx:
                mesh_da.edges[edgeIdx].use_seam = True


def findMergedEdges(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace):
    findMergedVert(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace, oldFace[0])
    findMergedVert(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace, oldFace[1])
    findMergedVert(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace, oldFace[2])


def findMergedVert(seamEdgesDict, vertexDict, mergedVertList, mergedVertices, oldFace, mergedVert):
    v1Old = oldFace[0]
    v2Old = oldFace[1]
    v3Old = oldFace[2]
    # v1New = vertexDict[v1Old]
    # v2New = vertexDict[v2Old]
    # v3New = vertexDict[v3Old]
    vertX = vertexDict[mergedVert]
    if (mergedVertList[vertX].merged):
        # List Merged vertices original Create
        if (mergedVertices.get(vertX) is None):
            mergedVertices[vertX] = []

        # List Merged vertices original Loop
        for facesList in mergedVertices[vertX]:
            # Check if original vertices merge

            i = 0
            matchV1 = False
            while not matchV1 and i < 3:
                if ((vertX == vertexDict[facesList[i]]) and mergedVert != facesList[i]):
                    if (mergedVert != v1Old):
                        checkEdgePairForSeam(i, seamEdgesDict, vertexDict, vertX, v1Old, facesList)
                    if (mergedVert != v2Old):
                        checkEdgePairForSeam(i, seamEdgesDict, vertexDict, vertX, v2Old, facesList)
                    if (mergedVert != v3Old):
                        checkEdgePairForSeam(i, seamEdgesDict, vertexDict, vertX, v3Old, facesList)
                    matchV1 = True
                i = i + 1

        # List Merged vertices original Append
        mergedVertices[vertX].append((v1Old, v2Old, v3Old))


def checkEdgePairForSeam(i, seamEdgesDict, vertexDict, mergedVert, vert, facesList):
    if (i != 0):
        makeSeamEdgeDict(0, seamEdgesDict, vertexDict, mergedVert, vert, facesList)
    if (i != 1):
        makeSeamEdgeDict(1, seamEdgesDict, vertexDict, mergedVert, vert, facesList)
    if (i != 2):
        makeSeamEdgeDict(2, seamEdgesDict, vertexDict, mergedVert, vert, facesList)


def makeSeamEdgeDict(i, seamEdgesDict, vertexDict, mergedVert, vert, facesList):
    if (vertexDict[vert] == vertexDict[facesList[i]]):
        if (seamEdgesDict.get(mergedVert) is None):
            seamEdgesDict[mergedVert] = []
        seamEdgesDict[mergedVert].append(vertexDict[vert])


def setArmatureModifier(armature_ob, mesh_ob):
    mod = mesh_ob.modifiers.new(type="ARMATURE", name="Armature")
    mod.use_vertex_groups = True
    mod.object = armature_ob


def setParent(armature_ob, mesh_ob):
    mesh_ob.parent = armature_ob


def makeVertexGroups(mesh_ob, vertices):
    """Make vertex groups and assign weights."""
    # blender limits vertexGroupNames to 63 chars
    # armatures = [mesh_ob.find_armature()]
    armatures = mesh_ob.find_armature()
    for vertex in vertices:
        assignVertexGroup(vertex, armatures, mesh_ob)


def assignVertexGroup(vert, armature, mesh_ob):
    for i in range(len(vert.boneWeights)):
        vertBoneWeight = vert.boneWeights[i]
        boneIdx = vertBoneWeight.id
        vertexWeight = vertBoneWeight.weight
        if vertexWeight != 0:
            # use original index to get current bone name in blender
            boneName = XnaL_GetBoneNameByIndex(boneIdx)
            if boneName:
                vertGroup = mesh_ob.vertex_groups.get(boneName)
                if not vertGroup:
                    vertGroup = mesh_ob.vertex_groups.new(name=boneName)
                vertGroup.add([vert.id], vertexWeight, 'REPLACE')


if __name__ == "__main__":

    readfilename = r'C:\XPS Tutorial\Yaiba MOMIJIII\momi3.mesh.mesh'
    uvDisplX = 0
    uvDisplY = 0
    impDefPose = True
    joinMeshRips = True
    joinMeshParts = True
    vColors = True
    connectBones = True
    autoIk = True
    importNormals = True
    separate_optional_objects = True

    xpsSettings = xps_types.XpsImportSettings(
        readfilename, uvDisplX, uvDisplY, impDefPose, joinMeshRips,
        markSeams, vColors,
        joinMeshParts, connectBones, autoIk, importNormals, separate_optional_objects)
    getInputFilename(xpsSettings)
