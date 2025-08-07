# import bpy


# class ALX_OT_Operator_Modal_InfoPopupAwaitCompletion(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.operator_modal_info_popup_await_completion"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context: bpy.types.Context):
#         return {"FINISHED"}

#     def modal(self, context: bpy.types.Context, event: bpy.types.Event):
#         return {"RUNNING_MODAL"}

#     def draw(self, context: bpy.types.Context):
#         template_list

#     def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
#         wm: bpy.types.WindowManager = context.window_manager
#         return wm.invoke_popup(self, width=180)


# def register_info():
#     bpy.types.WindowManager


# def unregister_info():
