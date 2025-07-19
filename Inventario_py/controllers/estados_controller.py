from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QObject

class EstadosController(QObject):
    def __init__(self, app_instance, page_widget: QWidget):
        """
        Inicializa el controlador de la página de Inicio.
        
        Args:
            app_instance: La instancia principal de la aplicación (InventoryApp).
            page_widget (QWidget): El QWidget que representa la página de Inicio
                                   dentro del QStackedWidget de main_menu.ui.
        """
        super().__init__()
        self.app = app_instance
        self.page_widget = page_widget # Guardamos la referencia al QWidget de la página