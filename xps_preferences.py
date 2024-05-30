import bpy
from . import addon_updater_ops

class XNAlaraMesh4X_AddonPreferences(bpy.types.AddonPreferences):
    """Updater Class."""

    bl_idname = __package__

    auto_check_update : bpy.props.BoolProperty(name="Auto-check for Update", description="If enabled, auto-check for updates using an interval", default=False) #type:ignore

    updater_interval_months : bpy.props.IntProperty(name='Months', description="Number of months between checking for updates", default=0, min=0) #type:ignore
    updater_interval_days : bpy.props.IntProperty(name='Days', description="Number of days between checking for updates", default=7, min=0, max=31) #type:ignore
    updater_interval_hours : bpy.props.IntProperty(name='Hours', description="Number of hours between checking for updates", default=0, min=0, max=23) #type:ignore
    updater_interval_minutes : bpy.props.IntProperty(name='Minutes', description="Number of minutes between checking for updates", default=0, min=0, max=59) #type:ignore


    def draw(self, context):
        """Draw Method."""
        addon_updater_ops.update_settings_ui(self, context)