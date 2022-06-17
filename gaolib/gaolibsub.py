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
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog

from coretools.uiloader import loadUi
from gaolib.createposewidget import CreatePoseWidget
from gaolib.gaolibinfowidget import GaoLibInfoWidget
from gaolib.model.gaolibitem import GaoLibItem
from gaolib.model.gaoliblistmodel import GaoLibListModel
from gaolib.model.gaolibtreeitem import GaoLibTreeItem
from gaolib.model.gaolibtreeitemmodel import GaoLibTreeItemModel
from gaolib.model.rootitemwidget import RootItemWidget
from gaolib.model.treeitemfilterproxymodel import TreeItemFilterProxyModel
from gaolib.ui.newfolderdialogui import Ui_Dialog as NewFolderDialog
from gaolib.ui.settingsdialogui import Ui_Dialog as SettingsDialog
from gaolib.ui.yesnodialogui import Ui_Dialog as YesNoDialog

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))

try:
    import bpy

    from gaolib.model.blenderutils import copyAnim, copyPose, pasteAnim, pastePose
    from gaolib.model.gifgenerator import generateGif
except Exception as e:
    print("IMPORT EXCEPTION : " + str(e))


class GaoLib(QtWidgets.QMainWindow):
    """GAOLIB Main window"""

    # Manage window resize
    resized = QtCore.Signal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        loadUi(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/gaolib.ui"),
            self,
        )

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)

        # Set data variables
        self.currentTreeElement = None
        self.items = {}
        self.projName = ""
        self.rootPath = None
        self.rootList = []
        self.initUi()
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
        createMenu.addAction(poseIcon, "New Pose", self.createPose)
        animIcon = QtGui.QIcon(QtGui.QPixmap(os.path.join(iconFolder, "anim2.png")))
        createMenu.addAction(animIcon, "New Animation", self.createAnim)
        selectIcon = QtGui.QIcon(
            QtGui.QPixmap(os.path.join(iconFolder, "selectionset.png"))
        )
        createMenu.addAction(selectIcon, "New Selection Set", self.createSelectionSet)
        folderIcon = QtGui.QIcon(QtGui.QPixmap(os.path.join(iconFolder, "folder2.png")))
        createMenu.addAction(folderIcon, "New Folder", self.createFolder)
        self.newPushButton.setMenu(createMenu)

    def createMenuSettings(self):
        """Create settings menu"""
        # Settings functionnalities
        createMenu = QtWidgets.QMenu(self.settingsPushButton)
        createMenu.addAction("Settings", self.settings)
        self.settingsPushButton.setMenu(createMenu)

    def getRootList(self):
        """Read Json config"""
        self.rootList = []
        self.rootPath = None
        if os.path.exists(self.configPath):
            with open(self.configPath) as file:
                itemdata = json.load(file)
                self.rootList = itemdata["rootpath"]

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
        # File browser
        dialog.ui.browsePushButton.released.connect(
            lambda: self.openFileNameDialog(dialog)
        )
        rsp = dialog.exec_()
        # retrieve editLine infos from the dialog
        path = dialog.ui.pathLineEdit.text()
        pathName = dialog.ui.lineEdit.text()
        # The user clicks OK
        if rsp == QtWidgets.QDialog.Accepted:
            self.getRootList()
            createRoot = False
            newRootItem = {"path": path, "name": pathName}
            try:
                if not (len(path)):
                    pass
                elif os.path.exists(path):
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
                            {"rootpath": self.rootList}, file, indent=4, sort_keys=True
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
                        {"rootpath": self.rootList}, file, indent=4, sort_keys=True
                    )

        self.currentTreeElement = None
        self.setTreeView()

    def openFileNameDialog(self, dialog):
        """File browser to change the ROOT location"""
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)

        options = fileDialog.Options()
        directory = fileDialog.getExistingDirectory(self)
        if directory:
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
                    # Creates new folder and add it to the hierachy
                    os.mkdir(folderPath)
                    sourceModel = self.hierarchyTreeView.model().sourceModel()
                    parentItem = self.currentTreeElement
                    indexes = (
                        self.hierarchyTreeView.selectionModel().selection().indexes()
                    )
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
                    parentItem.addChild(newItem)

                    # refresh TreeView
                    self.setTreeView()
                    self.currentTreeElement = self.treeroot
                    for i in range(len(ancestorNames)):
                        ancestorNames[i]
                        if i != 0:
                            self.selectChildItemInTree(ancestorNames[i])

            else:
                QtWidgets.QMessageBox.about(
                    self, "Abort action", "Folder name must not be empty."
                )

    def createGenericItem(self):
        """Create new animation/pose/selection set item"""

        # Temporary path for thumnail
        self.thumbTempPath = os.path.join(
            # os.path.dirname(os.path.abspath(__file__)),
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "thumbnail.png",
        )
        self.jsonTempPath = os.path.join(
            # os.path.dirname(os.path.abspath(__file__)),
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "temp.json",
        )
        # Delete files before creating new item
        if os.path.exists(self.jsonTempPath):
            os.remove(self.jsonTempPath)
        if os.path.exists(self.thumbTempPath):
            os.remove(self.thumbTempPath)
        sequencePath = os.path.join(os.path.dirname(self.thumbTempPath), "sequence")
        if os.path.exists(sequencePath):
            shutil.rmtree(sequencePath)
        os.makedirs(sequencePath)
        # Clear information layout
        for i in reversed(range(self.verticalLayout_5.count())):
            self.verticalLayout_5.itemAt(i).widget().deleteLater()

    def createAnim(self):
        """Sets the UI to Create new animation item"""
        itemType = "ANIMATION"
        self.createGenericItem()
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

    def createPose(self):
        """Sets the UI to Create new pose item"""
        itemType = "POSE"
        self.createGenericItem()
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

    def createSelectionSet(self):
        """Sets the UI to Create new selection set item"""
        self.createGenericItem()
        itemType = "SELECTION SET"
        # Create widget for create selection set
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
            copyAnim(poseDir)
        elif itemType == "POSE":
            thumbPath = os.path.join(poseDir, "thumbnail.png")
            shutil.copyfile(thumbTempPath, thumbPath)
            # Copy blend in pose directory
            copyPose(poseDir)
        elif itemType == "SELECTION SET":
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
                pasteAnim(self.currentListItem.path, frameIn, frameOut, self.infoWidget)
            elif itemType == "POSE":
                pastePose(
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

    def writejson(self, name, directory, itemType="POSE"):
        """Create json file corresponding to pose/animation item"""
        if itemType == "ANIMATION":
            jsonFile = os.path.join(directory, "animation.json")
        elif itemType == "POSE":
            jsonFile = os.path.join(directory, "pose.json")
        elif itemType == "SELECTION SET":
            jsonFile = os.path.join(directory, "selection_set.json")

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
        # write json
        with open(jsonFile, "w") as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def createThumbnail(self, itemType="POSE"):
        """Create the animation/pose thumbnail"""
        if not os.path.exists(bpy.context.preferences.filepaths.temporary_directory):
            QtWidgets.QMessageBox.about(
                self,
                "Abort action",
                "Please add a valid path for Blender temporary files in : Edit > Preferences > File Paths > Temporary Files",
            )
            return
        self.thumbTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory,
            "temp",
            "thumbnail.png",
        )
        self.jsonTempPath = os.path.join(
            bpy.context.preferences.filepaths.temporary_directory, "temp", "temp.json"
        )
        bpy.context.scene.gaolib_tool.gaolibNewAnimation = False
        bpy.context.scene.gaolib_tool.gaolibNewPose = False
        bpy.context.scene.gaolib_tool.gaolibNewSelectionSet = False
        if self.beginCreateThumb:
            self.createThumbnailBegin(itemType=itemType)
            self.beginCreateThumb = False
        else:
            self.createThumbnailEnd(itemType=itemType)
            self.beginCreateThumb = True

    def createThumbnailBegin(self, itemType="POSE"):
        """First click on the create thumbnail button, prepare the scene for creating the animation/pose files"""
        if itemType == "ANIMATION":
            bpy.context.scene.gaolib_tool.gaolibNewAnimation = True
            self.createPosewidget.movie = None
            photoButtonText = "Please use the Create\nAnimation Tool in Blender\nWhen it is done\nclick HERE again"
            renderpath = os.path.join(
                os.path.dirname(self.thumbTempPath), "sequence", "thumbnail.####.png"
            )
            bpy.context.scene.gaolib_tool.gaolibKeyLastFrame = (
                self.createPosewidget.keyLastCheckBox.isChecked()
            )
        elif itemType == "POSE":
            bpy.context.scene.gaolib_tool.gaolibNewPose = True
            photoButtonText = "Please use the Create\nPose Tool in Blender\nWhen it is done\nclick HERE again"
            renderpath = self.thumbTempPath
        elif itemType == "SELECTION SET":
            bpy.context.scene.gaolib_tool.gaolibNewSelectionSet = True
            photoButtonText = "Please use the Create\nSelection Set \nTool in Blender\nWhen it is done\nclick HERE again"
            renderpath = self.thumbTempPath

        self.createPosewidget.pushButton.setText(photoButtonText)
        self.createPosewidget.pushButton.setIcon(QtGui.QIcon())
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

    def createThumbnailEnd(self, itemType="POSE"):
        """Second click on the create thumbnail button,create item files"""
        if itemType == "ANIMATION":
            bpy.context.scene.gaolib_tool.gaolibNewAnimation = False
        elif itemType == "POSE":
            bpy.context.scene.gaolib_tool.gaolibNewPose = False
        elif itemType == "SELECTION SET":
            bpy.context.scene.gaolib_tool.gaolibNewSelectionSet = False
        # unhide hidden overlay params
        try:
            for area in bpy.context.screen.areas:
                if area.type == "VIEW_3D":
                    for space in area.spaces:
                        if space.type == "VIEW_3D":
                            space.overlay.show_bones = True
                            space.overlay.show_axis_x = True
                            space.overlay.show_axis_y = True
                            space.overlay.show_floor = True
                            break
        except:
            print("Could not set the overlay parameters")

        itemdata = {}
        # Read Json Datas
        if os.path.exists(self.jsonTempPath):
            with open(self.jsonTempPath) as file:
                itemdata = json.load(file)
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

        self.createPosewidget.pushButton.setText("")
        icon = QtGui.QIcon()
        if itemType == "ANIMATION":
            thumbpath = os.path.join(os.path.dirname(self.thumbTempPath), "sequence")
            # Create GIF
            try:
                thumbpath = generateGif(thumbpath, fps=bpy.context.scene.render.fps)
            except:
                print("No images to generate GIF from")
        elif itemType == "POSE" or itemType == "SELECTION SET":
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
            elif itemType == "POSE" or itemType == "SELECTION SET":
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
            self.treeElementSelected(selectedItem)

    def listItemSelected(self):
        """Display selected item informations"""
        indexes = self.listView.selectionModel().selection().indexes()
        if len(indexes) != 0:

            selectedItem = self.listView.model().data(indexes[0], QtCore.Qt.UserRole)
            self.currentListItem = selectedItem
            self.displayInfos(selectedItem)

    def displayInfos(self, selectedItem):
        """Display selected item informations"""
        layout = self.verticalLayout_5
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
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

    def treeElementSelected(self, selectedItem):
        """Manage selection in tree view"""
        self.currentTreeElement = selectedItem
        self.items = self.getListItems()
        self.setListView()
        if len(selectedItem.ancestors) > 1:
            self.rootPath = selectedItem.ancestors[1].path
        else:
            self.rootPath = selectedItem.path

    def recursivelyPopulateTreeView(self, parentItem, itemPath, newName=None):
        """Recursively populate treeView by parsing directories from the ROOT directory"""
        ancestors = parentItem.ancestors + [parentItem]

        for directory in os.listdir(itemPath):
            directoryPath = os.path.join(itemPath, directory)
            if (
                os.path.isdir(directoryPath)
                and ".anim" not in directory
                and ".selection" not in directory
                and ".pose" not in directory
                and directory != "trash"
                and not directory.startswith(".")
            ):
                # Create Item
                item = GaoLibTreeItem(
                    directory, ancestors=ancestors, path=directoryPath, newName=newName
                )
                parentItem.addChild(item)
                self.recursivelyPopulateTreeView(item, directoryPath)

    def getListItems(self):
        """Display current selected folder content in listView"""
        folder = self.currentTreeElement.name
        ancestorNames = [a.name for a in self.currentTreeElement.ancestors[1:]]
        ancestors = "/".join(ancestorNames)

        # folderPath = os.path.join(self.rootPath, ancestors, folder)
        folderPath = self.currentTreeElement.path

        items = {}
        # Parse folder
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
                ):
                    thumbpath = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), "icons/folder2.png"
                    )
                else:
                    thumbpath = None

                # Create Item
                gaoLibItem = GaoLibItem(name=it, thumbpath=thumbpath, path=itPath)
                items[i] = gaoLibItem
                i += 1
        return items

    def selectChildItemInTree(self, itemName):
        """Select one item in treeView knowing its parent and its name"""
        parent = self.currentTreeElement
        for child in parent.children:
            if child.name == itemName:
                indexes = self.hierarchyTreeView.selectionModel().selection().indexes()
                if not indexes:
                    indexes = [self.hierarchyTreeView.rootIndex()]
                index = self.hierarchyTreeView.model().index(child.row(), 0, indexes[0])
                self.treeSelectionModel.clear()
                self.treeSelectionModel.select(index, QtCore.QItemSelectionModel.Select)
                self.hierarchyTreeView.expand(indexes[0])
                break

    def itemDoubleClick(self):
        """Double click on a List folder item sets the current selection in TreeView"""
        itemType = self.currentListItem.itemType
        itemName = self.currentListItem.name
        index = None
        if itemType == "FOLDER":
            self.selectChildItemInTree(itemName)

    def setListView(self):
        """Set list model and connect it to UI"""
        try:
            self.listView.doubleClicked.disconnect()
        except:
            print("listView.doubleClicked not connected to any function")
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

    def setTreeView(self):
        """Set Tree model and connect it to UI"""
        self.getRootList()

        self.treeroot = GaoLibTreeItem("root")
        rootName = None
        for rootItem in self.rootList:
            # self.treeroot = GaoLibTreeItem("Root", path=self.rootPath)
            rootPath = rootItem["path"]
            rootName = rootItem["name"]
            if not self.currentTreeElement:
                self.currentTreeElement = self.treeroot

            self.recursivelyPopulateTreeView(self.treeroot, rootPath, newName=rootName)
            self.rootPath = rootPath

        model = GaoLibTreeItemModel(self.treeroot, projName=self.projName)
        self.treeItemProxyModel = TreeItemFilterProxyModel()

        self.treeItemProxyModel.setSourceModel(model)
        self.treeItemProxyModel.setSortRole(QtCore.Qt.DisplayRole)
        self.hierarchyTreeView.setModel(self.treeItemProxyModel)

        self.treeSelectionModel = self.hierarchyTreeView.selectionModel()
        self.treeSelectionModel.selectionChanged.connect(self.folderSelected)
        self.treeItemProxyModel.sort(0, QtCore.Qt.AscendingOrder)
        self.treeItemProxyModel.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)

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
        # Set case sensitivity to insensitive
        regExp = QtCore.QRegExp(str(filterText))
        regExp.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.treeItemProxyModel.text = filterText
        self.treeItemProxyModel.setFilterRegExp(regExp)
        self.treeItemProxyModel.setFilterKeyColumn(1)

    @QtCore.Slot()
    def filterList(self):
        """Manage text filter research for ListView"""
        filterText = self.searchEdit.text()
        regExp = QtCore.QRegExp(str(filterText))
        regExp.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.proxyModel.setFilterRegExp(regExp)
        self.proxyModel.setFilterKeyColumn(1)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainWin = GaoLib()
    mainWin.show()
    sys.exit(app.exec_())
