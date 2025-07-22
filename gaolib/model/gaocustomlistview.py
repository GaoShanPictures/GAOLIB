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


from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QListView


class GaoCustomListView(QListView):
    def __init__(self, parent=None):
        super(GaoCustomListView, self).__init__(parent)
        self.middle_button_pressed = False
        self.cancelBlending = False
        self.pressedPositionX = 0
        self.mainWin = parent
        self.currentItemType = None
        self.blendValue = 0

    def getEventPosition(self, event):
        return (
            event.position().toPoint(),
            event.position().x(),
            event.position().y(),
        )

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        super(GaoCustomListView, self).keyPressEvent(event)
        if self.mainWin.infoWidget.flippedCheckBox.isVisible():
            if event.key() == QtCore.Qt.Key_Shift:
                self.mainWin.infoWidget.flippedCheckBox.setChecked(False)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super(GaoCustomListView, self).keyPressEvent(event)
        if self.mainWin.infoWidget.flippedCheckBox.isVisible():
            if event.key() == QtCore.Qt.Key_Shift:
                self.mainWin.infoWidget.flippedCheckBox.setChecked(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # prevent right click from selecting an item
        if (
            event.button() == QtCore.Qt.LeftButton
            or event.button() == QtCore.Qt.MiddleButton
        ):
            super(GaoCustomListView, self).mousePressEvent(event)
        # get mouve position
        eventPosition, eventX, eventY = self.getEventPosition(event)
        # manage blending
        if self.mainWin.useWheelToBlendPose:
            if event.button() == QtCore.Qt.MiddleButton:
                # begin blending for POSE item
                index = self.indexAt(eventPosition)
                if index.isValid():
                    self.middle_button_pressed = True
                    self.start_pos = eventPosition
                    self.current_item = self.model().data(index, QtCore.Qt.DisplayRole)
                    self.currentItemType = (
                        self.model().data(index, QtCore.Qt.UserRole).itemType
                    )
                    if self.currentItemType == "POSE":
                        self.pressedPositionX = eventX
                        # set to 100%
                        self.mainWin.infoWidget.blendPoseSlider.setValue(100)
                        self.blendValue = (
                            self.mainWin.infoWidget.blendPoseSlider.value()
                        )
            if event.button() == QtCore.Qt.RightButton:
                # Cancel blending for POSE item
                if self.currentItemType == "POSE":
                    self.cancelBlending = True
                    self.mainWin.infoWidget.blendPoseSlider.setValue(0)
                    self.blendValue = 0
                    self.mainWin.statusBar().showMessage(
                        "Cancel Blending",
                        timeout=5000,
                    )

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if self.mainWin.useDoubleClickToApplyPose:
            eventPosition, eventX, eventY = self.getEventPosition(event)
            index = self.indexAt(eventPosition)
            if index.isValid():
                item_text = self.model().data(index, QtCore.Qt.DisplayRole)
                self.currentItemType = (
                    self.model().data(index, QtCore.Qt.UserRole).itemType
                )
                if self.currentItemType == "POSE":
                    # self.mainWin.infoWidget.selectBones()
                    self.mainWin.applyPose(
                        itemType="POSE",
                        blendPose=1,
                        currentPose=self.mainWin.infoWidget.currentPose,
                    )
                    self.mainWin.statusBar().showMessage(
                        "Applied pose " + item_text + " to 100%",
                        timeout=5000,
                    )
        super(GaoCustomListView, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.mainWin.useWheelToBlendPose:
            if self.currentItemType == "POSE":
                if self.middle_button_pressed and not self.cancelBlending:
                    eventPosition, eventX, eventY = self.getEventPosition(event)
                    self.current_pos = eventPosition
                    if (eventX - self.pressedPositionX) / 2 + self.blendValue < 0:
                        newBlendValue = 0
                    elif (eventX - self.pressedPositionX) / 2 + self.blendValue > 100:
                        newBlendValue = 100
                    else:
                        newBlendValue = int(
                            (eventX - self.pressedPositionX) / 2 + self.blendValue
                        )
                    if self.mainWin.infoWidget.blendPoseSlider.value() != newBlendValue:
                        self.mainWin.infoWidget.blendPoseSlider.setValue(newBlendValue)
                    self.mainWin.statusBar().showMessage(
                        "Blend pose to " + str(newBlendValue) + "%", timeout=5000
                    )
        super(GaoCustomListView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if self.mainWin.useWheelToBlendPose:
            if event.button() == QtCore.Qt.RightButton:
                # prevent selection of other item if right click for cancelling blending
                return
            if self.currentItemType == "POSE":
                if (
                    event.button() == QtCore.Qt.MiddleButton
                    and self.middle_button_pressed
                ):
                    eventPosition, eventX, eventY = self.getEventPosition(event)
                    self.middle_button_pressed = False
                    self.cancelBlending = False
                    self.end_pos = eventPosition
                    blendValue = self.mainWin.infoWidget.blendPoseSlider.value()
                    if blendValue > 0:
                        self.mainWin.applyPose(
                            itemType="POSE",
                            blendPose=blendValue / 100,
                            currentPose=self.mainWin.infoWidget.currentPose,
                            flipped=self.mainWin.infoWidget.flippedCheckBox.isChecked(),
                        )
                        self.mainWin.statusBar().showMessage(
                            "Applied pose to " + str(blendValue) + "%", timeout=5000
                        )
                    return

        super(GaoCustomListView, self).mouseReleaseEvent(event)
