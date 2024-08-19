from typing import Iterable

import bpy

xnal_model_bone_names = []

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