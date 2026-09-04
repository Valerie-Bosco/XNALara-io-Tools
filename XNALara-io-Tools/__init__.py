from . import xps_tools
from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdater import Alx_Addon_Updater
from .modules.ALXModuleManager.ALXModuleManager.module_manager import (
    ALXModuleManager,
    SET_module_manager,
)

bl_info = {
    "name": "XNALara-io-Tools",
    "author": "Valerie Bosco[Valy Arhal], johnzero7[Original Developer]",
    "description": "Import-Export for XNALara/XPS files",
    "version": (1, 3, 8),
    "blender": (3, 6, 0),
    "category": "Import-Export",
    "location": "File > Import-Export > XNALara/XPS",
    "doc_url": "https://github.com/Valerie-Bosco/XNALara-io-Tools/wiki",
    "tracker_url": "https://github.com/Valerie-Bosco/XNALara-io-Tools/issues",
}

ALX_module_manager = ALXModuleManager(path=__path__, bl_info=bl_info, mute=False)
SET_module_manager(ALX_module_manager)

addon_updater = Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    engine="Github",
    engine_user_name="Valerie-Bosco",
    engine_repo_name="XNALara-io-Tools",
    manual_download_website="https://github.com/Valerie-Bosco/XNALara-io-Tools/releases/tag/main_branch_latest",
)


def register():
    ALX_module_manager.register_modules()
    addon_updater.register_addon_updater(mute=True)

    xps_tools.register()


def unregister():
    ALX_module_manager.unregister_modules()
    addon_updater.unregister_addon_updater()

    xps_tools.unregister()


if __name__ == "__main__":
    register()
