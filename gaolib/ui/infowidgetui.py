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


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infowidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(245, 613)
        Form.setStyleSheet("QMainWindow{\n"
"    color: #b1b1b1;\n"
"    background-color: #3c3c3c;\n"
"}\n"
"\n"
"QWidget{\n"
"            background-color: #444;\n"
"            color: white;\n"
"}\n"
"\n"
"QScrollArea{\n"
"            background-color: #444;\n"
"            color: white;\n"
"            border: 0px solid #222;\n"
"            \n"
"}\n"
"\n"
"QListWidget{\n"
"            background-color: #444;\n"
"            color: white;\n"
"            border: 0px solid #222;\n"
"            \n"
"}\n"
"\n"
"QStatusBar{\n"
"    color: white;\n"
"}\n"
"\n"
"QMenuBar {\n"
"            background-color: #444;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"            background-color: #444;\n"
"            color: rgb(255,255,255);\n"
"}\n"
"\n"
"QMenuBar::item::selected {\n"
"            background-color: rgb(30,30,30);\n"
"}\n"
"\n"
"QMenu {\n"
"            background-color: #3c3c3c;\n"
"}\n"
"\n"
"QMenu::item {\n"
"            background-color: #3c3c3c;\n"
"            color: rgb(255,255,255);\n"
"}\n"
"\n"
"QMenu::item::selected {\n"
"            background-color: rgb(30,30,30);\n"
"}\n"
"\n"
"QDialog\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #3c3c3c;\n"
"}\n"
"\n"
"QTabWidget QWidget\n"
"{\n"
"    background: #444;\n"
"}\n"
"\n"
"#page, #page_2, #page_3 {\n"
"    background-color: #3c3c3c;\n"
"}\n"
"\n"
"QGroupBox {\n"
"     color: #628CB2;\n"
"     border: 1px solid #222;\n"
"     border-radius: 5px;\n"
"     margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"     subcontrol-origin: margin;\n"
"     subcontrol-position: top center; /* position at the top center */\n"
"     padding: 0 3px;\n"
"     background-color: QLinearGradient( x1: 0, y1: 1, x2: 0, y2: 0, stop: 0 #333, stop: 1 #3c3c3c);\n"
"}\n"
"\n"
"QHeaderView::section:vertical\n"
"{\n"
"    margin-bottom: 4px;\n"
"    border: 1px solid;\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #4D5056;\n"
"    border-radius: 5;\n"
"    color: #b1b1b1;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #555555;\n"
"    border-style: solid;\n"
"    border-radius: 5;\n"
"    padding: 3px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    outline: 0;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #3d3d3d, stop: 0.1 #3b3b3b, stop: 0.5 #393939, stop: 0.9 #383838, stop: 1 #353535);\n"
"}\n"
"\n"
"QPushButton:disabled\n"
"{\n"
"    background-color: rgb(110, 110, 110)\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border: 1px outset #4D5056;\n"
"    border-radius: 3px;\n"
"    padding: 1px 3px 1px 5px;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #097ace, stop: 1 #097ace);\n"
"    combobox-popup: 1;\n"
"}\n"
"\n"
"QComboBox:hover, QPushButton:hover\n"
"{\n"
"    border: 1px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #333 , stop: 1 #333);\n"
"}\n"
"\n"
"QComboBox:on\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     border-left-width: 0px;\n"
"     border-left-color: black;\n"
"     border-left-style: inset;\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"     image: url(./icons/arrow.png);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    selection-background-color: lightgray;\n"
"    background-color: #3c3c3c;\n"
"    border: 1px outset #3c3c3c;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"    color: #b1b1b1;\n"
"}\n"
"\n"
"QSplitter::handle:vertical\n"
"{\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #494949, stop:1 #6f6f6f);\n"
"    height: 2px;\n"
"}\n"
"\n"
"QSplitter::handle:horizontal\n"
"{\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #494949, stop:1 #6f6f6f);\n"
"    width: 2px;\n"
"}\n"
"\n"
"QToolBox {\n"
"    background: #444;\n"
"}\n"
"\n"
"QToolBox QScrollArea>QWidget>QWidget\n"
"{\n"
"    background: #444;\n"
"}\n"
"\n"
"QToolBox::tab {\n"
"   background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"   color: darkgray;\n"
"}\n"
"\n"
"QToolBox::tab:selected {\n"
"    color: black;\n"
"}\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"    border: 1px solid #333;\n"
"    background-color: #3c3c3c;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: #3a3a3a;\n"
"    border: 1px solid #222;\n"
"    border-bottom-color: #444; /* same as the pane color */\n"
"    min-width: 8ex;\n"
"    border-top-left-radius: 2px;\n"
"    border-top-right-radius: 2px;\n"
"    padding: 3px;\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: #444;\n"
"    border-bottom-color: #444; /* same as the pane color */\n"
"    color: white;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
"QPlainTextEdit {\n"
"    background-color: #111;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.thumbnailLabel = QtWidgets.QLabel(self.widget)
        self.thumbnailLabel.setMinimumSize(QtCore.QSize(200, 200))
        self.thumbnailLabel.setMaximumSize(QtCore.QSize(200, 200))
        self.thumbnailLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.thumbnailLabel.setText("")
        self.thumbnailLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnailLabel.setObjectName("thumbnailLabel")
        self.horizontalLayout.addWidget(self.thumbnailLabel)
        spacerItem1 = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget)
        self.infoGroupBox = QtWidgets.QGroupBox(Form)
        self.infoGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.infoGroupBox.setObjectName("infoGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.infoGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.infoGroupBox)
        self.label.setEnabled(True)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.infoGroupBox)
        self.label_3.setEnabled(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.infoGroupBox)
        self.label_2.setEnabled(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.infoGroupBox)
        self.label_4.setEnabled(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.dateLabel = QtWidgets.QLabel(self.infoGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.gridLayout.addWidget(self.dateLabel, 3, 1, 1, 1)
        self.contentLabel = QtWidgets.QLabel(self.infoGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.contentLabel.setFont(font)
        self.contentLabel.setObjectName("contentLabel")
        self.gridLayout.addWidget(self.contentLabel, 4, 1, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.infoGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 1, 1, 1)
        self.ownerLabel = QtWidgets.QLabel(self.infoGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ownerLabel.setFont(font)
        self.ownerLabel.setObjectName("ownerLabel")
        self.gridLayout.addWidget(self.ownerLabel, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.infoGroupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.frameRangeLabel = QtWidgets.QLabel(self.infoGroupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.frameRangeLabel.setFont(font)
        self.frameRangeLabel.setObjectName("frameRangeLabel")
        self.gridLayout.addWidget(self.frameRangeLabel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.infoGroupBox)
        self.optionsGroupBox = QtWidgets.QGroupBox(Form)
        self.optionsGroupBox.setObjectName("optionsGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.optionsGroupBox)
        self.verticalLayout_2.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.startFrameComboBox = QtWidgets.QComboBox(self.optionsGroupBox)
        self.startFrameComboBox.setObjectName("startFrameComboBox")
        self.startFrameComboBox.addItem("")
        self.startFrameComboBox.addItem("")
        self.startFrameComboBox.addItem("")
        self.verticalLayout_2.addWidget(self.startFrameComboBox)
        self.frameRangeWidget = QtWidgets.QWidget(self.optionsGroupBox)
        self.frameRangeWidget.setObjectName("frameRangeWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frameRangeWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.frameRangeWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.fromRangeSpinBox = QtWidgets.QSpinBox(self.frameRangeWidget)
        self.fromRangeSpinBox.setMaximum(1000000)
        self.fromRangeSpinBox.setObjectName("fromRangeSpinBox")
        self.horizontalLayout_2.addWidget(self.fromRangeSpinBox)
        self.label_7 = QtWidgets.QLabel(self.frameRangeWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.toRangeSpinBox = QtWidgets.QSpinBox(self.frameRangeWidget)
        self.toRangeSpinBox.setMaximum(1000000)
        self.toRangeSpinBox.setProperty("value", 100)
        self.toRangeSpinBox.setObjectName("toRangeSpinBox")
        self.horizontalLayout_2.addWidget(self.toRangeSpinBox)
        self.verticalLayout_2.addWidget(self.frameRangeWidget)
        self.quickPasteCheckBox = QtWidgets.QCheckBox(self.optionsGroupBox)
        self.quickPasteCheckBox.setObjectName("quickPasteCheckBox")
        self.verticalLayout_2.addWidget(self.quickPasteCheckBox)
        self.verticalLayout.addWidget(self.optionsGroupBox)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.selectBonesPushButton = QtWidgets.QPushButton(self.widget_2)
        self.selectBonesPushButton.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectBonesPushButton.setIcon(icon)
        self.selectBonesPushButton.setObjectName("selectBonesPushButton")
        self.horizontalLayout_3.addWidget(self.selectBonesPushButton)
        self.trashPushButton = QtWidgets.QPushButton(self.widget_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trashPushButton.setIcon(icon1)
        self.trashPushButton.setObjectName("trashPushButton")
        self.horizontalLayout_3.addWidget(self.trashPushButton)
        self.verticalLayout.addWidget(self.widget_2)
        self.applyPushButton = QtWidgets.QPushButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/pose2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.applyPushButton.setIcon(icon2)
        self.applyPushButton.setObjectName("applyPushButton")
        self.verticalLayout.addWidget(self.applyPushButton)
        self.progressWidget = QtWidgets.QWidget(Form)
        self.progressWidget.setObjectName("progressWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.progressWidget)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.progressWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.progressBar = QtWidgets.QProgressBar(self.progressWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.progressWidget)
        spacerItem2 = QtWidgets.QSpacerItem(20, 114, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.infoGroupBox.setTitle(_translate("Form", "Info"))
        self.label.setText(_translate("Form", "Name"))
        self.label_3.setText(_translate("Form", "Date"))
        self.label_2.setText(_translate("Form", "Created by"))
        self.label_4.setText(_translate("Form", "Content"))
        self.dateLabel.setText(_translate("Form", "Test"))
        self.contentLabel.setText(_translate("Form", "00000 bone(s) selected"))
        self.nameLabel.setText(_translate("Form", "Testlala.anim"))
        self.ownerLabel.setText(_translate("Form", "Test"))
        self.label_5.setText(_translate("Form", "Frame Range"))
        self.frameRangeLabel.setText(_translate("Form", "0-100"))
        self.optionsGroupBox.setTitle(_translate("Form", "Options"))
        self.startFrameComboBox.setItemText(0, _translate("Form", "From current frame"))
        self.startFrameComboBox.setItemText(1, _translate("Form", "From start frame"))
        self.startFrameComboBox.setItemText(2, _translate("Form", "From source start"))
        self.label_6.setText(_translate("Form", "Source from"))
        self.label_7.setText(_translate("Form", "to"))
        self.quickPasteCheckBox.setText(_translate("Form", "Quick Paste Action"))
        self.selectBonesPushButton.setText(_translate("Form", "Select bones"))
        self.trashPushButton.setText(_translate("Form", "Trash"))
        self.applyPushButton.setText(_translate("Form", "APPLY"))
        self.label_8.setText(_translate("Form", "Pasting Animation ..."))