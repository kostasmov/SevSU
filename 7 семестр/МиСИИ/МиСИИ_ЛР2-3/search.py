# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
В search.py вам необходимо реализовать общие алгоритмы поиска, которые вызываются
агентом Pacman (в searchAgents.py).
"""

import util

class SearchProblem:
    """
    Этот класс описывает структуру задачи поиска, но не реализует 
    ни один из методов (в объектно-ориентированной терминологии: абстрактный класс).

    Вам не нужно ничего менять в этом классе.
    """

    def getStartState(self):
        """
        Возвращает начальное состояние для задачи поиска.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Возвращает True, когда состояние (state) является допустимым целевым состоянием.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Для данного состояния (state) возвращает список из триплетов (successor,
        action, stepCost), где 'successor' - это преемник текущего
        состояния, 'action' - это действие, необходимое для этого, а "stepCost" - 
        затраты раскрытия преемника.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: Список действий, которые нужно предпринять

        Этот метод возвращает общую стоимость определенной последовательности
        действий. Последовательность должна состоять из разрешенных ходов.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Поиск в глубину. 

    Ваш алгоритм поиска должен возвращать список действий, которые 
    ведут к цели. Убедитесь, что реализуете алгоритм поиска на графе

    Прежде чем кодировать,полезно выполнить функцию  с этими простыми
    командами,чтобы понять смысл задачи (problem), передаваемой на вход:
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    "-----------------------------"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Находит самые поверхностные узлы в дереве поиска """

    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Находит узел минимальной стоимости """

    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    Эвристическая функция оценивает стоимость от текущего состояния до 
    ближайшей цели в задаче SearchProblem. Эта эвристика тривиальна.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Находит узел с наименьшей комбинированной стоимостью, включающей эвристику
    """

    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

    util.raiseNotDefined()


# Аббревиатуры
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
