import random
from typing import Iterable

import bpy
import utilities

from ..utilities.color_utilities import random_color_rgb

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
    pose_bone_normal_color = random_color_rgb()
    pose_bone_select_color = random_color_rgb()
    pose_bone_active_color = random_color_rgb()

    if (bpy.app.version[0:2] in [(3, 6)]):
        bone_group = armature.pose.bone_groups.new(name=mesh_object.name)
        bone_group.color_set = "CUSTOM"
        bone_group.colors.normal = pose_bone_normal_color
        bone_group.colors.select = pose_bone_select_color
        bone_group.colors.active = pose_bone_active_color

        for bone_vertex_group_name in mesh_object.vertex_groups.keys():
            armature.pose.bones.get(bone_vertex_group_name).bone_group = bone_group

    if (bpy.app.version[0:2] in [(4, 0), (4, 2), (4, 3), (4, 4)]):
        bone_collection = armature.collections.new(name=mesh_object.name)

        for bone_vertex_group_name in mesh_object.vertex_groups.keys():
            pose_bone = armature_object.pose.bones.get(bone_vertex_group_name)
            bone_collection.assign(pose_bone)
            pose_bone.color.palette = "CUSTOM"
            pose_bone.color.custom.normal = pose_bone_normal_color
            pose_bone.color.custom.select = pose_bone_select_color
            pose_bone.color.custom.active = pose_bone_active_color
