"""
Вкладка отображения результатов оптимизации
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QGroupBox,
    QTextEdit, QPushButton, QSplitter, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush

from model.results import OptimizationResults
from model.parameters import TaskParameters


# Цвета для типов заданий
TYPE_COLORS = [
    "#4472C4", "#ED7D31", "#A9D18E", "#FF0000", "#7030A0",
    "#00B0F0", "#FF9900", "#92D050", "#FF0066", "#00B050",
]

STATUS_COLORS = {
    "Оптимальное решение": "#00B050",
    "Допустимое решение (не оптимальное)": "#FF9900",
    "Задача не имеет решения": "#FF0000",
    "Превышен лимит времени": "#FF9900",
    "Ошибка решателя": "#FF0000",
    "Задача не решена": "#7F7F7F",
}


class ResultTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Статус-панель
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_layout = QHBoxLayout(status_frame)

        self.lbl_status = QLabel("Задача не решена")
        self.lbl_status.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.lbl_status)

        self.lbl_objective = QLabel("")
        self.lbl_objective.setFont(QFont("Arial", 12))
        status_layout.addWidget(self.lbl_objective)

        self.lbl_improvement = QLabel("")
        self.lbl_improvement.setFont(QFont("Arial", 11))
        self.lbl_improvement.setStyleSheet("color: #00B050;")
        status_layout.addWidget(self.lbl_improvement)

        self.lbl_time = QLabel("")
        status_layout.addWidget(self.lbl_time)
        status_layout.addStretch()
        layout.addWidget(status_frame)

        splitter = QSplitter(Qt.Horizontal)

        # --- Левая панель: составы пакетов ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        batch_group = QGroupBox("Состав пакетов")
        batch_layout = QVBoxLayout(batch_group)
        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(3)
        self.batch_table.setHorizontalHeaderLabels(["Позиция j", "Тип заданий i", "Кол-во mj"])
        self.batch_table.horizontalHeader().setStretchLastSection(True)
        self.batch_table.setAlternatingRowColors(True)
        batch_layout.addWidget(self.batch_table)
        left_layout.addWidget(batch_group)

        # Запаздывания (для G)
        delay_group = QGroupBox("Запаздывания (критерий G)")
        delay_layout = QVBoxLayout(delay_group)
        self.delay_table = QTableWidget()
        self.delay_table.setColumnCount(3)
        self.delay_table.setHorizontalHeaderLabels(["Тип i", "Окончание gi", "Запаздывание pi"])
        self.delay_table.horizontalHeader().setStretchLastSection(True)
        self.delay_table.setAlternatingRowColors(True)
        delay_layout.addWidget(self.delay_table)
        left_layout.addWidget(delay_group)

        splitter.addWidget(left_widget)

        # --- Правая панель: расписание ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        sched_group = QGroupBox("Расписание (моменты начала q_lj)")
        sched_layout = QVBoxLayout(sched_group)
        self.sched_table = QTableWidget()
        self.sched_table.setColumnCount(6)
        self.sched_table.setHorizontalHeaderLabels(
            ["Прибор l", "Позиция j", "Тип", "Начало q_lj", "Длительность", "Окончание"])
        self.sched_table.setAlternatingRowColors(True)
        sched_layout.addWidget(self.sched_table)
        right_layout.addWidget(sched_group)

        maint_group = QGroupBox("Техническое обслуживание (ТО)")
        maint_layout = QVBoxLayout(maint_group)
        self.maint_table = QTableWidget()
        self.maint_table.setColumnCount(5)
        self.maint_table.setHorizontalHeaderLabels(
            ["Прибор l", "Перед позицией", "Начало ТО", "Длительность", "Окончание ТО"])
        self.maint_table.setAlternatingRowColors(True)
        maint_layout.addWidget(self.maint_table)
        right_layout.addWidget(maint_group)

        splitter.addWidget(right_widget)
        layout.addWidget(splitter)

        # Текстовый лог
        log_group = QGroupBox("Сводка")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setFont(QFont("Courier New", 9))
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)

    def update_results(self, results: OptimizationResults, params: TaskParameters):
        # Статус
        color = STATUS_COLORS.get(results.status, "#000000")
        self.lbl_status.setText(results.status)
        self.lbl_status.setStyleSheet(f"color: {color}; font-weight: bold;")

        if results.objective_value is not None:
            crit = "Cmax" if results.criterion == "Cmax" else "G (суммарное запаздывание)"
            self.lbl_objective.setText(f"  │  {crit} = {results.objective_value:.4f}")
        else:
            self.lbl_objective.setText("")

        if results.improvement_percent is not None and results.fixed_objective is not None:
            self.lbl_improvement.setText(
                f"  │  Фикс.пакеты: {results.fixed_objective:.2f}"
                f"  →  Улучшение: {results.improvement_percent:.1f}%"
            )
        else:
            self.lbl_improvement.setText("")

        self.lbl_time.setText(f"  │  Время решения: {results.solve_time:.2f} с")

        # Составы пакетов
        self.batch_table.setRowCount(len(results.batches))
        for row, b in enumerate(sorted(results.batches, key=lambda x: x.position)):
            self._set_cell(self.batch_table, row, 0, str(b.position))
            ci = QTableWidgetItem(str(b.task_type))
            ci.setTextAlignment(Qt.AlignCenter)
            color_hex = TYPE_COLORS[(b.task_type - 1) % len(TYPE_COLORS)]
            ci.setBackground(QBrush(QColor(color_hex)))
            ci.setForeground(QBrush(QColor("white")))
            self.batch_table.setItem(row, 1, ci)
            self._set_cell(self.batch_table, row, 2, str(b.count))

        # Расписание
        self.sched_table.setRowCount(len(results.schedule))
        for row, e in enumerate(sorted(results.schedule, key=lambda x: (x.device, x.position))):
            self._set_cell(self.sched_table, row, 0, str(e.device))
            self._set_cell(self.sched_table, row, 1, str(e.position))
            ti = QTableWidgetItem(str(e.task_type))
            ti.setTextAlignment(Qt.AlignCenter)
            color_hex = TYPE_COLORS[(e.task_type - 1) % len(TYPE_COLORS)]
            ti.setBackground(QBrush(QColor(color_hex)))
            ti.setForeground(QBrush(QColor("white")))
            self.sched_table.setItem(row, 2, ti)
            self._set_cell(self.sched_table, row, 3, f"{e.start_time:.3f}")
            self._set_cell(self.sched_table, row, 4, f"{e.process_time:.3f}")
            self._set_cell(self.sched_table, row, 5, f"{e.end_time:.3f}")

        # ТО
        self.maint_table.setRowCount(len(results.maintenance))
        for row, m in enumerate(sorted(results.maintenance, key=lambda x: (x.device, x.start_time))):
            self._set_cell(self.maint_table, row, 0, str(m.device))
            self._set_cell(self.maint_table, row, 1, str(m.before_position))
            self._set_cell(self.maint_table, row, 2, f"{m.start_time:.3f}")
            self._set_cell(self.maint_table, row, 3, f"{m.duration:.3f}")
            self._set_cell(self.maint_table, row, 4, f"{m.end_time:.3f}")

        # Запаздывания
        if results.delays:
            self.delay_table.setRowCount(len(results.delays))
            for row, (i, dval) in enumerate(sorted(results.delays.items())):
                self._set_cell(self.delay_table, row, 0, str(i))
                g = results.completion_times.get(i, 0)
                self._set_cell(self.delay_table, row, 1, f"{g:.3f}")
                di = QTableWidgetItem(f"{dval:.3f}")
                di.setTextAlignment(Qt.AlignCenter)
                if dval > 0:
                    di.setForeground(QBrush(QColor("#FF0000")))
                self.delay_table.setItem(row, 2, di)
        else:
            self.delay_table.setRowCount(0)

        self.log_text.setPlainText(results.summary())

    def _set_cell(self, table, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsEnabled)
        table.setItem(row, col, item)

    def clear(self):
        self.lbl_status.setText("Задача не решена")
        self.lbl_objective.setText("")
        self.lbl_improvement.setText("")
        self.lbl_time.setText("")
        self.batch_table.setRowCount(0)
        self.sched_table.setRowCount(0)
        self.maint_table.setRowCount(0)
        self.delay_table.setRowCount(0)
        self.log_text.clear()
