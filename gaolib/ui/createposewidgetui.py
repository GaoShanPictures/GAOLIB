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

################################################################################
## Form generated from reading UI file 'createposewidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(313, 448)
        Form.setStyleSheet(
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
            "			border: 0px solid #222;\n"
            "			\n"
            "}\n"
            "\n"
            "QListWidget{\n"
            "            background-color: #444;\n"
            "            color: white;\n"
            "			border: 0px solid #222;\n"
            "			\n"
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
            "            background-color: rgb(30,30,30);"
            "\n"
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
            "    border: 1px solid "
            "#4D5056;\n"
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
            "    selectio"
            "n-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #097ace, stop: 1 #097ace);\n"
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
            "     border-"
            "bottom-right-radius: 3px;\n"
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
            "    col"
            "or: black;\n"
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
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(140, 140))
        self.pushButton.setMaximumSize(QSize(140, 140))
        icon = QIcon()
        icon.addFile("icons/photo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(130, 130))

        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayout.addWidget(self.widget)

        self.label = QLabel(Form)
        self.label.setObjectName("label")
        self.label.setEnabled(True)
        self.label.setScaledContents(False)

        self.verticalLayout.addWidget(self.label)

        self.nameLineEdit = QLineEdit(Form)
        self.nameLineEdit.setObjectName("nameLineEdit")

        self.verticalLayout.addWidget(self.nameLineEdit)

        self.frameRangeWidget = QWidget(Form)
        self.frameRangeWidget.setObjectName("frameRangeWidget")
        self.gridLayout = QGridLayout(self.frameRangeWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 9, 0, -1)
        self.label_3 = QLabel(self.frameRangeWidget)
        self.label_3.setObjectName("label_3")
        font = QFont()
        font.setBold(True)
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.fromRangeSpinBox = QSpinBox(self.frameRangeWidget)
        self.fromRangeSpinBox.setObjectName("fromRangeSpinBox")
        self.fromRangeSpinBox.setMinimum(-10000000)
        self.fromRangeSpinBox.setMaximum(10000000)

        self.gridLayout.addWidget(self.fromRangeSpinBox, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frameRangeWidget)
        self.label_7.setObjectName("label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)

        self.label_2 = QLabel(self.frameRangeWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 3)

        self.toRangeSpinBox = QSpinBox(self.frameRangeWidget)
        self.toRangeSpinBox.setObjectName("toRangeSpinBox")
        self.toRangeSpinBox.setMinimum(-10000000)
        self.toRangeSpinBox.setMaximum(10000000)
        self.toRangeSpinBox.setValue(100)

        self.gridLayout.addWidget(self.toRangeSpinBox, 1, 3, 1, 1)

        self.spinBox = QSpinBox(self.frameRangeWidget)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.spinBox, 3, 0, 1, 4)

        self.label_4 = QLabel(self.frameRangeWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 4)

        self.keyLastCheckBox = QCheckBox(self.frameRangeWidget)
        self.keyLastCheckBox.setObjectName("keyLastCheckBox")

        self.gridLayout.addWidget(self.keyLastCheckBox, 4, 0, 1, 4)

        self.verticalLayout.addWidget(self.frameRangeWidget)

        self.contentLabel = QLabel(Form)
        self.contentLabel.setObjectName("contentLabel")

        self.verticalLayout.addWidget(self.contentLabel)

        self.applyPushButton = QPushButton(Form)
        self.applyPushButton.setObjectName("applyPushButton")

        self.verticalLayout.addWidget(self.applyPushButton)

        self.cancelPushButton = QPushButton(Form)
        self.cancelPushButton.setObjectName("cancelPushButton")

        self.verticalLayout.addWidget(self.cancelPushButton)

        self.verticalSpacer = QSpacerItem(
            20, 114, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.pushButton.setText("")
        self.label.setText(QCoreApplication.translate("Form", "Name", None))
        self.label_3.setText(QCoreApplication.translate("Form", "From", None))
        self.label_7.setText(QCoreApplication.translate("Form", "to", None))
        self.label_2.setText(QCoreApplication.translate("Form", "Frame Range", None))
        self.label_4.setText(
            QCoreApplication.translate("Form", "Thumbnail frame step", None)
        )
        self.keyLastCheckBox.setText(
            QCoreApplication.translate("Form", "Key last frame", None)
        )
        self.contentLabel.setText("")
        self.applyPushButton.setText(
            QCoreApplication.translate("Form", "SAVE POSE", None)
        )
        self.cancelPushButton.setText(
            QCoreApplication.translate("Form", "CANCEL", None)
        )

    # retranslateUi
