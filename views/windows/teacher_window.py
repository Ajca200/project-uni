from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)
import sys, os

from utils.window import WindowConfiguration
from utils.image import ImageLoader

class TeacherWindow(QMainWindow):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        WindowConfiguration.configure(self, 'Login2', '../resources/images/logo.png', 350, 150, 200, 400)
        self.widgets_loader()

    def widgets_loader(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        image = ImageLoader('../../resources/images/logo.png', 200)
        layout.addWidget(image)
