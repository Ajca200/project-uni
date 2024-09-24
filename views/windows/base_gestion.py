import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCommandLinkButton,
    QFrame, QScrollArea, QSizePolicy, QToolButton
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from utils.config import CONFIG
from utils.window import WindowConfiguration

# Define the base path for resources
PATH = os.path.join(os.path.dirname(__file__), '..', '..')

class BaseGestion(QMainWindow):
    def __init__(self, config, type):
        super().__init__()
        self.config = config
        self.type = type
        self.init_UI()

    def init_UI(self):
        """Initialize the UI components"""
        # Configure the main window using external configuration
        WindowConfiguration.configure(
            self, 
            self.config["WINDOW_TITLE"],
            os.path.join(PATH, self.config["IMAGE_PATH"]),
            self.config["WINDOW_X"],
            self.config["WINDOW_Y"],
            self.config["WINDOW_WIDTH"],
            self.config["WINDOW_HEIGHT"]
        )
        
        # Apply external styles to the window
        WindowConfiguration.apply_styles(
            self, 
            os.path.join(PATH, self.config["STYLES_PATH"])
        )
        
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the widgets in the main window"""
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Create and arrange action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        self.create_action_buttons(actions_layout)
        main_layout.addWidget(actions_widget)

        # Create and add welcome message labels
        self.add_welcome_message(main_layout)

        # Create and set up the table content area
        self.setup_table_content(main_layout)
        self.footer(main_layout)

        self.setCentralWidget(main_widget)

    def create_action_buttons(self, layout):
        """Create action buttons and add them to the layout"""
        buttons_info = [
            ('Cerrar Sesion', 'link_session_close'),
            ('Docentes', 'link_teacher'),
            ('Administradores', 'link_admin'),
            ('Secciones', 'link_sections'),
            ('Historial', 'link_history'),
            ('Olvido de contraseña', 'link_forgot_password')
        ]

        for text, _ in buttons_info:
            button = QCommandLinkButton(text)
            layout.addWidget(button)

    def add_welcome_message(self, layout):
        """Create and add welcome message labels"""
        font = QFont()
        font.setBold(True)

        message_welcome = QLabel(f'GESTION DE {self.type.upper()}')
        message_welcome.setAlignment(Qt.AlignCenter)
        message_welcome.setObjectName('message_welcome')
        message_welcome.setFont(font)
        layout.addWidget(message_welcome)

        message_description = QLabel(
            'Bienvenido al centro de gestion\n'
            f'Aqui veras todos los {self.type.lower()} registrados en el plantel'
        )
        message_description.setAlignment(Qt.AlignCenter)
        message_description.setFont(font)
        message_description.setObjectName('message_description')
        layout.addWidget(message_description)

    def setup_table_content(self, layout):
        """Set up the table content with a scrollable area"""
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)

        # Add table header
        self.add_header(table_layout)

        # Create a QFrame to hold the content
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a layout for the frame
        frame_layout = QVBoxLayout(frame)
    
        # Create a scrollable area and set the frame as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(frame)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Populate the frame with data
        self.get_data(frame_layout)

        # Add the scrollable area to the table layout
        table_layout.addWidget(scroll_area)

        # Add the table layout to the main layout
        layout.addWidget(table_widget)

    def footer(self, layout):
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)

        btn_report = QToolButton()
        btn_report.setIcon(QIcon(os.path.join(PATH, 'resources/images/descargar.png')))
        btn_report.setIconSize(QSize(70,70))
        btn_report.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        footer_layout.addWidget(btn_report)

        btn_add_user = QToolButton()
        btn_add_user.setIcon(QIcon(os.path.join(PATH, 'resources/images/agregar.png')))
        btn_add_user.setIconSize(QSize(70,70))
        btn_add_user.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        footer_layout.addWidget(btn_add_user)

        layout.addWidget(footer_widget)

    def add_header(self, layout):
        raise NotImplementedError

    def get_data(self, scroll):
        raise NotImplementedError
