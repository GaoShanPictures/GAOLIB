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

from PySide2 import QtCore, QtGui, QtWidgets

from gaolib.ui.createposewidgetui import Ui_Form as CreatePoseWidget


class CreatePoseWidget(QtWidgets.QWidget, CreatePoseWidget):
    """Manage pose/animation item creation"""

    def __init__(self, itemType="POSE", parent=None):
        super(CreatePoseWidget, self).__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.type = itemType
        self.movie = None

        self.parent.infoGroupBox.setTitle(self.type)
        if self.type == "POSE":
            self.frameRangeWidget.setVisible(False)
        elif self.type == "SELECTION SET":
            self.frameRangeWidget.setVisible(False)
            self.applyPushButton.setText("SAVE SELECTION SET")
        elif self.type == "CONSTRAINT SET":
            self.frameRangeWidget.setVisible(False)
            self.applyPushButton.setText("SAVE CONSTRAINT SET")
        elif self.type == "ANIMATION":
            self.applyPushButton.setText("SAVE ANIMATION")
            self.pushButton.installEventFilter(self)

        self.contentLabel.setText("")

    def eventFilter(self, obj, event):
        """Event filter to play movie when hovered"""
        if obj == self.pushButton and event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered()
        if obj == self.pushButton and event.type() == QtCore.QEvent.HoverLeave:
            self.leaveHovered()
        return super(CreatePoseWidget, self).eventFilter(obj, event)

    def updateMovie(self):
        """Set pushbutton icon"""
        if not self.movie:
            return
        icon = QtGui.QIcon()
        icon.addPixmap(self.movie.currentPixmap())
        self.pushButton.setIcon(icon)

    def leaveHovered(self):
        """Stop movie when leaving hovered"""
        if self.movie:
            self.movie.stop()

    def onHovered(self):
        """Play movie on hovered"""
        if self.movie:
            self.movie.start()
