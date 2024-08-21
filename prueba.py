from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame, QAbstractScrollArea, QScrollArea)

class Prueba(QMainWindow):
    def __init__(self):
        self.setWindowTitle('prueba')
        self.setGeometry(350,150,150,150)

        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        frame = QFrame()
        container = QAbstractScrollArea()
        area = QScrollArea