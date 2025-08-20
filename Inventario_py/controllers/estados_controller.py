from PyQt6.QtWidgets import QWidget, QLabel, QTableView, QComboBox, QHeaderView, QMessageBox, QLineEdit, QPushButton
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QObject, Qt, QTimer, QEvent

class EstadosController(QObject):
    def __init__(self, app_instance, page_widget: QWidget):  # Recibe page_widget
        super().__init__()
        self.app = app_instance
        self.page_widget = page_widget

        # Modelo compartido
        self.estado_model = self.app.estado_model

        # --- UI de Designer ---
        # Acceder a los elementos de UI diseñados en 'estados_page'
        self.tableView_estado = self.page_widget.findChild(QTableView, "tableView_estado")
        # Asegúrate de que los siguientes objectNames existen en tu .ui para la página de estados
        self.lineEdit_estado_id = self.page_widget.findChild(QLineEdit, "lineEdit_estado_id")
        if self.lineEdit_estado_id: self.lineEdit_estado_id.setReadOnly(True)

        self.pushButton_add_estado = self.page_widget.findChild(QPushButton, "pushButton_add_estado")
        self.pushButton_edit_estado = self.page_widget.findChild(QPushButton, "pushButton_edit_estado")
        self.pushButton_delete_estado = self.page_widget.findChild(QPushButton, "pushButton_delete_estado")
        self.pushButton_clear_estado = self.page_widget.findChild(QPushButton, "pushButton_clear_estado")
        self.lineEdit_search_estado = self.page_widget.findChild(QLineEdit, "lineEdit_search_estado")
        self.pushButton_search_estado = self.page_widget.findChild(QPushButton, "pushButton_search_estado")
        self.label_estados_titulo = self.page_widget.findChild(QLabel, "label_estados_titulo")


        # Proporciones deseadas (No., Asunto, Descripción, Fecha, Estado)
        # Usaremos estos para setear anchos iniciales fijos para las primeras columnas
        self._col_widths = [5, 250, 450, 160] # Anchos fijos para las primeras 4 columnas


        # --- Tabla + modelo ---
        self.table_model = QStandardItemModel()
        if self.tableView_estado:
            tv = self.tableView_estado
            tv.setModel(self.table_model)
            tv.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            tv.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

            # Estilos
            tv.horizontalHeader().setStyleSheet(
                "QHeaderView::section { background-color: #26282A; color: white; border: none; }" # Color oscuro como en otros headers
            )
            tv.verticalHeader().setVisible(False) # Ocultar encabezado vertical
            tv.setStyleSheet("QTableView { border: none; color: white; }")
            tv.horizontalHeader().setMinimumSectionSize(0)
            tv.verticalHeader().setMinimumSectionSize(0)

            # Ya no es necesario installEventFilter para el redimensionamiento de columnas
            # ya que la última sección se estirará automáticamente.
            # tv.installEventFilter(self)

        else:
            print("Advertencia: tableView_estado NO encontrado en la página de estados del Designer.")

        # Conexiones de botones (asegúrate de que los botones existen en tu .ui)
        if self.pushButton_add_estado: self.pushButton_add_estado.clicked.connect(self.open_add_dialog)
        if self.pushButton_edit_estado: self.pushButton_edit_estado.clicked.connect(self.open_edit_dialog)
        if self.pushButton_delete_estado: self.pushButton_delete_estado.clicked.connect(self.delete_estado_record)
        if self.pushButton_clear_estado: self.pushButton_clear_estado.clicked.connect(self.clear_fields)
        if self.pushButton_search_estado: self.pushButton_search_estado.clicked.connect(self.search_estado_records)
        if self.tableView_estado: self.tableView_estado.clicked.connect(self._on_table_item_clicked) # Conectar clic de tabla

        if self.label_estados_titulo:
            self.label_estados_titulo.setText("Gestión de Registros de Estado de Inventario")
            self.label_estados_titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")


        # Señal del modelo
        self.estado_model.estados_updated.connect(self._load_estados_data) # Cambiado a _load_estados_data para consistencia

        # Cargar datos iniciales
        self._load_estados_data()

    # --------- Núcleo del ajuste de columnas ---------
    def _apply_column_widths(self):
        """Aplica anchos fijos a las primeras columnas y estira la última."""
        tv = self.tableView_estado
        if not tv:
            return

        header = tv.horizontalHeader()
        cols = self.table_model.columnCount()

        # Si no hay columnas definidas en el modelo todavía, no hacer nada
        if cols == 0:
            return

        # Aplicar anchos fijos a las columnas especificadas
        for i, width in enumerate(self._col_widths):
            if i < cols: # Asegurarse de no exceder el número de columnas reales
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed) # Modo Fixed para anchos exactos
                header.resizeSection(i, width)
        
        # Estirar la última columna para que ocupe el espacio restante
        # Asegurarse de que hay al menos 5 columnas (4 fijas + 1 que se estira)
        if cols >= len(self._col_widths) + 1:
            header.setSectionResizeMode(cols - 1, QHeaderView.ResizeMode.Stretch)
        elif cols > 0: # Si hay columnas, y no hay suficientes para un "stretch" más allá de las fijas, estira la última que hay.
             header.setSectionResizeMode(cols - 1, QHeaderView.ResizeMode.Stretch)


    # El eventFilter para redimensionamiento automático de columnas ya no es necesario
    # con setStretchLastSection si solo quieres que la última columna se estire.
    # Si quieres redimensionamiento complejo de todas las columnas al cambiar el tamaño de la ventana,
    # entonces el eventFilter podría volver.
    # def eventFilter(self, obj, event):
    #     if obj is self.tableView_estado and event.type() == QEvent.Type.Resize:
    #         # Es importante que el layout del QWidget padre permita que la tabla crezca.
    #         # self._apply_column_widths() # Re-aplicar al redimensionar si es necesario
    #     return super().eventFilter(obj, event)

    # --------- Carga de datos ---------
    def _load_estados_data(self): # Renombrado para consistencia con StatesController
        if not self.table_model or not self.tableView_estado:
            return

        self.table_model.clear()

        # Cabeceras PRIMERO (importante: crean las secciones del header)
        headers = ["No.", "Asunto", "Descripción", "Fecha", "Estado"]
        self.table_model.setHorizontalHeaderLabels(headers)

        # Datos (obtener todos los registros de estado del modelo)
        all_estado_records = self.estado_model.get_all_estados()
        
        records_to_display = all_estado_records # Cargar todos los registros

        for row_idx, record in enumerate(records_to_display):
            id_item = QStandardItem(str(record.get("id", "")))
            asunto_item = QStandardItem(record.get("asunto", ""))
            descripcion_item = QStandardItem(record.get("descripcion", ""))
            fecha_item = QStandardItem(record.get("fecha_creacion", ""))
            estado_nombre_item = QStandardItem(record.get("estado_nombre", ""))

            estado_texto = record.get("estado_nombre", "")
            if estado_texto == "Urgente":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkRed)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto == "Baja prioridad":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkYellow)
                estado_nombre_item.setForeground(Qt.GlobalColor.black)
            elif estado_texto in ("Completado", "Resuelto"):
                estado_nombre_item.setBackground(Qt.GlobalColor.darkGreen)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto == "En progreso":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkBlue)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto in ("Pendiente de revisión", "En espera"):
                estado_nombre_item.setBackground(Qt.GlobalColor.darkGray)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)

            self.table_model.setItem(row_idx, 0, id_item)
            self.table_model.setItem(row_idx, 1, asunto_item)
            self.table_model.setItem(row_idx, 2, descripcion_item)
            self.table_model.setItem(row_idx, 3, fecha_item)
            self.table_model.setItem(row_idx, 4, estado_nombre_item)

        # ¡Ahora sí! aplicar anchos y estiramiento después de que los datos estén cargados
        # y las columnas existan en el modelo
        self._apply_column_widths()

    # --- Manejo de la selección de tabla ---
    def _on_table_item_clicked(self, index):
        """
        Cuando se selecciona una fila en la tabla, se guarda el ID del registro
        y se muestra en el lineEdit correspondiente si existe.
        """
        if not self.table_model or not self.lineEdit_estado_id: return
        row = index.row()
        record_id = int(self.table_model.item(row, 0).text())
        self.selected_record_id = record_id
        self.lineEdit_estado_id.setText(str(record_id))

    # --- Lógica de CRUD para Estados (usando QMessageBox en lugar de show_message de la vista) ---
    def open_add_dialog(self):
        # Importación local para evitar circular imports si es un diálogo independiente
        from controllers.estado_form_dialog_controller import EstadoFormDialogController
        dialog_controller = EstadoFormDialogController(self, self.app.estado_model) # Pasar el modelo de estado
        result = dialog_controller.show_dialog(mode="add")

        if result:
            self.estado_model.add_estado_record(
                result["asunto"],
                result["descripcion"],
                result["estado_nombre"]
            )
            QMessageBox.information(self.page_widget, "Éxito", "Registro de estado agregado exitosamente.")
            self.clear_fields() # Limpia los campos y refresca la tabla

    def open_edit_dialog(self):
        from controllers.estado_form_dialog_controller import EstadoFormDialogController
        if not hasattr(self, 'selected_record_id') or self.selected_record_id is None:
            QMessageBox.warning(self.page_widget, "Selección Requerida", "Selecciona un registro de estado de la tabla para editar.")
            return

        record_to_edit = self.estado_model.get_estado_by_id(self.selected_record_id)
        if not record_to_edit:
            QMessageBox.warning(self.page_widget, "Error", "Registro de estado no encontrado para edición.")
            return
        
        data_for_dialog = {
            "id": record_to_edit["id"],
            "asunto": record_to_edit["asunto"],
            "descripcion": record_to_edit["descripcion"],
            "estado_nombre": record_to_edit["estado_nombre"]
        }

        dialog_controller = EstadoFormDialogController(self, self.app.estado_model)
        result = dialog_controller.show_dialog(mode="edit", data=data_for_dialog)

        if result:
            self.estado_model.update_estado_record(
                self.selected_record_id, # Usar el ID seleccionado
                result["asunto"],
                result["descripcion"],
                result["estado_nombre"]
            )
            QMessageBox.information(self.page_widget, "Éxito", "Registro de estado actualizado exitosamente.")
            self.clear_fields()

    def delete_estado_record(self):
        if not hasattr(self, 'selected_record_id') or self.selected_record_id is None:
            QMessageBox.warning(self.page_widget, "Selección Requerida", "Selecciona un registro de estado de la tabla para eliminar.")
            return

        reply = QMessageBox.question(self.page_widget, "Confirmar Eliminación",
                                     f"¿Estás seguro de que quieres eliminar el registro de estado con ID: {self.selected_record_id}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.estado_model.delete_estado_record(self.selected_record_id):
                QMessageBox.information(self.page_widget, "Éxito", "Registro de estado eliminado exitosamente.")
                self.clear_fields()
            else:
                QMessageBox.warning(self.page_widget, "Error", "No se pudo eliminar el registro de estado. ID no encontrado.")
    
    def search_estado_records(self):
        if not self.lineEdit_search_estado: return
        search_term = self.lineEdit_search_estado.text().strip()
        
        if search_term:
            results = self.estado_model.search_estados(search_term)
            self._display_estados_in_table(results) # Usar un método para display
        else:
            self._load_estados_data() # Cargar todos si la búsqueda está vacía

    def _display_estados_in_table(self, records_list: list):
        """
        Muestra una lista de registros de estado en la QTableView.
        Usado para resultados de búsqueda o carga completa.
        """
        if not self.table_model or not self.tableView_estado: return
        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels(["No.", "Asunto", "Descripción", "Fecha", "Estado"])
        
        for row_idx, record in enumerate(records_list):
            id_item = QStandardItem(str(record.get("id", "")))
            asunto_item = QStandardItem(record.get("asunto", ""))
            descripcion_item = QStandardItem(record.get("descripcion", ""))
            fecha_item = QStandardItem(record.get("fecha_creacion", ""))
            estado_nombre_item = QStandardItem(record.get("estado_nombre", ""))

            estado_texto = record.get("estado_nombre", "")
            # Aplicar estilos de color a la columna 'Estado'
            if estado_texto == "Urgente":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkRed)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto == "Baja prioridad":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkYellow)
                estado_nombre_item.setForeground(Qt.GlobalColor.black)
            elif estado_texto in ("Completado", "Resuelto"):
                estado_nombre_item.setBackground(Qt.GlobalColor.darkGreen)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto == "En progreso":
                estado_nombre_item.setBackground(Qt.GlobalColor.darkBlue)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)
            elif estado_texto in ("Pendiente de revisión", "En espera"):
                estado_nombre_item.setBackground(Qt.GlobalColor.darkGray)
                estado_nombre_item.setForeground(Qt.GlobalColor.white)

            self.table_model.setItem(row_idx, 0, id_item)
            self.table_model.setItem(row_idx, 1, asunto_item)
            self.table_model.setItem(row_idx, 2, descripcion_item)
            self.table_model.setItem(row_idx, 3, fecha_item)
            self.table_model.setItem(row_idx, 4, estado_nombre_item)

    def clear_fields(self):
        """
        Limpia los campos de entrada de la UI de la página principal de Estados (si existen)
        y la selección de la tabla.
        """
        if self.lineEdit_estado_id: self.lineEdit_estado_id.clear()
        if self.lineEdit_search_estado: self.lineEdit_search_estado.clear()
        if self.tableView_estado: self.tableView_estado.clearSelection()
        self.selected_record_id = None
        self._load_estados_data() # Recargar datos para mostrar todos los registros

