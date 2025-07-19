from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from ui.menu_ui import Ui_MainWindow # Importa el diseño UI generado

class MainMenuView(QMainWindow):
    def __init__(self, parent=None):
        """
        Inicializa la vista del menú principal.
        """
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Asegúrate de que tu QStackedWidget y sus páginas estén correctamente nombrados en Designer
        # y que los botones de navegación estén conectados a los callbacks del controlador.
        
    def set_welcome_message(self, username):
        """
        Establece el mensaje de bienvenida en la interfaz del menú principal.
        """
        #self.ui.label_welcome.setText(f"¡Bienvenido, {username}!")

    def set_current_page(self, index: int):
        """
        Cambia la página visible en el QStackedWidget por su índice.
        
        Args:
            index (int): El índice de la página a mostrar.
        """
        if 0 <= index < self.ui.stackedWidget.count():
            self.ui.stackedWidget.setCurrentIndex(index)
        else:
            print(f"Error: Índice de página inválido: {index}. El QStackedWidget tiene {self.ui.stackedWidget.count()} páginas.")

    # --- Métodos para obtener las referencias a los QWidget de cada página ---
    # Estos métodos permiten a los controladores de página acceder a su QWidget contenedor.
    def get_inicio_page_widget(self) -> QWidget:
        return self.ui.inicio_page # Asumiendo objectName 'inicio_page' en main_menu.ui

    def get_inventario_page_widget(self) -> QWidget:
        return self.ui.inventario_page # Asumiendo objectName 'inventario_page' en main_menu.ui

    def get_proveedores_page_widget(self) -> QWidget:
        return self.ui.proveedores_page # Asumiendo objectName 'proveedores_page' en main_menu.ui

    def get_usuarios_page_widget(self) -> QWidget:
        return self.ui.usuarios_page # Asumiendo objectName 'usuarios_page' en main_menu.ui

    def get_estados_page_widget(self) -> QWidget:
        return self.ui.estados_page # Asumiendo objectName 'estados_page' en main_menu.ui


    # Métodos para conectar los botones del menú a callbacks del controlador
    def set_inicio_button_callback(self, callback):
        self.ui.btn_inicio.clicked.connect(callback) 

    def set_inventory_button_callback(self, callback):
        self.ui.btn_inventario.clicked.connect(callback) 

    def set_suppliers_button_callback(self, callback):
        self.ui.btn_proveedores.clicked.connect(callback) 

    def set_users_button_callback(self, callback):
        self.ui.btn_usuarios.clicked.connect(callback) 

    def set_states_button_callback(self, callback):
        self.ui.btn_estados.clicked.connect(callback) 

