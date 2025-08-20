from PyQt6.QtWidgets import QDialog, QMessageBox # Confirma que hereda de QDialog
from PyQt6.QtCore import Qt 
from ui.login_dialog_ui import Ui_LoginDialog # Importa el diseño UI generado por pyuic6

class LoginView(QDialog): # ¡Aquí debe ser QDialog!
    def __init__(self, parent=None):
        """
        Inicializa la vista de login.
        
        Args:
            parent: El widget padre de este diálogo.
        """
        super().__init__(parent)
        
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        
        self.ui.label_message.setText("") 

    def get_credentials(self):
        """
        Obtiene el nombre de usuario y la contraseña de los campos de entrada de la UI.
        
        Retorna:
            tuple: Una tupla que contiene (username, password).
        """
        username = self.ui.txt_user.text()
        password = self.ui.txt_psw.text()
        return username, password

    def show_message(self, message, is_error=False):
        """
        Muestra un mensaje en la interfaz de login, utilizando el QLabel 'label_message'.
        
        Args:
            message (str): El texto del mensaje a mostrar.
            is_error (bool): Si es True, el texto se mostrará en rojo para indicar un error.
        """
        self.ui.label_message.setText(message)
        if is_error:
            self.ui.label_message.setStyleSheet("color: red;")
        else:
            self.ui.label_message.setStyleSheet("color: green;")

    def clear_fields(self):
        """
        Limpia los campos de entrada de usuario y contraseña y el mensaje de estado.
        """
        self.ui.txt_user.clear()
        self.ui.txt_psw.clear()
        self.ui.label_message.setText("")

    def set_login_button_callback(self, callback):
        """
        Conecta la señal 'clicked' del botón de login a una función (callback) del controlador.
        
        Args:
            callback (callable): La función del controlador a ejecutar cuando se hace clic en el botón.
        """
        self.ui.btn_login.clicked.connect(callback)

    # NO necesitas un closeEvent especial aquí, ya que QDialog.exec() lo maneja.
    # Si tuvieras uno, asegúrate de que no interfiera con el accept/reject.
    # def closeEvent(self, event):
    #     event.accept()

