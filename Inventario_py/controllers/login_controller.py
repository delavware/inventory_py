from PyQt6.QtWidgets import QMainWindow # Importar QMainWindow para referencia
from PyQt6.QtCore import pyqtSignal, QObject # Necesario para definir señales
from views.login_view import LoginView
from models.user_model import UserModel

class LoginController(QObject): # Hereda de QObject para poder definir señales
    # Define señales personalizadas que este controlador emitirá
    # Esta señal se emite cuando el login es exitoso, llevando el nombre de usuario.
    login_successful = pyqtSignal(str)
    # Esta señal se emite cuando el login falla o la ventana se cierra sin éxito.
    login_failed = pyqtSignal()       

    def __init__(self, app_instance):
        super().__init__() # Llama al constructor de QObject, necesario para usar señales
        self.app = app_instance
        self.view = LoginView() # La vista de login ahora es una QMainWindow
        self.model = UserModel()
        
        # Conecta el botón de login de la vista al método handle_login del controlador.
        self.view.set_login_button_callback(self.handle_login)
        
        # Conectar la señal 'destroyed' de la ventana de login a un método del controlador.
        # Esto es crucial para detectar si el usuario cierra la ventana de login
        # sin haber intentado o completado la autenticación.
        self.view.destroyed.connect(self._on_view_destroyed)


    def show_login(self):
        """
        Muestra la ventana de login (QMainWindow).
        A diferencia de QDialog.exec(), QMainWindow.show() no bloquea la ejecución
        y no retorna un valor. El resultado del login se comunicará a través de señales.
        """
        self.view.clear_fields() # Limpia los campos antes de mostrar la ventana
        self.view.show() # Muestra la ventana de forma no modal

    def handle_login(self):
        """
        Maneja el intento de login cuando el botón 'Iniciar Sesión' es presionado.
        Esta es la lógica central del controlador para el proceso de autenticación.
        """
        # 1. Obtiene las credenciales ingresadas por el usuario desde la vista.
        username, password = self.view.get_credentials()
        
        # 2. Solicita al modelo de usuario que autentique estas credenciales.
        # El controlador no implementa la lógica de autenticación, solo la delega al modelo.
        if self.model.authenticate_user(username, password):
            # 3. Si la autenticación es exitosa:
            # Muestra un mensaje de éxito en la vista.
           # self.view.show_message("Login exitoso!", is_error=False)
            # Cierra la ventana de login.
            self.view.close() 
            # Emite la señal de login exitoso, pasando el nombre de usuario.
            # Esta señal será capturada por la clase InventoryApp (en main.py).
            self.login_successful.emit(username)
        else:
            # 4. Si la autenticación falla:
            # Muestra un mensaje de error en la vista.
            self.view.show_message("Usuario o contraseña incorrectos.", is_error=True)
            # Limpia los campos de la vista para un nuevo intento.
            self.view.clear_fields()

    def _on_view_destroyed(self):
        """
        Slot que se ejecuta cuando la ventana de login es destruida (cerrada).
        Esto se usa para detectar si el usuario cerró la ventana sin loguearse.
        """
        # Si la ventana se cierra y no hay un usuario logueado en la aplicación principal,
        # significa que el login fue cancelado o falló sin un intento exitoso.
        # En este caso, emitimos la señal de fallo para que la aplicación principal actúe (ej. salir).
        if not self.app.logged_in_username: # Verifica si la app principal ya tiene un usuario logueado
            self.login_failed.emit()

