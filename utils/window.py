from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from utils.path_absolute import PathLoader

class WindowConfiguration:
    @staticmethod
    def configure(window, title="Agregar", path_icon=None, x=350, y=150, width=200, height=200):
        """Configura la ventana con el título, icono y geometría especificados."""
        window.setWindowTitle(title)
        if path_icon:
            icon_path = PathLoader.get_path(path_icon)
            window.setWindowIcon(QIcon(icon_path))
        window.setGeometry(x, y, width, height)

    @staticmethod
    def apply_styles(window, path_styles=''):
        """Aplica estilos CSS a la ventana si se proporciona un archivo de estilos."""
        if path_styles:
            try:
                with open(path_styles, 'r') as style_file:
                    style = style_file.read()
                    window.setStyleSheet(style)
            except FileNotFoundError:
                print(f"Warning: No se encontró el archivo de estilos '{path_styles}'.")

