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

from PySide2 import QtCore, QtGui


class GaoLibListModel(QtCore.QAbstractItemModel):
    """Model for List view """
    def __init__(self, items={}, parent=None):
        super(GaoLibListModel, self).__init__(parent)
        self.__items = items

    def rowCount(self, parent):
        """length of the list (number of items)"""
        return len(self.__items.keys())

    def columnCount(self, parent):
        """List is a table of dimension one"""
        return 1

    def flags(self, index):
        """item flags list"""
        return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def data(self, index, role):
        """Manage display of items in the list"""
        row = index.row()
        col = index.column()
        item = self.__items[row]

        if role == QtCore.Qt.DisplayRole:
            itemName = item.name
            if itemName.endswith('.anim'):
                itemName = itemName[:-5]
            elif itemName.endswith ('.selection'):
                itemName = itemName[:-10]
            elif itemName.endswith('.pose'):
                itemName = itemName[:-5]
            if len(itemName) > 18:
                itemName = itemName[:15] + '...'
            return itemName

        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(QtGui.QPixmap(item.thumbpath).scaled(300, 300))
        elif role == QtCore.Qt.BackgroundRole:
            if item.itemType == 'POSE':
                return QtGui.QColor(200, 125, 42, 200)
            elif item.itemType == 'ANIMATION':
                return QtGui.QColor(37, 172, 182, 200)
            elif item.itemType == 'SELECTION SET':
                return QtGui.QColor(163, 46, 142, 200)

        elif role == QtCore.Qt.UserRole:
            return item

    def index(self, row, column, parent):
        """Return the index object of an item given its row, column and parent"""
        childItem = self.__items[row]
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
