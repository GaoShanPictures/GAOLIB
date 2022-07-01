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

from PySide2 import QtCore


class TreeItemFilterProxyModel(QtCore.QSortFilterProxyModel):
    """Filter model for tree items"""

    def __init__(self, parent=None):
        super(TreeItemFilterProxyModel, self).__init__(parent)
        self.text = ""

    # Recursive search
    def _accept_index(self, idx):
        """Accept items which display role contains given filter text"""
        if idx.isValid():
            text = idx.data(role=QtCore.Qt.DisplayRole).lower()
            condition = text.find(self.text) >= 0

            if condition:
                return True
            for childnum in range(idx.model().rowCount(parent=idx)):
                if self._accept_index(idx.model().index(childnum, 0, parent=idx)):
                    return True

        return False

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Only first column in model for search
        idx = self.sourceModel().index(sourceRow, 0, sourceParent)
        return self._accept_index(idx)

    def lessThan(self, left, right):
        """Items comparator"""
        leftData = self.sourceModel().data(left).lower()
        rightData = self.sourceModel().data(right).lower()
        return leftData < rightData
