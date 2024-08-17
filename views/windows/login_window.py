import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QShortcut)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

PATH = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(PATH)

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
        self._init_ui()

    def _init_ui(self) -> None:
        """ Set up the UI components """
        WindowConfiguration.configure(
            self, CONFIG["login_window"]["WINDOW_TITLE"],
            os.path.join(PATH, CONFIG["LOGO_PATH"]), CONFIG["login_window"]["WINDOW_X"],
            CONFIG["login_window"]["WINDOW_Y"], CONFIG["login_window"]["WINDOW_WIDTH"],
            CONFIG["login_window"]["WINDOW_HEIGHT"]
        )
        self._create_widgets()
        self._setup_shortcuts()
        WindowConfiguration.apply_styles(
            self, os.path.join(PATH, CONFIG["login_window"]["STYLES_PATH"])
        )

    def _create_widgets(self) -> None:
        """ Create and arrange the widgets """
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        logo_path = os.path.join(PATH, CONFIG["login_window"]["IMAGE_PATH"])
        logo = ImageLoader(logo_path, CONFIG["login_window"]["IMAGE_SIZE"])
        main_layout.addWidget(logo)

        self._add_input_field(main_layout, 'Usuario', 'Ingrese su usuario', 'username_input')
        self._add_input_field(main_layout, 'Contraseña', 'Ingrese su contraseña', 'password_input', echo_mode=True)

        login_button = QPushButton('Acceder')
        login_button.clicked.connect(self._handle_login)
        main_layout.addWidget(login_button)

        forgot_password_label = QLabel('<a href="#">¿Ha olvidado su contraseña?</a>')
        forgot_password_label.linkActivated.connect(self._recovery_password)
        forgot_password_label.setObjectName('recovery_password')
        main_layout.addWidget(forgot_password_label)

        self.setCentralWidget(main_widget)

    def _add_input_field(self, layout, label_text, placeholder, attribute_name, echo_mode=False):
        """ Add a label and input field to the layout """
        label = QLabel(label_text)
        layout.addWidget(label)

        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if echo_mode:
            input_field.setEchoMode(QLineEdit.Password)
        setattr(self, attribute_name, input_field)
        layout.addWidget(input_field)

    def _setup_shortcuts(self) -> None:
        """ Setup keyboard shortcuts """
        QShortcut(QKeySequence(Qt.Key_Down), self).activated.connect(lambda: self.password_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Up), self).activated.connect(lambda: self.username_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Return), self).activated.connect(self._handle_login)

    def _handle_login(self) -> None:
        """ Handle the login process """
        username = self.username_input.text()
        password = self.password_input.text()

        if not self._validate_inputs(username, password):
            return

        try:
            status, level, message = LoginController.authenticate(username, password)
        except Exception as e:
            self._show_message('Error', f'Error inesperado: {str(e)}', QMessageBox.Critical)
            return

        self._process_login_result(status, level, message)

    def _process_login_result(self, status, level, message) -> None:
        """ Process the result of the login attempt """
        if status:
            self._show_message('Éxito', message, QMessageBox.Information)
            self.close()
            if level == 'administrador':
                WindowsControllers.open_admin_window(status)
            else:
                WindowsControllers.open_teacher_window()
        else:
            msg_type = QMessageBox.Warning if level == 'warning' else QMessageBox.Critical
            self._show_message('Error', message, msg_type)

    def _validate_inputs(self, username: str, password: str) -> bool:
        """ Validate the inputs """
        if not username or not password:
            self._show_message('Error', 'Por favor ingrese usuario y contraseña.', QMessageBox.Warning)
            return False
        return True

    def _show_message(self, title: str, text: str, icon: QMessageBox.Icon) -> None:
        """ Show a message box with the specified parameters """
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()

    def _recovery_password(self) -> None:
        """ Open forgot password window """
        self.close()
        WindowsControllers.open_forgot_password_window()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
