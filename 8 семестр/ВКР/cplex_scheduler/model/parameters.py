"""
Классы параметров задачи оптимизации расписания
конвейерных систем с учётом технического обслуживания
"""

import json
import numpy as np


class TaskParameters:
    """Хранит все входные параметры задачи"""

    def __init__(self):
        # Размерности
        self.I = 3   # количество типов заданий
        self.L = 3   # количество приборов
        self.J = 4   # количество позиций (пакетов)

        # Количество заданий каждого типа (индекс 0..I-1)
        self.n = [4, 4, 4]

        # Времена обработки t[l][i]: прибор l, тип i (0-indexed)
        self.t = [
            [2.0, 4.0, 6.0],
            [3.0, 5.0, 7.0],
            [1.0, 3.0, 5.0],
        ]

        # Времена переналадки t_setup[l][i][k]: прибор l, с типа i на тип k
        self.t_setup = [
            [[0, 1, 2], [1, 0, 1], [2, 1, 0]],
            [[0, 2, 3], [2, 0, 2], [3, 2, 0]],
            [[0, 1, 2], [1, 0, 1], [2, 1, 0]],
        ]

        # Времена первоначальной наладки t_init[l][i]
        self.t_init = [
            [1.0, 2.0, 3.0],
            [2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0],
        ]

        # Директивные сроки окончания выполнения наборов заданий
        self.d = [30.0, 40.0, 50.0]

        # Параметры технического обслуживания
        self.TM = [20.0, 25.0, 18.0]       # период ТО (макс. время работы между ТО)
        self.tm_maint = [2.0, 3.0, 2.0]    # длительность одного сеанса ТО

        # Включить учёт ТО
        self.use_maintenance = True

    def validate(self):
        """Проверка корректности параметров. Возвращает список ошибок."""
        errors = []

        if self.I < 2:
            errors.append("Количество типов заданий I должно быть ≥ 2")
        if self.L < 2:
            errors.append("Количество приборов L должно быть ≥ 2")
        if self.J < 2:
            errors.append("Количество позиций J должно быть ≥ 2")
        if self.J < self.I:
            errors.append(
                f"Количество позиций J={self.J} должно быть ≥ числу типов заданий I={self.I}: "
                f"условие чередования типов требует минимум одну позицию на каждый тип."
            )
        if self.J > self.I * max(self.n) if self.n else True:
            pass  # нормально

        if len(self.n) != self.I:
            errors.append(f"Длина массива n ({len(self.n)}) не совпадает с I={self.I}")
        else:
            for i, ni in enumerate(self.n):
                if ni < 2:
                    errors.append(f"n[{i+1}]={ni} должно быть ≥ 2")

        if len(self.t) != self.L:
            errors.append(f"Матрица t должна иметь {self.L} строк (приборов)")
        else:
            for l in range(self.L):
                if len(self.t[l]) != self.I:
                    errors.append(f"t[{l+1}] должна иметь {self.I} элементов")
                else:
                    for i in range(self.I):
                        if self.t[l][i] <= 0:
                            errors.append(f"t[{l+1}][{i+1}]={self.t[l][i]} должно быть > 0")

        if len(self.d) != self.I:
            errors.append(f"Длина массива d ({len(self.d)}) не совпадает с I={self.I}")

        if self.use_maintenance:
            if len(self.TM) != self.L:
                errors.append(f"Длина TM ({len(self.TM)}) не совпадает с L={self.L}")
            if len(self.tm_maint) != self.L:
                errors.append(f"Длина tm_maint ({len(self.tm_maint)}) не совпадает с L={self.L}")
            for l in range(min(len(self.TM), self.L)):
                if self.TM[l] <= 0:
                    errors.append(f"TM[{l+1}]={self.TM[l]} должно быть > 0")
                if self.tm_maint[l] <= 0:
                    errors.append(f"tm_maint[{l+1}]={self.tm_maint[l]} должно быть > 0")

        return errors

    def to_dict(self):
        return {
            "I": self.I,
            "L": self.L,
            "J": self.J,
            "n": self.n,
            "t": self.t,
            "t_setup": self.t_setup,
            "t_init": self.t_init,
            "d": self.d,
            "TM": self.TM,
            "tm_maint": self.tm_maint,
            "use_maintenance": self.use_maintenance,
        }

    def to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data):
        p = cls()
        p.I = data["I"]
        p.L = data["L"]
        p.J = data["J"]
        p.n = data["n"]
        p.t = data["t"]
        p.t_setup = data["t_setup"]
        p.t_init = data.get("t_init", [[1.0]*p.I for _ in range(p.L)])
        p.d = data["d"]
        p.TM = data.get("TM", [20.0]*p.L)
        p.tm_maint = data.get("tm_maint", [2.0]*p.L)
        p.use_maintenance = data.get("use_maintenance", True)
        return p

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def get_u_j(self):
        """Максимальное число заданий в одном пакете"""
        n_min = min(self.n)
        return n_min - 2  # по статье Кротова: uj = n - 2

    @classmethod
    def example_small(cls):
        """Маленький пример для быстрого тестирования"""
        p = cls()
        p.I = 3
        p.L = 3
        p.J = 4
        p.n = [4, 4, 4]
        p.t = [[2,4,6],[3,5,7],[1,3,5]]
        p.t_setup = [
            [[0,1,2],[1,0,1],[2,1,0]],
            [[0,2,3],[2,0,2],[3,2,0]],
            [[0,1,2],[1,0,1],[2,1,0]],
        ]
        p.t_init = [[1,2,3],[2,3,4],[1,2,3]]
        p.d = [30, 40, 50]
        p.TM = [20, 25, 18]
        p.tm_maint = [2, 3, 2]
        p.use_maintenance = True
        return p

    @classmethod
    def example_medium(cls):
        """Средний пример из статьи Кротова"""
        p = cls()
        p.I = 5
        p.L = 5
        p.J = 6
        p.n = [8, 8, 8, 8, 8]
        # t[l][i]: прибор l, тип i — соотношение max/min = 4
        p.t = [
            [2, 4, 6, 8, 8],
            [3, 5, 7, 6, 9],
            [1, 3, 5, 4, 6],
            [2, 4, 6, 5, 7],
            [3, 5, 4, 6, 8],
        ]
        p.t_setup = [
            [[0,1,2,1,2],[1,0,1,2,1],[2,1,0,1,2],[1,2,1,0,1],[2,1,2,1,0]],
            [[0,2,3,2,3],[2,0,2,3,2],[3,2,0,2,3],[2,3,2,0,2],[3,2,3,2,0]],
            [[0,1,2,1,2],[1,0,1,2,1],[2,1,0,1,2],[1,2,1,0,1],[2,1,2,1,0]],
            [[0,2,3,2,3],[2,0,2,3,2],[3,2,0,2,3],[2,3,2,0,2],[3,2,3,2,0]],
            [[0,1,2,1,2],[1,0,1,2,1],[2,1,0,1,2],[1,2,1,0,1],[2,1,2,1,0]],
        ]
        p.t_init = [[1,2,3,2,3],[2,3,4,3,4],[1,2,3,2,3],[2,3,4,3,4],[1,2,3,2,3]]
        p.d = [40, 80, 80, 120, 160]
        p.TM = [40, 45, 35, 42, 38]
        p.tm_maint = [3, 4, 3, 4, 3]
        p.use_maintenance = True
        return p
