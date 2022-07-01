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


class GaoLibTreeItem(object):
    """Description of one item of the Tree View"""

    def __init__(self, name, parent=None, ancestors=[], path="", newName=None):
        if newName:
            self.name = newName
        else:
            self.name = name
        self.path = path
        self.parent = parent
        self.ancestors = ancestors
        self.children = []
        if self.parent is not None:
            self.parent.addChild(self)
        thumbnailPath = os.path.join(path, "thumbnail.png")
        if os.path.isfile(thumbnailPath):
            self.thumbnail = thumbnailPath
        else:
            self.thumbnail = None

    def parent(self):
        """Return the parent of the item"""
        return self.parent

    def clearChildren(self):
        """Remove all children of the item"""
        self.children = []

    def addChild(self, child):
        """Add given child to item children"""
        child.parent = self
        self.children.append(child)

    #############################
    # methods necessary for pyqt
    #############################

    def childCount(self):
        """Return number of children for item"""
        return len(self.children)

    def row(self):
        """Return the item row"""
        if self.parent is not None:
            return self.parent.children.index(self)

    def child(self, row):
        """Retun the child item corresponding to given row"""
        return self.children[row]
