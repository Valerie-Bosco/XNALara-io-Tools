# <pep8 compliant>

"""Blender Addon. XNALara/XPS importer/exporter."""

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "johnzero7, Valeria Bosco[Valy Arhal][4.x patch]",
    "version": (1, 0, 2, 2),
    "blender": (4, 0, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "full 4.x support is still in development",
    "category": "Import-Export",
    "tracker_url": "https://github.com/Valery-AA/XNALaraMesh-BL4_X/issues"
}


import bpy
from . import addon_updater_ops


#################################################
# ALX MODULE-AUTO-LOADER


import os
import importlib

folder_blacklist = ["__pycache__", "alxoverhaul_updater"]
file_blacklist = ["__init__.py", "addon_updater_ops", "addon_updater.py", "Extras.py", ]

addon_folders = list([__path__[0]])
addon_folders.extend( [os.path.join(__path__[0], folder_name) for folder_name in os.listdir(__path__[0]) if ( os.path.isdir( os.path.join(__path__[0], folder_name) ) ) and (folder_name not in folder_blacklist) ] )

addon_files = [[folder_path, file_name[0:-3]] for folder_path in addon_folders for file_name in os.listdir(folder_path) if (file_name not in file_blacklist) and (file_name.endswith(".py"))]

for folder_file_batch in addon_files:
    if (os.path.basename(folder_file_batch[0]) == os.path.basename(__path__[0])):
        file = folder_file_batch[1]

        if (file not in locals()):
            import_line = f"from . import {file}"
            exec(import_line)
        else:
            reload_line = f"{file} = importlib.reload({file})"
            exec(reload_line)
    
    else:
        if (os.path.basename(folder_file_batch[0]) != os.path.basename(__path__[0])):
            file = folder_file_batch[1]

            if (file not in locals()):
                import_line = f"from . {os.path.basename(folder_file_batch[0])} import {file}"
                exec(import_line)
            else:
                reload_line = f"{file} = importlib.reload({file})"
                exec(reload_line)


import inspect

class_blacklist = ["PSA_UL_SequenceList"]

bpy_class_object_list = tuple(bpy_class[1] for bpy_class in inspect.getmembers(bpy.types, inspect.isclass) if (bpy_class not in class_blacklist))
alx_class_object_list = tuple(alx_class[1] for file_batch in addon_files for alx_class in inspect.getmembers(eval(file_batch[1]), inspect.isclass) if issubclass(alx_class[1], bpy_class_object_list) and (not issubclass(alx_class[1], bpy.types.WorkSpaceTool)))

AlxClassQueue = alx_class_object_list

#################################################


from . import xps_tools


def AlxRegisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.register_class(AlxClass)
        except:
            bpy.utils.unregister_class(AlxClass)
            bpy.utils.register_class(AlxClass)
def AlxUnregisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.unregister_class(AlxClass)
        except:
            print("Can't Unregister", AlxClass)

def register():
    """Register addon classes."""
    addon_updater_ops.register(bl_info)
    AlxRegisterClassQueue()
    xps_tools.register()
    


def unregister():
    """Unregister addon classes."""
    addon_updater_ops.unregister()
    AlxUnregisterClassQueue()
    xps_tools.unregister()
    


if __name__ == "__main__":
    register()

    # call exporter
    # bpy.ops.xps_tools.export_model('INVOKE_DEFAULT')

    # call importer
    # bpy.ops.xps_tools.import_model('INVOKE_DEFAULT')
