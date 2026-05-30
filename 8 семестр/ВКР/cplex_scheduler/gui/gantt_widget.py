"""
Виджет диаграммы Ганта для отображения расписания
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QSizePolicy
)
from PyQt5.QtCore import Qt

try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from model.results import OptimizationResults
from model.parameters import TaskParameters

# Цветовая палитра для типов заданий
TASK_COLORS = [
    '#4472C4', '#ED7D31', '#70AD47', '#FF0000', '#7030A0',
    '#00B0F0', '#FF9900', '#92D050', '#FF0066', '#00B050',
]
MAINT_COLOR = '#BFBFBF'
MAINT_HATCH = '//'


class GanttWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._results = None
        self._params = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        if not HAS_MATPLOTLIB:
            lbl = QLabel("matplotlib не установлен.\nУстановите: pip install matplotlib")
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
            return

        # Кнопки
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🔄 Обновить")
        self.btn_refresh.clicked.connect(self._draw)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_save = QPushButton("💾 Сохранить PNG")
        self.btn_save.clicked.connect(self._save_png)
        btn_layout.addWidget(self.btn_save)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Canvas matplotlib
        self.figure = Figure(figsize=(12, 6), facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Подсказка
        self.lbl_hint = QLabel("Нажмите «Решить» для построения диаграммы Ганта")
        self.lbl_hint.setAlignment(Qt.AlignCenter)
        self.lbl_hint.setStyleSheet("color: #888; font-size: 11pt;")
        layout.addWidget(self.lbl_hint)

    def update_gantt(self, results: OptimizationResults, params: TaskParameters):
        self._results = results
        self._params = params
        if HAS_MATPLOTLIB and results.is_solved:
            self.lbl_hint.hide()
            self._draw()
        else:
            self.lbl_hint.show()

    def _draw(self):
        if not HAS_MATPLOTLIB or self._results is None:
            return
        results = self._results
        params = self._params
        if not results.is_solved:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        L = params.L
        bar_height = 0.6
        y_positions = list(range(L))
        I = params.I

        legend_patches = []
        drawn_types = set()

        # Расписание
        for entry in results.schedule:
            l = entry.device - 1
            y = y_positions[l]
            color = TASK_COLORS[(entry.task_type - 1) % len(TASK_COLORS)]

            rect = ax.barh(y, entry.process_time, left=entry.start_time,
                           height=bar_height, color=color, edgecolor='white',
                           linewidth=0.8, alpha=0.85)

            # Подпись внутри блока
            cx = entry.start_time + entry.process_time / 2
            ax.text(cx, y, f"T{entry.task_type}\nj={entry.position}",
                    ha='center', va='center', fontsize=7, color='white',
                    fontweight='bold')

            if entry.task_type not in drawn_types:
                legend_patches.append(
                    mpatches.Patch(color=color, label=f"Тип {entry.task_type}")
                )
                drawn_types.add(entry.task_type)

        # ТО
        maint_patch_added = False
        for m in results.maintenance:
            l = m.device - 1
            y = y_positions[l]
            ax.barh(y, m.duration, left=m.start_time,
                    height=bar_height, color=MAINT_COLOR,
                    hatch=MAINT_HATCH, edgecolor='#666666', linewidth=0.8,
                    alpha=0.9)
            cx = m.start_time + m.duration / 2
            ax.text(cx, y, "ТО", ha='center', va='center',
                    fontsize=7, color='#333', fontweight='bold')
            if not maint_patch_added:
                legend_patches.append(
                    mpatches.Patch(facecolor=MAINT_COLOR, hatch=MAINT_HATCH,
                                   edgecolor='#666', label="ТО")
                )
                maint_patch_added = True

        # Оформление
        ax.set_yticks(y_positions)
        ax.set_yticklabels([f"Прибор {l+1}" for l in range(L)], fontsize=10)
        ax.set_xlabel("Время", fontsize=10)
        ax.set_title("Диаграмма Ганта расписания выполнения пакетов заданий",
                     fontsize=12, fontweight='bold', pad=10)
        ax.grid(axis='x', linestyle='--', alpha=0.4)

        # Вертикальная линия Cmax
        cmax = results.get_makespan()
        if cmax:
            ax.axvline(x=cmax, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
            ax.text(cmax, L - 0.5, f'Cmax={cmax:.1f}',
                    ha='right', va='top', color='red', fontsize=9)

        if legend_patches:
            ax.legend(handles=legend_patches, loc='upper right',
                      fontsize=8, framealpha=0.8)

        # Информация
        info_parts = [f"Критерий: {results.criterion} = {results.objective_value:.3f}"]
        if results.improvement_percent is not None:
            info_parts.append(f"Улучшение vs фикс. пакеты: {results.improvement_percent:.1f}%")
        if results.maintenance:
            info_parts.append(f"Сеансов ТО: {len(results.maintenance)}")
        ax.set_xlabel(ax.get_xlabel() + "\n" + "  |  ".join(info_parts), fontsize=9)

        self.figure.tight_layout()
        self.canvas.draw()

    def _save_png(self):
        if not HAS_MATPLOTLIB:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить диаграмму", "gantt_chart.png",
            "PNG files (*.png);;All Files (*)"
        )
        if path:
            self.figure.savefig(path, dpi=150, bbox_inches='tight',
                                facecolor='white')

    def clear(self):
        if HAS_MATPLOTLIB:
            self.figure.clear()
            self.canvas.draw()
        self.lbl_hint.show()
