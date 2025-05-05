import bpy

from . import xps_tools
from .modules.addon_updater_system import addon_updater, addon_updater_ui
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

ADDON_NAME = __package__


class XNAlaraMesh4X_AddonPreferences(bpy.types.AddonPreferences):

    bl_idname = __package__

    # auto_check_update: bpy.props.BoolProperty(name="Auto-check for Update", description="If enabled, auto-check for updates using an interval", default=False)  # type:ignore

    # updater_interval_months: bpy.props.IntProperty(name='Months', description="Number of months between checking for updates", default=0, min=0)  # type:ignore
    # updater_interval_days: bpy.props.IntProperty(name='Days', description="Number of days between checking for updates", default=7, min=0, max=31)  # type:ignore
    # updater_interval_hours: bpy.props.IntProperty(name='Hours', description="Number of hours between checking for updates", default=0, min=0, max=23)  # type:ignore
    # updater_interval_minutes: bpy.props.IntProperty(name='Minutes', description="Number of minutes between checking for updates", default=0, min=0, max=59)  # type:ignore

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        layout.label(text="TEST")

        # addon_updater_ui.update_settings_ui(context, layout)


module_manager = Alx_Module_Manager(
    path=__path__,
    globals=globals()
)
addon_updater = addon_updater.Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    addon_name=ADDON_NAME,
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
