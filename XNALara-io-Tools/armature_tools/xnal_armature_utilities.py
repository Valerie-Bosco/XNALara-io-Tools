from typing import Iterable

import bpy

xnal_model_bone_names = []


def Xnal_CreateArmatureObject(name="Armature"):
    armature_da = bpy.data.armatures.new(name)
    armature_da.display_type = 'STICK'
    armature_obj = bpy.data.objects.new(name, armature_da)
    return armature_obj


def XnaL_AddRegisterBoneName(name: str):
    xnal_model_bone_names.append(name)


def XnaL_ShowHideBones(bones: Iterable[bpy.types.Bone], visibility: bool):
    try:
        bones[0]
        for bone in bones:
            bone.hide = visibility
    except:
        pass


def XnaL_GetBoneNameByIndex(original_index: int):
    try:
        return xnal_model_bone_names[original_index]
    except:
        return None


def XnaL_CreateBoneCollection(armature_object: bpy.types.Object, mesh_object: bpy.types.Object):
    armature: bpy.types.Armature = armature_object.data

    bone_collection = armature.collections.new(name=mesh_object.name)

    for bone_vertex_group_name in mesh_object.vertex_groups.keys():
        bone_collection.assign(armature_object.pose.bones.get(bone_vertex_group_name))
