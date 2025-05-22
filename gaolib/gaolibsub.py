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


import getpass
import json
import os
import shutil
import sys
from datetime import datetime

from PIL import Image

try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtWidgets import QFileDialog

    USE_PYSIDE6 = False
except ModuleNotFoundError:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtWidgets import QFileDialog

    USE_PYSIDE6 = True

from gaolib.createposewidget import CreatePoseWidget
from gaolib.gaolibinfowidget import GaoLibInfoWidget
from gaolib.model.gaocustomlistview import GaoCustomListView
from gaolib.model.gaolibitem import GaoLibItem
from gaolib.model.gaoliblistmodel import GaoLibListModel
from gaolib.model.gaolibtreeitem import GaoLibTreeItem
from gaolib.model.gaolibtreeitemmodel import GaoLibTreeItemModel
from gaolib.model.rootitemwidget import RootItemWidget
from gaolib.model.treeitemfilterproxymodel import TreeItemFilterProxyModel
from gaolib.ui.gaolibui import Ui_MainWindow as GaolibMainWindow
from gaolib.ui.newfolderdialogui import Ui_Dialog as NewFolderDialog
from gaolib.ui.settingsdialogui import Ui_Dialog as SettingsDialog
from gaolib.ui.yesnodialogui import Ui_Dialog as YesNoDialog

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))

try:
    import bpy

    import gaolib.model.blenderutils as utils
    from gaolib.model.gifgenerator import generateGif
except Exception as e:
    print("IMPORT EXCEPTION : " + str(e))


