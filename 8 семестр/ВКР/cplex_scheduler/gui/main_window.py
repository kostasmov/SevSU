"""
Главное окно приложения
"""

import os
import json
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QProgressBar,
    QStatusBar, QMenuBar, QMenu, QAction, QFileDialog,
    QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor

from gui.input_tab import InputTab
from gui.result_tab import ResultTab
from gui.gantt_widget import GanttWidget
from gui.analysis_tab import AnalysisTab
from model.parameters import TaskParameters
from model.milp_model import MILPModel, SOLVER_AVAILABLE
from model.results import OptimizationResults
from utils.exporter import export_to_excel, HAS_OPENPYXL


class SolverWorker(QThread):
    """Поток решателя, чтобы GUI не замерзал"""
    finished = pyqtSignal(OptimizationResults)
    error = pyqtSignal(str)

    def __init__(self, params, criterion, time_limit, verbose):
        super().__init__()
        self.params = params
        self.criterion = criterion
        self.time_limit = time_limit
        self.verbose = verbose

    def run(self):
        try:
            model = MILPModel(self.params, self.criterion,
                              self.time_limit, self.verbose)
            results = model.solve()
            self.finished.emit(results)
        except Exception as e:
            import traceback
            self.error.emit(traceback.format_exc())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оптимизация расписания конвейерных систем — ВКР")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 820)

        self._current_results = None
        self._current_params = None
        self._worker = None

        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        self._check_solver()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # ── Верхняя панель ──
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self.btn_solve = QPushButton("▶  Решить задачу")
        self.btn_solve.setFont(QFont("Arial", 11, QFont.Bold))
        self.btn_solve.setStyleSheet("""
            QPushButton {
                background-color: #2F5597;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #1F3E7A; }
            QPushButton:disabled { background-color: #AAAAAA; }
        """)
        self.btn_solve.clicked.connect(self._on_solve)
        toolbar.addWidget(self.btn_solve)

        self.btn_stop = QPushButton("⏹  Стоп")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #C00000;
                color: white;
                padding: 8px 14px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #900000; }
            QPushButton:disabled { background-color: #AAAAAA; }
        """)
        self.btn_stop.clicked.connect(self._on_stop)
        toolbar.addWidget(self.btn_stop)

        toolbar.addSpacing(8)

        # Разделитель
        sep = QLabel("|")
        sep.setStyleSheet("color: #CCC; font-size: 18px;")
        toolbar.addWidget(sep)

        toolbar.addSpacing(4)

        # Кнопки загрузки/сохранения
        btn_open = QPushButton("📂 Открыть")
        btn_open.setToolTip("Открыть параметры из JSON-файла (Ctrl+O)")
        btn_open.setStyleSheet("padding: 6px 12px;")
        btn_open.clicked.connect(self._open_params)
        toolbar.addWidget(btn_open)

        btn_save = QPushButton("💾 Сохранить")
        btn_save.setToolTip("Сохранить параметры в JSON-файл (Ctrl+S)")
        btn_save.setStyleSheet("padding: 6px 12px;")
        btn_save.clicked.connect(self._save_params)
        toolbar.addWidget(btn_save)

        toolbar.addSpacing(4)

        btn_ex_s = QPushButton("📋 Мал. пример")
        btn_ex_s.setToolTip("Загрузить малый пример (I=3, L=3)")
        btn_ex_s.setStyleSheet("padding: 6px 10px;")
        btn_ex_s.clicked.connect(lambda: self._load_example("small"))
        toolbar.addWidget(btn_ex_s)

        btn_ex_m = QPushButton("📋 Сред. пример")
        btn_ex_m.setToolTip("Загрузить средний пример (I=5, L=5)")
        btn_ex_m.setStyleSheet("padding: 6px 10px;")
        btn_ex_m.clicked.connect(lambda: self._load_example("medium"))
        toolbar.addWidget(btn_ex_m)

        toolbar.addSpacing(4)

        sep2 = QLabel("|")
        sep2.setStyleSheet("color: #CCC; font-size: 18px;")
        toolbar.addWidget(sep2)

        self.btn_export = QPushButton("📊 Экспорт Excel")
        self.btn_export.setEnabled(False)
        self.btn_export.setToolTip("Экспорт результатов в Excel")
        self.btn_export.setStyleSheet("padding: 6px 12px;")
        self.btn_export.clicked.connect(self._export_excel)
        toolbar.addWidget(self.btn_export)

        self.btn_save_results = QPushButton("💾 Результаты JSON")
        self.btn_save_results.setEnabled(False)
        self.btn_save_results.setToolTip("Сохранить результаты в JSON")
        self.btn_save_results.setStyleSheet("padding: 6px 12px;")
        self.btn_save_results.clicked.connect(self._save_results_json)
        toolbar.addWidget(self.btn_save_results)

        toolbar.addStretch()

        # Индикатор решателя
        solver_txt = f"Решатель: {SOLVER_AVAILABLE or 'НЕ НАЙДЕН'}"
        solver_color = "#00703C" if SOLVER_AVAILABLE else "#FF0000"
        self.lbl_solver = QLabel(solver_txt)
        self.lbl_solver.setStyleSheet(
            f"color: {solver_color}; font-weight: bold; padding: 0 8px;")
        toolbar.addWidget(self.lbl_solver)

        main_layout.addLayout(toolbar)

        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setMaximumHeight(5)
        self.progress.setTextVisible(False)
        self.progress.hide()
        main_layout.addWidget(self.progress)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 10))

        self.input_tab = InputTab()
        self.result_tab = ResultTab()
        self.gantt_tab = GanttWidget()
        self.analysis_tab = AnalysisTab()

        self.tabs.addTab(self.input_tab, "⚙️  Параметры задачи")
        self.tabs.addTab(self.result_tab, "📋  Результаты")
        self.tabs.addTab(self.gantt_tab, "📊  Диаграмма Ганта")
        self.tabs.addTab(self.analysis_tab, "📈  Анализ")

        main_layout.addWidget(self.tabs)

    def _setup_menu(self):
        menubar = self.menuBar()

        # Файл
        file_menu = menubar.addMenu("Файл")

        act_new = QAction("Новая задача", self)
        act_new.setShortcut("Ctrl+N")
        act_new.triggered.connect(self._new_task)
        file_menu.addAction(act_new)

        file_menu.addSeparator()

        act_open = QAction("📂 Открыть параметры (JSON)...", self)
        act_open.setShortcut("Ctrl+O")
        act_open.triggered.connect(self._open_params)
        file_menu.addAction(act_open)

        act_save = QAction("💾 Сохранить параметры (JSON)...", self)
        act_save.setShortcut("Ctrl+S")
        act_save.triggered.connect(self._save_params)
        file_menu.addAction(act_save)

        file_menu.addSeparator()

        act_import_csv = QAction("📊 Импорт матриц из CSV...", self)
        act_import_csv.triggered.connect(self._import_csv_menu)
        file_menu.addAction(act_import_csv)

        act_export_csv = QAction("📤 Экспорт матриц в CSV...", self)
        act_export_csv.triggered.connect(self._export_csv_menu)
        file_menu.addAction(act_export_csv)

        file_menu.addSeparator()

        act_export = QAction("📊 Экспорт результатов (Excel)...", self)
        act_export.triggered.connect(self._export_excel)
        file_menu.addAction(act_export)

        act_export_res = QAction("💾 Сохранить результаты (JSON)...", self)
        act_export_res.triggered.connect(self._save_results_json)
        file_menu.addAction(act_export_res)

        file_menu.addSeparator()

        act_exit = QAction("Выход", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        # Примеры
        ex_menu = menubar.addMenu("Примеры")
        ex_small = QAction("Загрузить малый пример (I=3, L=3)", self)
        ex_small.triggered.connect(lambda: self._load_example("small"))
        ex_menu.addAction(ex_small)

        ex_med = QAction("Загрузить средний пример (I=5, L=5)", self)
        ex_med.triggered.connect(lambda: self._load_example("medium"))
        ex_menu.addAction(ex_med)

        # Форматы CSV
        fmt_menu = menubar.addMenu("Формат CSV")
        act_fmt = QAction("Показать формат CSV-файлов", self)
        act_fmt.triggered.connect(self._show_csv_format)
        fmt_menu.addAction(act_fmt)

        # Справка
        help_menu = menubar.addMenu("Справка")
        act_about = QAction("О программе", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

        act_info = QAction("Информация о решателе", self)
        act_info.triggered.connect(self._show_solver_info)
        help_menu.addAction(act_info)

    def _setup_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(
            "Готов к работе. Введите параметры задачи или загрузите JSON/CSV и нажмите «Решить».")

    def _check_solver(self):
        if SOLVER_AVAILABLE is None:
            QMessageBox.warning(
                self,
                "Решатель не найден",
                "Не найден ни один MILP-решатель!\n\n"
                "Установите один из:\n"
                "  • pip install pulp\n"
                "  • pip install docplex  (требует IBM CPLEX)\n\n"
                "Без решателя расчёты невозможны."
            )

    def _on_solve(self):
        if SOLVER_AVAILABLE is None:
            QMessageBox.critical(self, "Ошибка", "Решатель не установлен!")
            return

        params = self.input_tab.get_params()
        errors = params.validate()
        if errors:
            QMessageBox.warning(
                self, "Некорректные параметры",
                "Обнаружены ошибки:\n\n" + "\n".join(f"• {e}" for e in errors)
            )
            return

        criterion = self.input_tab.get_criterion()
        time_limit = self.input_tab.get_time_limit()
        verbose = self.input_tab.get_verbose()

        self._current_params = params
        self.result_tab.clear()
        self.gantt_tab.clear()

        self.btn_solve.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_export.setEnabled(False)
        self.btn_save_results.setEnabled(False)
        self.progress.show()
        self.status.showMessage(
            f"Решение задачи [{criterion}], I={params.I}, L={params.L}, J={params.J}..."
        )
        self.tabs.setCurrentIndex(1)

        self._worker = SolverWorker(params, criterion, time_limit, verbose)
        self._worker.finished.connect(self._on_solve_done)
        self._worker.error.connect(self._on_solve_error)
        self._worker.start()

    def _on_stop(self):
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._worker.wait(2000)
        self._reset_ui()
        self.status.showMessage("Решение остановлено пользователем.")

    def _on_solve_done(self, results: OptimizationResults):
        self._current_results = results
        self._reset_ui()

        self.result_tab.update_results(results, self._current_params)
        self.gantt_tab.update_gantt(results, self._current_params)
        self.analysis_tab.set_params(self._current_params, results.criterion)

        if results.is_solved:
            self.btn_export.setEnabled(True)
            self.btn_save_results.setEnabled(True)
        elif results.status == OptimizationResults.STATUS_INFEASIBLE:
            msg_text = "Задача не имеет допустимого решения.\n"
            if results.message:
                msg_text += f"\n{results.message}"
            QMessageBox.warning(self, "Задача неразрешима", msg_text)
        elif results.status == OptimizationResults.STATUS_ERROR:
            msg_text = "Ошибка при решении задачи."
            if results.message:
                msg_text += f"\n\n{results.message}"
            QMessageBox.critical(self, "Ошибка решателя", msg_text)

        if results.is_solved and results.objective_value is not None:
            msg = (f"Решение: {results.status} | "
                   f"{results.criterion} = {results.objective_value:.4f} | "
                   f"Время: {results.solve_time:.2f} с")
            if results.improvement_percent:
                msg += f" | Улучшение: {results.improvement_percent:.1f}%"
        else:
            msg = (f"Статус: {results.status} | "
                   f"Время: {results.solve_time:.2f} с"
                   + (f" | {results.message}" if results.message else ""))
        self.status.showMessage(msg)

    def _on_solve_error(self, err: str):
        self._reset_ui()
        QMessageBox.critical(self, "Ошибка решателя", err[:800])
        self.status.showMessage("Ошибка при решении.")

    def _reset_ui(self):
        self.btn_solve.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.hide()

    def _load_example(self, name):
        self.input_tab.load_example(name)
        self.status.showMessage(f"Загружен пример: {name}")

    def _new_task(self):
        reply = QMessageBox.question(
            self, "Новая задача",
            "Очистить все данные и начать заново?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self._load_example("small")
            self.result_tab.clear()
            self.gantt_tab.clear()
            self._current_results = None
            self.btn_export.setEnabled(False)
            self.btn_save_results.setEnabled(False)

    def _open_params(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть параметры", "", "JSON (*.json);;Все файлы (*)"
        )
        if path:
            try:
                p = TaskParameters.from_json(path)
                self.input_tab.load_params(p)
                self.status.showMessage(f"Загружены параметры: {os.path.basename(path)}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{e}")

    def _save_params(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить параметры", "params.json", "JSON (*.json)"
        )
        if path:
            try:
                p = self.input_tab.get_params()
                p.to_json(path)
                self.status.showMessage(f"Параметры сохранены: {os.path.basename(path)}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def _import_csv_menu(self):
        """Вызвать импорт CSV из вкладки ввода"""
        self.tabs.setCurrentIndex(0)
        self.input_tab._import_csv()

    def _export_csv_menu(self):
        """Вызвать экспорт CSV из вкладки ввода"""
        self.tabs.setCurrentIndex(0)
        self.input_tab._export_csv()

    def _export_excel(self):
        if not self._current_results or not self._current_results.is_solved:
            QMessageBox.information(self, "Нет результатов",
                                    "Сначала решите задачу.")
            return
        if not HAS_OPENPYXL:
            QMessageBox.critical(self, "Ошибка",
                                 "openpyxl не установлен: pip install openpyxl")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт в Excel", "results.xlsx",
            "Excel (*.xlsx);;Все файлы (*)"
        )
        if path:
            try:
                export_to_excel(self._current_results, self._current_params, path)
                QMessageBox.information(
                    self, "Готово",
                    f"Результаты сохранены:\n{path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def _save_results_json(self):
        if not self._current_results:
            QMessageBox.information(self, "Нет результатов", "Сначала решите задачу.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить результаты", "results.json", "JSON (*.json)"
        )
        if path:
            try:
                self._current_results.to_json(path)
                self.status.showMessage(f"Результаты сохранены: {os.path.basename(path)}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def _show_csv_format(self):
        QMessageBox.information(
            self, "Формат CSV-файлов",
            "Программа поддерживает CSV с разделителями ; или ,\n\n"
            "── Матрица времён обработки (t_processing.csv) ──\n"
            "  Строки = приборы (L строк)\n"
            "  Столбцы = типы заданий (I столбцов)\n"
            "  Пример (L=3, I=3):\n"
            "  2;4;6\n"
            "  3;5;7\n"
            "  1;3;5\n\n"
            "── Вектор n[i] (n_counts.csv) ──\n"
            "  Одна строка, I значений:\n"
            "  4;4;4\n\n"
            "── Вектор d[i] (d_deadlines.csv) ──\n"
            "  Одна строка, I значений:\n"
            "  30;40;50\n\n"
            "── Переналадки (t_setup_device_N.csv) ──\n"
            "  Квадратная матрица I×I для прибора N.\n"
            "  Диагональ = 0.\n\n"
            "Используйте «Экспорт CSV» для создания шаблонов."
        )

    def _show_about(self):
        QMessageBox.about(
            self,
            "О программе",
            "<h3>Система оптимизации расписания КС</h3>"
            "<p>Выпускная квалификационная работа бакалавра</p>"
            "<p><b>Тема:</b> Разработка системы оптимизации расписания выполнения "
            "пакетов заданий в конвейерных системах при учёте технического "
            "обслуживания приборов с использованием целочисленного программирования</p>"
            "<p><b>Кафедра:</b> Информационные системы, СевГУ, 2024</p>"
            "<hr>"
            "<p><b>Основана на:</b> Кротов К.В. Модели MILP оптимизации включения "
            "заданий в пакеты. ИУС, 2024, № 6, с. 46–57.</p>"
            "<p><b>Решатель:</b> IBM CPLEX (docplex) / PuLP (CBC/GLPK)</p>"
            "<p><b>GUI:</b> PyQt5 + matplotlib</p>"
            "<hr>"
            "<p><b>Форматы ввода данных:</b><br>"
            "  • Ручной ввод в таблицы<br>"
            "  • Вставка из Excel (буфер обмена)<br>"
            "  • Загрузка из JSON-файла<br>"
            "  • Импорт матриц из CSV-файлов</p>"
            "<p><b>Форматы экспорта:</b><br>"
            "  • Параметры → JSON<br>"
            "  • Матрицы → CSV (набор файлов)<br>"
            "  • Результаты → Excel (.xlsx)<br>"
            "  • Результаты → JSON</p>"
        )

    def _show_solver_info(self):
        if SOLVER_AVAILABLE == "cplex":
            msg = ("IBM CPLEX доступен через docplex.\n\n"
                   "Высокопроизводительный коммерческий решатель.\n"
                   "Community Edition: до 1000 переменных бесплатно.")
        elif SOLVER_AVAILABLE == "pulp":
            msg = ("PuLP доступен (CBC/GLPK solver).\n\n"
                   "Бесплатный открытый решатель.\n"
                   "Для задач малого и среднего размера работает хорошо.\n\n"
                   "Для улучшения производительности установите:\n"
                   "pip install docplex  (+ IBM CPLEX)")
        else:
            msg = ("Решатель НЕ НАЙДЕН!\n\n"
                   "Установите:\n"
                   "  pip install pulp\n"
                   "  (опционально: pip install docplex)")
        QMessageBox.information(self, "Информация о решателе", msg)

    def closeEvent(self, event):
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
        event.accept()
