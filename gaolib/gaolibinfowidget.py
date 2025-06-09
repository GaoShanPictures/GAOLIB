#   Copyright (C) 2022 GAO SHAN PICTURES

#   This file is a part of GAOLIB.

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

__author__ = "Anne Beurard"

import json
import os
import shutil

try:
    import bpy
except Exception as e:
    print("IMPORT EXCEPTION : " + str(e))

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtCore, QtGui, QtWidgets

import gaolib.model.blenderutils as utils
from gaolib.ui.constraintinfopairingwidgetui import Ui_ConstraintForm as Constraint_Form
from gaolib.ui.constraintpairingwidgetui import Ui_Form as Pairing_Form
from gaolib.ui.infowidgetui import Ui_Form as InfoWidget
from gaolib.ui.newfolderdialogui import Ui_Dialog as NewFolderDialog
from gaolib.ui.yesnodialogui import Ui_Dialog as YesNoDialog


class ConstrainInfoWidget(QtWidgets.QWidget, Constraint_Form):
    def __init__(
        self,
        constraintName,
        bone,
        targetBone,
        targetObject,
        comboList,
        parent=None,
    ):
        super(ConstrainInfoWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.groupBox.setTitle(constraintName)
        self.constraintName = constraintName
        self.targetObject = targetObject
        self.targetBone = bone
        self.boneLabel.setText(bone)
        self.boneLabel.setToolTip(bone)
        self.sourceTargetLabel.setText(targetObject)
        self.sourceTargetLabel.setToolTip(targetObject)
        self.targetBoneLabel.setText(targetBone)
        self.targetBoneLabel.setToolTip(targetBone)
        self.comboBox.addItems(comboList)
        index = self.comboBox.findText(self.targetObject)
        if index >= 0:
            self.comboBox.setCurrentIndex(index)


class PairingWidget(QtWidgets.QWidget, Pairing_Form):
    def __init__(
        self,
        objectName,
        comboList,
        constraintDict,
        parent=None,
    ):
        super(PairingWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.objectName = objectName
        self.objectNameLabel.setText(objectName)
        self.armatureComboBox.addItems(comboList)
        index = self.armatureComboBox.findText(objectName)
        if index >= 0:
            self.armatureComboBox.setCurrentIndex(index)

        self.constraintInfoWidgets = []

        if objectName in constraintDict.keys():
            if "bone_constraints" in constraintDict[objectName].keys():
                for bone in constraintDict[objectName]["bone_constraints"]:
                    for constraintName in constraintDict[objectName][
                        "bone_constraints"
                    ][bone]:
                        consDict = constraintDict[objectName]["bone_constraints"][bone][
                            constraintName
                        ]
                        if "target" in consDict.keys():
                            if "subtarget" in consDict.keys():
                                targetBone = consDict["subtarget"]
                            else:
                                targetBone = None
                            targetObject = consDict["target"]["name"]
                            constraintItem = ConstrainInfoWidget(
                                constraintName,
                                bone,
                                targetBone,
                                targetObject,
                                comboList,
                                parent=None,
                            )
                            self.widgetVerticalLayout.addWidget(constraintItem)
                            self.constraintInfoWidgets.append(constraintItem)


class CustomSliderWidget(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(CustomSliderWidget, self).__init__(parent=parent)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # manage cancel blending at right click
        if event.button() == QtCore.Qt.RightButton:
            self.setValue(0)
            self.valueChanged.disconnect()
            self.valueChanged.connect(lambda: self.setValue(0))
            self.parentInfoWidget.mainWindow.statusBar().showMessage(
                "Cancel Blending",
                timeout=5000,
            )
        super(CustomSliderWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.valueChanged.disconnect()
            self.valueChanged.connect(
                lambda: self.parentInfoWidget.blendSliderChanged(
                    self.parentInfoWidget.item.path,
                    blend=self.parentInfoWidget.blendPoseSlider.value() / 100,
                )
            )

        super(CustomSliderWidget, self).mouseReleaseEvent(event)


class GaoLibInfoWidget(QtWidgets.QWidget, InfoWidget):
    """Manage display of the selected list item informations"""

    def __init__(self, selectedItem, mainWin, parent=None):
        super(GaoLibInfoWidget, self).__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.mainWindow = mainWin
        self.item = selectedItem
        self.thumbpath = self.item.thumbpath
        self.currentPose = None
        self.refPose = None
        self.bonesToBlend = None
        self.toggleAdditive = False
        utils.removeOrphans()

        # recast blendPoseSlider
        self.blendPoseSlider.__class__ = CustomSliderWidget
        self.blendPoseSlider.parentInfoWidget = self

        # For animation item use gif thumbnail
        self.movie = None
        if self.item.itemType == "ANIMATION":
            self.thumbpath = self.item.thumbpath.replace("png", "gif")
        self.showInfos()
        # Connect functions
        self.trashPushButton.released.connect(self.delete)
        self.selectBonesPushButton.released.connect(self.selectBones)
        self.addToSetPushButton.released.connect(
            lambda: utils.updateSelectionSet(self, add=True)
        )
        self.rmFromSetPushButton.released.connect(
            lambda: utils.updateSelectionSet(self, add=False)
        )
        self.additiveModeCheckBox.stateChanged.connect(self.additiveModeToggle)
        self.blendPoseSlider.valueChanged.connect(
            lambda: self.blendSliderChanged(
                self.item.path, blend=self.blendPoseSlider.value() / 100
            )
        )
        self.modifyPushButton.released.connect(self.modifyFolder)
        self.refreshPairingListPushButton.released.connect(
            self.updateConstraintPairingList
        )

    def modifyFolder(self):
        """Modify existing folder"""
        # creates the dialog
        dialog = QtWidgets.QDialog(self.mainWindow)
        dialog.ui = NewFolderDialog()
        dialog.ui.setupUi(dialog)

        thumbpath = self.thumbpath
        dialog.ui.iconLabel.setPixmap((QtGui.QPixmap(thumbpath).scaled(80, 80)))
        folderIcons = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "icons/folder_icons"
        )
        if os.path.isdir(folderIcons):
            for iconFile in os.listdir(folderIcons):
                iconPath = os.path.join(folderIcons, iconFile)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(iconPath))
                dialog.ui.iconComboBox.addItem(icon, iconFile)
        dialog.ui.iconComboBox.currentIndexChanged.connect(
            lambda: dialog.ui.iconLabel.setPixmap(
                QtGui.QPixmap(
                    os.path.join(folderIcons, dialog.ui.iconComboBox.currentText())
                ).scaled(80, 80)
            )
        )
        oldName = self.item.name
        # oldPath = os.path.realpath(self.item.path.replace("\\", "/"))
        oldPath = self.item.path
        oldParentPath = os.path.dirname(oldPath)
        dialog.ui.lineEdit.setText(oldName)
        dialog.ui.pathLineEdit.setText(oldParentPath)
        dialog.ui.pathLineEdit.setEnabled(True)
        dialog.ui.browsePushButton.setEnabled(True)
        dialog.ui.browsePushButton.released.connect(
            lambda: self.mainWindow.openFileNameDialog(dialog, openDirectory=oldPath)
        )
        doRefreshView = False

        isFolder = self.item.itemType == "FOLDER"
        if not isFolder:
            dialog.ui.iconComboBox.setEnabled(False)
        rsp = dialog.exec_()
        # retrieve editLine infos from the dialog
        name = dialog.ui.lineEdit.text()
        path = os.path.realpath(dialog.ui.pathLineEdit.text())
        # if user clicks on 'ok'
        if rsp == QtWidgets.QDialog.Accepted:
            if not isFolder:
                wrongName = False
                if self.item.itemType == "ANIMATION" and not name.endswith(".anim"):
                    suffix = ".anim"
                    name = name.split(".")[0] + suffix
                    wrongName = True
                elif self.item.itemType == "SELECTION SET" and not name.endswith(
                    ".selection"
                ):
                    suffix = ".selection"
                    name = name.split(".")[0] + suffix
                    wrongName = True
                elif self.item.itemType == "POSE" and not name.endswith(".pose"):
                    suffix = ".pose"
                    name = name.split(".")[0] + ".pose"
                    wrongName = True
                elif self.item.itemType == "CONSTRAINT SET" and not name.endswith(
                    ".constraint"
                ):
                    suffix = ".constraint"
                    name = name.split(".")[0] + ".constraint"
                    wrongName = True
                if wrongName:
                    utils.ShowDialog(
                        "Name must end with " + suffix + ", for example : \n\n" + name,
                        "Wrong Name",
                    )
                    return

            if name.replace(" ", "") != "":
                # Modify thumbnail
                folderIconPath = os.path.join(
                    folderIcons, dialog.ui.iconComboBox.currentText()
                )
                if os.path.isfile(folderIconPath):
                    thumbnailPath = os.path.join(oldPath, "thumbnail.png")
                    if os.path.isfile(thumbnailPath):
                        os.remove(thumbnailPath)
                    shutil.copyfile(folderIconPath, thumbnailPath)
                    # Refresh View
                    self.thumbnailLabel.setPixmap(
                        (QtGui.QPixmap(thumbnailPath).scaled(200, 200))
                    )
                if isFolder:
                    # Get tree item
                    treeModel = self.mainWindow.treeModel
                    treeItem = treeModel.getElemWithPath(oldPath)
                selectedItemPath = self.mainWindow.currentTreeElement.path
                expanded = self.mainWindow.getTreeExpandedItems()
                # Modify folder name
                if name != oldName:
                    # Rename folder
                    newPath = os.path.join(os.path.dirname(oldPath), name)
                    try:
                        if not isFolder:
                            # clean info widget
                            if self.movie is not None:
                                self.thumbnailLabel.removeEventFilter(self)
                                self.movie.setFileName("")
                            self.mainWindow.cleanInfoWidget()
                        os.rename(oldPath, newPath)
                        if not isFolder:
                            # Modify name in Json file
                            jsonFile = None
                            for file in os.listdir(newPath):
                                if file.endswith(".json"):
                                    jsonFile = os.path.join(newPath, file)
                                    break
                            if jsonFile:
                                with open(jsonFile) as file:
                                    data = json.load(file)
                                data["metadata"]["name"] = name
                                with open(jsonFile, "w") as file:
                                    json.dump(data, file, indent=4, sort_keys=True)
                        oldPath = newPath
                    except PermissionError as pe:
                        utils.ShowDialog(
                            "The folder or one of its sub folders might be open or used by another program.\n\n"
                            + str(pe),
                            "Impossible to rename folder",
                        )
                        return
                    except FileExistsError as fee:
                        utils.ShowDialog(
                            "A folder with name "
                            + name
                            + " already exists.\n\n"
                            + str(fee),
                            "Impossible to rename folder",
                        )
                        return
                    except Exception as e:
                        utils.ShowDialog(
                            "An error occured : \n\n" + str(e),
                            "Impossible to rename folder",
                        )
                        raise
                    if isFolder:
                        # Rename tree item
                        treeModel.modifyElement(treeItem, name, newPath)
                    doRefreshView = True

                # Modify location
                if os.path.realpath(path) != os.path.realpath(os.path.dirname(oldPath)):
                    try:
                        if not isFolder:
                            # clean info widget
                            if self.movie is not None:
                                self.thumbnailLabel.removeEventFilter(self)
                                self.movie.setFileName("")
                            self.mainWindow.cleanInfoWidget()
                        shutil.move(oldPath, path)
                    except Exception as e:
                        utils.ShowDialog(
                            "An error occured : \n\n" + str(e),
                            "Impossible to Move folder",
                        )
                        raise
                    if isFolder:
                        # Modify tree item
                        treeModel.modifyElement(
                            treeItem, name, os.path.join(path, name)
                        )
                    doRefreshView = True

                if doRefreshView:
                    # Restore expand state and selected item
                    self.mainWindow.restoreExpandedState(expanded, selectedItemPath)

                    # Select MODIFIED item
                    currentIndex = None
                    for item in self.mainWindow.items.keys():
                        if self.mainWindow.items[item].name == name:
                            currentIndex = item
                            break

                    if currentIndex is not None:
                        index = self.mainWindow.listView.model().index(currentIndex, 0)
                        self.mainWindow.listView.selectionModel().select(
                            index, QtCore.QItemSelectionModel.Select
                        )
                    else:
                        self.mainWindow.cleanInfoWidget()
            else:
                QtWidgets.QMessageBox.about(
                    self, "Abort action", "Folder name must not be empty."
                )

    def additiveModeToggle(self):
        """Set info widget to display infos for additive/regular mode"""
        self.toggleAdditive = True
        state = self.additiveModeCheckBox.isChecked()

        if state:
            # Additive mode on
            self.blendPoseSlider.setMinimum(-100)
            self.blendPoseSlider.setValue(0)
        else:
            self.blendPoseSlider.setMinimum(0)
            self.blendPoseSlider.setValue(0)
        self.bonesToBlend = None

    def getBonesToBlend(self, poseDir, additiveMode=False):
        bonesToBlend = {}
        # get pose selection set
        itemdata = {}
        jsonPath = os.path.join(poseDir, "pose.json")
        with open(jsonPath) as file:
            itemdata = json.load(file)
        selectionSetBones = []
        for key in itemdata["metadata"].keys():
            if key == "boneNames":
                selectionSetBones = itemdata["metadata"]["boneNames"]
        # Remember current pose
        selection = utils.getSelectedBones()
        if not len(selection):
            # If no bone is selected select all
            print("No selected bones, select all by default for blending pose")
            self.selectBones()
            selection = utils.getSelectedBones()
        if not self.currentPose:
            self.currentPose = utils.getCurrentPose()
        # Append pose object
        if not self.refPose:
            self.refPose = utils.getRefPoseFromLib(poseDir, selection)
        # populate bonesToBlend dict to only blend on bones with modified value
        for posebone in self.refPose.pose.bones:
            for selectedbone in selection:
                if not selectedbone.name in selectionSetBones:
                    # ignore bones outside original pose selection set
                    continue
                if posebone.name == selectedbone.name:
                    rotationMode = posebone.rotation_mode
                    # if additiveMode:
                    #     bonesToBlend[posebone] = selectedbone
                    # else:
                    for axis in range(3):
                        if not selectedbone.lock_location[axis]:
                            if (
                                not additiveMode
                                and selectedbone.location[axis]
                                != posebone.location[axis]
                            ) or (additiveMode and posebone.location[axis] != 0):
                                if posebone not in bonesToBlend.keys():
                                    bonesToBlend[posebone] = selectedbone
                                break
                        if rotationMode != "QUATERNION":
                            if not selectedbone.lock_rotation[axis]:
                                if (
                                    not additiveMode
                                    and selectedbone.rotation_euler[axis]
                                    != posebone.rotation_euler[axis]
                                ) or (
                                    additiveMode and posebone.rotation_euler[axis] != 0
                                ):
                                    if posebone not in bonesToBlend.keys():
                                        bonesToBlend[posebone] = selectedbone
                                    break
                        if not selectedbone.lock_scale[axis]:
                            if (
                                not additiveMode
                                and selectedbone.scale[axis] != posebone.scale[axis]
                            ) or (additiveMode and posebone.scale[axis] != 1):
                                if posebone not in bonesToBlend.keys():
                                    bonesToBlend[posebone] = selectedbone
                                break
                    if rotationMode == "QUATERNION":
                        if not selectedbone.lock_rotation_w:
                            if (
                                not additiveMode
                                and selectedbone.rotation_quaternion[0]
                                != posebone.rotation_quaternion[0]
                            ) or (
                                additiveMode and posebone.rotation_quaternion[0] != 1
                            ):
                                if posebone not in bonesToBlend.keys():
                                    bonesToBlend[posebone] = selectedbone
                        for axis in range(3):

                            if not selectedbone.lock_rotation[axis]:
                                if (
                                    not additiveMode
                                    and selectedbone.rotation_quaternion[axis + 1]
                                    != posebone.rotation_quaternion[axis + 1]
                                ) or (
                                    additiveMode
                                    and posebone.rotation_quaternion[axis + 1] != 0
                                ):
                                    if posebone not in bonesToBlend.keys():
                                        bonesToBlend[posebone] = selectedbone
                                        break
        return bonesToBlend

    def blendSliderChanged(self, poseDir, blend=1):
        """Update pose from current scene according to the blend slider parameter value"""
        # Refresh display
        additiveMode = self.additiveModeCheckBox.isChecked()
        value = self.blendPoseSlider.value()
        if additiveMode:
            self.blendPoseLabel.setText("Add to Pose " + str(value) + "%")
        else:
            self.blendPoseLabel.setText("Blend Pose " + str(value) + "%")
        if value:
            self.applyPushButton.setText("APPLY " + str(value) + "%")
        else:
            self.applyPushButton.setText("APPLY 100 %")
        # If additive mode checkbox has just been toggled, do not update pose
        if self.toggleAdditive:
            self.toggleAdditive = False
            return
        if not self.bonesToBlend:
            self.bonesToBlend = self.getBonesToBlend(poseDir, additiveMode=additiveMode)

        refPose = self.refPose
        pose = refPose.pose
        try:
            # Copy properties from ref bones current object
            for posebone, selectedbone in self.bonesToBlend.items():
                # Manage if different rotation modes used (WARNING : axis angle not supported !)
                rotationMode = posebone.rotation_mode
                if (
                    rotationMode == "AXIS_ANGLE"
                    or selectedbone.rotation_mode == "AXIS_ANGLE"
                ):
                    raise Exception(
                        "AXIS_ANGLE Rotation mode not supported, use QUATERNION or Euler."
                    )
                elif (
                    rotationMode == "QUATERNION"
                    and self.currentPose[selectedbone]["rotationMode"] != "QUATERNION"
                ):
                    currentPoseRotation = self.currentPose[selectedbone][
                        "rotation"
                    ].to_quaternion()
                elif (
                    rotationMode != "QUATERNION"
                    and self.currentPose[selectedbone]["rotationMode"] == "QUATERNION"
                ):
                    currentPoseRotation = self.currentPose[selectedbone][
                        "rotation"
                    ].to_euler()
                elif rotationMode == self.currentPose[selectedbone]["rotationMode"]:
                    currentPoseRotation = self.currentPose[selectedbone]["rotation"]
                else:
                    raise Exception(
                        "Conversion between Rotation modes other than QUATERNION and Euler are not supported !"
                    )

                selectedbone.rotation_mode = rotationMode

                for axis in range(3):
                    if not selectedbone.lock_location[axis]:
                        if additiveMode:
                            selectedbone.location[axis] = (
                                blend * posebone.location[axis]
                                + self.currentPose[selectedbone]["location"][axis]
                            )
                        else:
                            selectedbone.location[axis] = (
                                blend * posebone.location[axis]
                                + (1 - blend)
                                * self.currentPose[selectedbone]["location"][axis]
                            )
                    if rotationMode != "QUATERNION":
                        if not selectedbone.lock_rotation[axis]:
                            if additiveMode:
                                selectedbone.rotation_euler[axis] = (
                                    blend * posebone.rotation_euler[axis]
                                    + currentPoseRotation[axis]
                                )
                            else:
                                selectedbone.rotation_euler[axis] = (
                                    blend * posebone.rotation_euler[axis]
                                    + (1 - blend) * currentPoseRotation[axis]
                                )
                    if not selectedbone.lock_scale[axis]:
                        if additiveMode:
                            selectedbone.scale[axis] = (
                                blend * posebone.scale[axis]
                                + self.currentPose[selectedbone]["scale"][axis]
                                - blend
                            )
                        else:
                            selectedbone.scale[axis] = (
                                blend * posebone.scale[axis]
                                + (1 - blend)
                                * self.currentPose[selectedbone]["scale"][axis]
                            )
                if rotationMode == "QUATERNION":
                    if not selectedbone.lock_rotation[0]:
                        if additiveMode:
                            selectedbone.rotation_quaternion[0] = (
                                blend * posebone.rotation_quaternion[0]
                                + currentPoseRotation[0]
                                - blend
                            )
                        else:
                            selectedbone.rotation_quaternion[0] = (
                                blend * posebone.rotation_quaternion[0]
                                + (1 - blend) * currentPoseRotation[0]
                            )
                    for axis in range(3):
                        if not selectedbone.lock_rotation[axis]:
                            if additiveMode:
                                selectedbone.rotation_quaternion[axis + 1] = (
                                    blend * posebone.rotation_quaternion[axis + 1]
                                    + currentPoseRotation[axis + 1]
                                )
                            else:
                                selectedbone.rotation_quaternion[axis + 1] = (
                                    blend * posebone.rotation_quaternion[axis + 1]
                                    + (1 - blend) * currentPoseRotation[axis + 1]
                                )
                # handle properties
                for key in posebone.keys():
                    try:
                        propertyType = eval("selectedbone." + key).__class__.__name__
                        if propertyType == "float":
                            exec(
                                "selectedbone."
                                + key
                                + " = blend * posebone."
                                + key
                                + " + (1-blend) * self.currentPose[selectedbone]."
                                + key
                            )
                        else:
                            exec("selectedbone." + key + " = posebone." + key)
                    except:
                        try:
                            propertyType = eval(
                                'selectedbone["' + key + '"]'
                            ).__class__.__name__
                            if propertyType == "float":
                                command = (
                                    'selectedbone["'
                                    + key
                                    + '"] = blend * posebone["'
                                    + key
                                    + '"]'
                                    + '+ (1-blend) * self.currentPose[selectedbone]["properties"]["'
                                    + key
                                    + '"]'
                                )
                                exec(command)
                            else:
                                exec(
                                    'selectedbone["'
                                    + key
                                    + '"] = posebone["'
                                    + key
                                    + '"]'
                                )
                        except:
                            print(
                                "IMPOSSIBLE TO HANDLE PROPERTY "
                                + key
                                + " FOR "
                                + selectedbone.name
                            )
        except Exception as e:
            print("Blend Pose Exception : " + str(e))

    # def blendSliderChanged(self, poseDir, blend=1):
    #     """Update pose from current scene according to the blend slider parameter value"""
    #     # Refresh display
    #     additiveMode = self.additiveModeCheckBox.isChecked()
    #     value = self.blendPoseSlider.value()
    #     if additiveMode:
    #         self.blendPoseLabel.setText("Add to Pose " + str(value) + "%")
    #     else:
    #         self.blendPoseLabel.setText("Blend Pose " + str(value) + "%")
    #     if value:
    #         self.applyPushButton.setText("APPLY " + str(value) + "%")
    #     else:
    #         self.applyPushButton.setText("APPLY 100 %")
    #     # If additive mode checkbox has just been toggled, do not update pose
    #     if self.toggleAdditive:
    #         self.toggleAdditive = False
    #         return
    #     # get pose selection set
    #     itemdata = {}
    #     jsonPath = os.path.join(poseDir, "pose.json")
    #     with open(jsonPath) as file:
    #         itemdata = json.load(file)
    #     selectionSetBones = []
    #     for key in itemdata["metadata"].keys():
    #         if key == "boneNames":
    #             selectionSetBones = itemdata["metadata"]["boneNames"]
    #     # Remember current pose
    #     selection = utils.getSelectedBones()
    #     if not self.currentPose:
    #         self.currentPose = utils.getCurrentPose()
    #     # Append pose object
    #     if not self.refPose:
    #         self.refPose = utils.getRefPoseFromLib(poseDir, selection)
    #     refPose = self.refPose
    #     pose = refPose.pose
    #     try:
    #         # Copy properties from ref bones current object
    #         for posebone in pose.bones:
    #             for selectedbone in selection:
    #                 if not selectedbone.name in selectionSetBones:
    #                     # ignore bones outside original pose selection set
    #                     continue
    #                 if posebone.name == selectedbone.name:
    #                     # Manage if different rotation modes used (WARNING : axis angle not supported !)
    #                     rotationMode = posebone.rotation_mode
    #                     if (
    #                         rotationMode == "AXIS_ANGLE"
    #                         or selectedbone.rotation_mode == "AXIS_ANGLE"
    #                     ):
    #                         raise Exception(
    #                             "AXIS_ANGLE Rotation mode not supported, use QUATERNION or Euler."
    #                         )
    #                     elif (
    #                         rotationMode == "QUATERNION"
    #                         and self.currentPose[selectedbone]["rotationMode"]
    #                         != "QUATERNION"
    #                     ):
    #                         currentPoseRotation = self.currentPose[selectedbone][
    #                             "rotation"
    #                         ].to_quaternion()
    #                     elif (
    #                         rotationMode != "QUATERNION"
    #                         and self.currentPose[selectedbone]["rotationMode"]
    #                         == "QUATERNION"
    #                     ):
    #                         currentPoseRotation = self.currentPose[selectedbone][
    #                             "rotation"
    #                         ].to_euler()
    #                     elif (
    #                         rotationMode
    #                         == self.currentPose[selectedbone]["rotationMode"]
    #                     ):
    #                         currentPoseRotation = self.currentPose[selectedbone][
    #                             "rotation"
    #                         ]
    #                     else:
    #                         raise Exception(
    #                             "Conversion between Rotation modes other than QUATERNION and Euler are not supported !"
    #                         )

    #                     selectedbone.rotation_mode = rotationMode

    #                     for axis in range(3):
    #                         if not selectedbone.lock_location[axis]:
    #                             if additiveMode:
    #                                 selectedbone.location[axis] = (
    #                                     blend * posebone.location[axis]
    #                                     + self.currentPose[selectedbone]["location"][
    #                                         axis
    #                                     ]
    #                                 )
    #                             else:
    #                                 selectedbone.location[axis] = (
    #                                     blend * posebone.location[axis]
    #                                     + (1 - blend)
    #                                     * self.currentPose[selectedbone]["location"][
    #                                         axis
    #                                     ]
    #                                 )
    #                         if rotationMode != "QUATERNION":
    #                             if not selectedbone.lock_rotation[axis]:
    #                                 if additiveMode:
    #                                     selectedbone.rotation_euler[axis] = (
    #                                         blend * posebone.rotation_euler[axis]
    #                                         + currentPoseRotation[axis]
    #                                     )
    #                                 else:
    #                                     selectedbone.rotation_euler[axis] = (
    #                                         blend * posebone.rotation_euler[axis]
    #                                         + (1 - blend) * currentPoseRotation[axis]
    #                                     )
    #                         if not selectedbone.lock_scale[axis]:
    #                             if additiveMode:
    #                                 selectedbone.scale[axis] = (
    #                                     blend * posebone.scale[axis]
    #                                     + self.currentPose[selectedbone]["scale"][axis]
    #                                     - blend
    #                                 )
    #                             else:
    #                                 selectedbone.scale[axis] = (
    #                                     blend * posebone.scale[axis]
    #                                     + (1 - blend)
    #                                     * self.currentPose[selectedbone]["scale"][axis]
    #                                 )
    #                     if rotationMode == "QUATERNION":
    #                         if not selectedbone.lock_rotation[0]:
    #                             if additiveMode:
    #                                 selectedbone.rotation_quaternion[0] = (
    #                                     blend * posebone.rotation_quaternion[0]
    #                                     + currentPoseRotation[0]
    #                                     - blend
    #                                 )
    #                             else:
    #                                 selectedbone.rotation_quaternion[0] = (
    #                                     blend * posebone.rotation_quaternion[0]
    #                                     + (1 - blend) * currentPoseRotation[0]
    #                                 )
    #                         for axis in range(3):
    #                             if not selectedbone.lock_rotation[axis]:
    #                                 if additiveMode:
    #                                     selectedbone.rotation_quaternion[axis + 1] = (
    #                                         blend
    #                                         * posebone.rotation_quaternion[axis + 1]
    #                                         + currentPoseRotation[axis + 1]
    #                                     )
    #                                 else:
    #                                     selectedbone.rotation_quaternion[axis + 1] = (
    #                                         blend
    #                                         * posebone.rotation_quaternion[axis + 1]
    #                                         + (1 - blend)
    #                                         * currentPoseRotation[axis + 1]
    #                                     )
    #                     # handle properties
    #                     for key in posebone.keys():
    #                         try:
    #                             propertyType = eval(
    #                                 "selectedbone." + key
    #                             ).__class__.__name__
    #                             if propertyType == "float":
    #                                 exec(
    #                                     "selectedbone."
    #                                     + key
    #                                     + " = blend * posebone."
    #                                     + key
    #                                     + " + (1-blend) * self.currentPose[selectedbone]."
    #                                     + key
    #                                 )
    #                             else:
    #                                 exec("selectedbone." + key + " = posebone." + key)
    #                         except:
    #                             try:
    #                                 propertyType = eval(
    #                                     'selectedbone["' + key + '"]'
    #                                 ).__class__.__name__
    #                                 if propertyType == "float":
    #                                     command = (
    #                                         'selectedbone["'
    #                                         + key
    #                                         + '"] = blend * posebone["'
    #                                         + key
    #                                         + '"]'
    #                                         + '+ (1-blend) * self.currentPose[selectedbone]["properties"]["'
    #                                         + key
    #                                         + '"]'
    #                                     )
    #                                     exec(command)
    #                                 else:
    #                                     exec(
    #                                         'selectedbone["'
    #                                         + key
    #                                         + '"] = posebone["'
    #                                         + key
    #                                         + '"]'
    #                                     )
    #                             except:
    #                                 print(
    #                                     "IMPOSSIBLE TO HANDLE PROPERTY "
    #                                     + key
    #                                     + " FOR "
    #                                     + selectedbone.name
    #                                 )
    #     except Exception as e:
    #         print("Blend Pose Exception : " + str(e))

    def delete(self):
        """Delete selected item"""
        # Confirm delete dialog
        path = self.item.path
        dialog = QtWidgets.QDialog(self)
        dialog.ui = YesNoDialog()
        dialog.ui.setupUi(dialog)
        message = (
            "Do you want to delete the "
            + self.item.itemType
            + " item "
            + self.item.name
            + " ?"
        )
        dialog.ui.label.setText(message)
        rsp = dialog.exec_()
        # if user clicks on 'ok'
        if rsp == QtWidgets.QDialog.Accepted:
            # Remember current tree selection
            selectedItemPath = self.mainWindow.currentTreeElement.path

            trashPath = os.path.join(self.mainWindow.rootPath, "../trash")
            if not os.path.exists(trashPath):
                os.makedirs(trashPath)
            trashPath = os.path.join(trashPath, os.path.basename(path))

            # clean info widget
            if self.movie is not None:
                self.thumbnailLabel.removeEventFilter(self)
                self.movie.setFileName("")
            layout = self.mainWindow.verticalLayout_5
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().deleteLater()

            # delete files
            copied = False
            attempts = 0
            while not copied:
                try:
                    shutil.copytree(path, trashPath)
                    copied = True
                except FileExistsError:
                    attempts += 1
                    try:
                        trashPath = (
                            trashPath.split(" Copy (")[0]
                            + " Copy ("
                            + str(attempts)
                            + ")"
                        )
                        shutil.copytree(path, trashPath)
                        copied = True
                    except:
                        pass
                except WindowsError as e:
                    attempts += 1
                    if str(e).startswith("[Error 183]"):
                        try:
                            trashPath = (
                                trashPath.split(" Copy (")[0]
                                + " Copy ("
                                + str(attempts)
                                + ")"
                            )
                            shutil.copytree(path, trashPath)
                            copied = True
                        except:
                            pass
                    else:
                        raise
            try:
                if self.item.itemType == "ANIMATION":
                    os.remove(os.path.join(path, "thumbnail.gif"))
                else:
                    os.remove(os.path.join(path, "thumbnail.png"))
            except Exception as e:
                if self.item.itemType == "ANIMATION":
                    QtWidgets.QMessageBox.about(
                        self,
                        "Abort action",
                        "Cannot remove "
                        + os.path.join(path, "thumbnail.gif")
                        + " : "
                        + str(e),
                    )
                else:
                    os.remove(os.path.join(path, "thumbnail.png"))
                return
            shutil.rmtree(path)

            # Remember expanded states in tree view
            expanded = self.mainWindow.getTreeExpandedItems()
            if self.item.itemType == "FOLDER":
                # Delete item from model
                itemPath = self.item.path
                model = self.mainWindow.treeModel
                treeItem = model.getElemWithPath(itemPath)
                if itemPath == selectedItemPath:
                    selectedItemPath = treeItem.parent.path
                # Remove item
                model.removeElement(treeItem)
                # Update filter
                self.mainWindow.updateTreeFilter()
                # Restore expand state and selected item
                self.mainWindow.restoreExpandedState(expanded, selectedItemPath)
            else:
                self.mainWindow.items = self.mainWindow.getListItems()
                self.mainWindow.setListView()

    def updateConstraintPairingList(self):
        """Update pairing list combobox"""
        comboList = [obj.name for obj in utils.getSelectedObjects()]
        for widget in self.pairWidgets:
            widget.armatureComboBox.clear()
            widget.armatureComboBox.addItems(comboList)
            # set index
            index = widget.armatureComboBox.findText(widget.objectName)
            if index >= 0:
                widget.armatureComboBox.setCurrentIndex(index)
            for constraintWidget in widget.constraintInfoWidgets:
                constraintWidget.comboBox.clear()
                constraintWidget.comboBox.addItems(comboList)
                index = constraintWidget.comboBox.findText(
                    constraintWidget.targetObject
                )
                if index >= 0:
                    constraintWidget.comboBox.setCurrentIndex(index)

    def selectBones(self):
        """Select bones listed in json file"""
        for file in os.listdir(self.item.path):
            if file.endswith(".json"):
                jsonPath = os.path.join(self.item.path, file)
        if self.item.itemType != "CONSTRAINT SET":
            utils.selectBones(jsonPath)
        else:
            pairingDict = self.getConstraintPairing()
            utils.selectConstraintBones(jsonPath, pairingDict)

    def getConstraintPairing(self):
        """Return dict of json object name and selected objet to which we want to apply the constraint(s)"""
        pairingDict = {}
        for widget in self.pairWidgets:
            objName = widget.objectName
            pairingDict[objName] = {}
            pairingDict[objName]["object"] = widget.armatureComboBox.currentText()
            pairingDict[objName]["constraints"] = {}
            for constraintWidget in widget.constraintInfoWidgets:
                consInfo = {
                    "sourceTarget": constraintWidget.targetObject,
                    "sourceTargetBone": constraintWidget.targetBone,
                    "destinationTarget": constraintWidget.comboBox.currentText(),
                    "destinationTargetBone": constraintWidget.targetBone,
                }
                pairingDict[objName]["constraints"][
                    constraintWidget.constraintName
                ] = consInfo
        return pairingDict

    def getItemDict(self):
        for file in os.listdir(self.item.path):
            if file.endswith(".json"):
                jsonPath = os.path.join(self.item.path, file)
                itemdata = {}
                with open(jsonPath) as file:
                    itemdata = json.load(file)
                    return itemdata

    def showInfos(self):
        """Display thumbnail and infos from json file"""
        self.parent.infoGroupBox.setTitle(self.item.itemType)
        self.nameLabel.setText(self.item.name)
        self.ownerLabel.setText(self.item.owner)
        self.dateLabel.setText(self.item.date)
        self.contentLabel.setText(self.item.content)
        self.thumbnailLabel.setPixmap((QtGui.QPixmap(self.thumbpath).scaled(200, 200)))
        self.frameRangeLabel.setText(self.item.frameRange)

        if not self.item.bonesSelection:
            self.selectBonesPushButton.setEnabled(False)
        # Set visibility of widgets
        if self.item.itemType == "POSE":
            self.selectionSetOptionsWidget.setVisible(False)
            self.label_5.setVisible(False)
            self.frameRangeLabel.setVisible(False)
            self.animOptionsWidget.setVisible(False)
            self.constraintOptionsGroupBox.setVisible(False)
            self.applyPushButton.setText("APPLY 100 %")
            # self.optionsGroupBox.setVisible(True)
            # self.poseOptionsWidget.setVisible(True)
            self.flippedCheckBox.setVisible(False)
            self.flippedCheckBox.setEnabled(False)
        elif self.item.itemType == "SELECTION SET":
            self.label_5.setVisible(False)
            self.frameRangeLabel.setVisible(False)
            self.animOptionsWidget.setVisible(False)
            self.constraintOptionsGroupBox.setVisible(False)
            self.poseOptionsWidget.setVisible(False)
            self.optionsGroupBox.setVisible(False)
            self.applyPushButton.setVisible(False)
            # self.selectionSetOptionsWidget.setVisible(True)
        elif self.item.itemType == "CONSTRAINT SET":
            self.selectionSetOptionsWidget.setVisible(False)
            self.label_5.setVisible(False)
            self.frameRangeLabel.setVisible(False)
            self.animOptionsWidget.setVisible(False)
            self.poseOptionsWidget.setVisible(False)
            self.optionsGroupBox.setVisible(False)
            # self.constraintOptionsGroupBox.setVisible(True)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(
                QtGui.QPixmap("icons/constraint.png"),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.applyPushButton.setIcon(icon1)
            # set objects pairing widgets
            self.pairWidgets = []
            comboList = [obj.name for obj in utils.getSelectedObjects()]
            for objName in self.item.objects:
                constraintDict = self.getItemDict()["constraintData"]

                item = PairingWidget(objName, comboList, constraintDict, parent=self)
                self.verticalLayout_3.addWidget(item)
                self.pairWidgets.append(item)

        elif self.item.itemType == "FOLDER":
            self.selectionSetOptionsWidget.setVisible(False)
            self.label_5.setVisible(False)
            self.frameRangeLabel.setVisible(False)
            self.animOptionsWidget.setVisible(False)
            self.constraintOptionsGroupBox.setVisible(False)
            self.poseOptionsWidget.setVisible(False)
            self.optionsGroupBox.setVisible(False)
            self.applyPushButton.setVisible(False)
            self.ownerLabel.setVisible(False)
            self.dateLabel.setVisible(False)
            self.contentLabel.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.selectBonesPushButton.setVisible(False)
        elif self.item.itemType == "ANIMATION":
            self.selectionSetOptionsWidget.setVisible(False)
            self.poseOptionsWidget.setVisible(False)
            # self.optionsGroupBox.setVisible(True)
            self.constraintOptionsGroupBox.setVisible(False)
            # self.label_5.setVisible(True)
            # self.frameRangeLabel.setVisible(True)
            # self.animOptionsWidget.setVisible(True)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(
                QtGui.QPixmap("icons/anim2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.applyPushButton.setIcon(icon1)
            # Set spin box options
            self.fromRangeSpinBox.valueChanged.connect(self.fromSpinBoxChanged)
            self.toRangeSpinBox.valueChanged.connect(self.toSpinBoxChanged)
            self.fromRangeSpinBox.setValue(int(self.item.frameRange.split("-")[0]))
            self.toRangeSpinBox.setValue(int(self.item.frameRange.split("-")[-1]))
            self.fromRangeSpinBox.setMinimum(int(self.item.frameRange.split("-")[0]))
            self.toRangeSpinBox.setMaximum(int(self.item.frameRange.split("-")[-1]))
            # Display animated thumbnail
            self.thumbnailLabel.installEventFilter(self)
            self.movie = QtGui.QMovie(self.thumbpath, QtCore.QByteArray(), self)
            self.movie.setScaledSize(QtCore.QSize(200, 200))
            self.movie.setCacheMode(QtGui.QMovie.CacheNone)
            self.movie.setSpeed(100)
            self.thumbnailLabel.setMovie(self.movie)
            self.movie.start()
            self.movie.stop()

    def fromSpinBoxChanged(self):
        """Keep consistancy between spinboxes"""
        if self.fromRangeSpinBox.value() > self.toRangeSpinBox.value():
            self.toRangeSpinBox.setValue(self.fromRangeSpinBox.value())
        if self.fromRangeSpinBox.value() < self.fromRangeSpinBox.minimum():
            self.fromRangeSpinBox.setValue(self.fromRangeSpinBox.minimum())
        elif self.fromRangeSpinBox.value() > self.toRangeSpinBox.maximum():
            self.fromRangeSpinBox.setValue(self.toRangeSpinBox.maximum())

    def toSpinBoxChanged(self):
        """Keep consistancy between spinboxes"""
        if self.fromRangeSpinBox.value() > self.toRangeSpinBox.value():
            self.fromRangeSpinBox.setValue(self.toRangeSpinBox.value())
        if self.toRangeSpinBox.value() > self.toRangeSpinBox.maximum():
            self.toRangeSpinBox.setValue(self.toRangeSpinBox.maximum())

    def eventFilter(self, obj, event):
        """Event filter to play movie when hovered"""
        if obj == self.thumbnailLabel and event.type() == QtCore.QEvent.Enter:
            if self.movie:
                self.movie.start()
        if obj == self.thumbnailLabel and event.type() == QtCore.QEvent.Leave:
            if self.movie:
                self.movie.stop()
        return super(GaoLibInfoWidget, self).eventFilter(obj, event)
