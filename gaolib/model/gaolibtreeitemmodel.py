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

import os

from PySide2 import QtCore, QtGui


class GaoLibTreeItemModel(QtCore.QAbstractItemModel):
    """Model for Tree view"""

    def __init__(self, root, parent=None, projName=""):
        super(GaoLibTreeItemModel, self).__init__(parent)
        self._root = root
        self.__headers = ["Prod: %s" % projName]
        self.indexes = []

    def rowCount(self, parent):
        """Number of children for given parent"""
        if not parent.isValid():
            treeItem = self._root
        else:
            treeItem = parent.internalPointer()
        return treeItem.childCount()

    def columnCount(self, parent):
        """Number of columns"""
        return len(self.__headers)

    def flags(self, index):
        """item flags list"""
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        """Return index object of the parent to the current item"""
        elem = self.getElement(index)
        treeItem = elem.parent
        if treeItem == self._root:
            return QtCore.QModelIndex()
        return self.createIndex(treeItem.row(), 0, treeItem)

    def index(self, row, column, parent):
        """Return the index object of an item given its row, column and parent"""
        treeItem = self.getElement(parent)
        try:
            childItem = treeItem.child(row)
        except IndexError:
            return QtCore.QModelIndex()
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getElement(self, index):
        """Return item of given index"""
        if index.isValid():
            elem = index.internalPointer()
            if elem:
                return elem
        return self._root

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return self.__headers[section]
        elif role == QtCore.Qt.FontRole:
            myFont = QtGui.QFont("Helvetica", 9)
            myFont.setBold(True)
            return myFont

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Manage display of items in the tree"""
        if not index.isValid():
            return None

        # Create index list from model
        if index not in self.indexes:
            self.indexes.append(index)

        elem = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            return elem.name

        elif role == QtCore.Qt.ForegroundRole:
            return QtGui.QColor(QtCore.Qt.gray)

        elif role == QtCore.Qt.DecorationRole:
            if elem.thumbnail:
                folderPicture = elem.thumbnail
            else:
                folderPicture = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "../icons/folder2.png"
                )
            return QtGui.QIcon(QtGui.QPixmap(folderPicture))

        elif role == QtCore.Qt.UserRole:
            return elem

    def getIndex(self, elem):
        """Return index of given elem"""
        rootIdx = QtCore.QModelIndex()
        currentIdx = rootIdx
        rootElem = self._root
        currentElem = elem

        ancestors = [elem]
        while currentElem.parent != rootElem:
            ancestors.append(currentElem.parent)
            currentElem = currentElem.parent
        ancestors.reverse()

        currentElement = rootElem
        currentIdx = rootIdx
        while currentElement != elem:
            for child in currentElement.children:
                if child in ancestors:
                    currentElement = child
                    currentIdx = self.index(currentElement.row(), 0, currentIdx)
                    break
        return currentIdx

    def addElement(self, elem, parent):
        """Add elem as child of given parent"""
        self.beginInsertRows(
            QtCore.QModelIndex(),
            self.rowCount(QtCore.QModelIndex()),
            self.rowCount(QtCore.QModelIndex()),
        )
        parent.addChild(elem)
        self.endInsertRows()
        # self.layoutChanged.emit()

    def getAllIndexes(self):
        """Return List of all indexes in the model"""
        return self.indexes
