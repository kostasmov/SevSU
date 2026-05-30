"""
Вкладка анализа — графики зависимостей, сравнение с фиксированными пакетами
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
    QProgressBar, QComboBox, QSpinBox, QFileDialog,
    QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QBrush

try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from model.parameters import TaskParameters
from model.milp_model import MILPModel
from model.results import OptimizationResults


class AnalysisWorker(QThread):
    """Поток для серии расчётов (анализ чувствительности)"""
    progress = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    finished_all = pyqtSignal(list)

    def __init__(self, base_params, vary_param, values, criterion, time_limit):
        super().__init__()
        self.base_params = base_params
        self.vary_param = vary_param
        self.values = values
        self.criterion = criterion
        self.time_limit = time_limit
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        results_list = []
        total = len(self.values)
        for idx, val in enumerate(self.values):
            if self._stop:
                break
            import copy
            p = copy.deepcopy(self.base_params)

            if self.vary_param == "J":
                p.J = int(val)
            elif self.vary_param == "TM":
                p.TM = [val] * p.L
            elif self.vary_param == "tm_maint":
                p.tm_maint = [val] * p.L
            elif self.vary_param == "n":
                p.n = [int(val)] * p.I

            try:
                model = MILPModel(p, self.criterion, self.time_limit)
                res = model.solve()
                row = {
                    "param_value": val,
                    "objective": res.objective_value,
                    "fixed_objective": res.fixed_objective,
                    "improvement": res.improvement_percent,
                    "solve_time": res.solve_time,
                    "status": res.status,
                    "maint_count": len(res.maintenance),
                }
            except Exception as e:
                row = {
                    "param_value": val,
                    "objective": None,
                    "fixed_objective": None,
                    "improvement": None,
                    "solve_time": 0,
                    "status": str(e),
                    "maint_count": 0,
                }
            results_list.append(row)
            self.progress.emit(int((idx + 1) / total * 100))
            self.result_ready.emit(row)

        self.finished_all.emit(results_list)


class AnalysisTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._base_params = None
        self._criterion = "Cmax"
        self._worker = None
        self._results_data = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Настройки анализа
        ctrl_group = QGroupBox("Параметры анализа чувствительности")
        ctrl_layout = QHBoxLayout(ctrl_group)

        ctrl_layout.addWidget(QLabel("Варьируемый параметр:"))
        self.combo_param = QComboBox()
        self.combo_param.addItems([
            "J — количество позиций (пакетов)",
            "TM — период ТО",
            "tm — длительность ТО",
            "n — количество заданий каждого типа",
        ])
        ctrl_layout.addWidget(self.combo_param)

        ctrl_layout.addWidget(QLabel("Мин:"))
        self.spin_min = QSpinBox()
        self.spin_min.setRange(2, 100)
        self.spin_min.setValue(3)
        ctrl_layout.addWidget(self.spin_min)

        ctrl_layout.addWidget(QLabel("Макс:"))
        self.spin_max = QSpinBox()
        self.spin_max.setRange(2, 200)
        self.spin_max.setValue(8)
        ctrl_layout.addWidget(self.spin_max)

        ctrl_layout.addWidget(QLabel("Шаг:"))
        self.spin_step = QSpinBox()
        self.spin_step.setRange(1, 50)
        self.spin_step.setValue(1)
        ctrl_layout.addWidget(self.spin_step)

        self.btn_run = QPushButton("▶ Запустить анализ")
        self.btn_run.setStyleSheet("background-color: #2F5597; color: white; padding: 5px;")
        self.btn_run.clicked.connect(self._run_analysis)
        ctrl_layout.addWidget(self.btn_run)

        self.btn_stop = QPushButton("⏹ Остановить")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_analysis)
        ctrl_layout.addWidget(self.btn_stop)

        layout.addWidget(ctrl_group)

        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        layout.addWidget(self.progress)

        # Разделение: таблица | график
        h_layout = QHBoxLayout()

        # Таблица результатов
        tbl_group = QGroupBox("Результаты серии расчётов")
        tbl_layout = QVBoxLayout(tbl_group)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Параметр", "Критерий (опт.)",
            "Критерий (фикс.)", "Улучшение %",
            "Время решения, с", "Сеансов ТО"
        ])
        self.results_table.setAlternatingRowColors(True)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        tbl_layout.addWidget(self.results_table)

        self.btn_export_table = QPushButton("Экспорт таблицы в CSV")
        self.btn_export_table.clicked.connect(self._export_table)
        tbl_layout.addWidget(self.btn_export_table)
        h_layout.addWidget(tbl_group, 1)

        # График
        chart_group = QGroupBox("График зависимости")
        chart_layout = QVBoxLayout(chart_group)
        if HAS_MATPLOTLIB:
            self.figure = Figure(figsize=(6, 4), facecolor='white')
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            chart_layout.addWidget(self.canvas)

            self.btn_save_chart = QPushButton("Сохранить график PNG")
            self.btn_save_chart.clicked.connect(self._save_chart)
            chart_layout.addWidget(self.btn_save_chart)
        else:
            chart_layout.addWidget(QLabel("matplotlib не установлен"))
        h_layout.addWidget(chart_group, 1)

        layout.addLayout(h_layout)

    def set_params(self, params: TaskParameters, criterion: str):
        self._base_params = params
        self._criterion = criterion

    def _get_param_key(self):
        idx = self.combo_param.currentIndex()
        return ["J", "TM", "tm_maint", "n"][idx]

    def _run_analysis(self):
        if self._base_params is None:
            QMessageBox.warning(self, "Нет данных",
                                "Сначала введите параметры задачи и нажмите 'Решить'")
            return

        param_key = self._get_param_key()
        vmin = self.spin_min.value()
        vmax = self.spin_max.value()
        vstep = self.spin_step.value()
        values = list(range(vmin, vmax + 1, vstep))

        if not values:
            QMessageBox.warning(self, "Ошибка", "Диапазон значений пуст")
            return

        self._results_data = []
        self.results_table.setRowCount(0)
        self.progress.setValue(0)
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)

        self._worker = AnalysisWorker(
            self._base_params, param_key, values,
            self._criterion, time_limit=60
        )
        self._worker.progress.connect(self.progress.setValue)
        self._worker.result_ready.connect(self._on_result)
        self._worker.finished_all.connect(self._on_finished)
        self._worker.start()

    def _stop_analysis(self):
        if self._worker:
            self._worker.stop()

    def _on_result(self, row):
        self._results_data.append(row)
        r = self.results_table.rowCount()
        self.results_table.insertRow(r)
        self._fill_row(r, row)
        self._update_chart()

    def _fill_row(self, r, row):
        def _item(val, color=None):
            s = f"{val:.3f}" if isinstance(val, float) else str(val) if val is not None else "—"
            item = QTableWidgetItem(s)
            item.setTextAlignment(Qt.AlignCenter)
            if color:
                item.setForeground(QBrush(QColor(color)))
            return item

        self.results_table.setItem(r, 0, _item(row["param_value"]))
        self.results_table.setItem(r, 1, _item(row["objective"]))
        self.results_table.setItem(r, 2, _item(row["fixed_objective"]))
        imp = row["improvement"]
        color = "#00B050" if imp and imp > 0 else None
        self.results_table.setItem(r, 3, _item(imp, color))
        self.results_table.setItem(r, 4, _item(row["solve_time"]))
        self.results_table.setItem(r, 5, _item(row["maint_count"]))

    def _on_finished(self, results):
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.setValue(100)
        self._update_chart()

    def _update_chart(self):
        if not HAS_MATPLOTLIB or not self._results_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        x = [r["param_value"] for r in self._results_data]
        y_opt = [r["objective"] for r in self._results_data]
        y_fix = [r["fixed_objective"] for r in self._results_data]
        y_imp = [r["improvement"] for r in self._results_data]

        # Основной график
        ax2 = ax.twinx()

        y_opt_clean = [v for v in y_opt if v is not None]
        y_fix_clean = [v for v in y_fix if v is not None]
        x_clean_opt = [x[i] for i, v in enumerate(y_opt) if v is not None]

        if y_opt_clean:
            ax.plot(x_clean_opt, y_opt_clean, 'b-o', label='Оптим. пакеты',
                    linewidth=2, markersize=5)
        if y_fix_clean:
            ax.plot(x_clean_opt[:len(y_fix_clean)], y_fix_clean, 'r--s',
                    label='Фикс. пакеты', linewidth=1.5, markersize=4)

        y_imp_clean = [v for v in y_imp if v is not None]
        if y_imp_clean:
            x_imp = [x[i] for i, v in enumerate(y_imp) if v is not None]
            ax2.fill_between(x_imp, 0, y_imp_clean, alpha=0.15, color='green')
            ax2.plot(x_imp, y_imp_clean, 'g-^', label='Улучшение %',
                     linewidth=1.5, markersize=4)
            ax2.set_ylabel("Улучшение, %", color='green', fontsize=9)
            ax2.tick_params(axis='y', labelcolor='green')

        param_names = {"J": "Количество позиций J", "TM": "Период ТО",
                       "tm_maint": "Длительность ТО", "n": "Количество заданий n"}
        ax.set_xlabel(param_names.get(self._get_param_key(), "Параметр"), fontsize=9)
        ax.set_ylabel(f"Значение критерия {self._criterion}", fontsize=9)
        ax.set_title(f"Зависимость {self._criterion} от параметров", fontsize=10)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(linestyle='--', alpha=0.4)

        self.figure.tight_layout()
        self.canvas.draw()

    def _save_chart(self):
        if not HAS_MATPLOTLIB:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить", "analysis_chart.png", "PNG (*.png)")
        if path:
            self.figure.savefig(path, dpi=150, bbox_inches='tight')

    def _export_table(self):
        if not self._results_data:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт", "analysis.csv", "CSV (*.csv)")
        if path:
            with open(path, 'w', encoding='utf-8-sig') as f:
                f.write("Параметр;Критерий (опт.);Критерий (фикс.);Улучшение %;Время решения\n")
                for row in self._results_data:
                    f.write(f"{row['param_value']};"
                            f"{row['objective'] or ''};"
                            f"{row['fixed_objective'] or ''};"
                            f"{row['improvement'] or ''};"
                            f"{row['solve_time']}\n")
