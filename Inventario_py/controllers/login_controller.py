from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QObject

from views.login_view import LoginView
from models.user_model import UserModel # Asegúrate de que este modelo exista y su authenticate_user funcione

class LoginController(QObject):
    def __init__(self, app_instance):
        super().__init__() 
        self.app = app_instance
        self.view = LoginView() 
        self.model = UserModel()
        
        self.view.set_login_button_callback(self.handle_login)
        
    def show_login(self):
        """
        Muestra la ventana de login de forma modal (QDialog.exec()).
        """
        self.view.clear_fields() 
        print("DEPURACIÓN (LoginController): Llamando a self.view.exec()")
        dialog_result = self.view.exec()
        print(f"DEPURACIÓN (LoginController): self.view.exec() retornó: {dialog_result} ({QDialog.DialogCode(dialog_result).name})")

        if dialog_result == QDialog.DialogCode.Accepted:
            return True # Login exitoso (el diálogo fue aceptado)
        return False # Login fallido o cancelado (el diálogo fue rechazado o cerrado)

    def handle_login(self):
        """
        Maneja el intento de login cuando el botón 'Iniciar Sesión' es presionado.
        """
        username, password = self.view.get_credentials()
        print(f"DEPURACIÓN (LoginController): Intento de login para usuario: '{username}'")
        
        if self.model.authenticate_user(username, password):
            print("DEPURACIÓN (LoginController): Autenticación exitosa.")
            self.view.show_message("Login exitoso!", is_error=False)
            
            self.app.set_logged_in_user(username)
            
            print("DEPURACIÓN (LoginController): Llamando a self.view.accept()")
            self.view.accept() # Cierra el diálogo con Accepted
        else:
            print("DEPURACIÓN (LoginController): Autenticación fallida.")
            self.view.show_message("Usuario o contraseña incorrectos.", is_error=True)
            self.view.clear_fields()
            # El diálogo permanece abierto en caso de fallo para que el usuario reintente.
            # Si el usuario cierra el diálogo después de un fallo, show_login() devolverá False.

