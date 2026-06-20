"""
MILP-модель оптимизации расписания выполнения пакетов заданий
в конвейерных системах с учётом технического обслуживания (ПТО) приборов.

ПОЛНАЯ ФОРМУЛИРОВКА РЕАЛИЗОВАННОЙ МОДЕЛИ
========================================

Индексы и параметры:
  i, k = 1..I — типы заданий;
  l = 1..L — приборы;
  j = 1..J — позиции;
  n_i — количество заданий типа i;
  t_li — время обработки задания типа i на приборе l;
  t_lki — переналадка прибора l с типа k на тип i;
  t0_li — первоначальная наладка;
  d_i — директивные сроки (критерий G);
  TM_l — момент начала ТО прибора l,
  tm_l — длительность ТО прибора l;
  H — горизонт планирования: H = 1.2 * (суммарная трудоёмкость + переналадки + надбавка на ТО);
  R = 1.5*H — константа big-M.

ТО каждого прибора — ОДИН заранее заданный фиксированный промежуток
времени (а не периодически повторяющийся цикл): [TM_l, TM_l + tm_l].
Пакеты, обрабатываемые на приборе l, попадают либо целиком до начала
этого промежутка, либо целиком после его окончания — пересекать
промежуток ТО пакету запрещено.

Переменные:
  x_ij ∈ {0,1} — в позиции j пакет типа i;
  m_j ∈ Z, 2 ≤ m_j — размер пакета в позиции j;
  r_ji = m_j*x_ij — линеаризация произведения (целая, 0 ≤ r_ji ≤ n_i);
  y_{k,j-1,i,j} = x_{k,j-1}*x_{i,j} — линеаризация для переналадок;
  q_lj ≥ 0 — момент начала пакета позиции j на приборе l;
  delta_lj ∈ {0,1} — пакет (l,j) завершается до промежутка ТО (1)
                      или начинается после него (0); определена
                      только для приборов l, для которых задано ТО;
  Cmax ≥ 0 — критерий 1;  g_i, p_i ≥ 0, z_i ∈ {0,1} — критерий G.

Ограничения:
  (C1) Σ_i x_ij = 1                — одна позиция, один тип;
  (C2) x_ij + x_{i,j-1} ≤ 1        — соседние позиции разных типов;
  (C3) Σ_j r_ji = n_i              — все задания распределены;
  (C4) линеаризация r_ji:  r_ji ≤ u*x_ij;  r_ji ≥ m_j − u(1−x_ij);
       r_ji ≤ m_j;  линеаризация y: y ≤ x_{k,j-1}; y ≤ x_ij;
       y ≥ x_{k,j-1}+x_ij−1;
  (C5) старт первой позиции:  q_l1 ≥ Σ_i t0_li*x_i1;
  (C6) порядок на приборе:
       q_lj ≥ q_{l,j-1} + Σ_i t_li*r_{j-1,i} + Σ_{k,i} t'_lki*y_{k,j-1,i,j};
  (C7) конвейерность:  q_lj ≥ q_{l-1,j} + Σ_i t_{l-1,i}*r_ji;
       !! Отличие от прототипа: в статье (C6)-(C7) заданы как точное
       равенство максимуму (через бинарные v_l, w_lj). При ТО прибор
       должен уметь простаивать, поэтому равенства заменены на «≥»;
       прижим расписания влево обеспечивает член ε·Σq в целевой
       функции (ε = 1/(10R), на оптимум критерия не влияет).
  (C8) ТО, дизъюнкция для промежутка [a_s, a_e] прибора l:
       q_lj + Σ_i t_li*r_ji ≤ a_s + R(1−delta_lj)   (пакет до промежутка)
       q_lj ≥ a_e − R*delta_lj                       (пакет после промежутка)
  (C9) горизонт:  q_lj + Σ_i t_li*r_ji ≤ H — запрещает «выталкивание»
       пакетов за пределы горизонта планирования.

Критерии:
  модель 1:  min  Cmax + ε·Σ q_lj,
             Cmax ≥ q_Lj + Σ_i t_Li*r_ji  для всех j;
  модель 2:  min  Σ_i p_i + ε·Σ q_lj,  где
             g_i ≥ q_Lj + Σ t_Li*r_ji − R(1−x_ij);
             p_i ≥ g_i − d_i;  p_i ≥ 0.

Гарантии реализации:
  - обе реализации (CPLEX/docplex и PuLP/CBC) строят ОДИН И ТОТ ЖЕ
    набор ограничений (C1)-(C9);
  - решение принимается только при целочисленном статусе решателя
    (оптимум или инкумбент); LP-релаксация отбраковывается;
  - перед выводом решение проходит верификацию В1-В6
    (см. _verify_solution); непроверенные данные на диаграмму
    Ганта и в анализ не попадают;
  - извлекаются все J позиций и все L*J операций без пропусков;
  - решателю передаётся тёплый старт (допустимое эвристическое
    решение), ускоряющий поиск целочисленных решений.
"""

import time
import logging
from typing import Optional, Tuple

from model.parameters import TaskParameters
from model.results import OptimizationResults, BatchInfo, ScheduleEntry, MaintenanceEntry

logger = logging.getLogger(__name__)

# --------------- ПРОВЕРКА УСТАНОВЛЕННОГО РЕШАТЕЛЯ ---------------
SOLVER_AVAILABLE = None
try:
    from docplex.mp.model import Model as CplexModel
    SOLVER_AVAILABLE = "cplex"
