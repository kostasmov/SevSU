# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    Рефлекторный агент выбирает действие в каждой точке выбора,
    исследуя альтернативы с помощью функции оценки состояния.

    Приведенный ниже код предоставляется в качестве руководства.
    Вы можете изменить его так, как считаете нужным, при условии,
    что вы не касаетесь заголовков наших методов.
    """

    def getAction(self, gameState):
        """
        Вам не нужно менять этот метод, но вы можете это сделать.

        getAction возвращает одно из лучших действий в соответствии с
        функцией оценки.

        getAction принимает состояние GameState и
        возвращает направления Directions.X для некоторого X из мно-ва
        {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Получить допустимые действия для состояния
        legalMoves = gameState.getLegalActions()

        # Выбрать одно из лучших действий в состоянии, используя функцию оценки
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Случайно выбираем действие среди лучших

        "Добавьте свой код сюда, если хотите"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Разработайте здесь более совершенную функцию оценки.

        Функция оценки принимает текущее состояние и допустимое действие
        (pacman.py) и возвращает числовое значение функции оценки
        (большим числам отдается предпочтение).

        Приведенный ниже код извлекает некоторую полезную информацию из
        состояния, такую как оставшаяся еда (newFood) и положение Pacman после
        перемещения (newPos).

        newScaredTimes содержит количество ходов, на которое каждый призрак
        останется испуганным из-за того, что Пакман съел энерго-гранулу.

        Распечатайте эти переменные, чтобы увидеть и понять их значения, а затем
        комбинируйте их, чтобы создать подходящую функцию оценки.
        """

        # Полезная информация, которую вы можете извлечь из GameState (pacman.py)

        # дочернее состояниe после действия action
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # пример схемы дочернего состояния для поля testClassic, размером 10x5:
        #    %%%%%
        #    % . %
        #    %.G.%
        #    % . %
        #    %. .%
        #    %   %
        #    %  .%
        #    %   %
        #    %< .%
        #    %%%%%
        # Здесь G - призрак, < - Пакман, . - еда, % - стены

        # координаты Пакмана в виде кортежа (x,y)
        newPos = successorGameState.getPacmanPosition()
        #print("newPos:", newPos)

        # положение точек еды в виде логического массива
        newFood = successorGameState.getFood()

        # Для приведенной выше схемы newFood будет равен:
        # FFFFF
        # FFTFF
        # FTFTF
        # FFTFF
        # FTFTF
        # FFFFF
        # FFFTF
        # FFFFF
        # FFFTF
        # FFFFF
        # Здесь Т - есть еда, F - нет еды

        # новые состояния призраков
        newGhostStates = successorGameState.getGhostStates()
        #print("newGhostStateExample:", newGhostStates[0])

        # время испуга призраков
        # пример значения для newScaredTimes при 2-х призраках: [40, 40]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print("newScaredTimes:", newScaredTimes)

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        # список координат пищевых гранул
        newFoodPoses = newFood.asList()

        # список новых координат призраков
        newGhostPoses = [(G.getPosition()[0], G.getPosition()[1]) for G in newGhostStates]

        # проверка столкновения с призраком
        for i, pos in enumerate(newGhostPoses):
            if newPos == pos and not newScaredTimes[i]:
                return -1

        # проверка наличия гранулы
        if newPos in currentGameState.getFood().asList():
            return 1

        # расстояния до ближайшего призрака и гранулы
        closestGhostDist = min(manhattanDistance(g, newPos) for g in newGhostPoses)
        closestFoodDist = min(manhattanDistance(f, newPos) for f in newFoodPoses)

        # итоговая оценка (оценочная функция)
        return 1 / closestFoodDist - 1 / closestGhostDist
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    Это функция оценки по умолчанию, она просто возвращает оценку состояния.
    Эта оценка также отображается в графическом интерфейсе Pacman.

    Эта функция оценки предназначена для использования состязательными агентами.
    (не рефлекторными агентами).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
     Вам не нужно вносить в этот класс какие-либо изменения,
     но вы можете это сделать, если хотите добавить функциональность
     ко всем вашим состязательным поисковым агентам.
     Однако, пожалуйста, ничего не удаляйте.

     Примечание: это абстрактный класс: не нужно создавать его экземпляры. 
     Он определен лишь частично и предназначен для наследования.
     Agent (game.py) - еще один абстрактный класс.
     Глубина поиска по умолчанию равна 2
     Функция оценки, используемая  по умолчанию - scoreEvaluationFunction
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Индекс Пакмана всегда равен 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Ваш минимаксный агент (задание 2)
    """
    def value(self, gameState, currentDepth, agentIndex):
        """
         Оценивание вершин дерева поиска
        """
        # стат. оценка терминальной вершины
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # если же это агент MAX (игрок):
        elif agentIndex == 0:
            return self.max_value(gameState, currentDepth)

        # если же это один из агентов MIN (противник):
        else:
            return self.min_value(gameState, currentDepth, agentIndex)

    def max_value(self, gameState, currentDepth):
        """
         Динамическая оценка для игрока МАКС (pacman)
        """
        maxValue = -100000  # -∞

        # ищем наибольшую оценку нижнего уровня
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, self.value(succ, currentDepth, 1))

        return maxValue

    def min_value(self, gameState, currentDepth, agentIndex):
        """
         Динамическая оценка для игрока МИН (ghost)
        """
        minValue = 100000     #+∞

        # ищем наименьшую оценку нижнего уровня
        for action in gameState.getLegalActions(agentIndex):
            succ = gameState.generateSuccessor(agentIndex, action)

            # перебор цепочки MIN-агентов
            if agentIndex == gameState.getNumAgents() - 1:
                minValue = min(minValue, self.value(succ, currentDepth + 1, 0))
            else:
                minValue = min(minValue, self.value(succ, currentDepth, agentIndex + 1))

        return minValue

    def getAction(self, gameState):
        """
        Возвращает минимаксное действие для текущего состояния gameState,
        используя self.depth и self.evaluationFunction.

        Вот несколько вызовов методов, которые могут быть полезны при реализации
        минимаксного агента.

        gameState.getLegalActions(agentIndex):
        Возвращает список допустимых (легальных) действий для агента
        agentIndex=0 соответсвует Пакману, а для призраков agentIndex >= 1

        gameState.generateSuccessor(agentIndex, action):
        Возвращает состояние-преемник после того, как агент совершит действие action.

        gameState.getNumAgents():
        Возвращает общее количество агентов в игре.

        gameState.isWin():
        Возвращает True если состояние игры является выигрышным.

        gameState.isLose():
        Возвращает True если состояние игры является проигрышным.
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        nodeValue = -100000
        nextAction = Directions.STOP

        # осмотр допустимых действий Пакмана
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            nextValue = self.value(succ, 0, 1) # узнаём оценку

            # если есть что-то лучше чем просто стоять - так и делаем
            if nextValue > nodeValue:
                nodeValue = nextValue
                nextAction = action

        return nextAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Ваш минимаксный агент, реализующий альфа-бета отсечение (задание 3)
    """

    def value(self, gameState, currentDepth, agentIndex, alpha, beta):
        """
         Оценивание вершин дерева поиска
        """
        # стат. оценка терминальной вершины
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # если же это агент MAX (игрок):
        elif agentIndex == 0:
            return self.max_value(gameState, currentDepth, alpha, beta)

        # если же это один из агентов MIN (противник):
        else:
            return self.min_value(gameState, currentDepth, agentIndex, alpha, beta)

    def max_value(self, gameState, currentDepth, alpha, beta):
        """
         Динамическая оценка для игрока МАКС (игрок)
        """
        maxValue = -100000  # -∞

        # ищем наибольшую оценку нижнего уровня
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, self.value(succ, currentDepth, 1, alpha, beta))

            # альфа-отсечение
            if maxValue > beta:
                return maxValue
            alpha = max(maxValue, alpha)

        return maxValue

    def min_value(self, gameState, currentDepth, agentIndex, alpha, beta):
        """
         Динамическая оценка для игрока МИН (противники)
        """
        minValue = 100000     #+∞

        # ищем наименьшую оценку нижнего уровня
        for action in gameState.getLegalActions(agentIndex):
            succ = gameState.generateSuccessor(agentIndex, action)

            # перебор цепочки MIN-агентов
            if agentIndex == gameState.getNumAgents() - 1:
                minValue = min(minValue, self.value(succ, currentDepth + 1, 0, alpha, beta))
            else:
                minValue = min(minValue, self.value(succ, currentDepth, agentIndex + 1, alpha, beta))

            # бета-отсечение
            if minValue < alpha:
                return minValue
            beta = min(minValue, beta)

        return minValue

    def getAction(self, gameState):
        """
        Возвращает минимаксное действие, используя
        self.depth and self.evaluationFunction
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        nodeValue = -100000 # -∞
        alpha = -100000     # -∞
        beta = 100000       # +∞

        nextAction = Directions.STOP

        # осмотр допустимых действий Пакмана
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            nodeValue = max(nodeValue, self.value(succ, 0, 1, alpha, beta))

            # если есть что-то лучше, чем просто стоять - так и делаем
            if nodeValue > alpha:
                alpha = nodeValue
                nextAction = action

        return nextAction
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Ваш expectimax агент (задание 4)
    """
    def value(self, gameState, currentDepth, agentIndex):
        """
         Оценивание вершин дерева поиска
        """
        # стат. оценка терминальной вершины
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # если же это агент MAX (игрок):
        elif agentIndex == 0:
            return self.max_value(gameState, currentDepth)

        # если же это один из агентов MIN (противник):
        else:
            return self.min_value(gameState, currentDepth, agentIndex)

    def max_value(self, gameState, currentDepth):
        """
         Динамическая оценка для игрока МАКС (pacman)
        """
        maxValue = -100000  # -∞

        # ищем наибольшую оценку нижнего уровня
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, self.value(succ, currentDepth, 1))

        return maxValue

    def min_value(self, gameState, currentDepth, agentIndex):
        """
         Динамическая оценка для игрока МИН (ghost)
        """
        minValue = 0
        actions = gameState.getLegalActions(agentIndex)

        # ищем наименьшую оценку нижнего уровня
        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)

            # перебор цепочки MIN-агентов
            if agentIndex == gameState.getNumAgents() - 1:
                minValue += self.value(succ, currentDepth + 1, 0)
            else:
                minValue += self.value(succ, currentDepth, agentIndex + 1)

        # усреднённая оценка для равновероятных действий
        return minValue / len(actions)

    def getAction(self, gameState):
        """
        Возвращает  действие Пакмана, используя expectimax поиск и
        self.depth и self.evaluationFunction

        Все призраки должны выбирать свои случайные
        допустимые действия с равной вероятностью
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        nodeValue = -100000
        nextAction = Directions.STOP

        # осмотр допустимых действий Пакмана
        for action in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, action)
            nextValue = self.value(succ, 0, 1)  # узнаём оценку

            # если есть что-то лучше чем просто стоять - так и делаем
            if nextValue > nodeValue:
                nodeValue = nextValue
                nextAction = action

        return nextAction
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Ваша усовершенствованная функция оценки (вопрос 5)

     ОПИСАНИЕ: <втавьте сюда описание Вашей функции>
    """
    
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
   
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