class GaoLib(QtWidgets.QMainWindow, GaolibMainWindow):
    """GAOLIB Main window"""

    # Manage window resize
    resized = QtCore.Signal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

        # Set data variables
        self.currentTreeElement = None
        self.items = {}
        self.projName = ""
        self.rootPath = None
        self.rootList = []
        self.recursiveDisplayMode = False
        self.useDoubleClickToApplyPose = False
        self.useWheelToBlendPose = False
        self.listView = GaoCustomListView(parent=self)
        self.listView.setSpacing(10)
        self.listView.setMinimumSize(QtCore.QSize(50, 50))
        self.listView.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
            | QtWidgets.QAbstractItemView.EditKeyPressed
        )
        self.listView.setIconSize(QtCore.QSize(130, 130))
        self.listView.setResizeMode(QtWidgets.QListView.Fixed)
        self.listView.setViewMode(QtWidgets.QListView.IconMode)
        self.verticalLayout_2.addWidget(self.listView)
        self.initUi()
        if USE_PYSIDE6:
            self.settingsPushButton.setStyleSheet(
                "QPushButton::menu-indicator { width:0px; }"
            )
            self.newPushButton.setStyleSheet(
                "QPushButton::menu-indicator { width:0px; }"
            )
        self._connectUi()

    def _connectUi(self):
        # Connect Actions
        self.resized.connect(self.setListView)
        self.searchHierarchyEdit.textChanged.connect(self.filterTree)
        self.searchEdit.textChanged.connect(self.filterList)
        # Set menus for buttons in the main window
        self.createMenuNew()
        self.createMenuSettings()

    def createMenuNew(self):
        """Create items functionnalities"""
        iconFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        createMenu = QtWidgets.QMenu(self.newPushButton)
        poseIcon = QtGui.QIcon(QtGui.QPixmap(os.path.join(iconFolder, "pose2.png")))
        createMenu.addAction(poseIcon, "New Pose", lambda: self.createItemSetUI("POSE"))
        animIcon = QtGui.QIcon(QtGui.QPixmap(os.path.join(iconFolder, "anim2.png")))
        createMenu.addAction(animIcon, "New Animation", self.createAnimSetUI)
        constraintIcon = QtGui.QIcon(
            QtGui.QPixmap(os.path.join(iconFolder, "constraint.png"))
        )
        createMenu.addAction(
            constraintIcon,
            "New Constraint Set",
            lambda: self.createItemSetUI("CONSTRAINT SET"),
        )
        selectIcon = QtGui.QIcon(
            QtGui.QPixmap(os.path.join(iconFolder, "selectionset.png"))
        )
        createMenu.addAction(
            selectIcon,
            "New Selection Set",
            lambda: self.createItemSetUI("SELECTION SET"),
        )
        folderIcon = QtGui.QIcon(QtGui.QPixmap(os.path.join(iconFolder, "folder2.png")))
        createMenu.addAction(folderIcon, "New Folder", self.createFolder)
        self.newPushButton.setMenu(createMenu)

    def createMenuSettings(self):
        """Create settings menu"""
        # Settings functionnalities
        createMenu = QtWidgets.QMenu(self.settingsPushButton)
        createMenu.addAction("Settings", self.settings)
        refreshAction = createMenu.addAction("Refresh central view", self.setListView)
        refreshAction.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        self.settingsPushButton.setMenu(createMenu)

    def readConfig(self):
        """Read Json config"""
        self.rootList = []
        self.rootPath = None
        if os.path.exists(self.configPath):
            with open(self.configPath) as file:
                itemdata = json.load(file)
                self.rootList = itemdata["rootpath"]
                if "recursiveDisplayMode" in itemdata.keys():
                    self.recursiveDisplayMode = itemdata["recursiveDisplayMode"]
                else:
                    self.recursiveDisplayMode = False
                if "useWheelToBlendPose" in itemdata.keys():
                    self.useWheelToBlendPose = itemdata["useWheelToBlendPose"]
                else:
                    self.useWheelToBlendPose = False
                if "useDoubleClickToApplyPose" in itemdata.keys():
                    self.useDoubleClickToApplyPose = itemdata[
                        "useDoubleClickToApplyPose"
                    ]
                else:
                    self.useDoubleClickToApplyPose = False

    def settings(self):
        """Manage change of ROOT folder location"""
        # creates the dialog
        dialog = QtWidgets.QDialog(self)
        dialog.ui = SettingsDialog()
        dialog.ui.setupUi(dialog)

        dialog.ui.pathLineEdit.setText("")
        table = dialog.ui.tableWidget
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Read config
        if os.path.isfile(self.configPath):
            with open(self.configPath) as file:
                itemdata = json.load(file)
            for key in itemdata.keys():
                if key == "rootpath":
                    for e in itemdata[key]:
                        rtname = e["name"]
                        rtpath = e["path"]
                        row = table.rowCount()
                        itemWidget = RootItemWidget(rtname, rtpath, self.configPath)
                        table.insertRow(row)
                        table.setCellWidget(row, 0, itemWidget)
                if key == "recursiveDisplayMode":
                    dialog.ui.recursiveListModeCheckBox.setChecked(itemdata[key])
                if key == "useWheelToBlendPose":
                    dialog.ui.blendPoseOnWheelCheckBox.setChecked(itemdata[key])
                if key == "useDoubleClickToApplyPose":
                    dialog.ui.doubleClickPoseShortcutCheckBox.setChecked(itemdata[key])
        # File browser
        dialog.ui.browsePushButton.released.connect(
            lambda: self.openFileNameDialog(dialog)
        )
        rsp = dialog.exec_()
        # retrieve editLine infos from the dialog
        path = dialog.ui.pathLineEdit.text()
        pathName = dialog.ui.lineEdit.text()
        recursiveDisplayMode = dialog.ui.recursiveListModeCheckBox.isChecked()
        useWheelToBlendPose = dialog.ui.blendPoseOnWheelCheckBox.isChecked()
        useDoubleClickToApplyPose = (
            dialog.ui.doubleClickPoseShortcutCheckBox.isChecked()
        )
        # The user clicks OK
        if rsp == QtWidgets.QDialog.Accepted:
            self.readConfig()
            paramsChanged = (
                recursiveDisplayMode != self.recursiveDisplayMode
                or useWheelToBlendPose != self.useWheelToBlendPose
                or useDoubleClickToApplyPose != self.useDoubleClickToApplyPose
            )
            if not len(path):
                if paramsChanged:
                    # remember setting
                    with open(self.configPath, "w") as file:
                        json.dump(
                            {
                                "rootpath": self.rootList,
                                "recursiveDisplayMode": recursiveDisplayMode,
                                "useWheelToBlendPose": useWheelToBlendPose,
                                "useDoubleClickToApplyPose": useDoubleClickToApplyPose,
                            },
                            file,
                            indent=4,
                            sort_keys=True,
                        )
            else:
                createRoot = False
                newRootItem = {"path": path, "name": pathName}
                try:
                    if os.path.exists(path):
                        for e in self.rootList:
                            if e["path"] == path:
                                QtWidgets.QMessageBox.about(
                                    self,
                                    "Abort action",
                                    "Path already in root list :" + path,
                                )
                                self.setTreeView()
                                return
                        # Change the ROOT location
                        self.rootList.append(newRootItem)
                        if "ROOT" not in os.listdir(path):
                            createRoot = True
                            os.mkdir(os.path.join(path, "ROOT"))
                        # remember setting
                        with open(self.configPath, "w") as file:
                            json.dump(
                                {
                                    "rootpath": self.rootList,
                                    "recursiveDisplayMode": recursiveDisplayMode,
                                    "useWheelToBlendPose": useWheelToBlendPose,
                                    "useDoubleClickToApplyPose": useDoubleClickToApplyPose,
                                },
                                file,
                                indent=4,
                                sort_keys=True,
                            )
                    else:
                        QtWidgets.QMessageBox.about(
                            self, "Abort action", "Path does not exist " + path
                        )

                except WindowsError as e:
                    # if errors occure, set back the old ROOT location
                    if createRoot and not len(os.listdir(os.path.join(path, "ROOT"))):
                        os.rmdir(os.path.join(path, "ROOT"))
                    QtWidgets.QMessageBox.about(
                        self, "Abort action", "Access denied to path " + path
                    )
                    with open(self.configPath, "w") as file:
                        json.dump(
                            {
                                "rootpath": self.rootList,
                                "recursiveDisplayMode": self.recursiveDisplayMode,
                                "useWheelToBlendPose": self.useWheelToBlendPose,
                                "useDoubleClickToApplyPose": self.useDoubleClickToApplyPose,
                            },
                            file,
                            indent=4,
                            sort_keys=True,
                        )

        self.currentTreeElement = None
        self.setTreeView()

    def openFileNameDialog(self, dialog, openDirectory=None):
        """File browser to change the ROOT location"""
        fileDialog = QFileDialog(self)
        if USE_PYSIDE6:
            fileDialog.setFileMode(QFileDialog.Directory)
        else:
            fileDialog.setFileMode(QFileDialog.DirectoryOnly)
            options = fileDialog.Options()
        if openDirectory:
            openDirectory = os.path.realpath(openDirectory)
            fileDialog.setDirectory(os.path.dirname(openDirectory))
        directory = fileDialog.getExistingDirectory(self)
        if directory:
            directory = os.path.realpath(directory)
            if not openDirectory:
                dialog.ui.pathLineEdit.setText(directory)
            # Modifying an item path
            elif openDirectory:
                rootPaths = [
                    os.path.realpath(os.path.join(root["path"], "ROOT"))
                    for root in self.rootList
                ]
                foundRoot = False
                for rootPath in rootPaths:
                    if os.path.commonprefix([directory, rootPath]) == rootPath:
                        foundRoot = True
                        break
                if not foundRoot:
                    QtWidgets.QMessageBox.about(
                        self,
                        "Wrong Path",
                        "Chosen path must start with one of these known ROOT paths :\n\n"
                        + "\n".join(rootPaths),
                    )
                elif os.path.commonprefix([openDirectory, directory]) == openDirectory:
                    QtWidgets.QMessageBox.about(
                        self,
                        "Wrong Path",
                        "Parent path cannot include current folder path !",
                    )
                elif (
                    ".anim" in directory
                    or ".selection" in directory
                    or ".pose" in directory
                    or ".constraint" in directory
                ):
                    QtWidgets.QMessageBox.about(
                        self,
                        "Wrong Path",
                        "Parent path cannot be in an .anim/.pose/.selection/.constraint folder !",
                    )
                else:
                    dialog.ui.pathLineEdit.setText(directory)

    def createFolder(self):
        """Create new folder functionnality"""
        # creates the dialog
        dialog = QtWidgets.QDialog(self)
        dialog.ui = NewFolderDialog()
        dialog.ui.setupUi(dialog)

        thumbpath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "icons/folder2.png"
        )
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
        dialog.ui.pathLineEdit.setText(self.currentTreeElement.path.replace("\\", "/"))
        rsp = dialog.exec_()
        # retrieve editLine infos from the dialog
        name = dialog.ui.lineEdit.text()
        # if user clicks on 'ok'
        if rsp == QtWidgets.QDialog.Accepted:
            if name.replace(" ", "") != "":
                folderPath = os.path.join(self.currentTreeElement.path, name)
                # Check if the folder already exists
                if os.path.exists(folderPath):
                    QtWidgets.QMessageBox.about(
                        self, "Abort action", "Folder already exists : " + folderPath
                    )
                else:
                    # Remember expanded states in tree view
                    expanded = self.getTreeExpandedItems()
                    # Creates new folder and add it to the hierachy
                    os.mkdir(folderPath)
                    parentItem = self.currentTreeElement
                    selectedItemPath = parentItem.path
                    ancestors = parentItem.ancestors + [parentItem]
                    ancestorNames = []
                    for ances in ancestors:
                        ancestorNames.append(ances.name)

                    path = os.path.join(parentItem.path, name)
                    # Copy thumbnail
                    folderIconPath = os.path.join(
                        folderIcons, dialog.ui.iconComboBox.currentText()
                    )
                    if os.path.isfile(folderIconPath):
                        thumbnailPath = os.path.join(path, "thumbnail.png")
                        shutil.copyfile(folderIconPath, thumbnailPath)
                    newItem = GaoLibTreeItem(name, ancestors=ancestors, path=path)

                    # refresh TreeView
                    self.treeModel.addElement(newItem, parentItem)

                    # Update filter
                    self.updateTreeFilter()
                    # Restore expand state and selected item
                    self.restoreExpandedState(expanded, selectedItemPath)
            else:
                QtWidgets.QMessageBox.about(
                    self, "Abort action", "Folder name must not be empty."
                )

    def restoreExpandedState(self, expanded, selectedItemPath):
        """Expand items corresponding to given list of treeModel item indexes"""
        for idx in expanded:
            mappedIdx = self.treeItemProxyModel.mapFromSource(idx)
            self.hierarchyTreeView.expand(mappedIdx)
            # Restore current selection
            elem = self.treeModel.getElement(idx)
            if elem.path == selectedItemPath:
                self.treeSelectionModel.clear()
                self.treeSelectionModel.select(
                    mappedIdx, QtCore.QItemSelectionModel.Select
                )

    def getTreeExpandedItems(self):
        """Get list of index of expanded items in TreeView"""
        # Get all proxy filter indexes
        proxyIndexes = []
        allIndexes = self.treeModel.getAllIndexes(
            currentElem=None, currentIdx=QtCore.QModelIndex(), indexes=[]
        )
        for idx in allIndexes:
            mapped = self.treeItemProxyModel.mapFromSource(idx)
            proxyIndexes.append(mapped)

        # Check expand state in treeview for each proxy filter index
        expandedIndexes = []
        for idx in proxyIndexes:
            if self.hierarchyTreeView.isExpanded(idx):
                mappedIdx = idx.model().mapToSource(idx)
                expandedIndexes.append(mappedIdx)
            elif idx == self.hierarchyTreeView.selectionModel().currentIndex():
                mappedIdx = idx.model().mapToSource(idx)
                expandedIndexes.append(mappedIdx)
        return expandedIndexes

    def cleanTempFolder(self):
        if os.path.exists(self.jsonTempPath):
            os.remove(self.jsonTempPath)
        if os.path.exists(self.thumbTempPath):
            os.remove(self.thumbTempPath)
        sequencePath = os.path.join(os.path.dirname(self.thumbTempPath), "sequence")
        if os.path.exists(sequencePath):
            shutil.rmtree(sequencePath)
        os.makedirs(sequencePath)

    def createGenericItemSetUI(self):
        """Prepare UI to create new animation/pose/selection/constraint set item"""
        # Temporary path for thumnail
        self.thumbTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "thumbnail.png",
        )
        self.jsonTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "temp.json",
        )
        # # Delete files before creating new item
        self.cleanTempFolder()
        # Clear information layout
        for i in reversed(range(self.verticalLayout_5.count())):
            self.verticalLayout_5.itemAt(i).widget().deleteLater()

    def createAnimSetUI(self):
        """Prepare UI to Create new animation item"""
        itemType = "ANIMATION"
        self.createGenericItemSetUI()
        # Create widget for create anim
        self.createPosewidget = CreatePoseWidget(itemType=itemType, parent=self)
        self.verticalLayout_5.addWidget(self.createPosewidget)

        self.beginCreateThumb = True  # remember step of createThumbnail
        self.createPosewidget.pushButton.released.connect(
            lambda: self.createThumbnail(itemType=itemType)
        )
        self.createPosewidget.applyPushButton.released.connect(
            lambda: self.savePose(itemType=itemType)
        )
        self.createPosewidget.fromRangeSpinBox.setProperty(
            "value", bpy.context.scene.frame_start
        )
        self.createPosewidget.toRangeSpinBox.setProperty(
            "value", bpy.context.scene.frame_end
        )
        try:
            selectedObjs = utils.getSelectedObjects()
            if len(selectedObjs):
                selectedObj = selectedObjs[0]
                if selectedObj.animation_data and selectedObj.animation_data.action:
                    self.createPosewidget.nameLineEdit.setText(
                        selectedObj.animation_data.action.name.replace(".", "_")
                    )
        except Exception as e:
            print("Automatic name setting failed : " + str(e))

    def createItemSetUI(self, itemType):
        """Prepare UI to Create new pose item"""
        self.createGenericItemSetUI()
        # Create widget for create pose
        self.createPosewidget = CreatePoseWidget(itemType=itemType, parent=self)
        self.verticalLayout_5.addWidget(self.createPosewidget)

        self.beginCreateThumb = True  # remember step of createThumbnail
        self.createPosewidget.pushButton.released.connect(
            lambda: self.createThumbnail(itemType=itemType)
        )
        self.createPosewidget.applyPushButton.released.connect(
            lambda: self.savePose(itemType=itemType)
        )

    def savePose(self, itemType="POSE"):
        """Save a new item in the library"""
        if itemType == "ANIMATION":
            itemTypeStr = "anim"
            thumbTempPath = self.thumbTempPath.replace(".png", ".gif")
            stamp = "icons/anim2.png"
        elif itemType == "POSE":
            itemTypeStr = "pose"
            thumbTempPath = self.thumbTempPath
            stamp = "icons/pose2.png"
        elif itemType == "SELECTION SET":
            itemTypeStr = "selection"
            thumbTempPath = self.thumbTempPath
            stamp = "icons/selectionset.png"
        elif itemType == "CONSTRAINT SET":
            itemTypeStr = "constraint"
            thumbTempPath = self.thumbTempPath
            stamp = "icons/constraint.png"

        # Check if valid name
        name = self.createPosewidget.nameLineEdit.text()
        if name.replace(" ", "") != "":
            name = name.replace(" ", "_") + "." + itemTypeStr
        else:
            QtWidgets.QMessageBox.about(
                self,
                "Abort action",
                "Cannot save " + itemTypeStr + ', Invalid name : "' + name + '".',
            )
            return
        # Check if thumbnail exists
        if not os.path.exists(thumbTempPath):
            QtWidgets.QMessageBox.about(
                self,
                "Abort action",
                "Cannot save " + itemTypeStr + ", Please create one.",
            )
            return
        # Create pose directory
        parentDir = self.currentTreeElement.path
        poseDir = os.path.join(parentDir, name)
        # Check if item with same name already exists
        if os.path.exists(poseDir):
            dialog = QtWidgets.QDialog(self)
            dialog.ui = YesNoDialog()
            dialog.ui.setupUi(dialog)
            message = (
                " An item named "
                + name
                + " already exists. Do you want to overrite this file ?"
            )
            dialog.ui.label.setText(message)
            rsp = dialog.exec_()
            # if user clicks on 'ok'
            if rsp == QtWidgets.QDialog.Accepted:
                if itemType == "ANIMATION":
                    try:
                        os.remove(os.path.join(poseDir, "thumbnail.gif"))
                    except Exception as e:
                        QtWidgets.QMessageBox.about(
                            self,
                            "Abort action",
                            "Cannot remove "
                            + os.path.join(poseDir, "thumbnail.gif")
                            + " : "
                            + str(e),
                        )
                        return
                shutil.rmtree(poseDir)
            else:
                return
        try:
            os.mkdir(poseDir)
        except OSError as e:
            print("OSError : " + str(e))
            QtWidgets.QMessageBox.about(
                self,
                "Abort action",
                "Cannot save " + itemTypeStr + ', Invalid name : "' + name + '".',
            )
            return
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "Abort action", "ERROR : " + str(e))
            print("ERROR : " + str(e))
            return

        # Copy thumbnail in pose directory
        if itemType == "ANIMATION":
            pngThumb = os.path.join(poseDir, "thumbnail.png")
            tempPngDir = os.path.join(os.path.dirname(self.thumbTempPath), "sequence")
            tempPng = None
            if os.path.isdir(tempPngDir):
                if len(os.listdir(tempPngDir)):
                    tempPng = os.path.join(tempPngDir, os.listdir(tempPngDir)[0])
            if tempPng:
                shutil.copyfile(tempPng, pngThumb)

            thumbPath = os.path.join(poseDir, "thumbnail.gif")
            shutil.copyfile(thumbTempPath, thumbPath)
            # Copy blend in pose directory
            utils.copyAnim(poseDir)
        elif itemType == "POSE":
            thumbPath = os.path.join(poseDir, "thumbnail.png")
            shutil.copyfile(thumbTempPath, thumbPath)
            # Copy blend in pose directory
            utils.copyPose(poseDir)
        elif itemType == "SELECTION SET":
            thumbPath = os.path.join(poseDir, "thumbnail.png")
            shutil.copyfile(thumbTempPath, thumbPath)
        elif itemType == "CONSTRAINT SET":
            thumbPath = os.path.join(poseDir, "thumbnail.png")
            shutil.copyfile(thumbTempPath, thumbPath)

        # Add stamp on thumbnail
        try:
            pngThumb = os.path.join(poseDir, "thumbnail.png")
            im1 = Image.open(pngThumb)
            im2 = Image.open(stamp)
            im2 = im2.resize((30, 30))
            im1.paste(im2, (165, 170), im2)
            destination = os.path.join(poseDir, "thumbnail_stamped.png")
            im1.save(destination, quality=100)

        except Exception as e:
            print("Stamp Exception : " + str(e))

        # Create json in pose directory
        self.writejson(name, poseDir, itemType=itemType)

        # Refresh view
        oldItems = self.items
        self.items = self.getListItems()
        self.setListView()

        # Find new item
        newIndex = None
        for item in self.items.keys():
            if self.items[item].name == name:
                newIndex = item
                break
        # disconnect pushbutton
        if self.createPosewidget.movie is not None:
            self.createPosewidget.movie.setFileName("")
        # Select newItem
        index = self.listView.model().index(newIndex, 0)
        self.listView.selectionModel().clear()
        self.listView.selectionModel().select(index, QtCore.QItemSelectionModel.Select)

    def applyPose(self, itemType="POSE", flipped=False, blendPose=1, currentPose=None):
        """Paste animation/pose from the library to the selected object of the scene"""
        try:
            if itemType == "ANIMATION":
                frameIn = self.infoWidget.fromRangeSpinBox.value()
                frameOut = self.infoWidget.toRangeSpinBox.value()
                utils.pasteAnim(
                    self.currentListItem.path, frameIn, frameOut, self.infoWidget
                )
            elif itemType == "CONSTRAINT SET":
                pairingDict = self.infoWidget.getConstraintPairing()
                utils.pasteConstraints(self.currentListItem.path, pairingDict)
            elif itemType == "POSE":
                if not blendPose:
                    blendPose = 1
                if self.infoWidget.refPose:
                    refPose = self.infoWidget.refPose
                    utils.deleteRefPose(refPose, self.infoWidget)
                utils.pastePose(
                    self.currentListItem.path,
                    flipped=flipped,
                    blend=blendPose,
                    currentPose=currentPose,
                    additiveMode=self.infoWidget.additiveModeCheckBox.isChecked(),
                )
        except Exception as e:
            QtWidgets.QMessageBox.about(
                self, "Abort action", "An error has occured, check Console : " + str(e)
            )
            raise
        # Reset currentPose to applied one
        self.infoWidget.currentPose = None
        self.infoWidget.bonesToBlend = None
        self.infoWidget.blendPoseSlider.setValue(0)

    def writejson(self, name, directory, itemType="POSE"):
        """Create json file corresponding to pose/animation item"""
        if itemType == "ANIMATION":
            jsonFile = os.path.join(directory, "animation.json")
        elif itemType == "POSE":
            jsonFile = os.path.join(directory, "pose.json")
        elif itemType == "SELECTION SET":
            jsonFile = os.path.join(directory, "selection_set.json")
        elif itemType == "CONSTRAINT SET":
            jsonFile = os.path.join(directory, "constraint_set.json")

        if os.path.exists(self.jsonTempPath):
            with open(self.jsonTempPath) as file:
                itemdata = json.load(file)

        if os.path.exists(jsonFile):
            os.remove(jsonFile)
        date = datetime.now().strftime("%d/%m/%Y")
        # gather the datas
        data = {
            "metadata": {
                "name": name,
                "boneNames": itemdata["boneNames"],
                "objects": itemdata["objects"],
                "type": itemType,
                "user": getpass.getuser(),
                "date": date,
                "content": self.createPosewidget.contentLabel.text(),
                "frameRange": str(self.createPosewidget.fromRangeSpinBox.value())
                + "-"
                + str(self.createPosewidget.toRangeSpinBox.value()),
            }
        }
        for key in itemdata.keys():
            if key == "constraintData":
                data[key] = itemdata[key]
            elif key not in data["metadata"].keys():
                data["metadata"][key] = itemdata[key]
        # write json
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def contextCheck(self, itemType):
        """Check if context and selections are compatible with the creation of item"""
        # Check that a temporary path is set
        if not os.path.exists(bpy.context.preferences.filepaths.temporary_directory):
            utils.ShowDialog(
                "Please add a valid path for Blender temporary files in : Edit > Preferences > File Paths > Temporary Files",
                title="Abort action",
            )
            return
        # Check area (VIEW_3D exists)
        foundSpace = False
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space == self.context["space_data"]:
                        foundSpace = True
        if not foundSpace:
            utils.ShowDialog('Context is lost ! Please, use "Get Context" tool.')
            return False
        # set context with self.context
        with bpy.context.temp_override(
            area=self.context["area"],
            region=self.context["region"],
            region_data=self.context["region_data"],
            screen=self.context["screen"],
            space_data=self.context["space_data"],
            window=self.context["window"],
        ):
            # Check number of selected objects
            selectedObjects = []
            for o in bpy.context.selected_objects:
                selectedObjects.append(o.name)
            if itemType == "CONSTRAINT SET":
                # # constraint set need at least one object selected
                if len(selectedObjects) == 0:
                    utils.ShowDialog("PLEASE, SELECT AT LEAST ONE OBJECT.")
                    return False
            else:
                # # animation, pose and selection set need nly one objet selected
                if len(selectedObjects) != 1:
                    utils.ShowDialog("PLEASE, SELECT EXACTLY ONE OBJECT.")
                    return False
            # Check POSE mode
            if bpy.context.object.mode != "POSE":
                utils.ShowDialog("PLEASE, SET POSE MODE.")
                return False
            # Count bones
            if not len(bpy.context.selected_pose_bones):
                utils.ShowDialog("PLEASE, SELECT AT LEAST ONE BONE.")
                return False
        return True

    def poseCreateThumbnail(self):
        """Save new item datas and thumbnail to temp directory"""
        # Get selectd object
        selectedObjects = []
        for o in bpy.context.selected_objects:
            selectedObjects.append(o.name)
        # Write Json file
        data = {
            "bones": len(bpy.context.selected_pose_bones),
            "boneNames": [bone.name for bone in bpy.context.selected_pose_bones],
            "objects": selectedObjects,
        }
        jsonFile = os.path.join(
            os.path.dirname(bpy.context.scene.render.filepath), "temp.json"
        )
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
        # Copy selection
        bpy.ops.pose.copy()
        # hide some overlays before rendering
        space = bpy.context.space_data
        space.overlay.show_overlays = False
        # Render
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=False, write_still=True)

    def animCreateThumbnail(self):
        """Save new item datas and thumbnail to temp directory"""
        # get frame range
        frameIn = bpy.context.scene.frame_start
        frameOut = bpy.context.scene.frame_end
        # Get selectd object
        selectedObjects = []
        for o in bpy.context.selected_objects:
            selectedObjects.append(o.name)
        # Write Json file
        data = {
            "bones": len(bpy.context.selected_pose_bones),
            "boneNames": [bone.name for bone in bpy.context.selected_pose_bones],
            "objects": selectedObjects,
        }
        jsonFile = os.path.join(
            os.path.dirname(os.path.dirname(bpy.context.scene.render.filepath)),
            "temp.json",
        )
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
        # Copy Animation
        currentObject = bpy.context.selected_objects[0]
        try:
            currentAction = currentObject.animation_data.action
        except:
            utils.ShowDialog("FOUND NO ACTION ON SELECTED OBJECT.", title="ABORT")
            return
        newAction = currentAction.copy()
        newAction.name = "Animation"
        currentObject.animation_data.action = None
        currentObject.animation_data.action = newAction
        # key first frame
        bpy.context.scene.frame_set(frameIn)
        for bone in bpy.context.selected_pose_bones:
            bone.keyframe_insert(data_path="rotation_mode", frame=frameIn)
            for axis in range(3):
                if not bone.lock_location[axis]:
                    bone.keyframe_insert(
                        data_path="location", index=axis, frame=frameIn
                    )
                if not bone.lock_rotation[axis]:
                    bone.keyframe_insert(
                        data_path="rotation_euler", index=axis, frame=frameIn
                    )
                if not bone.lock_scale[axis]:
                    bone.keyframe_insert(data_path="scale", index=axis, frame=frameIn)
            for key in bone.keys():
                try:
                    bone.keyframe_insert(data_path='["' + key + '"]', frame=frameIn)
                except Exception as e:
                    pass
        keyLastFrame = self.createPosewidget.keyLastCheckBox.isChecked()
        if keyLastFrame:
            bpy.context.scene.frame_set(frameOut)
            for bone in bpy.context.selected_pose_bones:
                bone.keyframe_insert(data_path="rotation_mode", frame=frameOut)
                for axis in range(3):
                    if not bone.lock_location[axis]:
                        bone.keyframe_insert(
                            data_path="location", index=axis, frame=frameOut
                        )
                    if not bone.lock_rotation[axis]:
                        bone.keyframe_insert(
                            data_path="rotation_euler", index=axis, frame=frameOut
                        )
                    if not bone.lock_scale[axis]:
                        bone.keyframe_insert(
                            data_path="scale", index=axis, frame=frameOut
                        )
                for key in bone.keys():
                    try:
                        bone.keyframe_insert(
                            data_path='["' + key + '"]', frame=frameOut
                        )
                    except Exception as e:
                        pass
        # Create animation.blend file
        animDir = bpy.context.preferences.filepaths.temporary_directory
        filename = "animation.blend"
        filepath = os.path.join(animDir, filename)
        bpy.data.libraries.write(filepath, set([newAction]))
        # hide some overlays before rendering
        space = bpy.context.space_data
        space.overlay.show_overlays = False
        # Render
        print("Render animation")
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=True, write_still=True)
        # Delete temp action
        currentObject.animation_data.action = currentAction
        bpy.data.actions.remove(newAction)

    def constraintCreateThumbnail(self):
        """Save new item datas and thumbnail to temp directory"""
        # Get selected objects
        selectedObjects = []
        for o in bpy.context.selected_objects:
            selectedObjects.append(o.name)
        # get contraint datas
        boneDict = {}
        for objName in selectedObjects:
            obj = bpy.data.objects.get(objName)
            if obj.pose:
                for bone in bpy.context.selected_pose_bones:
                    for objBone in obj.pose.bones:
                        if bone == objBone:
                            if not obj.name in boneDict.keys():
                                boneDict[obj.name] = []
                            boneDict[obj.name].append(bone.name)
                            break

        data = {
            "bones": len(bpy.context.selected_pose_bones),
            "boneDict": boneDict,
            "boneNames": [bone.name for bone in bpy.context.selected_pose_bones],
            "objects": selectedObjects,
        }
        constraintData = utils.getConstraintsForSelection()
        if not constraintData:
            utils.ShowDialog("Found no constraint data.", title="ABORT")
            return
        data["constraintData"] = constraintData
        # Write Json file
        jsonFile = os.path.join(
            os.path.dirname(bpy.context.scene.render.filepath), "temp.json"
        )
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
        # Render
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=False, write_still=True)

    def selectionCreateThumbnail(self):
        """Save new item datas and thumbnail to temp directory"""
        # Get selected objects
        selectedObjects = []
        for o in bpy.context.selected_objects:
            selectedObjects.append(o.name)
        # Write Json file
        data = {
            "bones": len(bpy.context.selected_pose_bones),
            "boneNames": [bone.name for bone in bpy.context.selected_pose_bones],
            "objects": selectedObjects,
        }
        jsonFile = os.path.join(
            os.path.dirname(bpy.context.scene.render.filepath), "temp.json"
        )
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)
        # hide some overlays before rendering
        space = bpy.context.space_data
        overlayHide = ["show_axis_x", "show_axis_y", "show_floor"]
        overlayHidden = []
        for toHide in overlayHide:
            isVisible = eval("space.overlay." + toHide)
            if isVisible:
                exec("space.overlay." + toHide + " = False")
                overlayHidden.append(toHide)
        # Render
        bpy.ops.render.opengl("INVOKE_DEFAULT", animation=False, write_still=True)

    def createThumbnail(self, itemType="POSE"):
        """Create item thumbnail and prepare to save as new item"""
        # Clean any existing temp files
        self.cleanTempFolder()
        # check context and selection
        isValid = self.contextCheck(itemType)
        if not isValid:
            return
        # Set temporary paths to store thumbnail and item datas
        self.thumbTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "thumbnail.png",
        )
        self.jsonTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory, "temp", "temp.json"
        )
        if not os.path.isdir(os.path.dirname(self.jsonTempPath)):
            os.makedirs(os.path.dirname(self.jsonTempPath))
        # PRE RENDER SETTINGS
        if itemType == "ANIMATION":
            self.createPosewidget.movie = None
            renderpath = os.path.join(
                os.path.dirname(self.thumbTempPath),
                "sequence",
                "thumbnail.####.png",
            )
        else:
            renderpath = self.thumbTempPath
        # Remember current render settings
        self.renderPath = bpy.context.scene.render.filepath
        self.renderFormat = bpy.context.scene.render.image_settings.file_format
        self.frameStep = bpy.context.scene.frame_step
        self.frameStart = bpy.context.scene.frame_start
        self.frameEnd = bpy.context.scene.frame_end
        self.xres = bpy.context.scene.render.resolution_x
        self.yres = bpy.context.scene.render.resolution_y
        self.use_stamp = bpy.context.scene.render.use_stamp
        self.color_mode = bpy.context.scene.render.image_settings.color_mode
        # Modify render settings
        bpy.context.scene.render.filepath = renderpath
        bpy.context.scene.render.image_settings.file_format = "PNG"
        bpy.context.scene.render.use_stamp = False
        bpy.context.scene.render.image_settings.color_mode = "RGB"

        bpy.context.scene.render.resolution_x = 200
        bpy.context.scene.render.resolution_y = 200
        if itemType == "ANIMATION":
            bpy.context.scene.frame_step = self.createPosewidget.spinBox.value()
            bpy.context.scene.frame_start = (
                self.createPosewidget.fromRangeSpinBox.value()
            )
            bpy.context.scene.frame_end = self.createPosewidget.toRangeSpinBox.value()
        # set context with self.context before calling blender operations
        with bpy.context.temp_override(
            area=self.context["area"],
            region=self.context["region"],
            region_data=self.context["region_data"],
            screen=self.context["screen"],
            space_data=self.context["space_data"],
            window=self.context["window"],
        ):
            if itemType == "POSE":
                self.poseCreateThumbnail()
            elif itemType == "ANIMATION":
                self.animCreateThumbnail()
            elif itemType == "CONSTRAINT SET":
                self.constraintCreateThumbnail()
            elif itemType == "SELECTION SET":
                self.selectionCreateThumbnail()
        # Wait for end of render to call createThumbnailEnd
        bpy.app.timers.register(
            lambda: self.createThumbnailEnd(itemType=itemType), first_interval=0.1
        )

    def createThumbnailEnd(self, itemType="POSE"):
        """Second click on the create thumbnail button,create item files"""
        # Chec if render is done before ending
        lastFrame = bpy.context.scene.render.filepath.replace(
            ".####.", "." + format(bpy.context.scene.frame_end, "04d") + "."
        )
        lastFrameList = []
        for i in range(bpy.context.scene.frame_step):
            lastFrameList.append(
                bpy.context.scene.render.filepath.replace(
                    ".####.", "." + format(bpy.context.scene.frame_end + i, "04d") + "."
                )
            )
        foundLastFrame = False
        for lastFramePath in lastFrameList:
            if os.path.exists(lastFramePath):
                foundLastFrame = True
                break
        if not foundLastFrame:
            # Try again in 0.5 sec
            print("Wait for " + lastFrame)
            return 0.5
        # Reset overlays
        try:
            with bpy.context.temp_override(
                area=self.context["area"],
                region=self.context["region"],
                region_data=self.context["region_data"],
                screen=self.context["screen"],
                space_data=self.context["space_data"],
                window=self.context["window"],
            ):
                if itemType in ["ANIMATION", "POSE"]:
                    bpy.context.space_data.overlay.show_overlays = True
                elif itemType == "SELECTION SET":
                    bpy.ops.development.show_overlay_params()
        except Exception as e:
            print("Could not set the overlay parameters")

        itemdata = {}
        # Read Json Datas
        if os.path.exists(self.jsonTempPath):
            with open(self.jsonTempPath) as file:
                itemdata = json.load(file)
        if itemType != "CONSTRAINT SET":
            if "objects" in itemdata.keys():
                if len(itemdata["objects"]) != 1:
                    QtWidgets.QMessageBox.about(
                        self,
                        "Abort action",
                        "Found no or several selected objects. Need exactly one.",
                    )
                    os.remove(self.thumbTempPath)
                    os.remove(self.jsonTempPath)
            # manage display
            if "bones" in itemdata.keys():
                self.createPosewidget.contentLabel.setText(
                    str(itemdata["bones"]) + " bone(s)"
                )
            else:
                self.createPosewidget.contentLabel.setText("")
        else:
            msg = ""
            if "objects" in itemdata.keys():
                msg += str(len(itemdata["objects"])) + " object(s) \n"
            if "bones" in itemdata.keys():
                msg += str(itemdata["bones"]) + " bone(s)"
            self.createPosewidget.contentLabel.setText(msg)
        self.createPosewidget.pushButton.setText("")
        icon = QtGui.QIcon()
        if itemType == "ANIMATION":
            thumbpath = os.path.join(os.path.dirname(self.thumbTempPath), "sequence")
            # Create GIF
            try:
                thumbpath = generateGif(thumbpath, fps=bpy.context.scene.render.fps)
            except Exception as e:
                print("An error occured during GIF generation : " + str(e))
        else:
            thumbpath = self.thumbTempPath
        if os.path.isfile(thumbpath):
            if itemType == "ANIMATION":
                movie = QtGui.QMovie(thumbpath, QtCore.QByteArray(), self)
                movie.frameChanged.connect(self.createPosewidget.updateMovie)
                movie.setCacheMode(QtGui.QMovie.CacheAll)
                movie.setSpeed(100)
                self.createPosewidget.movie = movie
                movie.start()
                movie.stop()
                icon = QtGui.QIcon(movie.currentPixmap())
                self.createPosewidget.pushButton.setIcon(icon)
            else:
                icon.addPixmap(
                    QtGui.QPixmap(thumbpath), QtGui.QIcon.Normal, QtGui.QIcon.Off
                )
                self.createPosewidget.pushButton.setIcon(icon)
        else:
            icon.addPixmap(
                QtGui.QPixmap("icons/photo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.createPosewidget.pushButton.setIcon(icon)

        # put back previous render settings
        bpy.context.scene.render.filepath = self.renderPath
        bpy.context.scene.render.image_settings.file_format = self.renderFormat
        bpy.context.scene.render.resolution_x = self.xres
        bpy.context.scene.render.resolution_y = self.yres
        bpy.context.scene.render.use_stamp = self.use_stamp
        bpy.context.scene.render.image_settings.color_mode = self.color_mode
        if itemType == "ANIMATION":
            bpy.context.scene.frame_step = self.frameStep
            bpy.context.scene.frame_start = self.frameStart
            bpy.context.scene.frame_end = self.frameEnd

    def resizeEvent(self, event):
        """Manage window resizing"""
        self.resized.emit()
        return super(GaoLib, self).resizeEvent(event)

    def folderSelected(self):
        """Update treeView to display selected folder content"""
        indexes = self.treeSelectionModel.selection().indexes()
        if len(indexes) != 0:
            selectedItem = self.hierarchyTreeView.model().data(
                indexes[0], QtCore.Qt.UserRole
            )
            if selectedItem:
                self.treeElementSelected(selectedItem)
            else:
                print("Warning : Selected Item is None")

    def listItemSelected(self):
        """Display selected item informations"""
        indexes = self.listView.selectionModel().selection().indexes()
        if len(indexes) != 0:
            selectedItem = self.listView.model().data(indexes[0], QtCore.Qt.UserRole)
            self.currentListItem = selectedItem
            self.displayInfos(selectedItem)

    def cleanInfoWidget(self):
        """Clean Info Widget"""
        layout = self.verticalLayout_5
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def displayInfos(self, selectedItem):
        """Display selected item informations"""
        layout = self.verticalLayout_5
        self.cleanInfoWidget()
        self.infoWidget = GaoLibInfoWidget(selectedItem, self, parent=self)
        self.infoWidget.infoGroupBox.setToolTip(self.infoWidget.nameLabel.text())
        layout.addWidget(self.infoWidget)
        if selectedItem.itemType == "POSE":
            # self.infoWidget.applyPushButton.released.connect(lambda: self.applyPose(itemType=selectedItem.itemType, flipped=self.infoWidget.flippedCheckBox.isChecked()))
            self.infoWidget.applyPushButton.released.connect(
                lambda: self.applyPose(
                    itemType=selectedItem.itemType,
                    blendPose=self.infoWidget.blendPoseSlider.value() / 100,
                    currentPose=self.infoWidget.currentPose,
                )
            )

        elif selectedItem.itemType == "ANIMATION":
            self.infoWidget.applyPushButton.released.connect(
                lambda: self.applyPose(itemType=selectedItem.itemType)
            )
        elif selectedItem.itemType == "CONSTRAINT SET":
            self.infoWidget.applyPushButton.released.connect(
                lambda: self.applyPose(itemType=selectedItem.itemType)
            )

    def treeElementSelected(self, selectedItem):
        """Manage selection in tree view"""
        self.currentTreeElement = selectedItem
        self.items = self.getListItems()
        self.setListView()
        if len(selectedItem.ancestors) > 1:
            self.rootPath = selectedItem.ancestors[1].path
        else:
            self.rootPath = selectedItem.path

    def recursivelyPopulateTreeView(self, parentItem, itemPath, newName=None, step=0):
        """Recursively populate treeView by parsing directories from the ROOT directory"""
        ancestors = parentItem.ancestors + [parentItem]
        for directory in os.listdir(itemPath):
            if step == 0 and directory != "ROOT":
                continue
            directoryPath = os.path.join(itemPath, directory)
            if (
                os.path.isdir(directoryPath)
                and ".anim" not in directory
                and ".selection" not in directory
                and ".pose" not in directory
                and ".constraint" not in directory
                and directory != "trash"
                and not directory.startswith(".")
            ):
                # Create Item
                item = GaoLibTreeItem(
                    directory, ancestors=ancestors, path=directoryPath, newName=newName
                )
                parentItem.addChild(item)

                self.recursivelyPopulateTreeView(item, directoryPath, step=step + 1)

    def getListItems(self):
        """Display current selected folder content in listView"""
        recursiveSearch = self.recursiveDisplayMode
        folderPath = self.currentTreeElement.path
        items = {}
        # Parse folder
        if recursiveSearch:
            i = 0
            for root, dirs, files in os.walk(folderPath):
                for it in dirs:
                    itPath = os.path.join(root, it)
                    if os.path.isdir(itPath):
                        if (
                            it.endswith(".anim")
                            or it.endswith(".pose")
                            or it.endswith(".selection")
                            or it.endswith(".constraint")
                        ):
                            thumbnailPath = os.path.join(itPath, "thumbnail.png")
                            if os.path.isfile(thumbnailPath):
                                thumbpath = thumbnailPath
                            else:
                                thumbpath = None

                            # Create Item
                            gaoLibItem = GaoLibItem(
                                name=it, thumbpath=thumbpath, path=itPath
                            )
                            items[i] = gaoLibItem
                            i += 1
        else:
            i = 0
            for it in os.listdir(folderPath):
                itPath = os.path.join(folderPath, it)
                if os.path.isdir(itPath):
                    thumbnailPath = os.path.join(itPath, "thumbnail.png")
                    if os.path.isfile(thumbnailPath):
                        thumbpath = thumbnailPath
                    elif (
                        os.path.isdir(itPath)
                        and not it.endswith(".anim")
                        and not it.endswith(".pose")
                        and not it.endswith(".selection")
                        and not it.endswith(".constraint")
                    ):
                        thumbpath = os.path.join(
                            os.path.dirname(os.path.realpath(__file__)),
                            "icons/folder2.png",
                        )
                    else:
                        thumbpath = None

                    # Create Item
                    gaoLibItem = GaoLibItem(name=it, thumbpath=thumbpath, path=itPath)
                    items[i] = gaoLibItem
                    i += 1
        return items

    def selectChildItemInTree(self, itemName):
        """Select one item in treeView knowing its parent(the current selection) and its name"""

        parent = self.currentTreeElement
        # Get all parent children names
        childrenNames = []
        for child in parent.children:
            childrenNames.append(child.name.lower())
        childrenNames.sort()

        for child in parent.children:
            if child.name == itemName:
                indexes = self.treeSelectionModel.selection().indexes()
                if not indexes:
                    indexes = [self.hierarchyTreeView.rootIndex()]

                # Get child index
                childRow = 0
                for i in range(len(childrenNames)):
                    if child.name.lower() == childrenNames[i]:
                        childRow = i
                        break
                index = self.hierarchyTreeView.model().index(childRow, 0, indexes[0])
                # index = self.hierarchyTreeView.model().index(child.row(), 0, indexes[0])

                # Select child item in tree
                self.treeSelectionModel.clear()
                self.treeSelectionModel.select(index, QtCore.QItemSelectionModel.Select)
                self.hierarchyTreeView.expand(index)
                break

    # def selectParentItemInTree(self):
    #     """Select the parent of current item in treeView"""
    #     child = self.currentTreeElement
    #     parent = child.parent
    #     parentIdx = self.treeModel.createIndex(parent.row(), 0, parent)
    #     self.treeSelectionModel.clear()
    #     self.treeSelectionModel.select(parentIdx, QtCore.QItemSelectionModel.Select)

    # def selectCurrentItemInTree(self):
    #     """Select current item in treeView"""
    #     indexes = self.treeSelectionModel.selection().indexes()
    #     if not indexes:
    #         indexes = [self.hierarchyTreeView.rootIndex()]
    #     index = indexes[0]

    #     self.treeSelectionModel.clear()
    #     self.treeSelectionModel.select(index, QtCore.QItemSelectionModel.Select)

    def itemDoubleClick(self):
        """Double click on a List folder item sets the current selection in TreeView"""
        itemType = self.currentListItem.itemType
        itemName = self.currentListItem.name
        if itemType == "FOLDER":
            self.selectChildItemInTree(itemName)

    def setListView(self):
        """Set list model and connect it to UI"""
        try:
            self.listView.doubleClicked.disconnect()
        except:
            pass
        # Manage ListView (central widget)
        # Create Qt Model
        model = GaoLibListModel(self.items)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.listView.setModel(self.proxyModel)
        self.listView.selectionModel().selectionChanged.connect(self.listItemSelected)
        self.proxyModel.sort(0, QtCore.Qt.AscendingOrder)
        self.proxyModel.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.listView.doubleClicked.connect(self.itemDoubleClick)

    def updateTreeFilter(self):
        """Update QSortFilterProxyModel for tree View"""
        self.treeItemProxyModel = TreeItemFilterProxyModel()
        self.treeItemProxyModel.setSourceModel(self.treeModel)
        self.treeItemProxyModel.setSortRole(QtCore.Qt.DisplayRole)

        self.hierarchyTreeView.setModel(self.treeItemProxyModel)
        self.treeSelectionModel = self.hierarchyTreeView.selectionModel()
        self.treeSelectionModel.selectionChanged.connect(self.folderSelected)
        self.treeItemProxyModel.sort(0, QtCore.Qt.AscendingOrder)
        self.treeItemProxyModel.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)

    def setTreeView(self):
        """Set Tree model and connect it to UI"""
        self.readConfig()

        self.treeroot = GaoLibTreeItem("root")
        rootName = None
        for rootItem in self.rootList:
            # self.treeroot = GaoLibTreeItem("Root", path=self.rootPath)
            rootPath = rootItem["path"]
            rootName = rootItem["name"]

            if not self.currentTreeElement:
                self.currentTreeElement = self.treeroot
            if os.path.isdir(rootPath):
                self.recursivelyPopulateTreeView(
                    self.treeroot, rootPath, newName=rootName
                )
                self.rootPath = rootPath
            else:
                QtWidgets.QMessageBox.about(
                    self,
                    "FOLDER NOT FOUND",
                    "Root folder does not exist :\n" + str(rootPath),
                )

        self.treeModel = GaoLibTreeItemModel(self.treeroot, projName=self.projName)
        self.updateTreeFilter()

        if rootName:
            self.selectChildItemInTree(rootName)
        else:
            self.items = {}

        self.setListView()

    def initUi(self):
        """INIT"""
        self.configPath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "config.json"
        )

        self.setTreeView()

        if not len(self.rootList):
            self.settings()

    @QtCore.Slot()
    def filterTree(self):
        """Manage text filter research for treeView"""
        filterText = self.searchHierarchyEdit.text().lower()
        if len(filterText):
            self.hierarchyTreeView.expandToDepth(-1)
        else:
            self.hierarchyTreeView.collapseAll()

        if USE_PYSIDE6:
            regExp = QtCore.QRegularExpression(
                str(filterText), QtCore.QRegularExpression.CaseInsensitiveOption
            )
            self.treeItemProxyModel.text = filterText
            self.treeItemProxyModel.setFilterRegularExpression(regExp)
            self.hierarchyTreeView.expandAll()
        else:
            regExp = QtCore.QRegExp(str(filterText))
            # Set case sensitivity to insensitive
            regExp.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
            self.treeItemProxyModel.text = filterText
            self.treeItemProxyModel.setFilterRegExp(regExp)
            self.treeItemProxyModel.setFilterKeyColumn(1)

    @QtCore.Slot()
    def filterList(self):
        """Manage text filter research for ListView"""
        filterText = self.searchEdit.text()
        if USE_PYSIDE6:
            regExp = QtCore.QRegularExpression(
                str(filterText), QtCore.QRegularExpression.CaseInsensitiveOption
            )
            self.proxyModel.setFilterRegularExpression(regExp)
        else:
            regExp = QtCore.QRegExp(str(filterText))
            # Set case sensitivity to insensitive
            regExp.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
            self.proxyModel.setFilterRegExp(regExp)
            self.proxyModel.setFilterKeyColumn(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = GaoLib()
    mainWin.show()
    sys.exit(app.exec_())