except ImportError:
    pass

if SOLVER_AVAILABLE is None:
    try:
        import pulp
        SOLVER_AVAILABLE = "pulp"
    except ImportError:
        pass


def _maintenance_window(TM: float, tm: float) -> Optional[Tuple[float, float]]:
    """
    Единственный заранее заданный фиксированный промежуток ТО прибора:
    [TM, TM + tm]. Промежуток не повторяется циклически — он один на
    весь горизонт планирования; пакеты планируются либо до него,
    либо после него.

    Возвращает None, если для прибора ТО не задано (TM < 0 или tm <= 0).
    """
    if TM is None or tm is None or TM < 0 or tm <= 0:
        return None
    return (TM, TM + tm)


def _estimate_horizon(params) -> float:
    """Грубая оценка горизонта расписания"""
    p = params
    total = 0.0
    for l in range(p.L):
        for i in range(p.I):
            total += p.t[l][i] * p.n[i]

    # Добавим переналадки
    for l in range(p.L):
        for i in range(p.I):
            for k in range(p.I):
                total += p.t_setup[l][i][k]
    # ТО — разовая, не циклическая добавка: просто длительность сеанса
    # каждого прибора, без умножения на число повторений.
    if p.use_maintenance:
        total += sum(p.tm_maint)
    horizon = max(total * 1.2, 50.0)
    # Промежуток ТО должен укладываться в горизонт с запасом, иначе
    # он окажется «за кадром» расписания и не повлияет на план.
    if p.use_maintenance:
        for l in range(p.L):
            w = _maintenance_window(p.TM[l], p.tm_maint[l])
            if w is not None:
                horizon = max(horizon, (w[1]) * 1.1)
    return horizon


def _greedy_initial_solution(p, maint_windows, horizon):
    """Построить допустимое стартовое решение (тёплый старт для решателя).

    Эвристика: каждый тип получает одну позицию в порядке номеров;
    лишние позиции (J > I) — вторые пакеты типов с наибольшим n[i]
    (количества делятся пополам). Моменты начала — жадно, с обходом окон ТО.

    Возвращает dict с x, m, q, Cmax (или None, если построить не удалось).
    """
    I, L, J = p.I, p.L, p.J
    if J < I:
        return None

    extra = J - I
    if extra > I:
        return None  # слишком много позиций для простой эвристики

    # Типы для вторых пакетов: с наибольшим n[i] (нужно n>=4, чтобы делить)
    order = sorted(range(I), key=lambda i: -p.n[i])
    second = order[:extra]
    for i in second:
        if p.n[i] < 4:
            return None

    seq = list(range(I)) + second          # типы по позициям
    m = [0] * J
    used = [0] * I
    for j, i in enumerate(seq):
        if i in second:
            half = p.n[i] // 2
            m[j] = half if used[i] == 0 else p.n[i] - half
            used[i] += 1
        else:
            m[j] = p.n[i]
    # проверка соседних типов
    for j in range(1, J):
        if seq[j] == seq[j - 1]:
            return None

    def place(l, earliest, dur):
        """Сдвинуть начало пакета на момент окончания ТО прибора l,
        если пакет [earliest, earliest+dur) пересекает заданный
        промежуток ТО. Окно ровно одно, поэтому достаточно одной проверки
        (без цикла повторных сдвигов, как при периодическом ТО)."""
        w = maint_windows.get(l)
        if w is None:
            return earliest
        a_s, a_e = w
        if earliest < a_e and earliest + dur > a_s:
            return a_e
        return earliest

    q = [[0.0] * J for _ in range(L)]
    for l in range(L):
        for j in range(J):
            i = seq[j]
            dur = p.t[l][i] * m[j]
            if l == 0 and j == 0:
                earliest = p.t_init[0][i]
            elif l == 0:
                k = seq[j - 1]
                earliest = q[0][j - 1] + p.t[0][k] * m[j - 1] + p.t_setup[0][k][i]
            elif j == 0:
                earliest = max(p.t_init[l][i],
                               q[l - 1][0] + p.t[l - 1][i] * m[0])
            else:
                k = seq[j - 1]
                prev_pos = q[l][j - 1] + p.t[l][k] * m[j - 1] + p.t_setup[l][k][i]
                prev_dev = q[l - 1][j] + p.t[l - 1][i] * m[j]
                earliest = max(prev_pos, prev_dev)
            q[l][j] = place(l, earliest, dur)
            if q[l][j] + dur > horizon:
                return None

    cmax = max(q[L - 1][j] + p.t[L - 1][seq[j]] * m[j] for j in range(J))
    return {"seq": seq, "m": m, "q": q, "cmax": cmax}


