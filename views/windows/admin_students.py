import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit)

# add path completed
PATH = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(PATH)

# imports local
from utils.config import CONFIG
from utils.window import WindowConfiguration

class AdminStudents(QMainWindow):
    _instance = None

    def __new__(cls):
        """ Singleton pattern to ensure only one instance """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """ initialize the application"""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """ set up the UI components"""
        WindowConfiguration.configure(self,
                                      CONFIG["admin_students"]["WINDOW_TITLE"],
                                      os.path.join(PATH, CONFIG["admin_students"]["IMAGE_PATH"]),
                                      CONFIG["admin_students"]["WINDOW_X"],
                                      CONFIG["admin_students"]["WINDOW_Y"],
                                      CONFIG["admin_students"]["WINDOW_WIDTH"],
                                      CONFIG["admin_students"]["WINDOW_HEIGHT"])
        
    def create_widgets(self):
        """ create and arrange the widgets"""
        pass
        
if __name__ == "__main__":
    app = QApplication([])
    window = AdminStudents()
    window.showMaximized()
    sys.exit(app.exec_())
