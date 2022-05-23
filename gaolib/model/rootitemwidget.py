from gaolib.ui.rootitemwidgetui import Ui_Form

from PySide2 import QtWidgets, QtCore, QtGui
import json
import os

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
        if os.path.isfile(self.configPath):
            with open(self.configPath) as file:
                itemdata = json.load(file)
        for key in itemdata.keys():
            if key == 'rootpath':
                for e in itemdata[key]:
                    rtPath = e['path']
                    if rtPath == self.pathLabel.text():
                        itemdata['rootpath'].remove(e)
                        self.nameLabel.setText('')
                        self.pathLabel.setText('')
                break
        with open(self.configPath, 'w') as file:
            json.dump(itemdata, file, indent=4, sort_keys=True)

    




   
