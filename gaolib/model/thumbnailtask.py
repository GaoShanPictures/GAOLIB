import os
from PySide6 import QtCore, QtGui


class ThumbnailTask(QtCore.QRunnable):
    def __init__(self, path, callback):
        super().__init__()
        self.path = path
        self.callback = callback

    def run(self):
        # return the nopreview image if the thumbnail does not exist
        if not self.path or not os.path.isfile(self.path):
            noPreviewPath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../icons/nopreview2.png",
            )
            image = QtGui.QImage(noPreviewPath)
        else:
            image = QtGui.QImage(self.path)
        # scale it for performance
        image = image.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )

        self.callback(self.path, image)
