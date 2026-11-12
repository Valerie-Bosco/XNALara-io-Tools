import bpy


class XNAL_OT_MasterDragAndDropHandler(bpy.types.FileHandler):
    bl_label = ""
    bl_idname = "xnal.operator_master_drag_and_drop_handler"
    bl_import_operator = "xnal.operator_master_drag_and_drop"
    bl_file_extensions = ".ascii;.xps;.mesh;.pose;.obj"

    @classmethod
    def poll_drop(cls, context):
        return context.area is not None and context.area.type == "VIEW_3D"


class XNAL_OT_MasterDragAndDrop(bpy.types.Operator):
    bl_idname = "xnal.operator_master_drag_and_drop"
    bl_label = ""
    bl_description = ""

    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)  # type: ignore
    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore

    def execute(self, context):
        file: bpy.types.OperatorFileListElement
        for file in self.files:
            file_type = file.name.split(".")[-1].lower()

            match file_type:
                case "ascii" | "xps" | "mesh":
                    bpy.ops.xps_tools.import_model(
                        "INVOKE_DEFAULT", filepath=self.directory + file.name
                    )
                case "pose":
                    bpy.ops.xps_tools.import_pose(
                        "INVOKE_DEFAULT", filepath=self.directory + file.name
                    )
                case "obj":
                    bpy.ops.import_xps_ngff.obj(
                        "INVOKE_DEFAULT", filepath=self.directory + file.name
                    )
        return {"FINISHED"}
