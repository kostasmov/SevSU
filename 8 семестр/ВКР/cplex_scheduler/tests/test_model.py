"""
Тесты модели MILP
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.parameters import TaskParameters
from model.milp_model import MILPModel, SOLVER_AVAILABLE
from model.results import OptimizationResults


def test_params_validate():
    """ТЕСТ 1 - Валидация параметров"""
    p = TaskParameters.example_small()
    errors = p.validate()
    assert len(errors) == 0, f"Ошибки валидации: {errors}"
    print("✓ Валидация параметров — OK")


def test_params_serialization():
    """ТЕСТ 2 - Сохранение параметров в JSON"""
    import tempfile, json
    p = TaskParameters.example_small()
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
        p.to_json(f.name)
        fname = f.name
    p2 = TaskParameters.from_json(fname)
    assert p.I == p2.I
    assert p.L == p2.L
    assert p.J == p2.J
    print("✓ Сериализация параметров — OK")


def test_fixed_objective():
    """ТЕСТ 3 - вычисление критерия при неопитимизированном расписании"""
    p = TaskParameters.example_small()
    model = MILPModel(p, "Cmax", time_limit=30)
    val = model._compute_suboptimal_criterion()
    assert val is not None and val > 0
    print(f"✓ Фиксированные пакеты Cmax = {val:.3f}")


def test_solve_small_cmax():
    if SOLVER_AVAILABLE is None:
        print("⚠ Решатель не найден, тест пропущен")
        return
    p = TaskParameters.example_small()
    p.use_maintenance = False   # без ТО для скорости
    model = MILPModel(p, "Cmax", time_limit=60)
    results = model.solve()
    print(f"✓ Решение (Cmax, без ТО): status={results.status}, "
          f"Cmax={results.objective_value}, время={results.solve_time:.2f}с")
    assert results.objective_value is not None
    assert len(results.batches) > 0
    assert len(results.schedule) > 0


def test_solve_small_cmax_with_maint():
    if SOLVER_AVAILABLE is None:
        print("⚠ Решатель не найден, тест пропущен")
        return
    p = TaskParameters.example_small()
    p.use_maintenance = True
    model = MILPModel(p, "Cmax", time_limit=60)
    results = model.solve()
    print(f"✓ Решение (Cmax, с ТО): status={results.status}, "
          f"Cmax={results.objective_value}, ТО={len(results.maintenance)}, "
          f"время={results.solve_time:.2f}с")


def test_solve_small_G():
    if SOLVER_AVAILABLE is None:
        print("⚠ Решатель не найден, тест пропущен")
        return
    p = TaskParameters.example_small()
    p.use_maintenance = False
    model = MILPModel(p, "G", time_limit=60)
    results = model.solve()
    print(f"✓ Решение (G, без ТО): status={results.status}, "
          f"G={results.objective_value}, время={results.solve_time:.2f}с")


if __name__ == '__main__':
    print("=== Запуск тестов модели ===\n")
    test_params_validate()
    test_params_serialization()
    test_fixed_objective()
    test_solve_small_cmax()
    test_solve_small_cmax_with_maint()
    test_solve_small_G()
    print("\n=== Все тесты пройдены ===")
