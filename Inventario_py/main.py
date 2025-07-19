import sys
from PyQt6.QtWidgets import QApplication

from controllers.login_controller import LoginController
from controllers.main_menu_controller import MainMenuController

class InventoryApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_controller = None 
        self.main_menu_controller = None
        self.logged_in_username = None

    def set_logged_in_user(self, username):
        """Guarda el nombre de usuario que ha iniciado sesión."""
        self.logged_in_username = username

    def show_login(self):
        """Muestra la ventana de login."""
        # Se asegura de que no haya una ventana principal abierta si se vuelve del logout
        if self.main_menu_controller and self.main_menu_controller.view.isVisible():
            self.main_menu_controller.view.close()

        # Inicializa el LoginController solo cuando se necesita
        if self.login_controller is None:
            self.login_controller = LoginController(self)
            # *** CRUCIAL: Conectar las señales del LoginController a los slots de InventoryApp ***
            self.login_controller.login_successful.connect(self._on_login_success)
            self.login_controller.login_failed.connect(self._on_login_failure)

        # Muestra la ventana de login. Ya no se espera un valor de retorno aquí.
        self.login_controller.show_login()

    def _on_login_success(self, username):
        """
        Método (slot) llamado por LoginController cuando el login es exitoso.
        """
        self.set_logged_in_user(username)
        # Si el login es exitoso, mostrar el menú principal
        if self.main_menu_controller is None:
            self.main_menu_controller = MainMenuController(self.logged_in_username, self)
        else:
            # Si ya existe, solo actualiza el mensaje de bienvenida y lo muestra
            self.main_menu_controller.view.set_welcome_message(self.logged_in_username)
        self.main_menu_controller.show_main_menu()

    def _on_login_failure(self):
        """
        Método (slot) llamado por LoginController cuando el login falla o la ventana se cierra.
        """
        # Si el login falla o se cierra la ventana de login sin éxito, salimos de la aplicación.
        sys.exit(0) 

    def run(self):
        """Inicia la aplicación."""
        self.show_login() # Directamente muestra la pantalla de login
        # app.exec() inicia el bucle de eventos de la aplicación.
        # La aplicación se mantendrá abierta hasta que se llame a sys.exit().
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = InventoryApp()
    app.run()
