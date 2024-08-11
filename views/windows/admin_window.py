from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QPushButton, QMessageBox, QCommandLinkButton, QGroupBox, QFormLayout, QToolButton)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from datetime import datetime

# local impots
from controllers.adminDashboard_controller import AdminDashboardController
from utils.window import WindowConfiguration
from utils.config import CONFIG
from utils.image import ImageLoader

class AdminWindow(QMainWindow):
    _instance = None
    
    def __new__(cls, user_id):
        """ Singleton pattern to ensure only one instance """
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self, user_id):
        """ initialize the application """
        super().__init__()
        print(user_id)
        self.__user_data = AdminDashboardController.get_data(user_id)
        self.initUI()

    def initUI(self) -> None:
        """ set up the UI components """
        WindowConfiguration.configure(self,CONFIG['admin_window']['WINDOW_TITLE'],
                                    CONFIG['admin_window']['IMAGE_PATH'],
                                    CONFIG['admin_window']['WINDOW_X'],
                                    CONFIG['admin_window']['WINDOW_Y'],
                                    CONFIG['admin_window']['WINDOW_WIDTH'],
                                    CONFIG['admin_window']['WINDOW_HEIGHT'])
        self.create_widgets()
        WindowConfiguration.apply_styles(self, CONFIG['admin_window']['STYLES_PATH'])

    def create_widgets(self):
        """ create and arrange the widgets """

        main_widget = QWidget()
        main_widget.setObjectName('main')
        main_layout = QHBoxLayout(main_widget)

        # container options
        left_widget = QWidget()
        left_widget.setObjectName('left_widget')
        left_layout = QVBoxLayout(left_widget)

        # add llin button
        btn_close_session = QCommandLinkButton('Cerrar Sesion')
        btn_close_session.setIcon(QIcon(CONFIG['admin_window']['ICON_PATH']))
        left_layout.addWidget(btn_close_session)

        # add message welcome
        message_welcome = QLabel('BIENVENIDO')
        message_welcome.setAlignment(Qt.AlignCenter)
        message_welcome.setObjectName('message_welcome')
        font = QFont()
        font.setBold(True)
        message_welcome.setFont(font)
        left_layout.addWidget(message_welcome)

        message_description = QLabel('Por favor seleccione la opcion que deea realizar')
        message_description.setAlignment(Qt.AlignCenter)
        message_description.setFont(font)
        message_description.setObjectName('message_decription')
        left_layout.addWidget(message_description)

        # container of botons
        grid_layout = QGridLayout()

        icon_size = QSize(500,500)

        btn_student = QToolButton()
        btn_student.setText("ESTUDIANTE")
        btn_student.setIcon(QIcon("resources/images/image_student.png"))
        btn_student.setIconSize(icon_size)
        btn_student.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        btn_teacher = QToolButton()
        btn_teacher.setText("DOCENTES")
        btn_teacher.setIcon(QIcon("resources/images/image_teachers.png"))
        btn_teacher.setIconSize(icon_size)
        btn_teacher.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        btn_admin = QToolButton()
        btn_admin.setText("ADMIN")
        btn_admin.setIcon(QIcon("resources/images/image_admins.png"))
        btn_admin.setIconSize(icon_size)
        btn_admin.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        btn_sections = QToolButton()
        btn_sections.setText("SECCIONES")
        btn_sections.setIcon(QIcon("resources/images/image_sections.png"))
        btn_sections.setIconSize(icon_size)
        btn_sections.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        btn_history = QToolButton()
        btn_history.setText("HISTORIAL")
        btn_history.setIcon(QIcon("resources/images/image_history.png"))
        btn_history.setIconSize(icon_size)
        btn_history.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        btn_forgot_password = QToolButton()
        btn_forgot_password.setText("OLVIDO DE CLAVE")
        btn_forgot_password.setIcon(QIcon("resources/images/image_forgot_password.png"))
        btn_forgot_password.setIconSize(icon_size)
        btn_forgot_password.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Añadir botones al layout de la cuadrícula
        grid_layout.addWidget(btn_student, 0, 0)
        grid_layout.addWidget(btn_teacher, 0, 1)
        grid_layout.addWidget(btn_admin, 0, 2)
        grid_layout.addWidget(btn_sections, 1, 0)
        grid_layout.addWidget(btn_history, 1, 1)
        grid_layout.addWidget(btn_forgot_password, 1, 2)

        left_layout.addLayout(grid_layout)

        # Sección derecha (información del administrador)
        right_widget = QGroupBox("ADMINISTRADOR")
        right_layout = QFormLayout(right_widget)

        profile_picture = ImageLoader('resources/images/image_none.png', 200)
        lbl_id = QLabel(f'CEDULA: {self.__user_data[0]}')
        lbl_name = QLabel(f"NOMBRE: {self.__user_data[1]}")
        lbl_lastname = QLabel(f"APELLIDO: {self.__user_data[2]}")
        lbl_birthdate = QLabel(f"FECHA DE NACIMIENTO: {datetime.strftime(self.__user_data[3], '%d/%m/%Y')}")
        lbl_phone = QLabel(f"TELÉFONO: {self.__user_data[4]}")
        lbl_email = QLabel(f"CORREO: {self.__user_data[5]}")
        lbl_address = QLabel(f"DIRECCIÓN: {self.__user_data[6]}")

        right_layout.addRow('', profile_picture)  # Para la imagen
        right_layout.addRow(lbl_id)
        right_layout.addRow(lbl_name)
        right_layout.addRow(lbl_lastname)
        right_layout.addRow(lbl_birthdate)
        right_layout.addRow(lbl_phone)
        right_layout.addRow(lbl_email)
        right_layout.addRow(lbl_address)


        # main container
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

       
        self.setCentralWidget(main_widget)

