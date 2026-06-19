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


def _check_solvers(app):
    """Проверить наличие решателей при старте и подсказать пользователю.

    Логика:
    - есть pulp  -> всё решается всегда (CPLEX, если установлен, используется
      для малых задач, PuLP/CBC подхватывает остальные);
    - есть только CPLEX (Community) -> предупредить: большие задачи не решатся,
      предложить установить pulp;
    - нет ничего -> критическая ошибка с инструкцией.
    """
    from PyQt5.QtWidgets import QMessageBox

    has_cplex = False
    has_pulp = False
    try:
        import docplex.mp.model  # noqa: F401
        has_cplex = True
    except ImportError:
        pass
    try:
        import pulp  # noqa: F401
        has_pulp = True
    except ImportError:
        pass

    if not has_cplex and not has_pulp:
        QMessageBox.critical(
            None, "Решатель не найден",
            "Не найден ни один решатель MILP.\n\n"
            "Установите хотя бы бесплатный решатель PuLP/CBC.\n"
            "Откройте командную строку и выполните одну строку:\n\n"
            "pip install pulp\n\n"
            "После установки запустите программу заново.")
        return False

    if has_cplex and not has_pulp:
        QMessageBox.warning(
            None, "Рекомендация",
            "Найден IBM CPLEX, но не найден резервный решатель PuLP/CBC.\n\n"
            "Бесплатная Community-версия CPLEX решает задачи только до "
            "1000 переменных / 1000 ограничений (малый пример укладывается, "
            "средний — нет).\n\n"
            "Чтобы решались задачи любой размерности, установите бесплатный "
            "PuLP — программа будет переключаться на него автоматически.\n"
            "Откройте командную строку и выполните одну строку:\n\n"
            "pip install pulp")
    return True


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

    if not _check_solvers(app):
        return 1

    window = MainWindow()
    window.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
