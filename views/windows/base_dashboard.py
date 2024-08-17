import os
import requests
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCommandLinkButton, QLabel,
                             QGridLayout, QToolButton, QGroupBox, QFormLayout)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from dotenv import load_dotenv

# local imports
from utils.window import WindowConfiguration

# contantes
PATH = os.path.join(os.path.dirname(__file__), '..', '..')

class BaseDashboard(QMainWindow):
    _instance = None

    def __new__(cls, *argvs):
        """ Singleton pattern to ensure only one instance """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.__user_data = self.get_user_data()
        self.init_UI()

    def init_UI(self):
        """Set up the UI components"""
        WindowConfiguration.configure(self, self.config["WINDOW_TITLE"],
                                      os.path.join(PATH, self.config["IMAGE_PATH"]),
                                      self.config["WINDOW_X"],
                                      self.config["WINDOW_Y"],
                                      self.config["WINDOW_WIDTH"],
                                      self.config["WINDOW_HEIGHT"])
        WindowConfiguration.apply_styles(self, os.path.join(PATH, self.config["STYLES_PATH"]))
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the widgets"""
        main_widget = QWidget()
        main_widget.setObjectName('main')
        main_layout = QHBoxLayout(main_widget)

        # Left widget
        left_widget = QWidget()
        left_widget.setObjectName('left_widget')
        left_layout = QVBoxLayout(left_widget)

        btn_close_session = QCommandLinkButton('Cerrar Sesion')
        btn_close_session.setIcon(QIcon(os.path.join(PATH, self.config['ICON_PATH'])))
        left_layout.addWidget(btn_close_session)

        # Welcome message
        message_welcome = QLabel('BIENVENIDO')
        message_welcome.setAlignment(Qt.AlignCenter)
        message_welcome.setObjectName('message_welcome')
        font = QFont()
        font.setBold(True)
        message_welcome.setFont(font)
        left_layout.addWidget(message_welcome)

        message_description = QLabel('Por favor seleccione la opción que desea realizar')
        message_description.setAlignment(Qt.AlignCenter)
        message_description.setFont(font)
        message_description.setObjectName('message_description')
        left_layout.addWidget(message_description)

        # Container of buttons
        grid_layout = QGridLayout()
        self.add_buttons(grid_layout)
        left_layout.addLayout(grid_layout)

        # Main container
        main_layout.addWidget(left_widget)
        self.setup_right_widget(main_layout)

        main_layout.setStretch(0, 7)
        main_layout.setStretch(1, 3)

        self.setCentralWidget(main_widget)

    def setup_right_widget(self, main_layout):
        """Setup the right widget area, overridden by subclasses if needed"""
        right_widget = QGroupBox(self.get_user_role())
        right_layout = QFormLayout(right_widget)

        self.profile_picture_label = QLabel()
        self.profile_picture_label.setPixmap(QPixmap(os.path.join(PATH, "resources/images/image_none.png")).scaled(300, 300, Qt.KeepAspectRatio))

        lbl_id = QLabel(f'CEDULA: {self.__user_data[0]}')
        lbl_name = QLabel(f"NOMBRE: {self.__user_data[1]}")
        lbl_lastname = QLabel(f"APELLIDO: {self.__user_data[2]}")
        lbl_birthdate = QLabel(f"FECHA DE NACIMIENTO: {datetime.strftime(self.__user_data[3], '%d/%m/%Y')}")
        lbl_phone = QLabel(f"TELÉFONO: {self.__user_data[4]}")
        lbl_email = QLabel(f"CORREO: {self.__user_data[5]}")
        lbl_address = QLabel(f"DIRECCIÓN: {self.__user_data[6]}")

        right_layout.addRow('', self.profile_picture_label)
        right_layout.addRow(lbl_id)
        right_layout.addRow(lbl_name)
        right_layout.addRow(lbl_lastname)
        right_layout.addRow(lbl_birthdate)
        right_layout.addRow(lbl_phone)
        right_layout.addRow(lbl_email)
        right_layout.addRow(lbl_address)

        main_layout.addWidget(right_widget)

    def get_user_data(self):
        raise NotImplementedError

    def get_user_role(self):
        """Return the role of the user, to be implemented by subclasses"""
        raise NotImplementedError

    def add_buttons(self, grid_layout):
        """Add specific buttons, to be implemented by subclasses"""
        raise NotImplementedError

    def load_profile_picture(self):
        """ Load and display the profile picture """
        name_image = self.__user_data[7]  # Cambia esto por el nombre real de la imagen
        image_data = self.get_profile_picture(name_image)
        if image_data:
            image = QPixmap()
            image.loadFromData(image_data)
            self.profile_picture_label.setPixmap(image.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            print("No se pudo cargar la imagen de perfil.")

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

class TeacherDashboard(BaseDashboard):
    def get_user_role(self):
        return "DOCENTE"

    def add_buttons(self, grid_layout):
        icon_size = QSize(500, 500)

        buttons = [
            ("ESTUDIANTE", "image_student.png"),
            ("SECCIONES", "image_sections.png"),
            ("HISTORIAL", "image_history.png"),
        ]

        for i, (text, icon) in enumerate(buttons):
            button = QToolButton()
            button.setText(text)
            button.setIcon(QIcon(os.path.join(PATH, f"resources/images/{icon}")))
            button.setIconSize(icon_size)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            grid_layout.addWidget(button, i // 3, i % 3)
