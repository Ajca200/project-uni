import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt


PATH = os.path.join(os.path.dirname(__file__),'..','..')
sys.path.append(PATH)

# imports local
from utils.config import CONFIG
from utils.window import WindowConfiguration
from views.windows.base_gestion_teachers import BaseGestionTeachers
from controllers.admin_teachers_controller import AdminTeachercontroller

class AdminTeachers(BaseGestionTeachers):
    _instance = None
    
    def __new__(cls):
       """ Singleton pattern to ensure only one instance """
       if cls._instance is None:
            cls._instance = super().__new__(cls)
       return cls._instance 
     
    def __init__(self):
        """initialize the application"""
        super().__init__(CONFIG["teachers"])
        
    def add_header(self, layout):
        header_table = QHBoxLayout()
        header_table.setSpacing(40)
        
        header = ('IDENTIFICADOR', 'NOMBRE', 'APELLIDO','..')
        
        for label in header:
            item = QLabel(label)
            item.setAlignment(Qt.AlignCenter)
            header_table.addWidget(item)
        
        layout.addLayout(header_table)
    
    def get_data(self, scroll):
        teachers = AdminTeachercontroller.get__data__all()
        
        
        if not teachers:
            return
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        layout.setAlignment(Qt.AlignTop)
        
        for teacher in teachers: 
            row_layout = QHBoxLayout()
            
            row_data = [
                teacher['id_teacher'],
                teacher['name'],
                teacher['surname']
            ]
            
            objectname = [ 'id_teacher','name','surname']
            
            for i, data in enumerate(row_data):
                item = QLabel(str(data))
                item.setObjectName(objectname[i])
                item.setAlignment(Qt.AlignCenter)
                item.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                row_layout.addWidget(item)
            layout.addLayout(row_layout)

        # Asignar el widget de contenido al scroll
        scroll.addWidget(content_widget)

        
if __name__ == "__main__":
    app = QApplication([])
    window = AdminTeachers()
    window.showMaximized()
    sys.exit(app.exec_())