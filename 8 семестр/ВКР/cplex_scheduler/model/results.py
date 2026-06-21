"""
Класс для параметров результата оптимизации
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class BatchInfo:
    """Информация об одном пакете заданий"""
    position: int        # позиция j (1-indexed)
    task_type: int       # тип заданий i (1-indexed)
    count: int           # количество заданий в пакете


@dataclass
class ScheduleEntry:
    """Запись расписания для одного прибора и позиции"""
    device: int          # прибор l (1-indexed)
    position: int        # позиция j (1-indexed)
    task_type: int       # тип заданий
    start_time: float    # момент начала q_lj
    process_time: float  # время обработки
    end_time: float      # момент окончания


@dataclass
class MaintenanceEntry:
    """Запись о сеансе технического обслуживания"""
    device: int          # прибор l (1-indexed)
    before_position: int # перед какой позицией
    start_time: float    # момент начала ТО
    duration: float      # длительность ТО
    end_time: float      # момент окончания ТО


class OptimizationResults:
    """Результаты оптимизации"""

    # Статусы решения
    STATUS_OPTIMAL = "Оптимальное решение"
    STATUS_FEASIBLE = "Допустимое решение (не оптимальное)"
    STATUS_INFEASIBLE = "Задача не имеет решения"
    STATUS_TIMEOUT = "Превышен лимит времени"
    STATUS_ERROR = "Ошибка решателя"
    STATUS_NOT_SOLVED = "Задача не решена"

    def __init__(self):
        self.status = self.STATUS_NOT_SOLVED
        self.objective_value: Optional[float] = None
        self.criterion: str = "Cmax"   # "Cmax" или "G"
        self.solve_time: float = 0.0
        self.solver_name: str = ""

        # Составы пакетов
        self.batches: List[BatchInfo] = []

        # Расписание (по приборам и позициям)
        self.schedule: List[ScheduleEntry] = []

        # Расписание ТО
        self.maintenance: List[MaintenanceEntry] = []

        # Запаздывания (для критерия G)
        self.delays: Dict[int, float] = {}   # тип -> запаздывание
        self.completion_times: Dict[int, float] = {}  # тип -> момент окончания

        # Для сравнения с фиксированными пакетами
        self.fixed_objective: Optional[float] = None
        self.improvement_percent: Optional[float] = None

        # Сообщение об ошибке/статусе
        self.message: str = ""

        # Значения переменных (для отладки)
        self.raw_x: Dict = {}   # x[i][j]
        self.raw_m: Dict = {}   # m[j]
        self.raw_q: Dict = {}   # q[l][j]

    @property
    def is_solved(self):
        return self.status in (self.STATUS_OPTIMAL, self.STATUS_FEASIBLE, self.STATUS_TIMEOUT)

    def get_schedule_for_device(self, device: int) -> List[ScheduleEntry]:
        return sorted([e for e in self.schedule if e.device == device],
                      key=lambda e: e.position)

    def get_maintenance_for_device(self, device: int) -> List[MaintenanceEntry]:
        return sorted([m for m in self.maintenance if m.device == device],
                      key=lambda m: m.start_time)

    def get_makespan(self) -> Optional[float]:
        if self.criterion == "Cmax":
            return self.objective_value
        if self.schedule:
            return max(e.end_time for e in self.schedule)
        return None

    def to_dict(self):
        return {
            "status": self.status,
            "criterion": self.criterion,
            "objective_value": self.objective_value,
            "solve_time": self.solve_time,
            "solver_name": self.solver_name,
            "fixed_objective": self.fixed_objective,
            "improvement_percent": self.improvement_percent,
            "batches": [
                {"position": b.position, "task_type": b.task_type, "count": b.count}
                for b in self.batches
            ],
            "schedule": [
                {"device": e.device, "position": e.position,
                 "task_type": e.task_type, "start_time": e.start_time,
                 "process_time": e.process_time, "end_time": e.end_time}
                for e in self.schedule
            ],
            "maintenance": [
                {"device": m.device, "before_position": m.before_position,
                 "start_time": m.start_time, "duration": m.duration,
                 "end_time": m.end_time}
                for m in self.maintenance
            ],
            "delays": self.delays,
            "completion_times": self.completion_times,
        }

    def to_json(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def summary(self) -> str:
        lines = [
            f"Статус: {self.status}",
            f"Критерий: {self.criterion}",
        ]
        if self.objective_value is not None:
            lines.append(f"Значение критерия: {self.objective_value:.4f}")
        if self.fixed_objective is not None:
            lines.append(f"Фиксированные пакеты: {self.fixed_objective:.4f}")
        if self.improvement_percent is not None:
            lines.append(f"Улучшение: {self.improvement_percent:.1f}%")
        lines.append(f"Время решения: {self.solve_time:.2f} с")
        if self.batches:
            lines.append(f"Пакетов: {len(self.batches)}")
        if self.maintenance:
            lines.append(f"Сеансов ТО: {len(self.maintenance)}")
        return "\n".join(lines)
