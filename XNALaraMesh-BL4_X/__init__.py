import importlib
from .Alx_module_manager import (
    Alx_Module_Manager
)


from . import xps_tools
from . import addon_updater_ops

bl_info = {
    "name": "XNALara/XPS Import/Export",
    "author": "Valeria Bosco[Valy Arhal], johnzero7[Original Developer]",
    "version": (1, 0, 5),
    "blender": (4, 0, 0),
    "location": "File > Import-Export > XNALara/XPS",
    "description": "Import-Export XNALara/XPS",
    "warning": "full 4.x support is still in development",
    "category": "Import-Export",
}

module_loader = Alx_Module_Manager(__path__, globals())


def register():
    addon_updater_ops.update_path_fix = __path__
    addon_updater_ops.register(bl_info)

    module_loader.developer_register_modules()
    xps_tools.register()


def unregister():
    addon_updater_ops.unregister()

    module_loader.developer_unregister_modules()
    xps_tools.unregister()


if __name__ == "__main__":
    register()
