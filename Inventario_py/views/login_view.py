from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt6.QtCore import Qt # Necesario para Qt.WindowType.Window (si se usa)
from ui.login_ui import Ui_LoginDialog # Importa el diseño UI generado por pyuic6

class LoginView(QMainWindow):
    def __init__(self, parent=None):
        """S
        Inicializa la vista de login.
        
        Args:
            parent: El widget padre de este diálogo.
        """
        super().__init__(parent)
        
        # Instancia la clase de la UI generada automáticamente desde login.ui
        self.ui = Ui_LoginDialog()
        
        # Configura la interfaz de usuario en este QDialog
        self.ui.setupUi(self)
    

    def get_credentials(self):
        """
        Obtiene el nombre de usuario y la contraseña de los campos de entrada de la UI.
        
        Retorna:
            tuple: Una tupla que contiene (username, password).
        """
        username = self.ui.txt_user.text()
        password = self.ui.txt_psw.text()
        return username, password
    

    def clear_fields(self):
        """
        Limpia los campos de entrada de usuario y contraseña y el mensaje de estado.
        """
        self.ui.txt_user.clear()
        self.ui.txt_psw.clear()


    def set_login_button_callback(self, callback):
        """
        Conecta la señal 'clicked' del botón de login a una función (callback) del controlador.
        
        Args:
            callback (callable): La función del controlador a ejecutar cuando se hace clic en el botón.
        """
        # Asegúrate de que tu `login.ui` tenga un QPushButton con objectName 'pushButton_login'
        self.ui.btn_login.clicked.connect(callback)

