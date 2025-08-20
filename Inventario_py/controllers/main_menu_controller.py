from views.main_menu_view import MainMenuView

# Importar los controladores de cada página
# Importar los controladores de cada página que se gestionarán
from controllers.inventario_controller import InventarioController
from controllers.inicio_controller import InicioController
from controllers.proveedores_controller import ProveedoresController
from controllers.usuarios_controller import UsuariosController
from controllers.estados_controller import EstadosController


class MainMenuController:
    def __init__(self, username, app_instance):
        """
        Inicializa el controlador del menú principal.
        """
        self.app = app_instance
        self.view = MainMenuView()
        self.view.set_welcome_message(username)

        self.page_controllers = {}
        
        # Conectar los botones de la vista del menú principal a los métodos del controlador.
        self.view.set_inicio_button_callback(lambda: self._show_page(0, "inicio"))
        self.view.set_inventory_button_callback(lambda: self._show_page(1, "inventario"))
        self.view.set_suppliers_button_callback(lambda: self._show_page(2, "proveedores"))
        self.view.set_users_button_callback(lambda: self._show_page(3, "usuarios"))
        self.view.set_states_button_callback(lambda: self._show_page(4, "estados"))

        # Inicializar todos los controladores de página y pasarles su QWidget contenedor.
        self._initialize_all_page_controllers()
        
        # Establecer la página inicial que se mostrará al abrir el menú principal.
        self.view.set_current_page(0) 

    def _initialize_all_page_controllers(self):
        """
        Inicializa todos los controladores de página, pasándoles su QWidget contenedor
        desde la vista principal (MainMenuView.get_X_page_widget()).
        """
        # Página de Inicio (Índice 0)
        if "inicio" not in self.page_controllers:
            inicio_page_widget = self.view.get_inicio_page_widget()
            controller = InicioController(self.app, inicio_page_widget) # Pasa page_widget
            self.page_controllers["inicio"] = controller

        # Página de Inventario (Índice 1)
        if "inventario" not in self.page_controllers:
            inventario_page_widget = self.view.get_inventario_page_widget()
            controller = InventarioController(self.app, inventario_page_widget) # Pasa page_widget
            self.page_controllers["inventario"] = controller

        # Página de Proveedores (Índice 2)
        if "proveedores" not in self.page_controllers:
            proveedores_page_widget = self.view.get_proveedores_page_widget()
            controller = ProveedoresController(self.app, proveedores_page_widget) # Pasa page_widget
            self.page_controllers["proveedores"] = controller

        # Página de Usuarios (Índice 3)
        if "usuarios" not in self.page_controllers:
            usuarios_page_widget = self.view.get_usuarios_page_widget()
            controller = UsuariosController(self.app, usuarios_page_widget) # Pasa page_widget
            self.page_controllers["usuarios"] = controller

        # Página de Estados (Índice 4)
        if "estados" not in self.page_controllers:
            estados_page_widget = self.view.get_estados_page_widget()
            controller = EstadosController(self.app, estados_page_widget) # Pasa page_widget
            self.page_controllers["estados"] = controller


    def _show_page(self, index: int, page_name: str):
        """
        Método genérico para mostrar una página específica del QStackedWidget.
        """
        self.view.set_current_page(index)
        

    def show_main_menu(self):
        """
        Muestra la ventana del menú principal.
        """
        self.view.show()

    def handle_logout(self):
        """
        Maneja la acción de cerrar sesión.
        Cierra la ventana del menú principal y le indica a la aplicación principal
        que regrese a la pantalla de login.
        """
        self.view.close()
        self.app.show_login()

