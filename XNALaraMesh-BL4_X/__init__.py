bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "Valeria Bosco[Valy Arhal], johnzero7[Original Developer]",
    "version": (1, 0, 3),
    "blender": (4, 0, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "full 4.x support is still in development",
    "category": "Import-Export",
}

#region ModuleAutoloader
import importlib
from os import sep as os_separator
from pathlib import Path

import bpy

from . import addon_updater_ops


folder_name_blacklist: list[str]=["__pycache__"] 
file_name_blacklist: list[str]=["__init__.py"]
file_name_blacklist.extend(["addon_updater", "addon_updater_ops"])


addon_folders = []
addon_files = []

addon_path_iter = [ Path( __path__[0] ) ]
addon_path_iter.extend(Path( __path__[0] ).iterdir())

for folder_path in addon_path_iter:
    
    
    if ( folder_path.is_dir() ) and ( folder_path.exists() ) and ( folder_path.name not in folder_name_blacklist ):
        addon_folders.append( folder_path )

        for subfolder_path in folder_path.iterdir():
            if ( subfolder_path.is_dir() ) and ( subfolder_path.exists()):
                addon_path_iter.append( subfolder_path )
                addon_folders.append( subfolder_path )

addon_files = [[folder_path, file_name.name[0:-3]] for folder_path in addon_folders for file_name in folder_path.iterdir() if ( file_name.is_file() ) and ( file_name.name not in file_name_blacklist ) and ( file_name.suffix == ".py" )]

for folder_file_batch in addon_files:
    file = folder_file_batch[1]
    
    if (file not in locals()):
        relative_path = str(folder_file_batch[0].relative_to( __path__[0] ) ).replace(os_separator,"." )

        import_line = f"from . {relative_path if relative_path != '.' else ''} import {file}"
        exec(import_line)
    else:
        reload_line = f"{file} = importlib.reload({file})"
        exec(reload_line)

import inspect
alx_class_object_list = tuple(alx_class[1] for file_batch in addon_files for alx_class in inspect.getmembers(eval(file_batch[1]), inspect.isclass) )

AlxClassQueue = alx_class_object_list
#endregion


from . import xps_tools


def AlxRegisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.register_class(AlxClass)
        except Exception as error:
            print(error)
            try:
                bpy.utils.unregister_class(AlxClass)
                bpy.utils.register_class(AlxClass)
            except Exception as error:
                print(error)

def AlxUnregisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.unregister_class(AlxClass)
        except:
            print("Can't Unregister", AlxClass)


def register():
    addon_updater_ops.update_path_fix = __path__
    addon_updater_ops.register(bl_info)

    AlxRegisterClassQueue()
    xps_tools.register()

def unregister():
    addon_updater_ops.unregister()

    AlxUnregisterClassQueue()
    xps_tools.unregister()
    
if __name__ == "__main__":
    register()