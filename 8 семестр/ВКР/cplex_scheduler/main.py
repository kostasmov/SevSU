"""
Точка входа приложения.
Система оптимизации расписания конвейерных систем.
ВКР бакалавра, СевГУ, кафедра ИС.
"""

import sys
import os

# Добавить корневую папку проекта в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
except ImportError:
    print("ОШИБКА: PyQt5 не установлен!")
    print("Выполните: pip install PyQt5")
    sys.exit(1)

from gui.main_window import MainWindow


def main():
    # Включить поддержку High DPI
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("FlowShop Batch Scheduler")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("SevGU")

    # Стиль
    app.setStyle('Fusion')

    # Шрифт по умолчанию
    font = QFont("Segoe UI", 9)
    app.setFont(font)

    # Цветовая схема (Fusion + синяя акцентная)
    from PyQt5.QtGui import QPalette, QColor
    palette = app.palette()
    palette.setColor(QPalette.Highlight, QColor("#2F5597"))
    palette.setColor(QPalette.HighlightedText, QColor("white"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
