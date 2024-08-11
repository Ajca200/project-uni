import re
import random
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QShortcut, QCommandLinkButton)
from PyQt5.QtGui import QKeySequence, QIntValidator
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Local imports
from utils.window import WindowConfiguration
from controllers.login_controllers import LoginController
from controllers.dialogs_controller import DialogController
from controllers.windows_controllers import WindowsControllers
from utils.config import CONFIG

class ForgotPasswordWorker(QThread):
    finished = pyqtSignal(bool, str, str)
    email_status = pyqtSignal(bool, str, str)

    def __init__(self, user_id, email):
        super().__init__()
        self.user_id = user_id
        self.email = email

    def run(self):
        status, level, message = LoginController.forgot_password(self.user_id, self.email)
        self.finished.emit(status, level, message)
        
        if status:
            generated_code = str(random.randint(100000, 999999))
            email_status, email_message = LoginController.send_email(generated_code, self.email)
            self.email_status.emit(email_status, email_message, generated_code)

class ForgotPasswordWindow(QMainWindow):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        WindowConfiguration.configure(
            self,
            CONFIG["forgot_password_window"]["WINDOW_TITLE"],
            CONFIG["LOGO_PATH"],
            CONFIG["forgot_password_window"]["WINDOW_X"],
            CONFIG["forgot_password_window"]["WINDOW_Y"],
            CONFIG["forgot_password_window"]["WINDOW_WIDTH"],
            CONFIG["forgot_password_window"]["WINDOW_HEIGHT"]
        )
        self.create_widgets()
        self.setup_shortcuts()
        WindowConfiguration.apply_styles(self, CONFIG["forgot_password_window"]["STYLES_PATH"])

    def create_widgets(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        back_login_button = QCommandLinkButton('Regresar')
        back_login_button.clicked.connect(self.handle_reject)
        main_layout.addWidget(back_login_button)

        title_label = QLabel('Recuperar Contraseña'.upper(), alignment=Qt.AlignCenter)
        title_label.setObjectName('title')
        main_layout.addWidget(title_label)

        message_label = QLabel('Por favor ingrese su correo electrónico registrado', alignment=Qt.AlignCenter)
        main_layout.addWidget(message_label)

        id_widget = self.create_id_widget()
        main_layout.addWidget(id_widget)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Correo electrónico')
        main_layout.addWidget(self.email_input)

        submit_button = QPushButton('Siguiente')
        submit_button.clicked.connect(self.handle_submit)
        main_layout.addWidget(submit_button)

        self.setCentralWidget(main_widget)

    def create_id_widget(self):
        id_widget = QWidget()
        id_layout = QHBoxLayout(id_widget)

        self.combobox = QComboBox()
        self.combobox.addItems(['V', 'E'])
        id_layout.addWidget(self.combobox)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('Cédula')
        self.id_input.setValidator(QIntValidator())
        id_layout.addWidget(self.id_input)

        return id_widget

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        QShortcut(QKeySequence(Qt.Key_Down), self).activated.connect(lambda: self.email_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Up), self).activated.connect(lambda: self.id_input.setFocus())
        QShortcut(QKeySequence(Qt.Key_Return), self).activated.connect(self.handle_submit)
        QShortcut(QKeySequence(Qt.Key_Escape), self).activated.connect(self.handle_reject)

    def handle_submit(self):
        self.user_id = self.combobox.currentText() + '-' + self.id_input.text()

        status, message = LoginController.verify_attempts_email(self.user_id)
        
        if status:
            QMessageBox.warning(self, 'Error', message)
            return
        
        self.email = self.email_input.text().lower()

        if not self.email or not self.user_id:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese un correo electrónico y una cédula.')
            return

        if not self.email_is_valid(self.email):
            QMessageBox.warning(self, 'Error', 'Por favor ingrese un correo electrónico válido.')
            return

        self.loading = DialogController.open_loading_dialog()

        self.worker = ForgotPasswordWorker(self.user_id, self.email)
        self.worker.finished.connect(self.on_finished)
        self.worker.email_status.connect(self.on_email_status)
        self.worker.start()

    def on_finished(self, status, level, message):
        if not status:
            if level == 'warning':
                QMessageBox.warning(self, 'Error', message)
            else:
                QMessageBox.critical(self, 'Error', message)

    def on_email_status(self, email_status, email_message, generated_code):
        if email_status:
            self.loading.close_dialog()
            self.close()
            status = DialogController.open_forgot_password_dialog(self.user_id, self.email, generated_code)
            if status:
                DialogController.open_new_password_dialog(generated_code)
        else:
            QMessageBox.critical(self, 'Error', email_message)

    def handle_reject(self):
        self.close()
        WindowsControllers.open_login_window()

    @staticmethod
    def email_is_valid(email) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
