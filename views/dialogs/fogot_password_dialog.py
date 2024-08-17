from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QMessageBox, QLabel, QLineEdit, QPushButton, QCommandLinkButton)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import random
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Local imports
from utils.window import WindowConfiguration
from controllers.dialogs_controller import DialogController
from controllers.login_controllers import LoginController
from utils.config import CONFIG

# Constante para el tiempo del temporizador
TIMER_DURATION_SECONDS = 10  # 5 minutos en segundos

class ResendPasswordWorker(QThread):
    finished = pyqtSignal(bool, str, str)
    email_status = pyqtSignal(bool, str, str)

    def __init__(self, user_id, email, generated_code):
        super().__init__()
        self.user_id = user_id
        self.email = email
        self.generated_code = generated_code

    def run(self):
        status, level, message = LoginController.forgot_password(self.user_id, self.email)
        self.finished.emit(status, level, message)
        
        if status:
            email_status, email_message = LoginController.send_email(self.generated_code, self.email)
            self.email_status.emit(email_status, email_message, self.generated_code)

class ForgotPasswordDialog(QDialog):
    def __init__(self, user_id, email, code):
        """ Initialize the dialog with the given code """
        super().__init__()
        self.user_id = user_id
        self.email = email
        self.code = str(code)
        self.remaining_seconds = TIMER_DURATION_SECONDS
        self.expired_code = []
        self.init_ui()

    def init_ui(self) -> None:
        """ Set up the UI components """
        WindowConfiguration.configure(
            self,
            CONFIG["forgot_password_dialog"]["WINDOW_TITLE"],
            os.path.join(PATH, CONFIG["LOGO_PATH"]),
            CONFIG["forgot_password_dialog"]["WINDOW_X"],
            CONFIG["forgot_password_dialog"]["WINDOW_Y"],
            CONFIG["forgot_password_dialog"]["WINDOW_WIDTH"],
            CONFIG["forgot_password_dialog"]["WINDOW_HEIGHT"]
        )
        self.create_widgets()
        WindowConfiguration.apply_styles(self, os.path.join(PATH, CONFIG["forgot_password_dialog"]["STYLES_PATH"]))

    def create_widgets(self):
        """ Create and arrange the widgets """
        main_layout = QVBoxLayout()

        btn_back = QCommandLinkButton('Regresar')
        btn_back.clicked.connect(self.handle_reject)
        main_layout.addWidget(btn_back)

        label_message = QLabel('Por favor ingrese el código que ha sido enviado a su correo electrónico', alignment=Qt.AlignCenter)
        label_message.setFont(QFont('Arial', 10))
        main_layout.addWidget(label_message)

        self.input_code = QLineEdit()
        self.input_code.setValidator(QIntValidator(0, 999999))
        main_layout.addWidget(self.input_code)

        btn_success = QPushButton('Aceptar')
        btn_success.clicked.connect(self.handle_success)
        main_layout.addWidget(btn_success)

        self.btn_resend_code = QPushButton()
        self.btn_resend_code.setEnabled(False)
        self.btn_resend_code.clicked.connect(self.handle_resend_code)
        main_layout.addWidget(self.btn_resend_code)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Actualizar cada segundo

    def handle_resend_code(self):
        status, message = LoginController.verify_attempts_email(self.user_id)
        
        if status:
            QMessageBox.warning(self, 'Error', message)
            return

        if self.update_attemps():
            QMessageBox.warning(self, 'Error', message)
            return

        self.expired_code.append(self.code)
        self.code = str(random.randint(100000, 999999))

        if self.code in self.expired_code:
            self.handle_resend_code()
            return    

        self.loading = DialogController.open_loading_dialog()

        self.worker = ResendPasswordWorker(self.user_id, self.email, self.code)
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
        self.loading.close_dialog()
        if email_status:
            self.update_attemps()
            self.btn_resend_code.setEnabled(False)
            self.remaining_seconds = TIMER_DURATION_SECONDS  # Reiniciar el contador
            self.timer.start(1000)
        else:
            QMessageBox.critical(self, 'Error', email_message)

    def handle_success(self):
        """ Authenticate the entered code """
        code_sent = self.input_code.text()

        if not code_sent:
            QMessageBox.warning(self, 'Error', 'Por favor introduzca el código enviado a su correo electrónico.')
            return

        if code_sent in self.expired_code:
            QMessageBox.critical(self, 'Error', 'El código ingresado ha caducado \n por favor introduzca el nuevo código enviado')
            return

        if code_sent == self.code:
            self.accept()
        else:
            QMessageBox.critical(self, 'Error', 'Código incorrecto, verifique e intente nuevamente.')

    def handle_reject(self):
        """ Cancel and close the dialog """
        self.reject()

    def update_timer(self):
        """ Update the countdown timer """
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            self.btn_resend_code.setText(f'Reenviar código: {minutes:02}:{seconds:02}')
        else:
            self.timer.stop()
            self.btn_resend_code.setEnabled(True)
            self.btn_resend_code.setText('Reenviar código')

    def update_attemps(self):
        status, message = LoginController.email_blocking_register(self.user_id)
        if not status:
            QMessageBox.critical(self, 'Error', message)

    def verify_attempts(self):
        status, message = LoginController.verify_attempts_email(self.user_id)
        if status:
            return message
        return False
