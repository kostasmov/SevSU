import json
import numpy as np

class TaskParameters:
    """Объект для хранения параметров задачи"""

    def __init__(self):
        # Размерность задачи
        self.I = 0  # количество типов заданий
        self.L = 0  # количество приборов
        self.J = 0  # количество позиций (пакетов)

        # Количество заданий каждого типа (n[i])
        self.n = []

        # Время обработки задания типа i на приборе l: t[l][i]:
        self.t = []

        # Время переналадки прибора l с типа i на тип k: t_setup[l][i][k]
        self.t_setup = []

        # Время первоначальной наладки прибора l на тип i: t_init[l][i]
        self.t_init = []

        # Директивные сроки окончания выполнения типов заданий d[i]
        # self.d = []

        # Параметры сеанса технического обслуживания:
        self.TM = []        # момент начала ПТО прибора l
        self.tm_maint = []  # длительность ПТО прибора l

        # Флаг надо ли включить в решение учёт ПТО
        self.use_maintenance = True

    def validate(self):
        """Проверка корректности параметров. Возвращает список ошибок."""
        errors = []

        # Проверка размерностей задачи
        if self.I < 2:
            errors.append("Количество типов заданий (I) должно быть ≥ 2")
        if self.L < 2:
            errors.append("Количество приборов (L) должно быть ≥ 2")
        if self.J < self.I:
            errors.append(f"Количество пакетов (J) должно быть ≥ числу типов заданий I={self.I}: ")
        # if self.J > self.I * max(self.n) if self.n else True:
        #     pass

        # Проверка списка количества заданий каждого типа (n[i])
        if len(self.n) != self.I:
            errors.append(f"Длина списка n[i] не совпадает с I={self.I}")
        else:
            for i, ni in enumerate(self.n):
                if ni < 2:
                    errors.append(f"Заданий n[{i+1}] не может быть меньше 2")

        # Проверка матрицы длительностей обработки t[l][i]
        if len(self.t) != self.L:
            errors.append(f"Матрица t должна иметь {self.L} строк (приборов)")
        else:
            for l in range(self.L):
                if len(self.t[l]) != self.I:
                    errors.append(f"Строка t[{l+1}] должна иметь {self.I} элементов (типов заданий)")
                else:
                    for i in range(self.I):
                        if self.t[l][i] <= 0:
                            errors.append(f"Длительность t[{l+1}][{i+1}] не может быть < 0")

        # if len(self.d) != self.I:
        #     errors.append(f"Длина массива d ({len(self.d)}) не совпадает с I={self.I}")

        # Валидация параметров ПТО
        if self.use_maintenance:
            # Проверка размерности матриц ПТО
            if len(self.TM) != self.L:
                errors.append(f"Число сеансов ПТО не совпадает с числом приборов L={self.L}")
            if len(self.tm_maint) != self.L:
                errors.append(f"Число длин ПТО не совпадает с числом приборов L={self.L}")

            # Проверка значений параметров ПТО
            for l in range(min(len(self.TM), self.L)):
                if self.TM[l] < 0:
                    errors.append(f"Сеанс ПТО TM[{l+1}] не может начаться раньше момента 0")
                if self.tm_maint[l] <= 0:
                    errors.append(f"Длина сеанса ПТО tm_maint[{l+1}] не может быть <= 0")

        return errors

    def to_dict(self):
        """Перевод объекта в форму словаря"""
        return {
            "I": self.I,
            "L": self.L,
            "J": self.J,
            "n": self.n,
            "t": self.t,
            "t_setup": self.t_setup,
            "t_init": self.t_init,
            #"d": self.d,
            "TM": self.TM,
            "tm_maint": self.tm_maint,
            "use_maintenance": self.use_maintenance,
        }

    def to_json(self, filepath):
        """Перевод объекта в форму для загрузки в JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data):
        """Формирование объекта из словаря"""
        p = cls()

        p.I = data["I"]
        p.L = data["L"]
        p.J = data["J"]

        p.n = data["n"]
        p.t = data["t"]
        p.t_setup = data["t_setup"]
        p.t_init = data.get("t_init")
        #p.d = data["d"]

        p.TM = data.get("TM")
        p.tm_maint = data.get("tm_maint")
        p.use_maintenance = data.get("use_maintenance", True)

        return p

    # def get_u_j(self):
    #     """Максимальное число заданий в одном пакете"""
    #     n_min = min(self.n)
    #     return n_min

    @classmethod
    def from_json(cls, filepath):
        """Формирование объекта из файла JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def example_small(cls):
        """Маленький пример (быстрый тест)"""
        p = cls()

        p.I = 3
        p.L = 3
        p.J = 4

        p.n = [4, 4, 4]

        p.t = [
            [2,4,6],
            [3,5,7],
            [1,3,5]
        ]

        p.t_setup = [
            [[0,1,2],[1,0,1],[2,1,0]],
            [[0,2,3],[2,0,2],[3,2,0]],
            [[0,1,2],[1,0,1],[2,1,0]],
        ]

        p.t_init = [
            [1,2,3],
            [2,3,4],
            [1,2,3]
        ]

        #p.d = [30, 40, 50]

        p.TM = [20, 25, 18]
        p.tm_maint = [2, 3, 2]
        p.use_maintenance = True

        return p

    @classmethod
    def example_medium(cls):
        """Средний пример"""
        p = cls()

        p.I = 5
        p.L = 5
        p.J = 6

        p.n = [8, 8, 8, 8, 8]

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

        p.t_init = [
            [1,2,3,2,3],
            [2,3,4,3,4],
            [1,2,3,2,3],
            [2,3,4,3,4],
            [1,2,3,2,3]
        ]

        #p.d = [120, 200, 280, 360, 420]

        p.TM = [80, 90, 75, 85, 80]
        p.tm_maint = [3, 4, 3, 4, 3]
        p.use_maintenance = True

        return p
