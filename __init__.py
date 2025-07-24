#   Copyright (C) 2022 GAO SHAN PICTURES

#   GAOLIB is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>


bl_info = {
    "name": "GAOLIB",
    "author": "Anne Beurard",
    "version": (3, 1, 0),
    "blender": (4, 0, 0),
    "location": "View 3D",
    "warning": "Requires installation of dependencies",
    "description": "Animation and Pose library tool for Blender.",
    "category": "3D View",
}


import importlib
import json
import os
import subprocess
import sys
from collections import namedtuple

import bpy

sys.path.append(os.path.dirname(__file__))


# ----------------------------------- MANAGE DEPENDENCIES -----------------------------------

"""
INFORMATION :  The following MANAGE DEPENDENCY section is partly copied from Robert Guetzkow work :
https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies


#    Copyright (C) 2020  Robert Guetzkow
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>


"""


Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.


dependenciesPySide6 = (
    Dependency(module="PySide6", package=None, name=None),
    Dependency(module="imageio", package=None, name=None),
)

dependencies_installed = False
dependenciesSet = [dependenciesPySide6]


def import_module(module_name, global_name=None, reload=True):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """
    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
        # the given name, just like the regular import would.
        globals()[global_name] = importlib.import_module(module_name)


def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_and_import_module(module_name, package_name=None, global_name=None):
    """
    Installs the package through pip and attempts to import the installed module.
    :param module_name: Module to import.
    :param package_name: (Optional) Name of the package that needs to be installed. If None it is assumed to be equal
       to the module_name.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: subprocess.CalledProcessError and ImportError
    """
    if package_name is None:
        package_name = module_name

    if global_name is None:
        global_name = module_name

    # Blender disables the loading of user site-packages by default. However, pip will still check them to determine
    # if a dependency is already installed. This can cause problems if the packages is installed in the user
    # site-packages and pip deems the requirement satisfied, but Blender cannot import the package from the user
    # site-packages. Hence, the environment variable PYTHONNOUSERSITE is set to disallow pip from checking the user
    # site-packages. If the package is not already installed for Blender's Python interpreter, it will then try to.
    # The paths used by pip can be checked with `subprocess.run([bpy.app.binary_path_python, "-m", "site"], check=True)`

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run(
        [sys.executable, "-m", "pip", "install", package_name],
        check=True,
        env=environ_copy,
    )

    # The installation succeeded, attempt to import the module again
    import_module(module_name, global_name)


def uninstall_module(module_name, package_name=None, global_name=None):
    if package_name is None:
        package_name = module_name

    if global_name is None:
        global_name = module_name

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", package_name],
        check=True,
        env=environ_copy,
    )


class GAOLIB_PT_warning_panel(bpy.types.Panel):
    bl_label = "GAOLIB Warning"
    bl_category = "GaoLib"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def draw(self, context):
        layout = self.layout

        lines = [
            f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
            f"1. Open the preferences (Edit > Preferences > Add-ons).",
            f"2. Search for the \"{bl_info.get('name')}\" add-on.",
            f"3. Open the details section of the add-on.",
            f'4. Click on the "{GAOLIB_OT_install_dependencies.bl_label}" button.',
            f"   This will download and install the missing Python packages, if Blender has the required",
            f"   permissions.",
            f"If you're attempting to run the add-on from the text editor, you won't see the options described",
            f"above. Please install the add-on properly through the preferences.",
            f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
            f'2. Press the "Install" button.',
            f"3. Search for the add-on file.",
            f'4. Confirm the selection by pressing the "Install Add-on" button in the file browser.',
        ]

        for line in lines:
            layout.label(text=line)


class GAOLIB_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "gaolib.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = (
        "Downloads and installs the required python packages for this add-on. "
        "Internet connection is required. Blender may have to be started with "
        "elevated permissions in order to install the package"
    )
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed

    def execute(self, context):
        for dependencies in dependenciesSet:
            try:
                install_pip()
                for dependency in dependencies:
                    install_and_import_module(
                        module_name=dependency.module,
                        package_name=dependency.package,
                        global_name=dependency.name,
                    )
            except (subprocess.CalledProcessError, ImportError) as err:
                self.report({"ERROR"}, str(err))
                # return {"CANCELLED"}
                continue

            global dependencies_installed
            dependencies_installed = True

            # Register the panels, operators, etc. since dependencies are installed
            for cls in classes:
                bpy.utils.register_class(cls)

            return {"FINISHED"}
        return {"CANCELLED"}


class GAOLIB_OT_uninstall_dependencies(bpy.types.Operator):
    bl_idname = "gaolib.uninstall_dependencies"
    bl_label = "Uninstall dependencies"
    bl_description = "Uninstalls the required python packages for this add-on. "
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return dependencies_installed

    def execute(self, context):
        dependenciesList = []

        for dset in dependenciesSet:
            for dependencies in dset:
                dependenciesList.append(dependencies)

        try:
            install_pip()
            for dependency in dependenciesList:
                uninstall_module(
                    module_name=dependency.module,
                    package_name=dependency.package,
                    global_name=dependency.name,
                )
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = False

        # Register the panels, operators, etc. since dependencies are installed
        for cls in classes:
            bpy.utils.unregister_class(cls)

        return {"FINISHED"}


class GAOLIB_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(GAOLIB_OT_install_dependencies.bl_idname, icon="CONSOLE")
        layout.operator(GAOLIB_OT_uninstall_dependencies.bl_idname, icon="CONSOLE")


preference_classes = (
    GAOLIB_PT_warning_panel,
    GAOLIB_OT_install_dependencies,
    GAOLIB_preferences,
    GAOLIB_OT_uninstall_dependencies,
)


# ---------------------------------- GAOLIB APP -----------------------------------------


class OT_gaolib(bpy.types.Operator):
    """GAOLIB TOOL"""

    bl_idname = "development.gaolib_operator"
    bl_label = "GaoLib"

    _app = None
    _widget = None
    _timer: bpy.types.Timer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from PySide6 import QtWidgets

        if not QtWidgets.QApplication.instance():
            self._app = QtWidgets.QApplication(sys.argv)
        else:
            self._app = QtWidgets.QApplication.instance()
        for tlw in self._app.topLevelWindows():
            tlw.close()

    def modal(self, context, event):
        # Finish running operator if window is closed
        try:
            if self._widget and not self._widget.isVisible():
                context.window_manager.event_timer_remove(self._timer)
                return {"FINISHED"}
            # Procecess any events
            self._app.processEvents()
        except Exception as e:
            print("Caught Exception : " + str(e))
            # widget already deleted
            context.window_manager.event_timer_remove(self._timer)
            return {"FINISHED"}
        return {"PASS_THROUGH"}

    def execute(self, context):
        from PySide6 import QtWidgets

        from .gaolib.gaolibsub import GaoLib

        # Show QT Widget
        self._widget = GaoLib()
        self._widget.show()
        # Timer controls when modal() function is called
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.05, window=context.window)
        wm.modal_handler_add(self)
        # Get current context
        bpy.ops.development.get_blender_context()
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        """Remove event timer when stopping the operator."""
        from PySide6 import QtWidgets

        self._widget.close()
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    @classmethod
    def poll(cls, context):
        return context.space_data is not None


# ----------------------------------GAOLIB ADDITIONAL OPERATORS-----------------------------------------


class OT_ShowOverlayParams(bpy.types.Operator):
    """Show the overlays hidden after creating an anim/pose."""

    bl_idname = "development.show_overlay_params"
    bl_label = "Show bones"

    def execute(self, context):
        area = bpy.context.area
        space = bpy.context.space_data
        space.overlay.show_overlays = True
        space.overlay.show_bones = True
        space.overlay.show_axis_x = True
        space.overlay.show_axis_y = True
        space.overlay.show_floor = True
        return {"FINISHED"}


class OT_GetBlenderContext(bpy.types.Operator):
    """Set context attribute to GAOLIB"""

    bl_idname = "development.get_blender_context"
    bl_label = "Get Blender Context"

    def execute(self, context):
        from PySide6 import QtWidgets

        gaolib = None
        app = None
        if QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication.instance()
            for widget in app.topLevelWidgets():
                if widget.__class__.__name__ == "GaoLib":
                    widget.context = context.copy()
                    gaolib = widget
        else:
            return {"CANCELLED"}
        if not gaolib:
            return {"CANCELLED"}
        return {"FINISHED"}


# ----------------------------------GAOLIB PROPERTIES-----------------------------------------


class GaolibCustomProperties(bpy.types.PropertyGroup):
    """Boolean values to keep track of the state of the scene or GAOLIB window"""

    gaolibKeyLastFrame: bpy.props.BoolProperty(name="keyLastFrame", default=False)

    gaolibNewAnimation: bpy.props.BoolProperty(name="newAnimation", default=False)

    gaolibNewPose: bpy.props.BoolProperty(name="newPose", default=False)

    gaolibNewSelectionSet: bpy.props.BoolProperty(name="newSelectionSet", default=False)

    gaolibNewConstraintSet: bpy.props.BoolProperty(
        name="newConstraintSet", default=False
    )


# ----------------------------------GAOLIB PANNEL-----------------------------


class VIEW3D_PT_Gaolib(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GaoLib"
    bl_label = "GAOLIB"

    def draw(self, context):
        col4 = self.layout.column(align=True)
        col4.operator("development.gaolib_operator", text="GAOLIB", icon="EVENT_G")
        col4.operator(
            "development.get_blender_context", text="Get Context", icon="WINDOW"
        )
        col4.operator(
            "development.show_overlay_params",
            text="Show overlay hidden",
            icon="OVERLAY",
        )


# ----------------------------------- REGISTER -----------------------------------


classes = [
    OT_gaolib,
    OT_ShowOverlayParams,
    OT_GetBlenderContext,
    GaolibCustomProperties,
    VIEW3D_PT_Gaolib,
]


def register():
    global dependencies_installed
    dependencies_installed = False

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gaolib"))

    for cls in preference_classes:
        bpy.utils.register_class(cls)

    foundDependenciesSet = False
    for dependencies in dependenciesSet:
        try:
            for dependency in dependencies:

                import_module(
                    module_name=dependency.module, global_name=dependency.name
                )

            dependencies_installed = True
        except ModuleNotFoundError:
            # Don't register other panels, operators etc. if missing dependencies
            # return
            continue
        foundDependenciesSet = True
        break
    if not foundDependenciesSet:
        # Don't register other panels, operators etc. if missing dependencies
        return

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.gaolib_tool = bpy.props.PointerProperty(type=GaolibCustomProperties)


def unregister():
    del bpy.types.Scene.gaolib_tool
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    if dependencies_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)

    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
