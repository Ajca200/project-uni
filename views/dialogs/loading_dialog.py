from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargando...")
        self.setFixedSize(110, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        
        layout = QVBoxLayout()
        
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(90, 80)  # Set the desired size here
        self.loading_label.setScaledContents(True)  # Allow scaling of the content
        layout.addWidget(self.loading_label)
        
        self.movie = QMovie("resources/gifs/loading.gif")
        self.loading_label.setMovie(self.movie)
        self.movie.start()
        
        self.setLayout(layout)

    def close_dialog(self):
        self.accept()
