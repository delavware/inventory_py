from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime

class EstadoModel(QObject):
    """
    Modelo de datos para la gestión de registros de estado de inventario.
    Cada registro incluye asunto, descripción, tipo de estado y fecha de creación.
    Emite una señal 'estados_updated' cada vez que los datos cambian.
    """
    estados_updated = pyqtSignal() # Señal emitida cuando la lista de estados se modifica

    def __init__(self):
        """
        Inicializa el modelo de estado con una lista vacía para registros y tipos de estado,
        y un ID inicial para los nuevos registros.
        """
        super().__init__()
        self._records = [] # Lista interna para almacenar los registros completos de estado de inventario
        self._next_id = 1 # Para asignar IDs únicos a los registros
        
        # Tipos de estado predefinidos que poblarán el QComboBox en el diálogo modal
        self._status_types = [
            {"id": 1, "nombre": "Urgente"},
            {"id": 2, "nombre": "Baja prioridad"},
            {"id": 3, "nombre": "Completado"},
            {"id": 4, "nombre": "En progreso"},
            {"id": 5, "nombre": "Pendiente de revisión"},
            {"id": 6, "nombre": "Resuelto"},
            {"id": 7, "nombre": "En espera"},
        ]

        # Añadir algunos datos de ejemplo al inicio para prueba
        # Estos datos son registros completos de estado de inventario
        self.add_estado_record(
            "Stock bajo: Aspirina 500mg", "Quedan 5 cajitas", "Urgente"
        )
        self.add_estado_record(
            "Entrega pendiente: Material quirúrgico", "Confirmar recepción", "En progreso"
        )
        self.add_estado_record(
            "Equipo averiado: Rayos X", "Mantenimiento requerido", "Baja prioridad"
        )
        self.add_estado_record(
            "Inventario completo: Guantes", "Verificación final", "Completado"
        )
        self.add_estado_record(
            "Nuevo proveedor: Vacunas", "Revisar documentación", "Pendiente de revisión"
        )
        self.add_estado_record(
            "Auditoría de almacén", "Revisión general de stock", "Resuelto"
        )
        self.add_estado_record(
            "Actualización de software", "Implementación pendiente", "En espera"
        )


    def get_status_types(self):
        """
        Retorna una copia de la lista de tipos de estado disponibles.
        Estos se usarán para poblar el QComboBox en el formulario modal.
        """
        return list(self._status_types)

    def add_estado_record(self, asunto: str, descripcion: str, estado_nombre: str):
        """
        Agrega un nuevo registro de estado de inventario.
        Genera automáticamente el ID y la fecha de creación.
        
        Args:
            asunto (str): El asunto del registro de estado.
            descripcion (str): La descripción del registro de estado.
            estado_nombre (str): El nombre del tipo de estado (ej. "Urgente", "Completado").
            
        Returns:
            bool: True si el registro se agregó exitosamente, False en caso contrario.
        """
        if not all([asunto, descripcion, estado_nombre]):
            return False
        
        new_record = {
            "id": self._next_id,
            "asunto": asunto,
            "descripcion": descripcion,
            "estado_nombre": estado_nombre,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Formato YYYY-MM-DD HH:MM:SS
        }
        self._records.append(new_record)
        self._next_id += 1
        self.estados_updated.emit() # Emite la señal porque los datos han cambiado
        return True

    def get_all_estados(self):
        """
        Retorna una copia de la lista de todos los registros de estado de inventario.
        
        Returns:
            list: Una lista de diccionarios, cada uno representando un registro de estado.
        """
        return list(self._records) 

    def get_estado_by_id(self, record_id: int):
        """
        Retorna un registro de estado por su ID.
        """
        for record in self._records:
            if record["id"] == record_id:
                return record
        return None

    def update_estado_record(self, record_id: int, asunto: str, descripcion: str, estado_nombre: str):
        """
        Actualiza los detalles de un registro de estado de inventario existente.
        
        Args:
            record_id (int): El ID del registro a actualizar.
            asunto (str): El nuevo asunto.
            descripcion (str): La nueva descripción.
            estado_nombre (str): El nuevo nombre del tipo de estado (ej. "Urgente").
            
        Returns:
            bool: True si el registro se actualizó exitosamente, False en caso contrario.
        """
        if not all([asunto, descripcion, estado_nombre]):
            return False

        for i, record in enumerate(self._records):
            if record["id"] == record_id:
                self._records[i]["asunto"] = asunto
                self._records[i]["descripcion"] = descripcion
                self._records[i]["estado_nombre"] = estado_nombre
                # La fecha de creación no se actualiza al editar, solo al crear.
                self.estados_updated.emit()
                return True
        return False

    def delete_estado_record(self, record_id: int):
        """
        Elimina un registro de estado de inventario por su ID.
        """
        initial_len = len(self._records)
        self._records = [r for r in self._records if r["id"] != record_id]
        if len(self._records) < initial_len:
            self.estados_updated.emit() 
            return True
        return False

    def search_estados(self, search_term: str):
        """
        Busca registros de estado por asunto, descripción o nombre de tipo de estado (insensible a mayúsculas/minúsculas).
        
        Args:
            search_term (str): El término de búsqueda.
            
        Returns:
            list: Una lista de registros de estado que coinciden con el término.
        """
        search_term = search_term.lower()
        return [
            record for record in self._records 
            if search_term in record["asunto"].lower() or 
               search_term in record["descripcion"].lower() or 
               search_term in record["estado_nombre"].lower()
        ]

