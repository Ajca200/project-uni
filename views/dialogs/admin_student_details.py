import sys
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication,QDialog, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QGroupBox, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

# contantes
PATH = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(PATH)

from controllers.admin_students_controller import AdminStudentController


class AdminStudentDetailsDialog(QDialog):
    def __init__(self, id_student, parent=None):
        super().__init__(parent)
        self._data_student = AdminStudentController.get_data_student(id_student)

        # configuracion de ventana
        self.setWindowTitle("Detalles del Estudiante")
        self.setWindowIcon(QIcon(os.path.join(PATH, 'resources/images/logo.png')))
        try:
            with open(os.path.join(PATH, 'resources/styles/admin_window.qss'), 'r') as style_file:
                style = style_file.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Warning: No se encontró el archivo de estilos.")

        # contenedor principal
        main_layout = QVBoxLayout()

        widget = QWidget()
        layout = QHBoxLayout(widget)

        form_student = self.container_student()
        layout.addWidget(form_student)

        form_representante = self.container_representante()
        layout.addWidget(form_representante)

        main_layout.addWidget(widget)

        btn_send_email = QPushButton('Enviar correo electronico al representante')
        btn_send_email.clicked.connect(self.open_send_email)
        main_layout.addWidget(btn_send_email)

        btn_donwload_pdf = QPushButton('Descargar planilla')
        main_layout.addWidget(btn_donwload_pdf)

        # Establecer el layout del diálogo
        self.setLayout(main_layout)

    def container_student(self):
        widget = QGroupBox('ESTUDIANTE')
        layout = QFormLayout(widget)

        self.profile_picture_label = QLabel()
        self.profile_picture_label.setPixmap(QPixmap(os.path.join(PATH, "resources/images/image_none.png")).scaled(300, 300, Qt.KeepAspectRatio))
        self.load_profile_picture(self._data_student[0])
        id = QLabel(f"ID: {self._data_student[0]}")
        name = QLabel(f"Nombre: {self._data_student[1]}")
        surname = QLabel(f"Apellido: {self._data_student[2]}")
        birthdate = QLabel(f"Fecha de nacimiento: {self._data_student[3].day}-{self._data_student[3].month}-{self._data_student[3].year}")
        section = QLabel(f"Seccion: {self._data_student[5]}")

        layout.addRow(self.profile_picture_label)
        layout.addRow(id)
        layout.addRow(name)
        layout.addRow(surname)
        layout.addRow(birthdate)
        layout.addRow(section)

        return widget

    def container_representante(self):
        widget = QGroupBox('REPRESENTANTE')
        layout = QFormLayout(widget)

        self.profile_picture_label = QLabel()
        self.profile_picture_label.setPixmap(QPixmap(os.path.join(PATH, "resources/images/image_none.png")).scaled(300, 300, Qt.KeepAspectRatio))
        self.load_profile_picture(self._data_student[6])

        id = QLabel(f"Cedula: {self._data_student[6]}")
        name = QLabel(f"Nombre: {self._data_student[7]}")
        surname = QLabel(f"Apellido: {self._data_student[8]}")
        birthdate = QLabel(f"Fecha de nacimiento: {self._data_student[9].day}-{self._data_student[9].month}-{self._data_student[3].year}")
        phone = QLabel(f"Telefono: {self._data_student[10]}")
        email = QLabel(f"Correo: {self._data_student[11]}")
        position = QLabel(f"Cargo Familiar: {self._data_student[12]}")

        layout.addRow(self.profile_picture_label)
        layout.addRow(id)
        layout.addRow(name)
        layout.addRow(surname)
        layout.addRow(birthdate)
        layout.addRow(phone)
        layout.addRow(email)
        layout.addRow(position)

        return widget

    def load_profile_picture(self, image):
        """ Load and display the profile picture """
        name_image = image  # Cambia esto por el nombre real de la imagen
        image_data = self.get_profile_picture(name_image)
        if image_data:
            image = QPixmap()
            image.loadFromData(image_data)
            self.profile_picture_label.setPixmap(image.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            print("No se pudo cargar la imagen de perfil.")

    def open_send_email(self):
        from views.dialogs.send_email import SendEmail
        
        email = self._data_student[11]

        dialog = SendEmail(email)
        dialog.exec_()

    @staticmethod
    def get_profile_picture(name_image):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()

        # Obtener la URL base del archivo .env
        base_url = os.getenv("URL")
        if not base_url:
            raise ValueError("La URL base no está configurada en el archivo .env")

        # Construir la URL completa
        endpoint = f"/image/{name_image}"
        url = base_url + endpoint

        # Realizar la solicitud GET
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si el código de estado no es 200
        except requests.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return None

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return response.content  # Devolver el contenido de la imagen
        else:
            print(f"Error al obtener la imagen: {response.status_code}")
            return None


# Ejemplo de uso:
if __name__ == "__main__":
   

    app = QApplication(sys.argv)

    dialog = AdminStudentDetailsDialog("V-30569860")
    dialog.showMaximized()

    sys.exit(app.exec_())