"""
MILP-модель оптимизации расписания выполнения пакетов заданий
в конвейерных системах с учётом технического обслуживания.

Основана на статье:
Кротов К.В. Модели смешанного целочисленного линейного программирования
оптимизации включения заданий в пакеты и порядков проведения операций
с ними в конвейерных системах. ИУС, 2024, № 6, с. 46–57.

Расширение: добавлен блок учёта технического обслуживания (ТО) приборов.
"""

import time
import logging
from typing import Optional

from model.parameters import TaskParameters
from model.results import OptimizationResults, BatchInfo, ScheduleEntry, MaintenanceEntry

logger = logging.getLogger(__name__)

# Попытка импорта решателей
SOLVER_AVAILABLE = None

try:
    from docplex.mp.model import Model as CplexModel
    SOLVER_AVAILABLE = "cplex"
    logger.info("Используется IBM CPLEX через docplex")
except ImportError:
    pass

if SOLVER_AVAILABLE is None:
    try:
        import pulp
        SOLVER_AVAILABLE = "pulp"
        logger.info("Используется PuLP (CBC solver)")
    except ImportError:
        pass

if SOLVER_AVAILABLE is None:
    logger.warning("Ни один решатель не найден! Установите docplex или pulp.")


class MILPModel:
    """
    Строит и решает MILP-модели для двух критериев:
    - Модель 1: минимизация Cmax (время окончания всех операций)
    - Модель 2: минимизация G (суммарное запаздывание)
    С опциональным учётом технического обслуживания приборов.
    """

    def __init__(self, params: TaskParameters, criterion: str = "Cmax",
                 time_limit: int = 300, verbose: bool = False):
        """
        params    - параметры задачи
        criterion - "Cmax" или "G"
        time_limit - максимальное время решения (секунды)
        verbose   - выводить лог решателя
        """
        self.params = params
        self.criterion = criterion
        self.time_limit = time_limit
        self.verbose = verbose
        self._results = None

    def solve(self) -> OptimizationResults:
        """Построить модель и запустить решатель"""
        if SOLVER_AVAILABLE is None:
            r = OptimizationResults()
            r.status = OptimizationResults.STATUS_ERROR
            r.message = ("Решатель не найден.\n"
                         "Установите: pip install pulp\n"
                         "или: pip install docplex (требует IBM CPLEX)")
            return r

        t_start = time.time()
        try:
            if SOLVER_AVAILABLE == "cplex":
                results = self._solve_cplex()
            else:
                results = self._solve_pulp()
        except Exception as e:
            results = OptimizationResults()
            results.status = OptimizationResults.STATUS_ERROR
            results.message = str(e)
            logger.exception("Ошибка при решении модели")

        results.solve_time = time.time() - t_start
        results.criterion = self.criterion
        results.solver_name = SOLVER_AVAILABLE or "none"

        # Вычислить улучшение относительно фиксированных пакетов
        if results.is_solved and results.objective_value is not None:
            fixed = self._compute_fixed_objective()
            if fixed is not None and fixed > 0:
                results.fixed_objective = fixed
                results.improvement_percent = (
                    (fixed - results.objective_value) / fixed * 100
                )

        self._results = results
        return results

    # -----------------------------------------------------------------------
    # PuLP реализация (основная, не требует лицензии)
    # -----------------------------------------------------------------------

    def _solve_pulp(self) -> OptimizationResults:
        import pulp

        p = self.params
        I, L, J = p.I, p.L, p.J
        R = 10000  # большое число

        # Максимальное число заданий в пакете
        n_min = min(p.n)
        u_max = max(n_min, 2)  # upBound для m[j]: не менее 2

        prob = pulp.LpProblem("FlowShop_Batch_Scheduling", pulp.LpMinimize)

        # --- Переменные ---

        # x[i][j] = 1 если задания i-го типа в j-й позиции
        x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", cat='Binary')
             for i in range(I) for j in range(J)}

        # m[j] - количество заданий в j-й позиции
        m = {j: pulp.LpVariable(f"m_{j}", lowBound=2, upBound=n_min,
                                cat='Integer')
             for j in range(J)}

        # q[l][j] - момент начала обработки пакета j на приборе l
        q = {(l, j): pulp.LpVariable(f"q_{l}_{j}", lowBound=0)
             for l in range(L) for j in range(J)}

        # Линеаризация m[j]*x[i][j] => r[j][i]
        r = {(j, i): pulp.LpVariable(f"r_{j}_{i}", lowBound=0, upBound=n_min)
             for j in range(J) for i in range(I)}

        # Для линеаризации m[1]*x[i][1] на первом приборе (r1)
        r1 = {i: pulp.LpVariable(f"r1_{i}", lowBound=0, upBound=n_min)
              for i in range(I)}

        # y[k][j-1][i][j] = x[k][j-1] * x[i][j]  (линеаризация произведений)
        y = {(k, j1, i, j): pulp.LpVariable(f"y_{k}_{j1}_{i}_{j}", cat='Binary')
             for j in range(1, J) for j1 in [j-1]
             for i in range(I) for k in range(I) if i != k}

        # Индикаторы для линеаризации max (вместо max в ограничениях)
        v = {l: pulp.LpVariable(f"v_{l}", cat='Binary')
             for l in range(1, L)}

        w = {(l, j): pulp.LpVariable(f"w_{l}_{j}", cat='Binary')
             for l in range(1, L) for j in range(1, J)}

        # ТО переменные
        if p.use_maintenance:
            # maint[l][j] = 1 если ТО перед позицией j на приборе l
            maint = {(l, j): pulp.LpVariable(f"maint_{l}_{j}", cat='Binary')
                     for l in range(L) for j in range(J)}
            # q_maint[l][j] - момент начала ТО
            q_maint = {(l, j): pulp.LpVariable(f"qm_{l}_{j}", lowBound=0)
                       for l in range(L) for j in range(J)}
            # Накопленное время работы прибора l к позиции j
            work_acc = {(l, j): pulp.LpVariable(f"wacc_{l}_{j}", lowBound=0)
                        for l in range(L) for j in range(J)}

        # --- Критерий ---
        if self.criterion == "Cmax":
            Cmax = pulp.LpVariable("Cmax", lowBound=0)
            prob += Cmax
        else:
            # Для критерия G
            g_time = {i: pulp.LpVariable(f"g_{i}", lowBound=0) for i in range(I)}
            delay = {i: pulp.LpVariable(f"p_{i}", lowBound=0) for i in range(I)}
            prob += pulp.lpSum(delay[i] for i in range(I))

        # --- Ограничения ---

        # (6) Каждая позиция j содержит задания ровно одного типа
        for j in range(J):
            prob += pulp.lpSum(x[i, j] for i in range(I)) == 1

        # (7) Соседние позиции — разные типы
        for j in range(1, J):
            for i in range(I):
                prob += x[i, j] + x[i, j-1] <= 1

        # (8) Все задания распределены по пакетам
        for i in range(I):
            prob += pulp.lpSum(r[j, i] for j in range(J)) == p.n[i]

        # Линеаризация r[j][i] = m[j] * x[i][j]
        for j in range(J):
            for i in range(I):
                prob += r[j, i] >= 0
                prob += r[j, i] <= n_min * x[i, j]
                prob += r[j, i] <= m[j]
                prob += r[j, i] >= m[j] - n_min * (1 - x[i, j])

        # Линеаризация r1[i] = m[0] * x[i][0]  (для первой позиции, первый прибор)
        for i in range(I):
            prob += r1[i] >= 0
            prob += r1[i] <= n_min * x[i, 0]
            prob += r1[i] <= m[0]
            prob += r1[i] >= m[0] - n_min * (1 - x[i, 0])

        # Минимальный размер пакета
        for j in range(J):
            prob += m[j] >= 2

        # Линеаризация y[k,j-1,i,j] = x[k,j-1]*x[i,j]
        for j in range(1, J):
            j1 = j - 1
            for i in range(I):
                for k in range(I):
                    if i == k:
                        continue
                    prob += y[k, j1, i, j] <= x[k, j1]
                    prob += y[k, j1, i, j] <= x[i, j]
                    prob += y[k, j1, i, j] >= x[k, j1] + x[i, j] - 1
                    prob += y[k, j1, i, j] >= 0

        # --- Расписание ---

        # (1) Первый прибор, первая позиция
        for i in range(I):
            if p.use_maintenance:
                # q[0][0] = t_init[0][i]*x[i,0] + tm_maint[0]*maint[0,0]
                pass  # обрабатывается ниже
            prob += q[0, 0] >= pulp.lpSum(p.t_init[0][i] * x[i, 0] for i in range(I))

        # (2) Первый прибор, позиции j >= 1
        for j in range(1, J):
            j1 = j - 1
            setup_expr = pulp.lpSum(
                p.t_setup[0][k][i] * y[k, j1, i, j]
                for i in range(I) for k in range(I) if i != k
            )
            prob += q[0, j] >= (q[0, j1]
                                + pulp.lpSum(p.t[0][i] * r[j1, i] for i in range(I))
                                + setup_expr)

        # (3) Прибор l >= 1, первая позиция — max(переналадка на l, окончание на l-1)
        for l in range(1, L):
            init_l = pulp.lpSum(p.t_init[l][i] * x[i, 0] for i in range(I))
            prev_end = q[l-1, 0] + pulp.lpSum(p.t[l-1][i] * r[0, i] for i in range(I))
            # Линеаризация max(init_l, prev_end)
            prob += q[l, 0] >= init_l
            prob += q[l, 0] >= prev_end
            # Точная линеаризация через v[l]
            prob += q[l, 0] >= init_l - R * v[l]
            prob += q[l, 0] >= prev_end - R * (1 - v[l])
            prob += q[l, 0] <= init_l + R * (1 - v[l])
            prob += q[l, 0] <= prev_end + R * v[l]

        # (4) Прибор l >= 1, позиции j >= 1
        for l in range(1, L):
            for j in range(1, J):
                j1 = j - 1
                setup_l = pulp.lpSum(
                    p.t_setup[l][k][i] * y[k, j1, i, j]
                    for i in range(I) for k in range(I) if i != k
                )
                prev_pos_end = (q[l, j1]
                                + pulp.lpSum(p.t[l][i] * r[j1, i] for i in range(I))
                                + setup_l)
                prev_dev_end = (q[l-1, j]
                                + pulp.lpSum(p.t[l-1][i] * r[j, i] for i in range(I)))
                prob += q[l, j] >= prev_pos_end
                prob += q[l, j] >= prev_dev_end
                # Линеаризация через w[l,j]
                prob += q[l, j] >= prev_pos_end - R * w[l, j]
                prob += q[l, j] >= prev_dev_end - R * (1 - w[l, j])
                prob += q[l, j] <= prev_pos_end + R * (1 - w[l, j])
                prob += q[l, j] <= prev_dev_end + R * w[l, j]

        # --- Блок ТО (расширение модели) ---
        if p.use_maintenance:
            for l in range(L):
                for j in range(J):
                    tm_l = p.tm_maint[l]
                    TM_l = p.TM[l]

                    # q_maint >= 0, если ТО проводится
                    prob += q_maint[l, j] >= 0
                    prob += q_maint[l, j] <= R * maint[l, j]

                    # Если ТО перед позицией j, то оно заканчивается до начала j
                    prob += q[l, j] >= q_maint[l, j] + tm_l * maint[l, j]

                    # Накопленное рабочее время к позиции j
                    if j == 0:
                        prob += work_acc[l, j] == pulp.lpSum(
                            p.t[l][i] * r[j, i] for i in range(I)
                        )
                    else:
                        prob += work_acc[l, j] == (
                            work_acc[l, j-1]
                            + pulp.lpSum(p.t[l][i] * r[j, i] for i in range(I))
                            - TM_l * maint[l, j]  # ТО "сбрасывает" счётчик
                        )
                    # Ограничение: накопленное время <= TM_l между ТО
                    prob += work_acc[l, j] <= TM_l

                    # Если накопленное время близко к TM_l, ТО обязательно
                    # Упрощённо: если work_acc > TM_l - max_t, нужно ТО
                    max_t = max(p.t[l])
                    prob += work_acc[l, j] >= 0

                    # ТО на первой позиции не обязательно (начало работы)
                    if j == 0:
                        # q_maint[l,0] = 0 (ТО перед первой операцией, если нужно)
                        prob += q_maint[l, 0] == 0

        # --- Критерий Cmax ---
        if self.criterion == "Cmax":
            for j in range(J):
                for i in range(I):
                    prob += Cmax >= (q[L-1, j]
                                     + pulp.lpSum(p.t[L-1][ii] * r[j, ii]
                                                  for ii in range(I)))

        # --- Критерий G (суммарное запаздывание) ---
        else:
            for i in range(I):
                # g[i] - момент окончания обработки заданий i-го типа
                # g[i] >= q[L-1,j] + sum(t[L-1][ii]*r[j,ii]) - R*(1-x[i,j])
                for j in range(J):
                    end_j = (q[L-1, j]
                             + pulp.lpSum(p.t[L-1][ii] * r[j, ii] for ii in range(I)))
                    prob += g_time[i] >= end_j - R * (1 - x[i, j])

                # Запаздывание pi = max(0, gi - di)
                di = p.d[i]
                prob += delay[i] >= 0
                prob += delay[i] >= g_time[i] - di

        # --- Запуск решателя ---
        solver_msg = 1 if self.verbose else 0

        # Выбор решателя: CBC -> GLPK
        available = pulp.listSolvers(onlyAvailable=True)
        if 'PULP_CBC_CMD' in available:
            solver = pulp.PULP_CBC_CMD(msg=solver_msg, timeLimit=self.time_limit,
                                        gapRel=0.05)
        elif 'GLPK_CMD' in available:
            solver = pulp.GLPK_CMD(msg=solver_msg, timeLimit=self.time_limit)
        else:
            solver = pulp.PULP_CBC_CMD(msg=solver_msg)

        status_code = prob.solve(solver)
        status_str = pulp.LpStatus[status_code]

        # --- Сбор результатов ---
        results = OptimizationResults()
        results.criterion = self.criterion

        if status_str == "Optimal":
            results.status = OptimizationResults.STATUS_OPTIMAL
        elif status_str in ("Feasible", "Not Solved"):
            results.status = OptimizationResults.STATUS_FEASIBLE
        elif status_str == "Infeasible":
            results.status = OptimizationResults.STATUS_INFEASIBLE
            return results
        else:
            results.status = OptimizationResults.STATUS_FEASIBLE

        try:
            if self.criterion == "Cmax":
                results.objective_value = pulp.value(Cmax)
            else:
                results.objective_value = pulp.value(prob.objective)
        except Exception:
            results.objective_value = None

        if results.objective_value is None:
            results.status = OptimizationResults.STATUS_INFEASIBLE
            results.message = "Решение не найдено"
            return results

        # Составы пакетов
        for j in range(J):
            for i in range(I):
                xval = pulp.value(x[i, j])
                if xval is not None and xval > 0.5:
                    mval = pulp.value(m[j])
                    cnt = round(mval) if mval else 0
                    results.batches.append(BatchInfo(
                        position=j+1, task_type=i+1, count=cnt
                    ))
                    results.raw_x[(i, j)] = 1
                    results.raw_m[j] = cnt

        # Расписание
        for l in range(L):
            for j in range(J):
                qval = pulp.value(q[l, j])
                if qval is None:
                    qval = 0
                # Определяем тип задания
                task_type = 1
                proc_time = 0
                for i in range(I):
                    xval = pulp.value(x[i, j])
                    if xval is not None and xval > 0.5:
                        task_type = i + 1
                        cnt = results.raw_m.get(j, 2)
                        proc_time = p.t[l][i] * cnt
                        break
                results.schedule.append(ScheduleEntry(
                    device=l+1, position=j+1, task_type=task_type,
                    start_time=qval,
                    process_time=proc_time,
                    end_time=qval + proc_time
                ))
                results.raw_q[(l, j)] = qval

        # Расписание ТО
        if p.use_maintenance:
            for l in range(L):
                for j in range(J):
                    mv = pulp.value(maint[l, j])
                    if mv is not None and mv > 0.5:
                        qm = pulp.value(q_maint[l, j]) or 0
                        results.maintenance.append(MaintenanceEntry(
                            device=l+1,
                            before_position=j+1,
                            start_time=qm,
                            duration=p.tm_maint[l],
                            end_time=qm + p.tm_maint[l]
                        ))

        # Времена окончания и запаздывания (критерий G)
        if self.criterion == "G":
            for i in range(I):
                gt = pulp.value(g_time[i])
                dt = pulp.value(delay[i])
                results.completion_times[i+1] = gt or 0
                results.delays[i+1] = dt or 0

        return results

    # -----------------------------------------------------------------------
    # CPLEX реализация (если доступна)
    # -----------------------------------------------------------------------

    def _solve_cplex(self) -> OptimizationResults:
        """Решение через IBM CPLEX docplex API"""
        p = self.params
        I, L, J = p.I, p.L, p.J
        R = 10000
        n_min = min(p.n)

        mdl = CplexModel(name="FlowShop_Batch")
        mdl.parameters.timelimit = self.time_limit
        if not self.verbose:
            mdl.context.solver.log_output = False

        # Переменные
        x = {(i, j): mdl.binary_var(name=f"x_{i}_{j}")
             for i in range(I) for j in range(J)}
        m = {j: mdl.integer_var(lb=2, ub=n_min, name=f"m_{j}")
             for j in range(J)}
        q = {(l, j): mdl.continuous_var(lb=0, name=f"q_{l}_{j}")
             for l in range(L) for j in range(J)}
        r = {(j, i): mdl.continuous_var(lb=0, ub=n_min, name=f"r_{j}_{i}")
             for j in range(J) for i in range(I)}
        y = {(k, j1, i, j): mdl.binary_var(name=f"y_{k}_{j1}_{i}_{j}")
             for j in range(1, J) for j1 in [j-1]
             for i in range(I) for k in range(I) if i != k}
        v = {l: mdl.binary_var(name=f"v_{l}") for l in range(1, L)}
        w = {(l, j): mdl.binary_var(name=f"w_{l}_{j}")
             for l in range(1, L) for j in range(1, J)}

        if p.use_maintenance:
            maint = {(l, j): mdl.binary_var(name=f"maint_{l}_{j}")
                     for l in range(L) for j in range(J)}
            q_maint = {(l, j): mdl.continuous_var(lb=0, name=f"qm_{l}_{j}")
                       for l in range(L) for j in range(J)}
            work_acc = {(l, j): mdl.continuous_var(lb=0, name=f"wacc_{l}_{j}")
                        for l in range(L) for j in range(J)}

        # Аналогичные ограничения как в PuLP версии
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

        # Расписание — первый прибор
        for j in range(J):
            if j == 0:
                mdl.add_constraint(
                    q[0, 0] >= mdl.sum(p.t_init[0][i] * x[i, 0] for i in range(I)))
            else:
                j1 = j - 1
                setup_expr = mdl.sum(
                    p.t_setup[0][k][i] * y[k, j1, i, j]
                    for i in range(I) for k in range(I) if i != k)
                mdl.add_constraint(
                    q[0, j] >= q[0, j1]
                    + mdl.sum(p.t[0][i] * r[j1, i] for i in range(I))
                    + setup_expr)

        # Прибор l >= 1
        for l in range(1, L):
            init_l = mdl.sum(p.t_init[l][i] * x[i, 0] for i in range(I))
            prev_end = q[l-1, 0] + mdl.sum(p.t[l-1][i] * r[0, i] for i in range(I))
            mdl.add_constraint(q[l, 0] >= init_l - R * v[l])
            mdl.add_constraint(q[l, 0] >= prev_end - R * (1 - v[l]))
            mdl.add_constraint(q[l, 0] <= init_l + R * (1 - v[l]))
            mdl.add_constraint(q[l, 0] <= prev_end + R * v[l])

            for j in range(1, J):
                j1 = j - 1
                setup_l = mdl.sum(
                    p.t_setup[l][k][i] * y[k, j1, i, j]
                    for i in range(I) for k in range(I) if i != k)
                prev_pos = (q[l, j1]
                            + mdl.sum(p.t[l][i] * r[j1, i] for i in range(I))
                            + setup_l)
                prev_dev = (q[l-1, j]
                            + mdl.sum(p.t[l-1][i] * r[j, i] for i in range(I)))
                mdl.add_constraint(q[l, j] >= prev_pos - R * w[l, j])
                mdl.add_constraint(q[l, j] >= prev_dev - R * (1 - w[l, j]))
                mdl.add_constraint(q[l, j] <= prev_pos + R * (1 - w[l, j]))
                mdl.add_constraint(q[l, j] <= prev_dev + R * w[l, j])

        # ТО блок
        if p.use_maintenance:
            for l in range(L):
                for j in range(J):
                    tm_l = p.tm_maint[l]
                    TM_l = p.TM[l]
                    mdl.add_constraint(q_maint[l, j] <= R * maint[l, j])
                    mdl.add_constraint(
                        q[l, j] >= q_maint[l, j] + tm_l * maint[l, j])
                    if j == 0:
                        mdl.add_constraint(
                            work_acc[l, j] == mdl.sum(p.t[l][i] * r[j, i]
                                                      for i in range(I)))
                        mdl.add_constraint(q_maint[l, 0] == 0)
                    else:
                        mdl.add_constraint(
                            work_acc[l, j] == (
                                work_acc[l, j-1]
                                + mdl.sum(p.t[l][i] * r[j, i] for i in range(I))
                                - TM_l * maint[l, j]))
                    mdl.add_constraint(work_acc[l, j] <= TM_l)
                    mdl.add_constraint(work_acc[l, j] >= 0)

        # Критерий
        if self.criterion == "Cmax":
            Cmax = mdl.continuous_var(lb=0, name="Cmax")
            for j in range(J):
                mdl.add_constraint(
                    Cmax >= q[L-1, j]
                    + mdl.sum(p.t[L-1][i] * r[j, i] for i in range(I)))
            mdl.minimize(Cmax)
        else:
            g_time = {i: mdl.continuous_var(lb=0, name=f"g_{i}") for i in range(I)}
            delay = {i: mdl.continuous_var(lb=0, name=f"p_{i}") for i in range(I)}
            z = {i: mdl.binary_var(name=f"z_{i}") for i in range(I)}
            for i in range(I):
                for j in range(J):
                    end_j = (q[L-1, j]
                             + mdl.sum(p.t[L-1][ii] * r[j, ii] for ii in range(I)))
                    mdl.add_constraint(
                        g_time[i] >= end_j - R * (1 - x[i, j]))
                    mdl.add_constraint(
                        g_time[i] <= end_j + R * (1 - x[i, j]))
                di = p.d[i]
                mdl.add_constraint(delay[i] >= g_time[i] - di)
                mdl.add_constraint(delay[i] >= 0)
                mdl.add_constraint(g_time[i] - di <= R * z[i])
                mdl.add_constraint(g_time[i] - di >= -R * (1 - z[i]))
                mdl.add_constraint(delay[i] <= g_time[i] - di + R * (1 - z[i]))
                mdl.add_constraint(delay[i] <= R * z[i])
            mdl.minimize(mdl.sum(delay[i] for i in range(I)))

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
            results.objective_value = sol.objective_value

        # Сбор результатов (аналогично PuLP)
        for j in range(J):
            for i in range(I):
                if sol.get_value(x[i, j]) > 0.5:
                    cnt = round(sol.get_value(m[j]))
                    results.batches.append(BatchInfo(position=j+1, task_type=i+1, count=cnt))
                    results.raw_x[(i, j)] = 1
                    results.raw_m[j] = cnt

        for l in range(L):
            for j in range(J):
                qval = sol.get_value(q[l, j]) or 0
                task_type = 1
                proc_time = 0
                for i in range(I):
                    if sol.get_value(x[i, j]) > 0.5:
                        task_type = i + 1
                        cnt = results.raw_m.get(j, 2)
                        proc_time = p.t[l][i] * cnt
                        break
                results.schedule.append(ScheduleEntry(
                    device=l+1, position=j+1, task_type=task_type,
                    start_time=qval, process_time=proc_time, end_time=qval+proc_time
                ))
                results.raw_q[(l, j)] = qval

        if p.use_maintenance:
            for l in range(L):
                for j in range(J):
                    if sol.get_value(maint[l, j]) > 0.5:
                        qm = sol.get_value(q_maint[l, j]) or 0
                        results.maintenance.append(MaintenanceEntry(
                            device=l+1, before_position=j+1,
                            start_time=qm, duration=p.tm_maint[l],
                            end_time=qm + p.tm_maint[l]
                        ))

        if self.criterion == "G":
            for i in range(I):
                results.completion_times[i+1] = sol.get_value(g_time[i]) or 0
                results.delays[i+1] = sol.get_value(delay[i]) or 0

        return results

    def _compute_fixed_objective(self) -> Optional[float]:
        """
        Вычислить значение критерия для фиксированных пакетов
        (каждый тип — отдельный пакет, последовательно).
        Используется для сравнения эффективности оптимизации.
        """
        p = self.params
        try:
            I, L = p.I, p.L
            # Фиксированное расписание: пакет 0 — тип 0, пакет 1 — тип 1, ...
            q = [[0.0] * I for _ in range(L)]

            # Прибор 0, первая позиция
            q[0][0] = p.t_init[0][0]

            # Прибор 0, остальные позиции
            for j in range(1, I):
                setup = p.t_setup[0][j-1][j]
                q[0][j] = q[0][j-1] + p.t[0][j-1] * p.n[j-1] + setup

            # Приборы 1..L-1
            for l in range(1, L):
                q[l][0] = max(
                    p.t_init[l][0],
                    q[l-1][0] + p.t[l-1][0] * p.n[0]
                )
                for j in range(1, I):
                    setup = p.t_setup[l][j-1][j]
                    prev_pos = q[l][j-1] + p.t[l][j-1] * p.n[j-1] + setup
                    prev_dev = q[l-1][j] + p.t[l-1][j] * p.n[j]
                    q[l][j] = max(prev_pos, prev_dev)

            if self.criterion == "Cmax":
                cmax = max(q[L-1][j] + p.t[L-1][j] * p.n[j] for j in range(I))
                return cmax
            else:
                total_delay = 0.0
                for i in range(I):
                    g_i = q[L-1][i] + p.t[L-1][i] * p.n[i]
                    total_delay += max(0.0, g_i - p.d[i])
                return total_delay
        except Exception:
            return None
