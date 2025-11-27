
from enum import Enum

import bpy
from bpy_extras.io_utils import ImportHelper

from . import import_xnalara_model, material_creator, xps_types

uv_x_displace = 0
uv_y_displace = 0


class XPS_ImportStatus(Enum):
    NotRunning = 0
    Running = 1
    Completed = 2


class XPS_OT_ImportModal(bpy.types.Operator, ImportHelper):
    """"""

    bl_lable = "Import XNALara/XPS"
    bl_idname = "xnal.operator_modal_import_xps"

    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    # import status
    status: XPS_ImportStatus = XPS_ImportStatus.NotRunning
    # import message
    status_message: str = ""

    # region ImportHelper parameters

    filename_ext = ".mesh"

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )  # type:ignore

    uvDisplX: bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )  # type:ignore

    uvDisplY: bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )  # type:ignore

    impDefPose: bpy.props.BoolProperty(
        name="Default Pose",
        description="Import Default Pose",
        default=False,
    )  # type:ignore

    markSeams: bpy.props.BoolProperty(
        name="Mark Seams",
        description="Mark as Seams the edged merged by the addon",
        default=True,
    )  # type:ignore

    vColors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Import Vertex Colors",
        default=True,
    )  # type:ignore

    joinMeshRips: bpy.props.BoolProperty(
        name="Merge Doubles by Normal",
        description="Merge vertices with the same position and normal",
        default=True,
    )  # type:ignore

    joinMeshParts: bpy.props.BoolProperty(
        name="Join MeshParts",
        description="Join MeshParts (meshes that contain 'nPart!' in the name)",
        default=True,
    )  # type:ignore

    connectBones: bpy.props.BoolProperty(
        name="Connect Bones",
        description="Connect Bones all bones",
        default=True,
    )  # type:ignore

    autoIk: bpy.props.BoolProperty(
        name="AutoIK",
        description="Set AutoIK",
        default=True,
    )  # type:ignore

    importNormals: bpy.props.BoolProperty(
        name="Import Normals",
        description="Import Custom Normals",
        default=True,
    )  # type:ignore

    separate_optional_objects: bpy.props.BoolProperty(
        name="Separate Optional Objects",
        description="Separate into collection object marked as optional",
        default=True
    )  # type:ignore

    # endregion

    def menu_func(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        self.layout.operator(
            Import_Xps_Model_Op.bl_idname,
            text="Text Export Operator")

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context: bpy.types.Context):
        xpsSettings = xps_types.XpsImportSettings(
            self.filepath,
            self.uvDisplX,
            self.uvDisplY,
            self.impDefPose,
            self.joinMeshRips,
            self.joinMeshParts,
            self.markSeams and self.joinMeshRips,
            self.vColors,
            self.connectBones,
            self.autoIk,
            self.importNormals,
            self.separate_optional_objects
        )
        material_creator.create_group_nodes()
        status = import_xnalara_model.getInputFilename(xpsSettings)
        if status == '{NONE}':
            # self.report({'DEBUG'}, "DEBUG File Format unrecognized")
            # self.report({'INFO'}, "INFO File Format unrecognized")
            # self.report({'OPERATOR'}, "OPERATOR File Format unrecognized")
            # self.report({'WARNING'}, "WARNING File Format unrecognized")
            # self.report({'ERROR'}, "ERROR File Format unrecognized")
            self.report({'ERROR'}, "ERROR File Format unrecognized")
        return {'FINISHED'}

    def modal(self, context, event):
        match self.status:
            case XPS_ImportStatus.Completed:
                return {"FINISHED"}

        return {"RUNNING_MODAL"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):

        bpy.ops.wm.call_menu(XPS_OT_ImportMenu)
        test = {"test"}
        self.status = XPS_ImportStatus.Running
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}


class XPS_OT_ImportMenu(bpy.types.Menu):
    """"""

    bl_label = ""
    bl_idname = "xnal_MT_menu_import_xps"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context: bpy.types.Context):
        pass


