# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'constraintinfopairingwidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_ConstraintForm(object):
    def setupUi(self, ConstraintForm):
        ConstraintForm.setObjectName("ConstraintForm")
        ConstraintForm.resize(256, 119)
        ConstraintForm.setStyleSheet(
            "QMainWindow{\n"
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
            "    background-color: transparent;\n"
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
            "}"
        )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ConstraintForm)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(ConstraintForm)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 7, 0, 1, 2)
        self.targetBoneLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.targetBoneLabel.setFont(font)
        self.targetBoneLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.targetBoneLabel.setObjectName("targetBoneLabel")
        self.gridLayout.addWidget(self.targetBoneLabel, 4, 1, 1, 1)
        self.boneLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        try:
            font.setWeight(50)
        except:
            font.setWeight(QtGui.QFont.Weight(50))
        self.boneLabel.setFont(font)
        self.boneLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.boneLabel.setObjectName("boneLabel")
        self.gridLayout.addWidget(self.boneLabel, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        try:
            font.setWeight(75)
        except:
            font.setWeight(QtGui.QFont.Weight(75))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.sourceTargetLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.sourceTargetLabel.setFont(font)
        self.sourceTargetLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.sourceTargetLabel.setObjectName("sourceTargetLabel")
        self.gridLayout.addWidget(self.sourceTargetLabel, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(ConstraintForm)
        QtCore.QMetaObject.connectSlotsByName(ConstraintForm)

    def retranslateUi(self, ConstraintForm):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("ConstraintForm", "GroupBox"))
        self.label_1.setText(_translate("ConstraintForm", "Bone :"))
        self.label_2.setText(_translate("ConstraintForm", "Target Bone :"))
        self.targetBoneLabel.setText(_translate("ConstraintForm", "TextLabel"))
        self.boneLabel.setText(_translate("ConstraintForm", "TextLabel"))
        self.label.setText(_translate("ConstraintForm", "Target Object"))
        self.label_3.setText(_translate("ConstraintForm", "Source Target :"))
        self.sourceTargetLabel.setText(_translate("ConstraintForm", "TextLabel"))
