from PySide6 import QtCore, QtGui, QtWidgets
from collections import OrderedDict
from gaolib.model.thumbnailtask import ThumbnailTask


class ThumbnailCache(QtCore.QObject):
    _instance = None
    thumbnailLoaded = QtCore.Signal(str)

    def __init__(self, max_kb=50000):
        super().__init__(QtWidgets.QApplication.instance())
        self.cache = OrderedDict()
        self.max_kb = max_kb
        self.current_kb = 0
        #
        self.loading = set()
        self.pool = QtCore.QThreadPool.globalInstance()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _pixmap_size(self, pixmap):
        return pixmap.width() * pixmap.height() * 4 // 1024

    def insert(self, key, pixmap):
        size = self._pixmap_size(pixmap)
        if key in self.cache:
            old = self.cache.pop(key)
            self.current_kb -= self._pixmap_size(old)
        self.cache[key] = pixmap
        self.current_kb += size
        while self.current_kb > self.max_kb:
            k, v = self.cache.popitem(last=False)
            self.current_kb -= self._pixmap_size(v)

    def find(self, key):
        pixmap = self.cache.get(key)
        if pixmap:
            self.cache.move_to_end(key)
        return pixmap

    def request(self, key):
        pixmap = self.cache.get(key)
        if pixmap:
            self.cache.move_to_end(key)
            return pixmap

        if key not in self.loading:
            self.loading.add(key)
            task = ThumbnailTask(key, self._on_loaded)
            self.pool.start(task)

        return None

    def _on_loaded(self, key, image):
        QtCore.QMetaObject.invokeMethod(
            self,
            "_store",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, key),
            QtCore.Q_ARG(QtGui.QImage, image),
        )

    @QtCore.Slot(str, QtGui.QImage)
    def _store(self, key, image):
        pixmap = QtGui.QPixmap.fromImage(image)

        self.insert(key, pixmap)
        self.loading.discard(key)

        self.thumbnailLoaded.emit(key)
