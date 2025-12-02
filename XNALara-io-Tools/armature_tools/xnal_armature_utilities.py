from typing import Iterable

import bpy

from ..XPS_Constants import BLENDER_VERSION
from ..utilities.color_utilities import random_color_rgb

xnal_model_bone_names = []


def Xnal_CreateArmatureObject(name="Armature"):
    armature_da = bpy.data.armatures.new(name)
    armature_da.display_type = 'STICK'
    armature_obj = bpy.data.objects.new(name, armature_da)
    return armature_obj


def XnaL_AddRegisterBoneName(name: str):
    xnal_model_bone_names.append(name)


def XNA_SET_BoneVisibility(
        armature_object: bpy.types.Object,
        bone: Iterable[str],
        visibility_target=["ALL"],
        visibility: bool = False
):
    """
    visibility_target: ["ALL"] \n
        ALL:      [Object | Edit | Pose] modes\n
        OBJECT:   Object mode
        EDIT:     Edit mode
        POSE:     Pose mode
    """

    if (armature_object is not None) or (len(bone) > 0):

        _bones = set()

        match visibility_target:
            case "OBJECT":
                _bones = {
                    armature_object.data.bones[bone_name]
                    for bone_name in bone
                    if (bone_name in armature_object.data.bones.keys())
                }
            case "EDIT":
                _bones = {
                    armature_object.data.edit_bones[bone_name]
                    for bone_name in bone
                    if (bone_name in armature_object.data.edit_bones.keys())
                }
            case "POSE":
                if BLENDER_VERSION >= 50:
                    _bones = {
                        armature_object.pose.bones[bone_name]
                        for bone_name in bone
                        if (bone_name in armature_object.pose.bones.keys())
                    }
                else:
                    _bones = {
                        armature_object.data.bones[bone_name]
                        for bone_name in bone
                        if (bone_name in armature_object.data.bones.keys())
                    }
            case _:
                for name in bone:
                    if name in armature_object.data.bones.keys():
                        _bones.add(armature_object.data.bones[name])

                    if name in armature_object.data.edit_bones.keys():
                        _bones.add(armature_object.data.edit_bones[name])

                    if name in armature_object.pose.bones.keys():
                        _bones.add(armature_object.pose.bones[name])

        for bone in _bones:
            match type(bone):
                case bpy.types.Bone:
                    bone.hide = visibility
                case bpy.types.EditBone:
                    bone.hide = visibility
                case bpy.types.PoseBone:
                    if BLENDER_VERSION >= 50:
                        bone.hide = visibility


def XnaL_GetBoneNameByIndex(index: int):
    try:
        return xnal_model_bone_names[index]
    except Exception as error:
        print(error)
        return None


def XnaL_CreateBoneCollection(armature_object: bpy.types.Object, mesh_object: bpy.types.Object):
    armature: bpy.types.Armature = armature_object.data
    pose_bone_normal_color = random_color_rgb()
    pose_bone_select_color = random_color_rgb()
    pose_bone_active_color = random_color_rgb()

    if (BLENDER_VERSION <= 36):
        bone_group = armature.pose.bone_groups.new(name=mesh_object.name)
        bone_group.color_set = "CUSTOM"
        bone_group.colors.normal = pose_bone_normal_color
        bone_group.colors.select = pose_bone_select_color
        bone_group.colors.active = pose_bone_active_color

        for bone_vertex_group_name in mesh_object.vertex_groups.keys():
            pose_bone = armature.pose.bones.get(bone_vertex_group_name)

            if (pose_bone is not None):
                pose_bone.bone_group = bone_group

    elif (BLENDER_VERSION >= 40):
        bone_collection = armature.collections.new(name=mesh_object.name)

        for bone_vertex_group_name in mesh_object.vertex_groups.keys():
            pose_bone = armature_object.pose.bones.get(bone_vertex_group_name)

            if (pose_bone is not None):
                bone_collection.assign(pose_bone)
                pose_bone.color.palette = "CUSTOM"
                pose_bone.color.custom.normal = pose_bone_normal_color
                pose_bone.color.custom.select = pose_bone_select_color
                pose_bone.color.custom.active = pose_bone_active_color
