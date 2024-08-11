import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QShortcut)
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtCore import Qt

# Añadir la ruta al sys.path (preferiblemente en el script principal)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importaciones locales
from controllers.login_controllers import LoginController
from controllers.windows_controllers import WindowsControllers
from utils.image import ImageLoader
from utils.window import WindowConfiguration
from utils.config import CONFIG

class LoginWindow(QMainWindow):
    _instance = None

    def __new__(cls):
        """ Singleton pattern to ensure only one instance """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """ Initialize the application """
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        """ Set up the UI components """
        WindowConfiguration.configure(self, CONFIG["login_window"]["WINDOW_TITLE"], CONFIG["LOGO_PATH"], CONFIG["login_window"]["WINDOW_X"], CONFIG["login_window"]["WINDOW_Y"], CONFIG["login_window"]["WINDOW_WIDTH"], CONFIG["login_window"]["WINDOW_HEIGHT"])
        self.create_widgets()
        self.setup_shortcuts()
        WindowConfiguration.apply_styles(self, CONFIG["login_window"]["STYLES_PATH"])

    def create_widgets(self) -> None:
        """ Create and arrange the widgets """
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Add logo
        logo = ImageLoader(CONFIG["login_window"]["IMAGE_PATH"], CONFIG["login_window"]["IMAGE_SIZE"])
        main_layout.addWidget(logo)

        # Add username input
        username_label = QLabel('Usuario')
        main_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Ingrese su usuario')
        main_layout.addWidget(self.username_input)

        # Add password input
        password_label = QLabel('Contraseña')
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Ingrese su contraseña')
        main_layout.addWidget(self.password_input)

        # Add login button
        login_button = QPushButton('Acceder')
        login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(login_button)

        # Add forgot password link
        forgot_password_label = QLabel('<a href="#">¿Ha olvidado su contraseña?</a>')
        forgot_password_label.linkActivated.connect(self.recovery_password)
        forgot_password_label.setObjectName('recovery_password')
        main_layout.addWidget(forgot_password_label)

        self.setCentralWidget(main_widget)

    def setup_shortcuts(self) -> None:
        """ Setup keyboard shortcuts """
        QShortcut(QKeySequence(Qt.Key_Down), self).activated.connect(lambda: self.password_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Up), self).activated.connect(lambda: self.username_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Return), self).activated.connect(self.handle_login)

    def handle_login(self) -> None:
        """ Handle the login process """
        username = self.username_input.text()
        password = self.password_input.text()

        if not self.validate_inputs(username, password):
            return

        try:
            status, level, message = LoginController.authenticate(username, password)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error inesperado: {str(e)}')
            return

        if status:
            QMessageBox.information(self, 'Éxito', message)
            self.close()
            if level == 'administrador':
                WindowsControllers.open_admin_window(status)
            else:
                WindowsControllers.open_teacher_window()
        else:
            if level == 'warning':
                QMessageBox.warning(self, 'Error', message)
            else:
                QMessageBox.critical(self, 'Error', message)

    def validate_inputs(self, username: str, password: str) -> bool:
        """ Validate the inputs """
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese usuario y contraseña.')
            return False
        # Add more validation logic if necessary
        return True

    def recovery_password(self) -> None:
        """ Open forgot password window """
        self.close()
        WindowsControllers.open_forgot_password_window()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
