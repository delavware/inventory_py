from PyQt6.QtWidgets import QWidget, QLabel, QTableView, QComboBox, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QObject, Qt, QTimer, QEvent

class InicioController(QObject):
    def __init__(self, app_instance, page_widget: QWidget):  # Recibe page_widget
        super().__init__()
        self.app = app_instance
        self.page_widget = page_widget

        # Modelo compartido
        self.estado_model = self.app.estado_model

        # --- UI de Designer ---
        self.label_estado_titulo = self.page_widget.findChild(QLabel, "label_estado_titulo")
        self.comboBox_categorias = self.page_widget.findChild(QComboBox, "comboBox_categorias")
        self.comboBox_periodo = self.page_widget.findChild(QComboBox, "comboBox_periodo")
        self.tableView_estado_inventario = self.page_widget.findChild(QTableView, "tableView_estado_inventario")

        # Proporciones deseadas (No., Asunto, Descripción, Fecha, Estado)
        self._col_props = [60, 250, 350, 160, 200]

        # --- Tabla + modelo ---
        self.table_model = QStandardItemModel()
        if self.tableView_estado_inventario:
            tv = self.tableView_estado_inventario
            tv.setModel(self.table_model)
            tv.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            tv.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

            # Estilos
            tv.horizontalHeader().setStyleSheet(
                "QHeaderView::section { background-color: red; color: white; border: none; }"
            )
            tv.verticalHeader().setVisible(False)
            tv.setStyleSheet("QTableView { border: none; color: white; }")
            tv.horizontalHeader().setMinimumSectionSize(0)
            tv.verticalHeader().setMinimumSectionSize(0)

            # Reajustar si la vista cambia de tamaño (por si en el futuro dejas de usar ancho fijo)
            tv.installEventFilter(self)
        else:
            print("Advertencia: tableView_estado_inventario NO encontrado en la página de inicio del Designer.")

        # Combos (demo)
        if self.comboBox_categorias:
            self.comboBox_categorias.addItems([
                "Todas las categorías", "Medicamentos", "Material Quirúrgico", "Equipos"
            ])
        if self.comboBox_periodo:
            self.comboBox_periodo.addItems(["Últimos 7 días", "Últimos 30 días", "Todo el tiempo"])

        # Título
        if self.label_estado_titulo:
            self.label_estado_titulo.setText("Estado de Inventario (Dashboard)")
            self.label_estado_titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")

        # Señal del modelo
        self.estado_model.estados_updated.connect(self._load_dashboard_estados_data)

        # Cargar datos iniciales
        self._load_dashboard_estados_data()

    # --------- Núcleo del ajuste proporcional ---------
    def _apply_column_proportions(self):
        """Aplica stretch y distribuye las columnas según self._col_props
        usando el ancho real del viewport."""
        tv = self.tableView_estado_inventario
        if not tv:
            return
        header = tv.horizontalHeader()
        cols = self.table_model.columnCount()
        if cols == 0 or cols < len(self._col_props):
            return

        # Asegurar Stretch en todas
        for i in range(cols):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Aplicar tamaños iniciales en proporción al ancho real del viewport.
        def _do_resize():
            if not tv.isVisible():
                return
            avail = tv.viewport().width()
            if avail <= 0:
                return

            # Proporciones normalizadas
            props = self._col_props[:cols]
            total = float(sum(props))
            widths = [max(1, int(avail * (p / total))) for p in props]
            # Ajuste por redondeo: que sumen exactamente avail
            diff = avail - sum(widths)
            if diff != 0:
                widths[-1] = max(1, widths[-1] + diff)

            for i, w in enumerate(widths):
                header.resizeSection(i, w)

        # Ejecutar al siguiente ciclo de eventos cuando ya hay tamaño real
        QTimer.singleShot(0, _do_resize)

    def eventFilter(self, obj, event):
        """Si la tabla se redimensiona, re-aplicamos las proporciones."""
        if obj is self.tableView_estado_inventario and event.type() == QEvent.Type.Resize:
            self._apply_column_proportions()
        return super().eventFilter(obj, event)

    # --------- Carga de datos ---------
    def _load_dashboard_estados_data(self):
        if not self.table_model or not self.tableView_estado_inventario:
            return

        self.table_model.clear()

        # Cabeceras PRIMERO (importante: crean las secciones del header)
        headers = ["No.", "Asunto", "Descripción", "Fecha", "Estado"]
        self.table_model.setHorizontalHeaderLabels(headers)

        # Datos (demo: primeros 5)
        all_estado_records = self.estado_model.get_all_estados()
        for row_idx, record in enumerate(all_estado_records[:5]):
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

        # ¡Ahora sí! aplicar proporciones cuando YA existen las columnas y la vista tiene tamaño.
        self._apply_column_proportions()
