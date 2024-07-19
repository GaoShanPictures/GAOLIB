from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog, QListView


class GaoCustomListView(QListView):
    def __init__(self, parent=None):
        super(GaoCustomListView, self).__init__(parent)
        self.middle_button_pressed = False
        self.pressedPositionX = 0
        self.mainWin = parent
        self.currentItemType = None
        self.blendValue = 0

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super(GaoCustomListView, self).mousePressEvent(event)
        if self.mainWin.useWheelToBlendPose:
            if event.button() == QtCore.Qt.MiddleButton:
                index = self.indexAt(event.pos())
                if index.isValid():
                    self.middle_button_pressed = True
                    self.start_pos = event.pos()
                    self.current_item = self.model().data(index, QtCore.Qt.DisplayRole)
                    self.currentItemType = (
                        self.model().data(index, QtCore.Qt.UserRole).itemType
                    )
                    if self.currentItemType == "POSE":
                        self.pressedPositionX = event.x()
                        self.blendValue = (
                            self.mainWin.infoWidget.blendPoseSlider.value()
                        )
                        # self.mainWin.infoWidget.selectBones()
        # super(GaoCustomListView, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if self.mainWin.useDoubleClickToApplyPose:
            index = self.indexAt(event.pos())
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
                if self.middle_button_pressed:
                    self.current_pos = event.pos()
                    if (event.x() - self.pressedPositionX) / 2 + self.blendValue < 0:
                        newBlendValue = 0
                    elif (
                        event.x() - self.pressedPositionX
                    ) / 2 + self.blendValue > 100:
                        newBlendValue = 100
                    else:
                        newBlendValue = int(
                            (event.x() - self.pressedPositionX) / 2 + self.blendValue
                        )
                    if self.mainWin.infoWidget.blendPoseSlider.value() != newBlendValue:
                        self.mainWin.infoWidget.blendPoseSlider.setValue(newBlendValue)
                    # print(newBlendValue)
                    self.mainWin.statusBar().showMessage(
                        "Blend pose to " + str(newBlendValue) + "%", timeout=5000
                    )
        super(GaoCustomListView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if self.mainWin.useWheelToBlendPose:
            if self.currentItemType == "POSE":
                if (
                    event.button() == QtCore.Qt.MiddleButton
                    and self.middle_button_pressed
                ):
                    self.middle_button_pressed = False
                    self.end_pos = event.pos()
                    blendValue = self.mainWin.infoWidget.blendPoseSlider.value()
                    if blendValue > 0:
                        self.mainWin.applyPose(
                            itemType="POSE",
                            blendPose=blendValue / 100,
                            currentPose=self.mainWin.infoWidget.currentPose,
                        )
                        self.mainWin.statusBar().showMessage(
                            "Applied pose to " + str(blendValue) + "%", timeout=5000
                        )
        super(GaoCustomListView, self).mouseReleaseEvent(event)
