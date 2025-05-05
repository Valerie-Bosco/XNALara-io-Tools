import bpy

from . import xps_tools
from .modules.addon_updater_system import addon_updater
from .modules.module_manager import Alx_Module_Manager

bl_info = {
    "name": "XNALara-io-Tools",
    "author": "Valerie Bosco[Valy Arhal], johnzero7[Original Developer]",
    "description": "Import-Export for XNALara/XPS files",
    "version": (1, 2, 0),
    "blender": (3, 6, 0),
    "category": "Import-Export",
    "location": "File > Import-Export > XNALara/XPS",
    "doc_url": "https://github.com/Valerie-Bosco/XNALara-io-Tools/wiki",
    "tracker_url": "https://github.com/Valerie-Bosco/XNALara-io-Tools/issues",
}


module_manager = Alx_Module_Manager(
    path=__path__,
    globals=globals()
)
addon_updater = addon_updater.Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    engine="Github",
    engine_user_name="Valerie-Bosco",
    engine_repo_name="XNALara-io-Tools",
    manual_download_website="https://github.com/Valerie-Bosco/XNALara-io-Tools/releases/tag/main_branch_latest"
)


def register():
    module_manager.developer_register_modules(True)
    addon_updater.register_addon_updater(True)

    xps_tools.register()


def unregister():
    module_manager.developer_unregister_modules()
    addon_updater.unregister_addon_updater()

    xps_tools.unregister()


if __name__ == "__main__":
    register()
