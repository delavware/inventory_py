import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget 
from PyQt6.QtCore import Qt, QTimer, QSize 
from pathlib import Path 

# Importar los controladores que gestionan el flujo de la aplicación
from controllers.login_controller import LoginController
from controllers.main_menu_controller import MainMenuController
# Importar el modelo de estados (asegúrate de que EstadoModel está definido y se inicializa en InventoryApp)
from models.estado_model import EstadoModel

class InventoryApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_controller = None 
        self.main_menu_controller = None
        self.logged_in_username = None
        
        # --- ¡CRUCIAL! Asegúrate de que EstadoModel se inicialice aquí ---
        # Si esta línea falta o está comentada, causará un AttributeError.
        self.estado_model = EstadoModel() 

    def set_logged_in_user(self, username):
        """Guarda el nombre de usuario que ha iniciado sesión."""
        self.logged_in_username = username

    def show_login(self):
        """
        Muestra la ventana de login (QDialog).
        Gestiona la creación del LoginController y el manejo de su resultado.
        """
        # Asegura que no haya una ventana principal abierta si se vuelve del logout
        if self.main_menu_controller and self.main_menu_controller.view.isVisible():
            self.main_menu_controller.view.close()

        # Inicializa el LoginController solo si no ha sido creado aún
        if self.login_controller is None:
            self.login_controller = LoginController(self)
            # --- IMPORTANTE: Eliminadas las conexiones a señales aquí ---
            # Ahora, LoginController.show_login() retornará directamente True/False.
            # self.login_controller.login_successful.connect(self._on_login_success)
            # self.login_controller.login_failed.connect(self._on_login_failure)

        # Muestra la ventana de login de forma modal y espera su resultado.
        # El método show_login() del controlador ahora retorna True (éxito) o False (fallo/cancelación).
        if self.login_controller.show_login(): # Si el login fue exitoso (retornó True)
            # Si el login fue exitoso, el LoginController ya habrá llamado a set_logged_in_user
            
            # Inicializa o muestra el menú principal
            if self.main_menu_controller is None:
                self.main_menu_controller = MainMenuController(self.logged_in_username, self)
            else:
                # Si ya existe (ej. después de un logout y re-login),
                # solo actualiza el mensaje de bienvenida y lo muestra.
                self.main_menu_controller.view.set_welcome_message(self.logged_in_username)
            self.main_menu_controller.show_main_menu()
        else:
            # Si el login falla o la ventana de login se cierra sin éxito, salimos de la aplicación.
            sys.exit(0) 

    # --- IMPORTANTE: Eliminados los métodos _on_login_success y _on_login_failure ---
    # La lógica ahora se maneja directamente en el bloque if/else después de login_controller.show_login().
    # def _on_login_success(self, username):
    #     pass
    # def _on_login_failure(self):
    #     pass

    def run(self):
        """Inicia la aplicación."""
        # Directamente muestra la pantalla de login (o el flujo que inicie tu app).
        self.show_login() 
        # Inicia el bucle de eventos de la aplicación.
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = InventoryApp()
    app.run()
