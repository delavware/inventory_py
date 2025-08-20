from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QObject
from typing import Union # Importar Union para las anotaciones de tipo si usas Python < 3.10

from views.estado_form_dialog_view import EstadoFormDialogView
from models.estado_model import EstadoModel # Para obtener los tipos de estado

class EstadoFormDialogController(QObject):
    """
    Controlador para el formulario modal de Agregar/Editar Registro de Estado.
    Gestiona la interacción entre la vista del diálogo y los datos.
    """
    def __init__(self, parent_controller, estado_model: EstadoModel):
        """
        Inicializa el controlador del diálogo de formulario de estado.
        
        Args:
            parent_controller: El controlador padre (EstadosController) que abre este diálogo.
            estado_model (EstadoModel): La instancia del modelo de estados para obtener la lista de tipos de estado.
        """
        super().__init__(parent_controller)
        # El padre del diálogo será la página de estados, para que el diálogo se posicione correctamente.
        self.view = EstadoFormDialogView(parent_controller.page_widget) 
        self.estado_model = estado_model
        self.mode = "add" # "add" o "edit"
        self.original_record_id = None # ID del registro que se está editando

        self.view.set_save_button_callback(self.handle_save)
        self.view.set_cancel_button_callback(self.handle_cancel)

    # --- CORRECCIÓN AQUÍ: Cambiado 'dict or None' a 'dict | None' (Python 3.10+) o Union[dict, None] ---
    def show_dialog(self, mode: str, data: dict = None) -> dict | None: # o Union[dict, None] para versiones anteriores
        """
        Muestra el diálogo modal para agregar o editar un registro de estado.
        
        Args:
            mode (str): "add" para agregar, "edit" para editar.
            data (dict, opcional): Datos para pre-rellenar el formulario en modo "edit".
                                   Debe contener 'id', 'asunto', 'descripcion', 'estado_nombre'.
                                   
        Returns:
            dict or None: Los datos del formulario si se guarda (aceptado), None si se cancela.
        """
        self.mode = mode
        # Poblar el combo box con los tipos de estado disponibles del modelo
        self.view.populate_estados_combobox(self.estado_model.get_status_types()) 

        if self.mode == "add":
            self.view.set_title("Agregar Registro de Estado de Inventario")
            self.view.set_button_text("Agregar")
            self.view.clear_fields() # Asegurarse de que los campos estén limpios
        elif self.mode == "edit":
            if not data or "id" not in data:
                self.view.show_message("Error", "Datos de edición incompletos.", is_error=True)
                return None
            self.original_record_id = data["id"] # Guardar el ID del registro original
            self.view.set_title(f"Editar Registro de Estado (ID: {self.original_record_id})")
            self.view.set_button_text("Guardar")
            self.view.set_form_data(data)
        
        # Muestra el diálogo de forma modal y espera el resultado (QDialog.Accepted o QDialog.Rejected)
        if self.view.exec() == QDialog.DialogCode.Accepted:
            return self.view.get_form_data() # Retorna los datos si el diálogo fue aceptado
        return None # Retorna None si el diálogo fue cancelado o rechazado

    def handle_save(self):
        """
        Maneja la lógica cuando el usuario hace clic en el botón 'Guardar'/'Agregar' del diálogo.
        Realiza la validación básica de los campos y acepta el diálogo si es válido.
        """
        form_data = self.view.get_form_data()
        
        # Validación básica de campos
        if not form_data["asunto"]:
            self.view.show_message("Validación", "El campo 'Asunto' no puede estar vacío.", is_error=True)
            return
        if not form_data["descripcion"]:
            self.view.show_message("Validación", "El campo 'Descripción' no puede estar vacío.", is_error=True)
            return
        if not form_data["estado_nombre"]:
            self.view.show_message("Validación", "Debes seleccionar un 'Estado'.", is_error=True)
            return
        
        # Si la validación es exitosa, aceptar el diálogo.
        # Esto provoca que show_dialog() retorne los datos validados.
        self.view.accept() 

    def handle_cancel(self):
        """
        Maneja la lógica cuando el usuario hace clic en el botón 'Cancelar' del diálogo.
        Rechaza el diálogo.
        """
        self.view.reject() # Rechazar el diálogo (show_dialog() retornará None)

