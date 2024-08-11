from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageLoader(QWidget):
    def __init__(self, path: str = "", scale: int = 200, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        image = QLabel()
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(scale, 200, Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.setAlignment(Qt.AlignCenter)

        layout.addWidget(image)
        self.setLayout(layout)