class Import_Xps_Model_Op(bpy.types.Operator, ImportHelper):
    """Load an XNALara model File."""

    bl_idname = "xps_tools.import_model"
    bl_label = "Import XNALara/XPS Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".mesh"

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.

    # filter File Extension
    filter_glob: bpy.props.StringProperty(
        default="*.ascii;*.mesh;*.xps",
        options={'HIDDEN'},
    )  # type:ignore

    uvDisplX: bpy.props.IntProperty(
        name="X",
        description="Displace UV X axis",
        default=uv_x_displace,
    )  # type:ignore

    uvDisplY: bpy.props.IntProperty(
        name="Y",
        description="Displace UV Y axis",
        default=uv_y_displace,
    )  # type:ignore

    impDefPose: bpy.props.BoolProperty(
        name="Default Pose",
        description="Import Default Pose",
        default=False,
    )  # type:ignore

    markSeams: bpy.props.BoolProperty(
        name="Mark Seams",
        description="Mark as Seams the edged merged by the addon",
        default=True,
    )  # type:ignore

    vColors: bpy.props.BoolProperty(
        name="Vertex Colors",
        description="Import Vertex Colors",
        default=True,
    )  # type:ignore

    joinMeshRips: bpy.props.BoolProperty(
        name="Merge Doubles by Normal",
        description="Merge vertices with the same position and normal",
        default=True,
    )  # type:ignore

    joinMeshParts: bpy.props.BoolProperty(
        name="Join MeshParts",
        description="Join MeshParts (meshes that contain 'nPart!' in the name)",
        default=True,
    )  # type:ignore

    connectBones: bpy.props.BoolProperty(
        name="Connect Bones",
        description="Connect Bones all bones",
        default=True,
    )  # type:ignore

    autoIk: bpy.props.BoolProperty(
        name="AutoIK",
        description="Set AutoIK",
        default=True,
    )  # type:ignore

    importNormals: bpy.props.BoolProperty(
        name="Import Normals",
        description="Import Custom Normals",
        default=True,
    )  # type:ignore

    separate_optional_objects: bpy.props.BoolProperty(
        name="Separate Optional Objects",
        description="Separate into collection object marked as optional",
        default=True
    )  # type:ignore

    def menu_func(self, context):
        self.layout.operator_context = 'INVOKE_DEFAULT'
        self.layout.operator(
            Import_Xps_Model_Op.bl_idname,
            text="Text Export Operator")

    @classmethod
    def poll(cls, context):
        # Always can import
        return True

    def execute(self, context):
        xpsSettings = xps_types.XpsImportSettings(
            self.filepath,
            self.uvDisplX,
            self.uvDisplY,
            self.impDefPose,
            self.joinMeshRips,
            self.joinMeshParts,
            self.markSeams and self.joinMeshRips,
            self.vColors,
            self.connectBones,
            self.autoIk,
            self.importNormals,
            self.separate_optional_objects
        )
        material_creator.create_group_nodes()
        status = import_xnalara_model.getInputFilename(xpsSettings)
        if status == '{NONE}':
            # self.report({'DEBUG'}, "DEBUG File Format unrecognized")
            # self.report({'INFO'}, "INFO File Format unrecognized")
            # self.report({'OPERATOR'}, "OPERATOR File Format unrecognized")
            # self.report({'WARNING'}, "WARNING File Format unrecognized")
            # self.report({'ERROR'}, "ERROR File Format unrecognized")
            self.report({'ERROR'}, "ERROR File Format unrecognized")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text='UV Displace')
        col.prop(self, "uvDisplX")
        col.prop(self, "uvDisplY")

        col = layout.column(align=True)
        col.label(text='Mesh')
        col.prop(self, "joinMeshParts")
        col.prop(self, "joinMeshRips")
        col.prop(self, "separate_optional_objects")

        sub = col.row()
        col.prop(self, "importNormals")
        sub.prop(self, "markSeams")
        col.prop(self, "vColors")

        sub.enabled = self.joinMeshRips
        self.markSeams = self.joinMeshRips and self.markSeams

        col = layout.column(align=True)
        col.label(text='Armature')
        col.prop(self, "impDefPose")
        col.prop(self, "connectBones")
        col.prop(self, "autoIk")