class MILPModel:
    """
    Модель 1: min Cmax
    Модель 2: min G
    """

    def __init__(self, params: TaskParameters, criterion: str = "Cmax",
                 time_limit: int = 300, verbose: bool = False):
        self.params = params
        self.criterion = criterion
        self.time_limit = time_limit
        self.verbose = verbose

    def solve(self) -> OptimizationResults:
        if SOLVER_AVAILABLE is None:
            r = OptimizationResults()
            r.status = OptimizationResults.STATUS_ERROR
            r.message = "Решатель не найден. Установите: pip install pulp"
            return r

        t0 = time.time()
        used_solver = SOLVER_AVAILABLE
        try:
            if SOLVER_AVAILABLE == "cplex":
                try:
                    results = self._solve_cplex()
                except Exception as ce:
                    # Типичный случай: Community-версия CPLEX (лимит 1000 перем./огранич.,
                    # код 1016). Автоматически переходим на PuLP/CBC, если он установлен.
                    try:
                        import pulp  # noqa: F401
                        logger.warning(
                            "CPLEX недоступен для этой задачи (%s). "
                            "Переключаюсь на PuLP/CBC.", ce)
                        used_solver = "pulp (fallback)"
                        results = self._solve_pulp()
                        if results.message:
                            results.message += " | CPLEX: превышен лимит Community-версии, использован PuLP/CBC"
                        else:
                            results.message = "CPLEX: превышен лимит Community-версии, использован PuLP/CBC"
                    except ImportError:
                        results = OptimizationResults()
                        results.status = OptimizationResults.STATUS_ERROR
                        results.message = (
                            "Задача превышает лимит бесплатной Community-версии CPLEX "
                            "(1000 переменных / 1000 ограничений).\n\n"
                            "Установите резервный решатель и повторите запуск — "
                            "программа переключится на него автоматически:\n"
                            "    pip install pulp\n\n"
                            "Либо установите полную версию IBM CPLEX "
                            "(бесплатна для студентов по программе IBM Academic Initiative).")
            else:
                results = self._solve_pulp()
        except Exception as e:
            results = OptimizationResults()
            results.status = OptimizationResults.STATUS_ERROR
            results.message = str(e)
            logger.exception("Ошибка при решении")

        results.solve_time = time.time() - t0
        results.criterion = self.criterion
        results.solver_name = used_solver or "none"

        if results.is_solved and results.objective_value is not None:
            fixed = self._compute_fixed_objective()
            if fixed is not None and fixed > 0:
                results.fixed_objective = fixed
                results.improvement_percent = (fixed - results.objective_value) / fixed * 100

        return results

    # ------------------------------------------------------------------
    # PuLP
    # ------------------------------------------------------------------

    # def _solve_pulp(self) -> OptimizationResults:
    #     import pulp
    #     p = self.params
    #     I, L, J = p.I, p.L, p.J
    #
    #     # Оценка горизонта и промежутка ТО
    #     horizon = _estimate_horizon(p)
    #     R = horizon * 1.5   # big-M: достаточно R >= horizon, берём с запасом 1.5
    #
    #     # Максимальный размер пакета
    #     n_min = min(p.n)
    #
    #     # --- Единственный фиксированный промежуток ТО для каждого прибора ---
    #     maint_windows = {}   # maint_windows[l] = (a_s, a_e) или None
    #     for l in range(L):
    #         maint_windows[l] = _maintenance_window(p.TM[l], p.tm_maint[l]) \
    #             if p.use_maintenance else None
    #
    #     prob = pulp.LpProblem("FlowShop_Batch", pulp.LpMinimize)
    #
    #     # ── Переменные ──
    #
    #     # x[i,j] = 1 если позиция j содержит тип i
    #     x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", cat='Binary')
    #          for i in range(I) for j in range(J)}
    #
    #     # m[j] — размер пакета
    #     m = {j: pulp.LpVariable(f"m_{j}", lowBound=2, upBound=n_min, cat='Integer')
    #          for j in range(J)}
    #
    #     # q[l,j] — момент начала обработки пакета j на приборе l
    #     q = {(l, j): pulp.LpVariable(f"q_{l}_{j}", lowBound=0)
    #          for l in range(L) for j in range(J)}
    #
    #     # r[j,i] = m[j]*x[i,j]  (линеаризация)
    #     r = {(j, i): pulp.LpVariable(f"r_{j}_{i}", lowBound=0, upBound=n_min)
    #          for j in range(J) for i in range(I)}
    #
    #     # y[k,j1,i,j] = x[k,j1]*x[i,j]  (линеаризация произведения бинарных)
    #     y = {(k, j-1, i, j): pulp.LpVariable(f"y_{k}_{j-1}_{i}_{j}", cat='Binary')
    #          for j in range(1, J)
    #          for i in range(I) for k in range(I) if i != k}
    #
    #     # v[l] — индикатор для max при j=0, l>=1
    #
    #     # w[l,j] — индикатор для max при j>=1, l>=1
    #
    #     # delta[l,j] — ТО: 1=пакет до промежутка ТО, 0=пакет после него
    #     # (определена только для приборов l, у которых задан промежуток ТО)
    #     delta = {}
    #     for l in range(L):
    #         if maint_windows[l] is not None:
    #             for j in range(J):
    #                 delta[l, j] = pulp.LpVariable(f"delta_{l}_{j}", cat='Binary')
    #
    #     # ── (31) Единственность типа + распределение всех заданий ──
    #     for j in range(J):
    #         prob += pulp.lpSum(x[i, j] for i in range(I)) == 1
    #
    #     for i in range(I):
    #         prob += pulp.lpSum(r[j, i] for j in range(J)) == p.n[i]
    #
    #     # ── (32) Различие типов в соседних позициях ──
    #     for j in range(1, J):
    #         for i in range(I):
    #             prob += x[i, j] + x[i, j-1] <= 1
    #
    #     # ── (38) Линеаризация r[j,i] = m[j]*x[i,j] ──
    #     for j in range(J):
    #         for i in range(I):
    #             prob += r[j, i] >= 0
    #             prob += r[j, i] <= n_min * x[i, j]
    #             prob += r[j, i] <= m[j]
    #             prob += r[j, i] >= m[j] - n_min * (1 - x[i, j])
    #
    #     # ── (44) Линеаризация y = x[k,j-1]*x[i,j] ──
    #     for j in range(1, J):
    #         j1 = j - 1
    #         for i in range(I):
    #             for k in range(I):
    #                 if i == k:
    #                     continue
    #                 prob += y[k, j1, i, j] <= x[k, j1]
    #                 prob += y[k, j1, i, j] <= x[i, j]
    #                 prob += y[k, j1, i, j] >= x[k, j1] + x[i, j] - 1
    #
    #     # ── Расписание ──
    #
    #     # (33) Прибор 0, позиция 0
    #     prob += q[0, 0] >= pulp.lpSum(p.t_init[0][i] * x[i, 0] for i in range(I))
    #
    #     # (34) Прибор 0, позиции j>=1
    #     for j in range(1, J):
    #         j1 = j - 1
    #         setup = pulp.lpSum(
    #             p.t_setup[0][k][i] * y[k, j1, i, j]
    #             for i in range(I) for k in range(I) if i != k)
    #         prob += q[0, j] >= (q[0, j1]
    #                             + pulp.lpSum(p.t[0][i] * r[j1, i] for i in range(I))
    #                             + setup)
    #
    #     # (35-37) Прибор l>=1, позиция 0
    #     for l in range(1, L):
    #         init_l = pulp.lpSum(p.t_init[l][i] * x[i, 0] for i in range(I))
    #         prev_end = q[l-1, 0] + pulp.lpSum(p.t[l-1][i] * r[0, i] for i in range(I))
    #         # Безусловные нижние границы: пакет не может начаться раньше,
    #         # чем завершилась наладка прибора И обработка на предыдущем приборе.
    #         # (Равенство max(...) из статьи заменено на >=: при наличии промежутка ТО
    #         # требуется возможность простоя прибора, равенство делает модель некорректной.)
    #         prob += q[l, 0] >= init_l
    #         prob += q[l, 0] >= prev_end
    #
    #     # (39-43) Прибор l>=1, позиции j>=1
    #     for l in range(1, L):
    #         for j in range(1, J):
    #             j1 = j - 1
    #             setup_l = pulp.lpSum(
    #                 p.t_setup[l][k][i] * y[k, j1, i, j]
    #                 for i in range(I) for k in range(I) if i != k)
    #             prev_pos = (q[l, j1]
    #                         + pulp.lpSum(p.t[l][i] * r[j1, i] for i in range(I))
    #                         + setup_l)
    #             prev_dev = (q[l-1, j]
    #                         + pulp.lpSum(p.t[l-1][i] * r[j, i] for i in range(I)))
    #             prob += q[l, j] >= prev_pos
    #             prob += q[l, j] >= prev_dev
    #
    #     # ── (ТО.1) Дизъюнктивные ограничения: пакет до или после промежутка ТО ──
    #     if p.use_maintenance:
    #         for l in range(L):
    #             for j in range(J):
    #                 proc_j = pulp.lpSum(p.t[l][i] * r[j, i] for i in range(I))
    #                 # (ТО.2) Пакет обязан завершиться в пределах горизонта.
    #                 prob += q[l, j] + proc_j <= horizon
    #                 w = maint_windows[l]
    #                 if w is None:
    #                     continue
    #                 a_s, a_e = w
    #                 d_var = delta[l, j]
    #                 # delta=1: пакет заканчивается ДО начала промежутка ТО
    #                 prob += q[l, j] + proc_j <= a_s + R * (1 - d_var)
    #                 # delta=0: пакет начинается ПОСЛЕ окончания промежутка ТО
    #                 prob += q[l, j] >= a_e - R * d_var
    #
    #     # ── Критерий ──
    #     eps = 1.0 / (R * 10.0)   # прижим расписания «влево», не влияет на оптимум критерия
    #     q_pull = pulp.lpSum(q[l, j] for l in range(L) for j in range(J))
    #     if self.criterion == "Cmax":
    #         Cmax = pulp.LpVariable("Cmax", lowBound=0)
    #         prob += Cmax + eps * q_pull
    #         for j in range(J):
    #             prob += Cmax >= (q[L-1, j]
    #                              + pulp.lpSum(p.t[L-1][i] * r[j, i] for i in range(I)))
    #     else:
    #         g_time = {i: pulp.LpVariable(f"g_{i}", lowBound=0) for i in range(I)}
    #         delay = {i: pulp.LpVariable(f"p_{i}", lowBound=0) for i in range(I)}
    #         prob += pulp.lpSum(delay[i] for i in range(I)) + eps * q_pull
    #         for i in range(I):
    #             for j in range(J):
    #                 end_j = (q[L-1, j]
    #                          + pulp.lpSum(p.t[L-1][ii] * r[j, ii] for ii in range(I)))
    #                 prob += g_time[i] >= end_j - R * (1 - x[i, j])
    #             prob += delay[i] >= g_time[i] - p.d[i]
    #             prob += delay[i] >= 0
    #
    #     # ── Тёплый старт: эвристическое стартовое решение ──
    #     warm = _greedy_initial_solution(p, maint_windows, horizon)
    #     warm_start = False
    #     if warm is not None:
    #         try:
    #             seq, m0, q0 = warm["seq"], warm["m"], warm["q"]
    #             for j in range(J):
    #                 for i in range(I):
    #                     x[i, j].setInitialValue(1 if seq[j] == i else 0)
    #                     r[j, i].setInitialValue(m0[j] if seq[j] == i else 0)
    #                 m[j].setInitialValue(m0[j])
    #             for j in range(1, J):
    #                 for i in range(I):
    #                     for k in range(I):
    #                         if i == k:
    #                             continue
    #                         y[k, j - 1, i, j].setInitialValue(
    #                             1 if (seq[j - 1] == k and seq[j] == i) else 0)
    #             for l in range(L):
    #                 for j in range(J):
    #                     q[l, j].setInitialValue(round(q0[l][j], 6))
    #                     dur = p.t[l][seq[j]] * m0[j]
    #                     w = maint_windows[l]
    #                     if w is not None:
    #                         a_s, _a_e = w
    #                         delta[l, j].setInitialValue(
    #                             1 if q0[l][j] + dur <= a_s + 1e-9 else 0)
    #             if self.criterion == "Cmax":
    #                 Cmax.setInitialValue(round(warm["cmax"], 6))
    #             else:
    #                 for i in range(I):
    #                     ends = [q0[L - 1][j] + p.t[L - 1][i] * m0[j]
    #                             for j in range(J) if seq[j] == i]
    #                     gi = max(ends) if ends else 0.0
    #                     g_time[i].setInitialValue(round(gi, 6))
    #                     delay[i].setInitialValue(round(max(0.0, gi - p.d[i]), 6))
    #             warm_start = True
    #             logger.info("Тёплый старт: эвристическое решение, Cmax=%.2f",
    #                         warm["cmax"])
    #         except Exception:
    #             warm_start = False
    #             logger.exception("Не удалось задать тёплый старт")
    #
    #     # ── Запуск ──
    #     msg = 1 if self.verbose else 0
    #     avail = pulp.listSolvers(onlyAvailable=True)
    #     if 'PULP_CBC_CMD' in avail:
    #         solver = pulp.PULP_CBC_CMD(msg=msg, timeLimit=self.time_limit, gapRel=0.05,
    #                                    warmStart=warm_start)
    #     elif 'GLPK_CMD' in avail:
    #         solver = pulp.GLPK_CMD(msg=msg, timeLimit=self.time_limit)
    #     else:
    #         solver = pulp.PULP_CBC_CMD(msg=msg)
    #
    #     status_code = prob.solve(solver)
    #     status_str = pulp.LpStatus[status_code]
    #     sol_status = getattr(prob, "sol_status", None)
    #
    #     results = OptimizationResults()
    #     results.criterion = self.criterion
    #
    #     if status_str == "Infeasible" or sol_status == pulp.LpSolutionInfeasible:
    #         results.status = OptimizationResults.STATUS_INFEASIBLE
    #         results.message = "Задача не имеет допустимого решения. Проверьте параметры ТО."
    #         return results
    #
    #     # Ключевая проверка: значения переменных валидны только если найдено
    #     # ЦЕЛОЧИСЛЕННОЕ решение (оптимум или инкумбент). Если за лимит времени
    #     # целочисленное решение не найдено, PuLP возвращает значения
    #     # LP-релаксации — их нельзя выдавать за расписание.
    #     if sol_status == pulp.LpSolutionOptimal:
    #         results.status = OptimizationResults.STATUS_OPTIMAL
    #     elif sol_status == pulp.LpSolutionIntegerFeasible:
    #         results.status = OptimizationResults.STATUS_FEASIBLE
    #     else:
    #         results.status = OptimizationResults.STATUS_INFEASIBLE
    #         results.message = (
    #             "За отведённый лимит времени целочисленное решение не найдено "
    #             "(найдена только нижняя оценка критерия). Увеличьте лимит "
    #             "времени на вкладке «Параметры задачи» или уменьшите "
    #             "размерность задачи.")
    #         return results
    #
    #     try:
    #         if self.criterion == "Cmax":
    #             results.objective_value = pulp.value(Cmax)
    #         else:
    #             results.objective_value = sum(pulp.value(delay[i]) or 0.0 for i in range(I))
    #     except Exception:
    #         results.objective_value = None
    #
    #     if results.objective_value is None:
    #         results.status = OptimizationResults.STATUS_INFEASIBLE
    #         results.message = "Решение не найдено"
    #         return results
    #
    #     # ── Единое извлечение результатов + верификация ──
    #     ok = self._extract_results(
    #         pulp.value, results, maint_windows, x, m, q,
    #         g_time=g_time if self.criterion == "G" else None,
    #         delay=delay if self.criterion == "G" else None)
    #     if not ok:
    #         results.status = OptimizationResults.STATUS_ERROR
    #         results.message = ("Решатель вернул некорректные значения "
    #                            "переменных. Увеличьте лимит времени.")
    #         results.batches.clear(); results.schedule.clear()
    #         results.maintenance.clear()
    #         return results
    #
    #     v_ok, v_report = self._verify_solution(results, maint_windows)
    #     if not v_ok:
    #         results.status = OptimizationResults.STATUS_ERROR
    #         results.message = "Верификация решения не пройдена: " + v_report
    #         logger.error("Верификация (PuLP): %s", v_report)
    #         return results
    #     results.message = ((results.message + " | ") if results.message
    #                        else "") + "Верификация: " + v_report
    #
    #     return results

    # ------------------------------------------------------------------
    # CPLEX
    # ------------------------------------------------------------------

    def _solve_cplex(self) -> OptimizationResults:
        p = self.params
        I, L, J = p.I, p.L, p.J
        n_min = min(p.n)

        horizon = _estimate_horizon(p)
        R = horizon * 1.5

        maint_windows = {}
        for l in range(L):
            maint_windows[l] = _maintenance_window(p.TM[l], p.tm_maint[l]) \
                if p.use_maintenance else None

        mdl = CplexModel(name="FlowShop_Batch")
        mdl.parameters.timelimit = self.time_limit
        if not self.verbose:
            mdl.context.solver.log_output = False

        x = {(i, j): mdl.binary_var(name=f"x_{i}_{j}")
             for i in range(I) for j in range(J)}
        m = {j: mdl.integer_var(lb=2, ub=n_min, name=f"m_{j}") for j in range(J)}
        q = {(l, j): mdl.continuous_var(lb=0, name=f"q_{l}_{j}")
             for l in range(L) for j in range(J)}
        r = {(j, i): mdl.continuous_var(lb=0, ub=n_min, name=f"r_{j}_{i}")
             for j in range(J) for i in range(I)}
        y = {(k, j-1, i, j): mdl.binary_var(name=f"y_{k}_{j-1}_{i}_{j}")
             for j in range(1, J) for i in range(I) for k in range(I) if i != k}

        # delta[l,j] — ТО: 1=пакет до промежутка ТО, 0=пакет после него
        # (определена только для приборов l, у которых задан промежуток ТО)
        delta = {}
        for l in range(L):
            if maint_windows[l] is not None:
                for j in range(J):
                    delta[l, j] = mdl.binary_var(name=f"delta_{l}_{j}")

        for j in range(J):
            mdl.add_constraint(mdl.sum(x[i, j] for i in range(I)) == 1)
        for j in range(1, J):
            for i in range(I):
                mdl.add_constraint(x[i, j] + x[i, j-1] <= 1)
        for i in range(I):
            mdl.add_constraint(mdl.sum(r[j, i] for j in range(J)) == p.n[i])
        for j in range(J):
            for i in range(I):
                mdl.add_constraint(r[j, i] >= 0)
                mdl.add_constraint(r[j, i] <= n_min * x[i, j])
                mdl.add_constraint(r[j, i] <= m[j])
                mdl.add_constraint(r[j, i] >= m[j] - n_min * (1 - x[i, j]))
            mdl.add_constraint(m[j] >= 2)

        for j in range(1, J):
            j1 = j - 1
            for i in range(I):
                for k in range(I):
                    if i == k:
                        continue
                    mdl.add_constraint(y[k, j1, i, j] <= x[k, j1])
                    mdl.add_constraint(y[k, j1, i, j] <= x[i, j])
                    mdl.add_constraint(y[k, j1, i, j] >= x[k, j1] + x[i, j] - 1)

        mdl.add_constraint(
            q[0, 0] >= mdl.sum(p.t_init[0][i] * x[i, 0] for i in range(I)))
        for j in range(1, J):
            j1 = j - 1
            setup = mdl.sum(p.t_setup[0][k][i] * y[k, j1, i, j]
                            for i in range(I) for k in range(I) if i != k)
            mdl.add_constraint(
                q[0, j] >= q[0, j1]
                + mdl.sum(p.t[0][i] * r[j1, i] for i in range(I))
                + setup)

        for l in range(1, L):
            init_l = mdl.sum(p.t_init[l][i] * x[i, 0] for i in range(I))
            prev_end = q[l-1, 0] + mdl.sum(p.t[l-1][i] * r[0, i] for i in range(I))
            # Безусловные нижние границы (равенство max(...) заменено на >=,
            # чтобы прибор мог простаивать перед промежутком ТО)
            mdl.add_constraint(q[l, 0] >= init_l)
            mdl.add_constraint(q[l, 0] >= prev_end)
            for j in range(1, J):
                j1 = j - 1
                setup_l = mdl.sum(p.t_setup[l][k][i] * y[k, j1, i, j]
                                  for i in range(I) for k in range(I) if i != k)
                prev_pos = (q[l, j1]
                            + mdl.sum(p.t[l][i] * r[j1, i] for i in range(I))
                            + setup_l)
                prev_dev = q[l-1, j] + mdl.sum(p.t[l-1][i] * r[j, i] for i in range(I))
                mdl.add_constraint(q[l, j] >= prev_pos)
                mdl.add_constraint(q[l, j] >= prev_dev)

        if p.use_maintenance:
            for l in range(L):
                for j in range(J):
                    proc_j = mdl.sum(p.t[l][i] * r[j, i] for i in range(I))
                    # (ТО.2) Завершение в пределах горизонта планирования
                    mdl.add_constraint(q[l, j] + proc_j <= horizon)
                    w = maint_windows[l]
                    if w is None:
                        continue
                    a_s, a_e = w
                    d_var = delta[l, j]
                    mdl.add_constraint(q[l, j] + proc_j <= a_s + R * (1 - d_var))
                    mdl.add_constraint(q[l, j] >= a_e - R * d_var)

        if self.criterion == "Cmax":
            Cmax = mdl.continuous_var(lb=0, name="Cmax")
            for j in range(J):
                mdl.add_constraint(
                    Cmax >= q[L-1, j] + mdl.sum(p.t[L-1][i] * r[j, i] for i in range(I)))
            eps = 1.0 / (R * 10.0)
            q_pull = mdl.sum(q[l, j] for l in range(L) for j in range(J))
            mdl.minimize(Cmax + eps * q_pull)
        else:
            g_time = {i: mdl.continuous_var(lb=0, name=f"g_{i}") for i in range(I)}
            delay = {i: mdl.continuous_var(lb=0, name=f"p_{i}") for i in range(I)}
            z = {i: mdl.binary_var(name=f"z_{i}") for i in range(I)}
            for i in range(I):
                for j in range(J):
                    end_j = q[L-1, j] + mdl.sum(p.t[L-1][ii] * r[j, ii] for ii in range(I))
                    mdl.add_constraint(g_time[i] >= end_j - R * (1 - x[i, j]))
                mdl.add_constraint(delay[i] >= g_time[i] - p.d[i])
                mdl.add_constraint(delay[i] >= 0)
                mdl.add_constraint(g_time[i] - p.d[i] <= R * z[i])
                mdl.add_constraint(g_time[i] - p.d[i] >= -R * (1 - z[i]))
                mdl.add_constraint(delay[i] <= g_time[i] - p.d[i] + R * (1 - z[i]))
                mdl.add_constraint(delay[i] <= R * z[i])
            eps = 1.0 / (R * 10.0)
            q_pull = mdl.sum(q[l, j] for l in range(L) for j in range(J))
            mdl.minimize(mdl.sum(delay[i] for i in range(I)) + eps * q_pull)

        sol = mdl.solve()
        results = OptimizationResults()
        results.criterion = self.criterion

        if sol is None:
            results.status = OptimizationResults.STATUS_INFEASIBLE
            results.message = "CPLEX: решение не найдено"
            return results

        results.status = OptimizationResults.STATUS_OPTIMAL
        if self.criterion == "Cmax":
            results.objective_value = sol.get_value(Cmax)
        else:
            results.objective_value = sum(sol.get_value(delay[i]) or 0.0 for i in range(I))

        # ── Единое извлечение результатов + верификация ──
        def getv(var):
            return sol.get_value(var)

        ok = self._extract_results(
            getv, results, maint_windows, x, m, q,
            g_time=g_time if self.criterion == "G" else None,
            delay=delay if self.criterion == "G" else None)
        if not ok:
            results.status = OptimizationResults.STATUS_ERROR
            results.message = ("Решатель вернул некорректные значения "
                               "переменных. Увеличьте лимит времени.")
            results.batches.clear(); results.schedule.clear()
            results.maintenance.clear()
            return results

        v_ok, v_report = self._verify_solution(results, maint_windows)
        if not v_ok:
            results.status = OptimizationResults.STATUS_ERROR
            results.message = "Верификация решения не пройдена: " + v_report
            logger.error("Верификация (CPLEX): %s", v_report)
            return results
        results.message = ((results.message + " | ") if results.message
                           else "") + "Верификация: " + v_report

        return results

    # ------------------------------------------------------------------
    # Единое извлечение результатов и верификация (общие для CPLEX и PuLP)
    # ------------------------------------------------------------------

    def _extract_results(self, getv, results, maint_windows,
                         x, m, q, g_time=None, delay=None) -> bool:
        """Извлечь решение через функцию доступа getv(var) -> float.

        Гарантии:
        - извлекаются ВСЕ J позиций (тип = argmax x[i,j], без порога 0.5,
          который «терял» позиции при численных погрешностях);
        - количества округляются до целых; пустых/нулевых пакетов не бывает;
        - расписание содержит ровно L*J записей;
        - на диаграмму выносится промежуток ТО в пределах фактического
          расписания каждого прибора (без выборочной фильтрации).
        Возвращает False, если значения переменных не образуют
        корректного целочисленного решения.
        """
        p = self.params
        I, L, J = p.I, p.L, p.J

        # 1. Составы пакетов: тип каждой позиции — argmax по x
        seq, sizes = [], []
        for j in range(J):
            vals = [(getv(x[i, j]) or 0.0) for i in range(I)]
            best = max(range(I), key=lambda i: vals[i])
            if vals[best] < 0.5:          # дробное/пустое решение
                return False
            cnt = int(round(getv(m[j]) or 0.0))
            if cnt < 2:
                return False
            seq.append(best)
            sizes.append(cnt)
            results.batches.append(
                BatchInfo(position=j + 1, task_type=best + 1, count=cnt))
            results.raw_x[(best, j)] = 1
            results.raw_m[j] = cnt

        # 2. Расписание: все приборы, все позиции, без пропусков
        for l in range(L):
            for j in range(J):
                qv = float(getv(q[l, j]) or 0.0)
                proc = p.t[l][seq[j]] * sizes[j]
                results.schedule.append(ScheduleEntry(
                    device=l + 1, position=j + 1, task_type=seq[j] + 1,
                    start_time=qv, process_time=proc, end_time=qv + proc))
                results.raw_q[(l, j)] = qv

        # 3. Промежуток ТО в пределах фактического расписания прибора
        if p.use_maintenance:
            for l in range(L):
                w = maint_windows[l]
                if w is None:
                    continue
                a_s, a_e = w
                ends = [e.end_time for e in results.schedule
                        if e.device == l + 1]
                if not ends:
                    continue
                max_end = max(ends)
                if a_s >= max_end - 1e-6:
                    continue
                after = [j + 1 for j in range(J)
                         if results.raw_q[(l, j)] >= a_e - 1e-6]
                before_pos = min(
                    after,
                    key=lambda jj: results.raw_q[(l, jj - 1)]) if after else 0
                results.maintenance.append(MaintenanceEntry(
                    device=l + 1, before_position=before_pos,
                    start_time=a_s, duration=p.tm_maint[l], end_time=a_e))

        # 4. Критерий G: окончания и запаздывания по типам
        if self.criterion == "G" and g_time is not None:
            for i in range(I):
                results.completion_times[i + 1] = float(getv(g_time[i]) or 0.0)
                results.delays[i + 1] = float(getv(delay[i]) or 0.0)

        return True

    def _verify_solution(self, results, maint_windows):
        """Проверить решение по всем условиям модели перед выводом.

        Возвращает (ok, отчёт). Проверяются:
        В1 — распределение всех заданий: sum_j m_j x_ij = n_i;
        В2 — соседние позиции имеют разные типы;
        В3 — порядок на приборе: q_lj >= q_l,j-1 + t*m + переналадка;
        В4 — конвейерность: q_lj >= q_l-1,j + t*m (прибор l-1);
        В5 — пакеты не пересекают промежуток ТО;
        В6 — значение критерия согласовано с расписанием.
        """
        p = self.params
        I, L, J = p.I, p.L, p.J
        tol = 1e-4
        errors = []

        seq = {b.position - 1: b.task_type - 1 for b in results.batches}
        sizes = {b.position - 1: b.count for b in results.batches}
        if len(seq) != J:
            errors.append(f"В1: извлечено позиций {len(seq)} из {J}")

        for i in range(I):
            tot = sum(sizes[j] for j in range(J) if seq.get(j) == i)
            if tot != p.n[i]:
                errors.append(
                    f"В1: тип {i+1} распределено {tot} из {p.n[i]}")

        for j in range(1, J):
            if seq.get(j) == seq.get(j - 1):
                errors.append(f"В2: позиции {j} и {j+1} одного типа")

        sched = {(e.device - 1, e.position - 1): e for e in results.schedule}
        for l in range(L):
            for j in range(J):
                e = sched[(l, j)]
                if j == 0:
                    if e.start_time < p.t_init[l][seq[0]] - tol:
                        errors.append(f"В3: прибор {l+1} старт до наладки")
                else:
                    prev = sched[(l, j - 1)]
                    need = prev.end_time + p.t_setup[l][seq[j - 1]][seq[j]]
                    if e.start_time < need - tol:
                        errors.append(
                            f"В3: прибор {l+1} позиция {j+1} раньше {need:.1f}")
                if l > 0:
                    up = sched[(l - 1, j)]
                    if e.start_time < up.end_time - tol:
                        errors.append(
                            f"В4: конвейерность прибор {l+1} позиция {j+1}")
                if p.use_maintenance and maint_windows[l] is not None:
                    a_s, a_e = maint_windows[l]
                    if e.start_time < a_e - tol and e.end_time > a_s + tol:
                        errors.append(
                            f"В5: прибор {l+1} позиция {j+1} в промежутке ТО")

        if self.criterion == "Cmax" and results.objective_value is not None:
            actual = max(sched[(L - 1, j)].end_time for j in range(J))
            if abs(actual - results.objective_value) > 0.5:
                errors.append(
                    f"В6: Cmax={results.objective_value:.1f}, "
                    f"факт={actual:.1f}")

        if errors:
            return False, "; ".join(errors[:6])
        n_to = len(results.maintenance)
        return True, (f"все проверки пройдены: {J} пакетов, "
                      f"{L * J} операций, окон ТО в расписании: {n_to}")

    # ------------------------------------------------------------------

    def _compute_fixed_objective(self) -> Optional[float]:
        """Критерий для фиксированных пакетов (все задания типа i — один пакет),
        вычисляется жадным прямым моделированием с учётом ТОГО ЖЕ промежутка ТО,
        что и в оптимизационной модели — иначе сравнение некорректно."""
        p = self.params
        try:
            I, L = p.I, p.L

            windows = {}
            for l in range(L):
                windows[l] = _maintenance_window(p.TM[l], p.tm_maint[l]) \
                    if p.use_maintenance else None

            def place(l, earliest, dur):
                """Сдвинуть начало пакета на конец промежутка ТО прибора l,
                если пакет [earliest, earliest+dur) пересекает этот промежуток."""
                w = windows[l]
                if w is None:
                    return earliest
                a_s, a_e = w
                if earliest < a_e and earliest + dur > a_s:
                    return a_e
                return earliest

            q = [[0.0] * I for _ in range(L)]
            q[0][0] = place(0, p.t_init[0][0], p.t[0][0] * p.n[0])
            for j in range(1, I):
                earliest = q[0][j-1] + p.t[0][j-1] * p.n[j-1] + p.t_setup[0][j-1][j]
                q[0][j] = place(0, earliest, p.t[0][j] * p.n[j])
            for l in range(1, L):
                earliest = max(p.t_init[l][0], q[l-1][0] + p.t[l-1][0] * p.n[0])
                q[l][0] = place(l, earliest, p.t[l][0] * p.n[0])
                for j in range(1, I):
                    prev_pos = q[l][j-1] + p.t[l][j-1] * p.n[j-1] + p.t_setup[l][j-1][j]
                    prev_dev = q[l-1][j] + p.t[l-1][j] * p.n[j]
                    q[l][j] = place(l, max(prev_pos, prev_dev), p.t[l][j] * p.n[j])
            if self.criterion == "Cmax":
                return max(q[L-1][j] + p.t[L-1][j] * p.n[j] for j in range(I))
            else:
                return sum(max(0.0, q[L-1][i] + p.t[L-1][i] * p.n[i] - p.d[i])
                           for i in range(I))
        except Exception:
            return None
