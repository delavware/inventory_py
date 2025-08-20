from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel # QMessageBox ya no es necesario aquí
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
        Este método ahora actualiza directamente un QLabel en la UI.
        
        Args:
            username (str): El nombre de usuario a mostrar.
        """
        # Asegúrate de que tu `main_menu.ui` (o `menu.ui` según tu importación `ui.menu_ui`)
        # tenga un QLabel con objectName 'label_welcome'.
        # Si tu QLabel de bienvenida tiene otro nombre (ej. `label_usuario_logueado`), cámbialo aquí.
        if hasattr(self.ui, 'label_welcome') and isinstance(self.ui.label_welcome, QLabel):
            self.ui.label_welcome.setText(f"¡Bienvenido, {username}!")
        else:
            print("Advertencia: QLabel 'label_welcome' no encontrado o no es un QLabel en main_menu.ui. No se pudo establecer el mensaje de bienvenida.")
            # Si no tienes un QLabel para esto, considera añadirlo en Qt Designer.


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
        # Asumiendo que tu QStackedWidget tiene páginas con objectName:
        # 'inicio_page', 'inventario_page', etc.
        # Verifica los objectName en tu archivo main_menu.ui (o menu.ui).
        return self.ui.inicio_page 

    def get_inventario_page_widget(self) -> QWidget:
        return self.ui.inventario_page 

    def get_proveedores_page_widget(self) -> QWidget:
        return self.ui.proveedores_page 

    def get_usuarios_page_widget(self) -> QWidget:
        return self.ui.usuarios_page 

    def get_estados_page_widget(self) -> QWidget:
        return self.ui.estados_page 


    # Métodos para conectar los botones del menú a callbacks del controlador
    # Asegúrate de que los objectName de tus botones en main_menu.ui (o menu.ui) coinciden.
    # Por ejemplo, si tu botón de inicio se llama 'btn_inicio' en Designer.
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

   
