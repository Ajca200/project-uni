from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import os

# local imports
from controllers.adminDashboard_controller import AdminDashboardController
from views.windows.base_dashboard import BaseDashboard
from utils.config import CONFIG

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class AdminDashboard(BaseDashboard):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(CONFIG["admin_window"])

    def get_user_data(self):
        return AdminDashboardController.get_data(self.user_id)
    
    def get_user_role(self):
        return "ADMINISTRADOR"

    def add_buttons(self, grid_layout):
        icon_size = QSize(500, 500)

        buttons = [
            ("ESTUDIANTE", "image_student.png", self.handle_student),
            ("DOCENTES", "image_teachers.png", self.handle_teacher),
            ("ADMIN", "image_admins.png", self.handle_admin),
            ("SECCIONES", "image_sections.png", self.handle_sections),
            ("HISTORIAL", "image_history.png", self.handle_history),
            ("OLVIDO DE CLAVE", "image_forgot_password.png", self.handle_forgot_password),
        ]

        for i, (text, icon, handler) in enumerate(buttons):
            button = QToolButton()
            button.setText(text)
            button.setIcon(QIcon(os.path.join(PATH, f"resources/images/{icon}")))
            button.setIconSize(icon_size)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.clicked.connect(handler)  # Conectar el evento clic al handler correspondiente
            grid_layout.addWidget(button, i // 3, i % 3)

    # Métodos manejadores de eventos
    def handle_student(self):
        print("Botón de Estudiante presionado")
        # Aquí pones la lógica que quieras ejecutar al presionar el botón de estudiante

    def handle_teacher(self):
        print("Botón de Docentes presionado")
        # Lógica para el botón de docentes

    def handle_admin(self):
        print("Botón de Admin presionado")
        # Lógica para el botón de admin

    def handle_sections(self):
        print("Botón de Secciones presionado")
        # Lógica para el botón de secciones

    def handle_history(self):
        print("Botón de Historial presionado")
        # Lógica para el botón de historial

    def handle_forgot_password(self):
        print("Botón de Olvido de Clave presionado")
        # Lógica para el botón de olvido de clave
