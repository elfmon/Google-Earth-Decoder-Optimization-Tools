import bpy
from bpy.props import StringProperty
from scripts.clean_package_files_script import clean_package_files
from scripts.init_msfs_scenery_project_script import init_msfs_scenery_project
from scripts.merge_sceneries_script import merge_sceneries
from scripts.optimize_scenery_script import optimize_scenery
from scripts.update_min_size_values_script import update_min_size_values
from scripts.compress_built_package_script import compress_built_package
from scripts.update_tiles_position_script import update_tiles_position
from utils import open_console
from .tools import reload_current_operator, reload_setting_props
from bpy_extras.io_utils import ImportHelper
from bpy_types import Operator


class FileBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.display_size = "NORMAL"


class DirectoryBrowserOperator(Operator, ImportHelper):
    def draw(self, context):
        space = context.space_data
        params = space.params
        params.use_filter = True
        params.use_filter_folder = True
        params.display_size = "NORMAL"


class OT_ProjectsPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.projects_path_operator"
    bl_label = "Path of the MSFS projects..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.projects_path = self.directory
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.projects_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_ProjectPathOperator(DirectoryBrowserOperator):
    bl_idname = "wm.project_path_operator"
    bl_label = "Path of the MSFS project..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.project_path = self.directory
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.project_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_ProjectPathToMergeOperator(DirectoryBrowserOperator):
    bl_idname = "wm.project_path_to_merge_operator"
    bl_label = "Path of the project you want to merge into the final one..."

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.project_path_to_merge = self.directory
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = context.scene.setting_props.project_path_to_merge
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_MsfsBuildExePathOperator(FileBrowserOperator):
    bl_idname = "wm.msfs_build_exe_path_operator"
    bl_label = "Path to the MSFS bin exe that builds the MSFS packages..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.msfs_build_exe_path = self.filepath
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.msfs_build_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_CompressonatorExePathOperator(FileBrowserOperator):
    bl_idname = "wm.compressonator_exe_path_operator"
    bl_label = "Path to the compressonator bin exe that compresses the package texture files..."

    filter_glob: StringProperty(
        default="*.exe",
        options={"HIDDEN"},
    )
    filepath: bpy.props.StringProperty(
        subtype="FILE_PATH"
    )

    def draw(self, context):
        super().draw(context)

    def execute(self, context):
        context.scene.setting_props.compressonator_exe_path = self.filepath
        reload_current_operator(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = context.scene.setting_props.compressonator_exe_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_InitMsfsSceneryProjectOperator(Operator):
    bl_idname = "wm.init_msfs_scenery_project"
    bl_label = "Initialize a new MSFS project scenery..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        init_msfs_scenery_project(context.scene.settings)
        return {'FINISHED'}


class OT_OptimizeMsfsSceneryOperator(Operator):
    bl_idname = "wm.optimize_msfs_scenery"
    bl_label = "Optimize an existing MSFS scenery..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        optimize_scenery(context.scene.settings)
        return {'FINISHED'}


class OT_CleanPackageFilesOperator(Operator):
    bl_idname = "wm.clean_package_files"
    bl_label = "Clean the unused files of the msfs project..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        clean_package_files(context.scene.settings)
        return {'FINISHED'}


class OT_MergeSceneriesOperator(Operator):
    bl_idname = "wm.merge_sceneries"
    bl_label = "Merge an existing MSFS scenery project into another one..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        merge_sceneries(context.scene.settings)
        return {'FINISHED'}


class OT_UpdateTilesPositionOperator(Operator):
    bl_idname = "wm.update_tiles_position"
    bl_label = "Update the position of the MSFS scenery tiles..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        update_tiles_position(context.scene.settings)
        return {'FINISHED'}


class OT_UpdateMinSizeValuesOperator(Operator):
    bl_idname = "wm.update_min_size_values"
    bl_label = "Update LOD min size values for each tile of the project..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        update_min_size_values(context.scene.settings)
        return {'FINISHED'}


class OT_CompressBuiltPackageOperator(Operator):
    bl_idname = "wm.compress_built_package"
    bl_label = "Optimize the built package by compressing the texture files..."

    def execute(self, context):
        # clear and open the system console
        open_console()
        compress_built_package(context.scene.settings)
        return {'FINISHED'}


class OT_ReloadSettingsOperator(Operator):
    bl_idname = "wm.reload_settings_operator"
    bl_label = "Reload settings..."

    def execute(self, context):
        reload_setting_props(context)
        return {'FINISHED'}


class OT_SaveSettingsOperator(Operator):
    bl_idname = "wm.save_settings_operator"
    bl_label = "Save settings..."

    def execute(self, context):
        context.scene.settings.save()
        return {'FINISHED'}