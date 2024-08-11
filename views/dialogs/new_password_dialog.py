from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt

# local imports
from utils.window import WindowConfiguration
from controllers.login_controllers import LoginController
from controllers.windows_controllers import WindowsControllers
from utils.config import CONFIG

# Constantes para la longitud de la contraseña
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 16

class NewPasswordDialog(QDialog):
    def __init__(self, id):
        """ Initialize the dialog with the given id """
        super().__init__()
        self.id = id
        self.init_ui()

    def init_ui(self):
        """ Set up the UI components """
        WindowConfiguration.configure(
            self, 
            CONFIG["new_password_dialog"]["WINDOW_TITLE"], 
            CONFIG["LOGO_PATH"], 
            CONFIG["new_password_dialog"]["WINDOW_X"], 
            CONFIG["new_password_dialog"]["WINDOW_Y"], 
            CONFIG["new_password_dialog"]["WINDOW_WIDTH"], 
            CONFIG["new_password_dialog"]["WINDOW_HEIGHT"]
        )
        self.create_widgets()

    def create_widgets(self):
        """ Create and arrange the widgets """
        main_layout = QVBoxLayout()

        # Add title and message
        label_title = QLabel('Recuperar Contraseña', alignment=Qt.AlignCenter)
        main_layout.addWidget(label_title)

        label_message = QLabel('Por favor ingrese su nueva Contraseña de acceso', alignment=Qt.AlignCenter)
        main_layout.addWidget(label_message)

        # Add label for new password
        label_new_password = QLabel('Nueva contraseña')
        main_layout.addWidget(label_new_password)

        # Add input for new password
        self.input_new_password = QLineEdit()
        self.input_new_password.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña mientras se escribe
        main_layout.addWidget(self.input_new_password)

        # Add label for confirm password
        label_confirm_password = QLabel('Introduzca nuevamente su contraseña')
        main_layout.addWidget(label_confirm_password)

        # Add input for confirm password
        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña mientras se escribe
        main_layout.addWidget(self.input_confirm_password)

        # Add button success
        btn_success = QPushButton('Aceptar')
        btn_success.clicked.connect(self.handle_success)
        main_layout.addWidget(btn_success)

        self.setLayout(main_layout)

    def handle_success(self):
        """ Handle the success button click event """
        new_password = self.input_new_password.text()
        confirm_password = self.input_confirm_password.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, 'Error', 'Por favor llene todos los campos')
            return

        if len(new_password) < MIN_PASSWORD_LENGTH:
            QMessageBox.warning(self, 'Error', f'La contraseña debe contener al menos {MIN_PASSWORD_LENGTH} caracteres')
            return

        if len(new_password) > MAX_PASSWORD_LENGTH:
            QMessageBox.warning(self, f'Error', f'La contraseña no debe tener más de {MAX_PASSWORD_LENGTH} caracteres!')
            return

        if new_password == confirm_password:
            status, message = LoginController.update_password(self.id, new_password)
            if status:
                QMessageBox.information(self, 'Éxito', message)
                self.close()
                WindowsControllers.open_login_window()
            else:
                QMessageBox.critical(self, 'Error', message)
        else:
            QMessageBox.warning(self, 'Error', 'Las contraseñas no coinciden!')
