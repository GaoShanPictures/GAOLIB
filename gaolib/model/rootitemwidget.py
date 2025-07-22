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


import json
import os

from PySide6 import QtWidgets

from gaolib.ui.rootitemwidgetui import Ui_Form


class RootItemWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self, name, path, configPath, parent=None):
        super(RootItemWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.name = name
        self.path = path
        self.nameLabel.setText(name)
        self.pathLabel.setText(path)
        self.configPath = configPath
        self.pushButton.released.connect(self.deleteItem)

    def deleteItem(self):
        """Delete root path"""
        # Read json config file
        if os.path.isfile(self.configPath):
            with open(self.configPath) as file:
                itemdata = json.load(file)
        # Remove root path from root list
        for key in itemdata.keys():
            if key == "rootpath":
                for e in itemdata[key]:
                    rtPath = e["path"]
                    if rtPath == self.pathLabel.text():
                        itemdata["rootpath"].remove(e)
                        self.nameLabel.setText("")
                        self.pathLabel.setText("")
                break
        # Update json config file
        with open(self.configPath, "w") as file:
            json.dump(itemdata, file, indent=4, sort_keys=True)
