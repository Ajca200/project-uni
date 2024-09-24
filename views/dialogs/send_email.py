import sys
import os
import threading
import requests
import time
from PyQt5.QtWidgets import (QApplication ,QDialog, QVBoxLayout, QTextEdit, QLabel, QPushButton, QDesktopWidget,
                             QMessageBox, QProgressBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QMetaObject, Q_ARG

PATH = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.append(PATH)

from controllers.admin_students_controller import AdminStudentController

# constantes
desktop = QDesktopWidget()
screen_width = desktop.screen().width() 
screen_height = desktop.screen().height()
PATH_ICON = 'resources/images/logo.png'
WIDTH, HEIGHT = 400, 400

class EmailService():

    @classmethod

    def send_email(cls, mensaje, email):

        progressbarDialog = BarraDeProgreso()

        progressbarDialog.show()


        # Create a separate thread for the email sending process

        thread = threading.Thread(target=cls._send_email, args=(mensaje, email, progressbarDialog))

        thread.start()


    @classmethod

    def _send_email(cls, mensaje, email, progressbarDialog):
        try:
            # Establecer un timeout de 10 segundos para el envío del correo electrónico
            timeout = 10
            start_time = time.time()
            
            status = AdminStudentController.send_email(mensaje, email)
            
            end_time = time.time()
            
            if end_time - start_time > timeout:
                # Si el timeout se alcanzó, cancelar el envío del correo electrónico
                raise TimeoutError("La conexión a internet es muy lenta o se cayó")
            
            QMetaObject.invokeMethod(progressbarDialog, "finish_progressbar_signal", Qt.QueuedConnection, Q_ARG(bool, status))

        
        except (requests.ConnectionError, TimeoutError):
            # Emitir un signal para mostrar un mensaje de error al usuario
            QMetaObject.invokeMethod(progressbarDialog, "show_error_message_signal", Qt.QueuedConnection, Q_ARG(str, "Revisa tu conexión a internet"))
            return False
        else:
            # Emitir un signal para actualizar la barra de progreso
            QMetaObject.invokeMethod(progressbarDialog, "update_progressbar_signal", Qt.QueuedConnection, Q_ARG(bool, status))
            return True
        
class BarraDeProgreso(QDialog):
    update_progressbar_signal = pyqtSignal(bool)
    show_error_message_signal = pyqtSignal(str)
    finish_progressbar_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        WIDTH, HEIGHT = 300, 100
        
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Barra de progreso")
        self.setWindowIcon(QIcon(os.path.join(PATH, PATH_ICON)))
        

        # Calculate the x-coordinate and y-coordinate
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2

        # Set the window's geometry
        self.setGeometry(x, y, WIDTH, HEIGHT)

        layout = QVBoxLayout()

        # creacion de barra de progreso
        self.progressbar = QProgressBar()
        self.progressbar.setGeometry(50,50,200,25)
        self.progressbar.setValue(0)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setTextVisible(True)

        layout.addWidget(self.progressbar)
        self.setLayout(layout)

        # creacion de setIntenval
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_progressbar)
        self.timer.start()
        self.update_progressbar_signal.connect(self.finish_progressbar)
        self.show_error_message_signal.connect(self.show_error_message)
        self.finish_progressbar_signal.connect(self.finish_progressbar)

    def update_progressbar(self):
        self.progressbar.setValue(self.progressbar.value() + 1)

        if self.progressbar.value() >= 69:
            self.timer.stop()

    def finish_progressbar(self, status):
        self.timer.stop()

        self.progressbar.setValue(100)
        
        self.on_email_sent(status)

    def on_email_sent(self, status):
        if status:
            QMessageBox.information(None, 'Exito', 'Mensaje enviado exitosamente!')
        else:
            QMessageBox.warning(None, 'Error', 'El mensaje no se ha podido enviar')

    def show_error_message(self, message):
        QMessageBox.warning(None, 'Error', message)

class SendEmail(QDialog):
    def __init__(self, email_destino, parent=None):
        super().__init__()
        self._email_destino = email_destino
        self.configure_window()
        self.init_widgets()

    def configure_window(self):
        self.setWindowTitle('Enviar Mensaje')
        self.setWindowIcon(QIcon(os.path.join(PATH, PATH_ICON)))

        # Calculate the x-coordinate and y-coordinate
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2

        # Set the window's geometry
        self.setGeometry(x, y, WIDTH, HEIGHT)

    def init_widgets(self):
        layout = QVBoxLayout()

        title = QLabel('Mensajeria de Correo')
        layout.addWidget(title)

        # correo de destino
        destino_label = QLabel(f'Correo destino: {self._email_destino}')
        layout.addWidget(destino_label)

        # campo de texto
        self.message_edit = QTextEdit()
        layout.addWidget(self.message_edit)

        # boton de enviar
        btn_send = QPushButton('Enviar')
        btn_send.clicked.connect(self.handle_send)
        layout.addWidget(btn_send)

        # boton de cancelar
        btn_reject = QPushButton('Cancelar')
        layout.addWidget(btn_reject)

        self.setLayout(layout)

    def handle_send(self):
        message = self.message_edit.toPlainText()

        if not message:
            QMessageBox.warning(None, 'Error', 'Por favor escriba el mensaje antes de enviar el correo!')
            return
        
        if self.check_internet():
            QMessageBox.warning(None, 'Error de conexion', 'Por favor verifique su conexion a internet\ne intente nuevamente')

        email = self._email_destino

        EmailService.send_email(message, email)

    def check_internet(self):
        import requests

        try:
            requests.head('http://www.google.com', timeout=5)
            return False
        except requests.ConnectionError:
            return True

        


if __name__ == "__main__":
    app = QApplication([])

    desktop = QDesktopWidget()
    screen_width = desktop.screen().width() 
    screen_height = desktop.screen().height()

    window = SendEmail('abrahancolmenares022@gmail.com')
    #window = BarraDeProgreso()
    window.show()

    sys.exit(app.exec_())