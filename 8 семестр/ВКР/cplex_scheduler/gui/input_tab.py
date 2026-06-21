"""
Вкладка ввода параметров задачи
"""

import os
import json
import csv
import io

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QScrollArea, QSizePolicy, QFrame, QMessageBox, QFileDialog,
    QToolButton, QMenu, QAction, QSplitter, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon

from model.parameters import TaskParameters


BTN_STYLE = "background-color: #2F5597; color: white; padding: 5px 10px; border-radius: 3px;"
BTN_GREEN = "background-color: #00703C; color: white; padding: 5px 10px; border-radius: 3px;"
BTN_ORANGE = "background-color: #C55A11; color: white; padding: 5px 10px; border-radius: 3px;"


class InputTab(QWidget):
    """Вкладка для ввода параметров задачи"""
    params_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    # -------------------- Построение интерфейса --------------------

    def _setup_ui(self):
        """Заполнение интерфейса для формы ввода данных"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # Панель быстрых действий
        self._build_action_bar(main_layout)

        # Прокручиваемая форма ввода данных
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self._input_form = QWidget()
        self._input_form_layout = QVBoxLayout(self._input_form)
        self._input_form_layout.setSpacing(8)

        self._build_input_form(self._input_form_layout)

        scroll.setWidget(self._input_form)
        main_layout.addWidget(scroll)

    def _build_action_bar(self, layout):
        """Создание панели быстрых действий"""
        action_bar = QHBoxLayout()
        action_bar.setSpacing(6)

        lbl = QLabel("Данные:")
        lbl.setFont(QFont("Arial", 9, QFont.Bold))
        action_bar.addWidget(lbl)

        btn_import_json = QPushButton("📂 Загрузить JSON")
        btn_import_json.setStyleSheet(BTN_STYLE)
        btn_import_json.setToolTip("Загрузить параметры из JSON-файла")
        btn_import_json.clicked.connect(self._import_json)
        action_bar.addWidget(btn_import_json)

        btn_export_json = QPushButton("💾 Сохранить JSON")
        btn_export_json.setStyleSheet(BTN_GREEN)
        btn_export_json.setToolTip("Сохранить текущие параметры в JSON")
        btn_export_json.clicked.connect(self._export_json)
        action_bar.addWidget(btn_export_json)

        # btn_import_csv = QPushButton("📊 Импорт CSV")
        # btn_import_csv.setStyleSheet(BTN_STYLE)
        # btn_import_csv.setToolTip("Загрузить времена обработки из CSV (строки=приборы, столбцы=типы)")
        # btn_import_csv.clicked.connect(self._import_csv)
        # action_bar.addWidget(btn_import_csv)
        #
        # btn_export_csv = QPushButton("📤 Экспорт CSV")
        # btn_export_csv.setStyleSheet(BTN_ORANGE)
        # btn_export_csv.setToolTip("Экспортировать все матрицы в CSV-файлы")
        # btn_export_csv.clicked.connect(self._export_csv)
        # action_bar.addWidget(btn_export_csv)

        action_bar.addSpacing(10)

        btn_example_small = QPushButton("📋 Малый пример")
        btn_example_small.clicked.connect(lambda: self.load_example("small"))
        action_bar.addWidget(btn_example_small)

        btn_example_medium = QPushButton("📋 Средний пример")
        btn_example_medium.clicked.connect(lambda: self.load_example("medium"))
        action_bar.addWidget(btn_example_medium)

        action_bar.addStretch()

        layout.addLayout(action_bar)

    def _build_input_form(self, layout):
        """Строит основное содержимое формы ввода"""

        self._build_dim_group(layout)
        self._build_n_group(layout)
        self._build_t_group(layout)
        self._build_t_init_group(layout)
        self._build_t_setup_group(layout)

        # ── Директивные сроки ──
        d_group = QGroupBox("Директивные сроки  d[тип]  (для критерия G — суммарное запаздывание)")
        d_layout = QVBoxLayout(d_group)
        self.d_table = QTableWidget(1, 3)
        self.d_table.setHorizontalHeaderLabels([f"d[{i+1}]" for i in range(3)])
        self.d_table.verticalHeader().hide()
        self.d_table.setMaximumHeight(60)
        for i, val in enumerate([30, 40, 50]):
            self._set_cell(self.d_table, 0, i, str(val))
        d_layout.addWidget(self.d_table)
        layout.addWidget(d_group)

        self._build_maint_group(layout)
        self._build_opt_group(layout)

        self._apply_dimensions()

    # -------------------- Построение блоков формы ввода --------------------

    def _build_dim_group(self, layout):
        """Создание блока ввода параметров размерности задачи"""
        dim_group = QGroupBox("Размерность задачи")
        dim_layout = QGridLayout(dim_group)

        dim_layout.addWidget(QLabel("Количество типов заданий:"), 0, 0)
        self.spin_I = QSpinBox()
        self.spin_I.setRange(2, 15)
        self.spin_I.setValue(3)
        self.spin_I.setToolTip("Количество типов заданий (2-15)")
        dim_layout.addWidget(self.spin_I, 0, 1)

        dim_layout.addWidget(QLabel("Количество приборов:"), 0, 2)
        self.spin_L = QSpinBox()
        self.spin_L.setRange(2, 10)
        self.spin_L.setValue(4)
        self.spin_I.setToolTip("Количество приборов (2-10)")
        dim_layout.addWidget(self.spin_L, 0, 3)

        dim_layout.addWidget(QLabel("Количество пакетов:"), 0, 4)
        self.spin_J = QSpinBox()
        self.spin_J.setRange(2, 20)
        self.spin_J.setValue(7)
        self.spin_I.setToolTip("Количество позиций (пакетов) в решении (2-20)")
        dim_layout.addWidget(self.spin_J, 0, 5)

        btn_apply_dim = QPushButton("✔ Применить размерность (перестроить матрицы)")
        btn_apply_dim.setStyleSheet(BTN_STYLE)
        btn_apply_dim.clicked.connect(self._apply_dimensions)
        dim_layout.addWidget(btn_apply_dim, 1, 0, 1, 6)

        layout.addWidget(dim_group)

        # Подсказка
        hint = QLabel(
            "ℹ  После изменения параметров нажмите «Применить размерность». "
            "Для загрузки своих данных используйте «Загрузить JSON»"
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #555; font-size: 9pt; background: #EEF2FF; "
                           "padding: 4px; border-radius: 3px;")
        layout.addWidget(hint)

    def _build_n_group(self, layout):
        """Создание блока ввода параметров n[i]"""
        n_group = QGroupBox("Количество заданий каждого типа:")
        n_layout = QVBoxLayout(n_group)

        self.n_table = QTableWidget(1, 2)
        self.n_table.verticalHeader().hide()
        self.n_table.setMaximumHeight(60)
        n_layout.addWidget(self.n_table)

        n_hint = QLabel("Минимальное значение - 2")
        n_hint.setStyleSheet("color: #777; font-size: 8pt;")
        n_layout.addWidget(n_hint)

        layout.addWidget(n_group)

    def _build_t_group(self, layout):
        """Создание блока ввода параметров t[l][i]"""

        # Время обработки задания типа i на приборе l: t[l][i]
        t_group = QGroupBox("Длительность обработки заданий разных типов на разных приборах:")
        t_layout = QVBoxLayout(t_group)

        self.t_table = QTableWidget()
        t_layout.addWidget(self.t_table)

        btn_paste_t = QPushButton("📋 Вставить из буфера (табуляция)")
        btn_paste_t.setToolTip("Вставьте данные скопированные из Excel (Tab-разделители)")
        btn_paste_t.clicked.connect(lambda: self._paste_from_clipboard(self.t_table))
        t_layout.addWidget(btn_paste_t)

        layout.addWidget(t_group)

    def _build_t_init_group(self, layout):
        """Создание блока ввода параметров t_init[l][i]"""

        # Время наладки прибора l на задания типа i: t_init[l][i]
        ti_group = QGroupBox("Время первоначальной наладки приборов на тип заданий:")
        ti_layout = QVBoxLayout(ti_group)

        self.ti_table = QTableWidget()
        ti_layout.addWidget(self.ti_table)

        btn_paste_ti = QPushButton("📋 Вставить из буфера")
        btn_paste_ti.clicked.connect(lambda: self._paste_from_clipboard(self.ti_table))
        ti_layout.addWidget(btn_paste_ti)

        layout.addWidget(ti_group)

    def _build_t_setup_group(self, layout):
        """Создание блока ввода параметров t_setup[l][i][k]"""

        # Время переналадки прибора l с типа i на тип k
        ts_group = QGroupBox("Длительность переналадки приборов с одного типа на другой:")
        self._ts_layout = QVBoxLayout(ts_group)

        ts_note = QLabel(
            "Для каждого прибора — квадратная матрица I×I. "
            "Строки — 'с какого типа', столбцы — 'на какой тип'. Диагональ = 0."
        )
        ts_note.setWordWrap(True)
        ts_note.setStyleSheet("color: #555; font-size: 9pt;")
        self._ts_layout.addWidget(ts_note)

        self.ts_tables = []
        self._ts_subtab = QTabWidget()
        self._ts_layout.addWidget(self._ts_subtab)
        self._rebuild_ts_tables(2, 2)

        layout.addWidget(ts_group)

    def _build_maint_group(self, layout):
        """Создание блока ввода параметров ПТО"""
        maint_group = QGroupBox("Профилактическое техническое обслуживание (ПТО) приборов")
        maint_layout = QVBoxLayout(maint_group)

        self.chk_maintenance = QCheckBox("Учитывать техобслуживание приборов")
        self.chk_maintenance.setChecked(True)
        self.chk_maintenance.setFont(QFont("Arial", 10, QFont.Bold))
        maint_layout.addWidget(self.chk_maintenance)

        maint_note = QLabel(
            "Для каждого прибора задаётся один заранее фиксированный интервал ПТО.\n"
            "Выполнение пакета планируется либо до начала интервала, либо после его окончания."
        )
        maint_note.setWordWrap(True)
        maint_note.setStyleSheet("color: #555; font-size: 9pt;")
        maint_layout.addWidget(maint_note)

        self.maint_table = QTableWidget(2, 3)
        self.maint_table.setHorizontalHeaderLabels(["Прибор", "Начало ПТО", "Длительность ПТО"])
        self.maint_table.verticalHeader().hide()
        self.maint_table.setMaximumHeight(115)

        maint_layout.addWidget(self.maint_table)
        self.chk_maintenance.toggled.connect(self.maint_table.setEnabled)

        layout.addWidget(maint_group)

    def _build_opt_group(self, layout):
        """Создание блока определения критерия оптимизации"""
        opt_group = QGroupBox("Настройки оптимизации")
        opt_layout = QGridLayout(opt_group)

        opt_layout.addWidget(QLabel("Критерий:"), 0, 0)
        self.combo_criterion = QComboBox()
        self.combo_criterion.addItems([
            "Cmax — минимизация времени завершения",
            #"G — минимизация суммарного запаздывания"
        ])
        opt_layout.addWidget(self.combo_criterion, 0, 1, 1, 3)

        opt_layout.addWidget(QLabel("Лимит времени (сек):"), 1, 0)
        self.spin_timelimit = QSpinBox()
        self.spin_timelimit.setRange(10, 3600)
        self.spin_timelimit.setValue(120)
        self.spin_timelimit.setSuffix(" с")
        opt_layout.addWidget(self.spin_timelimit, 1, 1)

        self.chk_verbose = QCheckBox("Показывать лог решателя")
        opt_layout.addWidget(self.chk_verbose, 1, 2)

        layout.addWidget(opt_group)

    # -------------------- Вспомогательные действия --------------------

    def _set_cell(self, table, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, col, item)

    def _set_cell_readonly(self, table, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsEnabled)
        table.setItem(row, col, item)

    def _setup_matrix_table(self, table, rows, cols, row_labels=None, col_labels=None):
        table.setRowCount(rows)
        table.setColumnCount(cols)
        if col_labels:
            table.setHorizontalHeaderLabels(col_labels)
        if row_labels:
            table.setVerticalHeaderLabels(row_labels)
        table.horizontalHeader().setDefaultSectionSize(72)
        table.verticalHeader().setDefaultSectionSize(28)

    def _fill_table(self, table, data):
        """Заполнение матрицы данными"""
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                self._set_cell(table, r, c, str(val))

    def _rebuild_ts_tables(self, L, I):
        """Перестраивает набор вкладок переналадок"""
        # Сохранить текущие данные
        old_data = []
        for tbl in self.ts_tables:
            rows = tbl.rowCount()
            cols = tbl.columnCount()
            mat = []
            for r in range(rows):
                row = []
                for c in range(cols):
                    item = tbl.item(r, c)
                    try:
                        row.append(float(item.text()) if item else 0.0)
                    except ValueError:
                        row.append(0.0)
                mat.append(row)
            old_data.append(mat)

        # Очистить вкладки
        self._ts_subtab.clear()
        self.ts_tables = []

        for l in range(L):
            tbl = QTableWidget(I, I)
            self._setup_matrix_table(
                tbl, I, I,
                row_labels=[f"с {i+1}" for i in range(I)],
                col_labels=[f"на {i+1}" for i in range(I)]
            )
            tbl.setMaximumHeight(max(150, I * 30 + 30))

            # Заполнить данными: старыми если есть, иначе default
            for r in range(I):
                for c in range(I):
                    if l < len(old_data) and r < len(old_data[l]) and c < len(old_data[l][r]):
                        v = old_data[l][r][c]
                    else:
                        v = 0 if r == c else abs(r - c)
                    self._set_cell(tbl, r, c, str(int(v) if v == int(v) else v))

            # Кнопка вставки
            w = QWidget()
            wl = QVBoxLayout(w)
            wl.addWidget(tbl)
            btn = QPushButton("📋 Вставить из буфера")
            btn.clicked.connect(lambda checked, t=tbl: self._paste_from_clipboard(t))
            wl.addWidget(btn)
            self._ts_subtab.addTab(w, f"Прибор {l+1}")
            self.ts_tables.append(tbl)

    def _paste_from_clipboard(self, table):
        """Вставка матрицы из буфера обмена (Excel)"""
        from PyQt5.QtWidgets import QApplication
        text = QApplication.clipboard().text()
        if not text.strip():
            QMessageBox.information(self, "Буфер пуст",
                                    "В буфере обмена нет текстовых данных.")
            return
        rows = text.strip().split('\n')
        for r, row_str in enumerate(rows):
            if r >= table.rowCount():
                break
            cols = row_str.split('\t')
            for c, val in enumerate(cols):
                if c >= table.columnCount():
                    break
                try:
                    float(val.strip().replace(',', '.'))
                    self._set_cell(table, r, c, val.strip().replace(',', '.'))
                except ValueError:
                    pass

    # -------------------- Применение размерностей --------------------

    def _apply_dimensions(self):
        I = self.spin_I.value()
        L = self.spin_L.value()

        # Таблица n[i]
        self.n_table.setColumnCount(I)
        self.n_table.setHorizontalHeaderLabels([f"Тип [{i+1}]" for i in range(I)])

        # d_table
        self.d_table.setColumnCount(I)
        self.d_table.setHorizontalHeaderLabels([f"d[{i+1}]" for i in range(I)])

        # Таблица t[i]
        self.t_table.setRowCount(L)
        self.t_table.setColumnCount(I)
        self.t_table.setHorizontalHeaderLabels([f"Тип {i+1}" for i in range(I)])
        self.t_table.setVerticalHeaderLabels([f"Прибор {l+1}" for l in range(L)])

        # Таблица t_init
        self.ti_table.setRowCount(L)
        self.ti_table.setColumnCount(I)
        self.ti_table.setHorizontalHeaderLabels([f"Тип {i+1}" for i in range(I)])
        self.ti_table.setVerticalHeaderLabels([f"Прибор {l+1}" for l in range(L)])

        # Таблицы t_setup[l][i]
        self._rebuild_ts_tables(L, I)

        # Таблица t_maint[l]
        self.maint_table.setRowCount(L)
        for l in range(L):
            self._set_cell_readonly(self.maint_table, l, 0, f"Прибор {l+1}")

        self.params_changed.emit()

    # ─────────────────── load/save params ──────────────────────

    def _load_params_to_ui(self):
        """Загрузить параметры в форму ввода"""
        p = self._params

        # размерность задачи
        self.spin_I.setValue(p.I)
        self.spin_L.setValue(p.L)
        self.spin_J.setValue(p.J)

        # список n[i]
        self.n_table.setColumnCount(p.I)
        self.n_table.setHorizontalHeaderLabels([f"n[{i+1}]" for i in range(p.I)])

        # self.d_table.setColumnCount(p.I)
        # self.d_table.setHorizontalHeaderLabels([f"d[{i+1}]" for i in range(p.I)])

        # матрица t_setup[l][i]
        self.t_table.setRowCount(p.L)
        self.t_table.setColumnCount(p.I)
        self.t_table.setHorizontalHeaderLabels([f"Тип {i+1}" for i in range(p.I)])
        self.t_table.setVerticalHeaderLabels([f"Прибор {l+1}" for l in range(p.L)])
        self._fill_table(self.t_table, p.t)

        # матрица t_init
        self.ti_table.setRowCount(p.L)
        self.ti_table.setColumnCount(p.I)
        self.ti_table.setHorizontalHeaderLabels([f"Тип {i+1}" for i in range(p.I)])
        self.ti_table.setVerticalHeaderLabels([f"Прибор {l+1}" for l in range(p.L)])
        self._fill_table(self.ti_table, p.t_init)

        # матрица t_setup[l][i]
        self._rebuild_ts_tables(p.L, p.I)
        for l in range(min(p.L, len(self.ts_tables))):
            self._fill_table(self.ts_tables[l], p.t_setup[l])

        # n
        for i in range(p.I):
            self._set_cell(self.n_table, 0, i, str(p.n[i]))

        # d
        for i in range(p.I):
            self._set_cell(self.d_table, 0, i, str(p.d[i]))

        # maint
        self.chk_maintenance.setChecked(p.use_maintenance)
        self.maint_table.setRowCount(p.L)
        for l in range(p.L):
            self._set_cell_readonly(self.maint_table, l, 0, f"Прибор {l+1}")
            self._set_cell(self.maint_table, l, 1, str(p.TM[l]))
            self._set_cell(self.maint_table, l, 2, str(p.tm_maint[l]))

    def _read_table_float(self, table, rows, cols, default=1.0):
        data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                item = table.item(r, c)
                try:
                    row.append(float(item.text().replace(',', '.')) if item else default)
                except ValueError:
                    row.append(default)
            data.append(row)
        return data

    def _read_row_float(self, table, cols, default=1.0):
        row = []
        for c in range(cols):
            item = table.item(0, c)
            try:
                row.append(float(item.text().replace(',', '.')) if item else default)
            except ValueError:
                row.append(default)
        return row

    def _read_row_int(self, table, cols, default=4):
        row = []
        for c in range(cols):
            item = table.item(0, c)
            try:
                row.append(max(2, int(float(item.text().replace(',', '.')) if item else default)))
            except ValueError:
                row.append(default)
        return row

    def get_params(self) -> TaskParameters:
        """Считать параметры из UI"""
        p = TaskParameters()
        p.I = self.spin_I.value()
        p.L = self.spin_L.value()
        p.J = self.spin_J.value()

        p.n = self._read_row_int(self.n_table, p.I, default=4)
        p.t = self._read_table_float(self.t_table, p.L, p.I, default=1.0)
        p.t_init = self._read_table_float(self.ti_table, p.L, p.I, default=1.0)
        p.t_setup = [
            self._read_table_float(self.ts_tables[l], p.I, p.I, default=0.0)
            for l in range(min(p.L, len(self.ts_tables)))
        ]
        while len(p.t_setup) < p.L:
            p.t_setup.append([[0] * p.I for _ in range(p.I)])

        p.d = self._read_row_float(self.d_table, p.I, default=30.0)
        p.use_maintenance = self.chk_maintenance.isChecked()

        p.TM = []
        p.tm_maint = []
        for l in range(p.L):
            try:
                p.TM.append(float(self.maint_table.item(l, 1).text().replace(',', '.')))
            except Exception:
                p.TM.append(20.0)
            try:
                p.tm_maint.append(float(self.maint_table.item(l, 2).text().replace(',', '.')))
            except Exception:
                p.tm_maint.append(2.0)

        return p

    def get_criterion(self) -> str:
        return "Cmax" if self.combo_criterion.currentIndex() == 0 else "G"

    def get_time_limit(self) -> int:
        return self.spin_timelimit.value()

    def get_verbose(self) -> bool:
        return self.chk_verbose.isChecked()

    def load_example(self, name="small"):
        if name == "small":
            self._params = TaskParameters.example_small()
        else:
            self._params = TaskParameters.example_medium()
        self._load_params_to_ui()

    def load_params(self, params: TaskParameters):
        self._params = params
        self._load_params_to_ui()

    # ─────────────────── Import / Export ───────────────────────

    def _import_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть параметры", "", "JSON (*.json);;Все файлы (*)"
        )
        if not path:
            return
        try:
            p = TaskParameters.from_json(path)
            self.load_params(p)
            QMessageBox.information(self, "Успех",
                                    f"Параметры загружены:\n{os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки",
                                 f"Не удалось загрузить JSON:\n{e}")

    def _export_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить параметры", "params.json", "JSON (*.json)"
        )
        if not path:
            return
        try:
            p = self.get_params()
            errors = p.validate()
            if errors:
                reply = QMessageBox.question(
                    self, "Предупреждение",
                    "Параметры содержат ошибки:\n" +
                    "\n".join(f"• {e}" for e in errors) +
                    "\n\nСохранить всё равно?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return
            p.to_json(path)
            QMessageBox.information(self, "Успех",
                                    f"Параметры сохранены:\n{os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    # def _import_csv(self):
    #     """Импорт CSV: выбор матрицы для загрузки"""
    #     msg = (
    #         "Выберите CSV-файл для импорта.\n\n"
    #         "Формат CSV:\n"
    #         "  • Разделитель: точка с запятой (;) или запятая (,)\n"
    #         "  • Строки соответствуют приборам (L строк)\n"
    #         "  • Столбцы соответствуют типам (I столбцов)\n\n"
    #         "Куда импортировать?"
    #     )
    #     from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QRadioButton
    #     dlg = QDialog(self)
    #     dlg.setWindowTitle("Импорт CSV")
    #     dlg_layout = QVBoxLayout(dlg)
    #     dlg_layout.addWidget(QLabel(msg))
    #
    #     opts = [
    #         ("Времена обработки t[l][i]", "t"),
    #         ("Первоначальная наладка t_init[l][i]", "ti"),
    #         ("Директивные сроки d[i] (одна строка)", "d"),
    #         ("Количество заданий n[i] (одна строка)", "n"),
    #     ]
    #     radios = []
    #     for label, key in opts:
    #         rb = QRadioButton(label)
    #         dlg_layout.addWidget(rb)
    #         radios.append((rb, key))
    #     radios[0][0].setChecked(True)
    #
    #     btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    #     btns.accepted.connect(dlg.accept)
    #     btns.rejected.connect(dlg.reject)
    #     dlg_layout.addWidget(btns)
    #
    #     if dlg.exec_() != dlg.Accepted:
    #         return
    #
    #     target = next(k for rb, k in radios if rb.isChecked())
    #
    #     path, _ = QFileDialog.getOpenFileName(
    #         self, "Открыть CSV", "", "CSV (*.csv);;Текст (*.txt);;Все файлы (*)"
    #     )
    #     if not path:
    #         return
    #
    #     try:
    #         data = self._read_csv_file(path)
    #         if target == "t":
    #             self._fill_table_raw(self.t_table, data)
    #         elif target == "ti":
    #             self._fill_table_raw(self.ti_table, data)
    #         elif target == "d":
    #             flat = [v for row in data for v in row]
    #             self.d_table.setColumnCount(len(flat))
    #             self.d_table.setHorizontalHeaderLabels(
    #                 [f"d[{i+1}]" for i in range(len(flat))])
    #             for i, v in enumerate(flat):
    #                 self._set_cell(self.d_table, 0, i, str(v))
    #         elif target == "n":
    #             flat = [v for row in data for v in row]
    #             self.n_table.setColumnCount(len(flat))
    #             self.n_table.setHorizontalHeaderLabels(
    #                 [f"n[{i+1}]" for i in range(len(flat))])
    #             for i, v in enumerate(flat):
    #                 self._set_cell(self.n_table, 0, i, str(int(float(v))))
    #         QMessageBox.information(self, "Импорт завершён",
    #                                 f"Данные загружены из:\n{os.path.basename(path)}")
    #     except Exception as e:
    #         QMessageBox.critical(self, "Ошибка импорта CSV", str(e))
    #
    # def _read_csv_file(self, path):
    #     """Читает CSV, автоопределяет разделитель"""
    #     with open(path, 'r', encoding='utf-8-sig') as f:
    #         sample = f.read(1024)
    #     sep = ';' if sample.count(';') >= sample.count(',') else ','
    #     data = []
    #     with open(path, 'r', encoding='utf-8-sig') as f:
    #         reader = csv.reader(f, delimiter=sep)
    #         for row in reader:
    #             if row:
    #                 data.append([v.strip().replace(',', '.') for v in row])
    #     return data

    def _fill_table_raw(self, table, data):
        rows = len(data)
        cols = max(len(r) for r in data) if data else 0
        table.setRowCount(rows)
        table.setColumnCount(cols)
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                self._set_cell(table, r, c, val)

    # def _export_csv(self):
    #     """Экспорт всех матриц в CSV-файлы в выбранную папку"""
    #     folder = QFileDialog.getExistingDirectory(
    #         self, "Выберите папку для экспорта CSV"
    #     )
    #     if not folder:
    #         return
    #
    #     try:
    #         p = self.get_params()
    #
    #         def write_matrix(filename, matrix, row_labels=None, col_labels=None):
    #             with open(os.path.join(folder, filename), 'w', newline='',
    #                       encoding='utf-8-sig') as f:
    #                 writer = csv.writer(f, delimiter=';')
    #                 if col_labels:
    #                     writer.writerow([''] + col_labels)
    #                 for idx, row in enumerate(matrix):
    #                     prefix = [row_labels[idx]] if row_labels else []
    #                     writer.writerow(prefix + [str(v) for v in row])
    #
    #         def write_row(filename, row, labels):
    #             with open(os.path.join(folder, filename), 'w', newline='',
    #                       encoding='utf-8-sig') as f:
    #                 writer = csv.writer(f, delimiter=';')
    #                 writer.writerow(labels)
    #                 writer.writerow([str(v) for v in row])
    #
    #         write_matrix("t_processing.csv", p.t,
    #                      row_labels=[f"Прибор {l+1}" for l in range(p.L)],
    #                      col_labels=[f"Тип {i+1}" for i in range(p.I)])
    #
    #         write_matrix("t_init.csv", p.t_init,
    #                      row_labels=[f"Прибор {l+1}" for l in range(p.L)],
    #                      col_labels=[f"Тип {i+1}" for i in range(p.I)])
    #
    #         write_row("n_counts.csv", p.n,
    #                   [f"n[{i+1}]" for i in range(p.I)])
    #
    #         write_row("d_deadlines.csv", p.d,
    #                   [f"d[{i+1}]" for i in range(p.I)])
    #
    #         for l in range(p.L):
    #             write_matrix(f"t_setup_device_{l+1}.csv", p.t_setup[l],
    #                          row_labels=[f"с {i+1}" for i in range(p.I)],
    #                          col_labels=[f"на {i+1}" for i in range(p.I)])
    #
    #         if p.use_maintenance:
    #             write_matrix("maintenance.csv",
    #                          [[p.TM[l], p.tm_maint[l]] for l in range(p.L)],
    #                          row_labels=[f"Прибор {l+1}" for l in range(p.L)],
    #                          col_labels=["TM[l]", "tm[l]"])
    #
    #         # Также JSON
    #         p.to_json(os.path.join(folder, "params.json"))
    #
    #         files = ["t_processing.csv", "t_init.csv", "n_counts.csv",
    #                  "d_deadlines.csv", "params.json"] + \
    #                 [f"t_setup_device_{l+1}.csv" for l in range(p.L)]
    #
    #         QMessageBox.information(
    #             self, "Экспорт завершён",
    #             f"Файлы сохранены в:\n{folder}\n\n" +
    #             "\n".join(f"  • {f}" for f in files)
    #         )
    #     except Exception as e:
    #         QMessageBox.critical(self, "Ошибка экспорта", str(e))
