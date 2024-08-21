import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt

# add path completed
PATH = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(PATH)

# imports local
from utils.config import CONFIG
from utils.window import WindowConfiguration
from views.windows.base_gestion import BaseGestion
from controllers.admin_students_controller import AdminStudentController

class AdminStudents(BaseGestion):
    _instance = None

    def __new__(cls):
        """ Singleton pattern to ensure only one instance """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """ initialize the application"""
        super().__init__(CONFIG["admin_students"])

    def add_header(self, layout):
        header_table = QHBoxLayout()
        header_table.setSpacing(40)

        header = ('IDENTIFICADOR', 'NOMBRE', 'APELLIDO', 'F/N', 'SECCION', '', '', '')

        for label in header:
            item = QLabel(label)
            item.setAlignment(Qt.AlignCenter)  # Establecer alineación
            item.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establecer política de tamaño
            header_table.addWidget(item)

        layout.addLayout(header_table)

    def get_data(self, scroll):
        students = AdminStudentController.get_data_all()

        if not students:
            return

        # Crear un widget que contendrá el layout
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        layout.setAlignment(Qt.AlignTop)
       
        for student in students:
            row_layout = QHBoxLayout()

            # Extraer datos del diccionario y agregarlos a la fila
            row_data = [
                student['id_student'],
                student['name'],
                student['surname'],
                student['birthdate'].strftime('%d/%m/%Y'),  # Formatear fecha
                student['fk_id_section']
            ]

            objectname = ['id_student', 'name', 'surname', 'birthdate', 'fk_id_section']

            for i, data in enumerate(row_data):
                item = QLabel(str(data))
                item.setObjectName(objectname[i])
                item.setAlignment(Qt.AlignCenter)
                item.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                item.setWordWrap(True)
                if objectname[i] == 'birthdate':
                    item.setFixedWidth(140)
                elif objectname[i] == 'fk_id_section':
                    item.setFixedWidth(100)
                else:
                    item.setFixedWidth(175)
                row_layout.addWidget(item)

            layout.addLayout(row_layout)

        # Asignar el widget de contenido al scroll
        scroll.addWidget(content_widget)

        
if __name__ == "__main__":
    app = QApplication([])
    window = AdminStudents()
    window.showMaximized()
    sys.exit(app.exec_())
