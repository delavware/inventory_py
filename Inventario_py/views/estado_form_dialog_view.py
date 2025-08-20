from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.estado_form_dialog_ui import Ui_Estado_form_dialog # Asegúrate que este nombre de clase sea correcto

class EstadoFormDialogView(QDialog):
    """
    Vista para el formulario modal de Agregar/Editar Estado.
    Carga el diseño UI desde estado_form_dialog.ui.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Estado_form_dialog() # Instancia la clase UI generada
        self.ui.setupUi(self) # Configura la UI en este diálogo

    def set_title(self, title: str):
        """Establece el título del diálogo modal."""
        if hasattr(self.ui, 'lbl_titulo'): # Asegúrate que este label existe en tu UI
            self.ui.lbl_titulo.setText(title)

    def set_button_text(self, text: str):
        """Establece el texto del botón de guardar/agregar."""
        if hasattr(self.ui, 'btn_agregar'):
            self.ui.btn_agregar.setText(text)

    def get_form_data(self) -> dict:
        """
        Obtiene los datos del formulario de entrada.
        
        Returns:
            dict: Diccionario con 'asunto', 'descripcion', 'estado_nombre'.
        """
        asunto = self.ui.txt_asunto.text().strip()
        descripcion = self.ui.lbl_descripcion.text().strip()
        estado_nombre = self.ui.cbo_estado.currentText()
        return {
            "asunto": asunto,
            "descripcion": descripcion,
            "estado_nombre": estado_nombre
        }

    def set_form_data(self, data: dict):
        """
        Rellena el formulario con los datos proporcionados (para edición).
        
        Args:
            data (dict): Diccionario con 'asunto', 'descripcion', 'estado_nombre'.
        """
        self.ui.txt_asunto.setText(data.get("asunto", ""))
        self.ui.txt_descripcion.setText(data.get("descripcion", ""))
        
        # Seleccionar el estado en el QComboBox
        estado_nombre = data.get("estado_nombre", "")
        index = self.ui.cbo_estado.findText(estado_nombre)
        if index != -1:
            self.ui.cbo_estado.setCurrentIndex(index)
        else:
            self.ui.cbo_estado.setCurrentIndex(0) # Seleccionar el primero si no se encuentra

    def populate_estados_combobox(self, estados_list: list):
        """
        Rellena el QComboBox con los nombres de los estados disponibles.
        
        Args:
            estados_list (list): Lista de diccionarios de estados (ej. [{'id': 1, 'nombre': 'Urgente'}]).
        """
        self.ui.cbo_estado.clear()
        for estado in estados_list:
            self.ui.cbo_estado.addItem(estado['nombre'])
        
    def set_save_button_callback(self, callback):
        """Conecta el botón 'Guardar'/'Agregar'."""
        self.ui.btn_agregar.clicked.connect(callback)

    def set_cancel_button_callback(self, callback):
        """Conecta el botón 'Cancelar'."""
        self.ui.btn_cancelar.clicked.connect(callback)

    def show_message(self, title: str, message: str, is_error: bool = False):
        """Muestra un mensaje al usuario (usando QMessageBox para el diálogo)."""
        if is_error:
            QMessageBox.critical(self, title, message)
        else:
            QMessageBox.information(self, title, message)

