from PySide6 import QtWidgets, QtGui, QtCore 
import gaolib.model.thumbnailcache as thc


class HoverDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        self.movie = None
        self.hover_index = QtCore.QPersistentModelIndex()

    def paint(self, painter, option, index):
        painter.save()

        item = index.data(QtCore.Qt.UserRole)
        rect = option.rect
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(rect, option.palette.highlight())
        else:
            if item.itemType in ["POSE", "MULTI POSE"]:
                painter.fillRect(rect, QtGui.QColor(200, 125, 42))
            elif item.itemType in ["ANIMATION", "MULTI ANIMATION"]:
                painter.fillRect(rect, QtGui.QColor(51, 160, 162))
            elif item.itemType == "SELECTION SET":
                painter.fillRect(rect, QtGui.QColor(163, 46, 142))
            elif item.itemType == "CONSTRAINT SET":
                painter.fillRect(rect, QtGui.QColor(100, 177, 50))

        margin = 1
        spacing = 1
        textHeight = 22
        imageRect = QtCore.QRect(rect.left() + margin, rect.top() + margin + 2, rect.width() - margin, rect.height() - textHeight - spacing - margin)
        textRect = QtCore.QRect(rect.left() + margin, imageRect.bottom() + spacing, rect.width() - margin, textHeight)

        # if animation, play the gif
        if index == self.hover_index and self.movie and item.itemType in ["ANIMATION", "MULTI ANIMATION"]:
            pixmap = self.movie.currentPixmap()
        else:
            # Get the thumbnail cache instance
            cache = thc.ThumbnailCache.instance()
            # lazy loading of the thumbnail
            pixmap = cache.request(item.thumbpath)
        
        if not pixmap:
            pixmap = QtGui.QPixmap()
        scaled = pixmap.scaled(
                imageRect.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
        # center image
        x = imageRect.x() + (imageRect.width() - scaled.width()) // 2
        y = imageRect.y() + (imageRect.height() - scaled.height()) // 2

        painter.drawPixmap(x, y, scaled)
        text = index.data(QtCore.Qt.DisplayRole)

        if index == self.hover_index:
            painter.setPen(QtGui.QColor("white"))
        else:
            painter.setPen(QtGui.QColor("black"))
        painter.drawText(
            textRect,
            QtCore.Qt.AlignCenter,
            text
        )
        painter.restore()

    def updateIndex(self, index):
        if index.isValid():
            rect = self.view.visualRect(index)
            QtCore.QTimer.singleShot(0, lambda: self.view.viewport().update(rect))
    
    def set_hover_index(self, index):
        if self.hover_index == index:
            return
        
        self.stopMovie()
        self.hover_index = QtCore.QPersistentModelIndex(index)
        item = index.data(QtCore.Qt.UserRole)
        gif_path = item.stamped.replace("png", "gif").replace("_stamped", "")
        self.movie = QtGui.QMovie(gif_path)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.frameChanged.connect(self.on_frame_changed)
        self.movie.start()
        self.updateIndex(index)

    def clear_hover_index(self):
        self.stopMovie()
        oldIdx = self.hover_index
        self.hover_index = QtCore.QPersistentModelIndex()
        if oldIdx.isValid():
            self.updateIndex(oldIdx)
    
    def stopMovie(self):
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None
    
    def on_frame_changed(self):
        if self.hover_index.isValid():
            self.updateIndex(self.hover_index)

    def sizeHint(self, option, index):
        return QtCore.QSize(140, 140)