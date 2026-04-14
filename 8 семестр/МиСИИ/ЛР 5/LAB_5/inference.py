# inference.py
# ------------
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


import random
import itertools
from typing import List, Dict, Tuple
import busters
import game
import bayesNet as bn
from bayesNet import normalize
import hunters
from util import manhattanDistance, raiseNotDefined
from factorOperations import joinFactorsByVariableWithCallTracking, joinFactors
from factorOperations import eliminateWithCallTracking

########### ########### ###########
########### Задание 1   ###########
########### ########### ###########

def constructBayesNet(gameState: hunters.GameState):
    """
    Постройте пустую сеть Байеса в соответствии со структурой, приведенной в задании 1. 
    Вы должны назвать все переменные используя константы этой функции.
    В этой функции вы должны: 
        - определить переменные, которые являются узлами сети Байеса;
        - определить каждое ребро сети Байеса, представив его в виде кортежа '(от, до)'; 
        - определить возможные значения переменных в словаре variableDomainsDict[var] 
          для каждой переменной var. 
    Каждая позиция агента - это кортеж (x, y), где x и y индексируется от 0.
    Каждое наблюдаемое расстояние OBS - это "зашумленное" расстояние Манхэттена:
        оно неотрицательное и ошибка в оценке расстояния равна |OBS - trueOBS| <= MAX_NOISE 
    """
    
    # имена узлов сети
    PAC = "Pacman"
    GHOST0 = "Ghost0"
    GHOST1 = "Ghost1"
    OBS0 = "Observation0"
    OBS1 = "Observation1"

    # размеры игрового поля
    X_RANGE = gameState.getWalls().width    # ширина
    Y_RANGE = gameState.getWalls().height   # высота

    # максимальная погрешность датчика (шум)
    MAX_NOISE = 7

    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    
    # узлы сети
    variables = [PAC, GHOST0, GHOST1, OBS0, OBS1]
    
    # рёбра сети
    edges = [(PAC, OBS0), (GHOST0, OBS0), (PAC, OBS1), (GHOST1, OBS1)]

    # множества значений для узлов сети
    variableDomainsDict = {}

    # все возможные позиции агентов
    pos_domain = [(x, y) for x in range(X_RANGE) for y in range(Y_RANGE)]

    variableDomainsDict[PAC] = pos_domain
    variableDomainsDict[GHOST0] = pos_domain
    variableDomainsDict[GHOST1] = pos_domain

    # возможные наблюдения сенсора
    max_dist = (X_RANGE - 1) + (Y_RANGE - 1)
    obs_domain = list(range(0, max_dist + MAX_NOISE + 1))
    
    variableDomainsDict[OBS0] = obs_domain
    variableDomainsDict[OBS1] = obs_domain
   
    "*** КОНЕЦ ВАШЕГО КОДА ***"

    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net


def inferenceByEnumeration(bayesNet: bn, queryVariables: List[str], evidenceDict: Dict):
    """
    An inference by enumeration implementation provided as reference.
    This function performs a probabilistic inference query that
    returns the factor:

    P(queryVariables | evidenceDict)

    bayesNet:       The Bayes Net on which we are making a query.
    queryVariables: A list of the variables which are unconditioned in
                    the inference query.
    evidenceDict:   An assignment dict {variable : value} for the
                    variables which are presented as evidence
                    (conditioned) in the inference query. 
    """
    callTrackingList = []
    joinFactorsByVariable = joinFactorsByVariableWithCallTracking(callTrackingList)
    eliminate = eliminateWithCallTracking(callTrackingList)

    # initialize return variables and the variables to eliminate
    evidenceVariablesSet = set(evidenceDict.keys())
    queryVariablesSet = set(queryVariables)
    eliminationVariables = (bayesNet.variablesSet() - evidenceVariablesSet) - queryVariablesSet

    # grab all factors where we know the evidence variables (to reduce the size of the tables)
    currentFactorsList = bayesNet.getAllCPTsWithEvidence(evidenceDict)

    # join all factors by variable
    for joinVariable in bayesNet.variablesSet():
        currentFactorsList, joinedFactor = joinFactorsByVariable(currentFactorsList, joinVariable)
        currentFactorsList.append(joinedFactor)

    # currentFactorsList should contain the connected components of the graph now as factors, must join the connected components
    fullJoint = joinFactors(currentFactorsList)

    # marginalize all variables that aren't query or evidence
    incrementallyMarginalizedJoint = fullJoint
    for eliminationVariable in eliminationVariables:
        incrementallyMarginalizedJoint = eliminate(incrementallyMarginalizedJoint, eliminationVariable)

    fullJointOverQueryAndEvidence = incrementallyMarginalizedJoint

    # normalize so that the probability sums to one
    # the input factor contains only the query variables and the evidence variables, 
    # both as unconditioned variables
    queryConditionedOnEvidence = normalize(fullJointOverQueryAndEvidence)
    # now the factor is conditioned on the evidence variables

    # the order is join on all variables, then eliminate on all elimination variables
    return queryConditionedOnEvidence

########### ########### ###########
########### Задание 4   ###########
########### ########### ###########

def inferenceByVariableEliminationWithCallTracking(callTrackingList=None):

    def inferenceByVariableElimination(bayesNet: bn, queryVariables: List[str], evidenceDict: Dict, eliminationOrder: List[str]):
        """
        Эта функция должна выполнять вероятностный выводной запрос, который
            возвращает фактор:

            P(queryVariables | evidenceDict)

        Она должна выполнять вывод путём чередования объединения по переменной
            и исключения этой переменной в порядке переменных в соответствии с 
            exceptionOrder. См. inferenceByEnumeration для примера использования
            этих функций.

        Вам нужно использовать joinFactorsByVariable для объединения всех факторов,
            содержащих переменную, чтобы автооценщик распознал, что вы выполнили
            правильное чередование объединений и исключений.

        Если фактор, из которого вы собираетесь исключить переменную, имеет
            только одну безусловную переменную, вам не следует исключать ее
            а вместо этого просто отбросить фактор. Это связано с тем, что
            результат исключения будет 1 (вы исключаете все безусловные переменные),
            но это не допустимый фактор. Поэтому это упрощает использование  
            результата исключения.

        Сумма вероятностей должна равняться единице (чтобы это была истинная 
            условная вероятность, обусловленная свидетельствами).

        bayesNet:       Байесовская сеть, на основе по которой мы делаем запрос.
        queryVariables: Список безусловных переменных запроса.
        evidenceDict:   Словарь присваиваний {переменная : значение} для
                        переменных, которые представлены как свидельства
                        (условные) в запросе вывода.
        eliminationOrder: Порядок исключения переменных.        


        Подсказка: BayesNet.getAllCPTsWithEvidence вернет все таблицы условных 
            вероятностей, даже если для evidenceDict передан пустой словарь (или None).
            В этом случае он не будет специализировать никакие домены переменных в CPT.

        Полезные функции:
        BayesNet.getAllCPTsWithEvidence
        normalize
        eliminate
        joinFactorsByVariable
        joinFactors
        """

        # необходимо для автооценивания -- не удалять!
        joinFactorsByVariable = joinFactorsByVariableWithCallTracking(callTrackingList)
        eliminate             = eliminateWithCallTracking(callTrackingList)

        if eliminationOrder is None: # установить произвольный порядок удаления, если задано None
            eliminationVariables = bayesNet.variablesSet() - set(queryVariables) -\
                                   set(evidenceDict.keys())
            eliminationOrder = sorted(list(eliminationVariables))

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        # список всех факторов (с учётом свидетельств)
        factors = bayesNet.getAllCPTsWithEvidence(evidenceDict)

        # перебор всех исключаемых переменных (var)
        for var in eliminationOrder:
            # перемножение факторов с исключаемой переменной
            factors, joinedFactor = joinFactorsByVariable(factors, var)

            # маргинализация по исклюаемой переменной и добавление в список
            if len(joinedFactor.unconditionedVariables()) > 1:
                factors.append(eliminate(joinedFactor, var))

        # объединить список факторов
        finalFactor = joinFactors(factors)

        "*** КОНЕЦ ВАШЕГО КОДА ***"

        # возвращаем нормализованный фактор
        return normalize(finalFactor)

    return inferenceByVariableElimination

inferenceByVariableElimination = inferenceByVariableEliminationWithCallTracking()

def sampleFromFactorRandomSource(randomSource=None):
    if randomSource is None:
        randomSource = random.Random()

    def sampleFromFactor(factor, conditionedAssignments=None):
        """
        Sample an assignment for unconditioned variables in factor with
        probability equal to the probability in the row of factor
        corresponding to that assignment.

        factor:                 The factor to sample from.
        conditionedAssignments: A dict of assignments for all conditioned
                                variables in the factor.  Can only be None
                                if there are no conditioned variables in
                                factor, otherwise must be nonzero.

        Useful for inferenceByLikelihoodWeightingSampling

        Returns an assignmentDict that contains the conditionedAssignments but 
        also a random assignment of the unconditioned variables given their 
        probability.
        """
        if conditionedAssignments is None and len(factor.conditionedVariables()) > 0:
            raise ValueError("Conditioned assignments must be provided since \n" +
                            "this factor has conditionedVariables: " + "\n" +
                            str(factor.conditionedVariables()))

        elif conditionedAssignments is not None:
            conditionedVariables = set([var for var in conditionedAssignments.keys()])

            if not conditionedVariables.issuperset(set(factor.conditionedVariables())):
                raise ValueError("Factor's conditioned variables need to be a subset of the \n"
                                    + "conditioned assignments passed in. \n" + \
                                "conditionedVariables: " + str(conditionedVariables) + "\n" +
                                "factor.conditionedVariables: " + str(set(factor.conditionedVariables())))

            # Reduce the domains of the variables that have been
            # conditioned upon for this factor 
            newVariableDomainsDict = factor.variableDomainsDict()
            for (var, assignment) in conditionedAssignments.items():
                newVariableDomainsDict[var] = [assignment]

            # Get the (hopefully) smaller conditional probability table
            # for this variable 
            CPT = factor.specializeVariableDomains(newVariableDomainsDict)
        else:
            CPT = factor
        
        # Get the probability of each row of the table (along with the
        # assignmentDict that it corresponds to)
        assignmentDicts = sorted([assignmentDict for assignmentDict in CPT.getAllPossibleAssignmentDicts()])
        assignmentDictProbabilities = [CPT.getProbability(assignmentDict) for assignmentDict in assignmentDicts]

        # calculate total probability in the factor and index each row by the 
        # cumulative sum of probability up to and including that row
        currentProbability = 0.0
        probabilityRange = []
        for i in range(len(assignmentDicts)):
            currentProbability += assignmentDictProbabilities[i]
            probabilityRange.append(currentProbability)

        totalProbability = probabilityRange[-1]

        # sample an assignment with probability equal to the probability in the row 
        # for that assignment in the factor
        pick = randomSource.uniform(0.0, totalProbability)
        for i in range(len(assignmentDicts)):
            if pick <= probabilityRange[i]:
                return assignmentDicts[i]

    return sampleFromFactor

sampleFromFactor = sampleFromFactorRandomSource()

class DiscreteDistribution(dict):
    """
    Класс для работы с распределением, 
    представляемым в виде словаря c 
    набором значений ключей и соответсвующих вероятностей
    """
    
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        """
        Возвращает копию распределения
        """
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        """
        Возвращает ключ с наибольшим значением
        """
        if len(self.keys()) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        """
        Возвращает сумму всех значений вероятностей
        """
        return float(sum(self.values()))
    
    ########### ########### ###########
    ########### Задание  5a ###########
    ########### ########### ###########

    def normalize(self):
        """
        Нормализуйте распределение таким образом, чтобы суммарное значение
            всех вероятностей ключей равнялось 1. Сотношение значений для всех
            ключей должно остаться прежним. В случае, когда суммарное значение 
            равно 0, ничего не делайте.
        
        Тесты:
            
        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # сумма значений распределения
        summa = self.total()

        # если все значения равны нулю - ничего не делать
        if summa == 0:
            return

        # нормализация
        for key in self:
            self[key] /= summa

        "*** КОНЕЦ ВАШЕГО КОДА ***"


    def sample(self):
        """
        Формирует случайную выборку по распределению, представляемому
            в виде словаря, и возвращает ключ,
            соответствующий  случайной выборке.
        
        Тесты:
            
        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0 
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # сумма всех значений распределения
        summa = self.total()
        # if total_prob == 0:
        #     return None

        # генерация случайного числа на отрезке [0, summa]
        rand_value = random.uniform(0, summa)

        # накопление вероятности
        prob_summa = 0.0

        # перебор всех элементов распределения
        for key, prob in self.items():
            prob_summa += prob

            # случайное число попало в интервал, соответствующий key
            if rand_value <= prob_summa:
                return key

        "*** КОНЕЦ ВАШЕГО КОДА ***"


class InferenceModule:
    """
    Модуль вывода, отслеживающий распределенние степеней доверия 
    локаций призраков
    """

    ############################################
    # Полезные методы для всех модулей вывода  #
    ############################################

    def __init__(self, ghostAgent):
        """
        Определяет агента-призрака 
        """
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = []  # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistributionHelper(self, gameState, pos, index, agent):
        try:
            jail = self.getJailPosition()
            gameState = self.setGhostPosition(gameState, pos, index + 1)
        except TypeError:
            jail = self.getJailPosition(index)
            gameState = self.setGhostPositions(gameState, pos)
        pacmanPosition = gameState.getPacmanPosition()
        ghostPosition = gameState.getGhostPosition(index + 1)  # The position you set
        dist = DiscreteDistribution()
        if pacmanPosition == ghostPosition:  # The ghost has been caught!
            dist[jail] = 1.0
            return dist
        pacmanSuccessorStates = game.Actions.getLegalNeighbors(pacmanPosition, \
                gameState.getWalls())  # Positions Pacman can move to
        if ghostPosition in pacmanSuccessorStates:  # Ghost could get caught
            mult = 1.0 / float(len(pacmanSuccessorStates))
            dist[jail] = mult
        else:
            mult = 0.0
        actionDist = agent.getDistribution(gameState)
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            if successorPosition in pacmanSuccessorStates:  # Ghost could get caught
                denom = float(len(actionDist))
                dist[jail] += prob * (1.0 / denom) * (1.0 - mult)
                dist[successorPosition] = prob * ((denom - 1.0) / denom) * (1.0 - mult)
            else:
                dist[successorPosition] = prob * (1.0 - mult)
        return dist

    def getPositionDistribution(self, gameState, pos, index=None, agent=None):
        """
        Return a distribution over successor positions of the ghost from the
        given gameState. You must first place the ghost in the gameState, using
        setGhostPosition below.
        """
        if index == None:
            index = self.index - 1
        if agent == None:
            agent = self.ghostAgent
        return self.getPositionDistributionHelper(gameState, pos, index, agent)
    
    ########### ########### ###########
    ########### ЗАДАНИЕ 5б  ###########
    ########### ########### ###########

    def getObservationProb(self, noisyDistance: int, pacmanPosition: Tuple, ghostPosition: Tuple, jailPosition: Tuple):
        """
        Возвращает вероятность P(noisyDistance | pacmanPosition, ghostPosition).
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # ОСОБЫЙ СЛУЧАЙ: призрак уже в темнице сырой
        if ghostPosition == jailPosition:
            return 1.0 if noisyDistance is None else 0.0

        # если призрак не в тюрьме, то расстояние до него должно быть
        if noisyDistance is None:
            return 0.0

        # истинное расстояние между пакманом и призраком
        trueDistance = manhattanDistance(pacmanPosition, ghostPosition)

        return busters.getObservationProbability(noisyDistance, trueDistance)

    def setGhostPosition(self, gameState, ghostPosition, index):
        """
        Set the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of
        the GameState object which is responsible for maintaining game state,
        not a reference to the original object.  Note also that the ghost
        distance observations are stored at the time the GameState object is
        created, so changing the position of the ghost will not affect the
        functioning of observe.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[index] = game.AgentState(conf, False)
        return gameState

    def setGhostPositions(self, gameState, ghostPositions):
        """
        Sets the position of all ghosts to the values in ghostPositions.
        """
        for index, pos in enumerate(ghostPositions):
            conf = game.Configuration(pos, game.Directions.STOP)
            gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
        return gameState

    def observe(self, gameState):
        """
        Collect the relevant noisy distance observation and pass it along.
        """
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index:  # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observeUpdate(obs, gameState)

    def initialize(self, gameState):
        """
        Initialize beliefs to a uniform distribution over all legal positions.
        """
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.allPositions = self.legalPositions + [self.getJailPosition()]
        self.initializeUniformly(gameState)

    ######################################
    # Методы, которые нужно переопределить #
    ######################################

    def initializeUniformly(self, gameState):
        """
        Set the belief state to a uniform prior belief over all positions.
        """
        raise NotImplementedError

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        raise NotImplementedError

    def elapseTime(self, gameState):
        """
        Predict beliefs for the next time step from a gameState.
        """
        raise NotImplementedError

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence so far.
        """
        raise NotImplementedError


class ExactInference(InferenceModule):
    """
    Модуль точного динамического вывода должен использовать
    прямой алгоритм обновления для вычисления точной степени доверия 
    на каждом временном шаге
    """
    def initializeUniformly(self, gameState):
      
        """
        Начинаем с равномерного распределения всех допустимых
        позиций призрака (т.е. позиция тюрьмы не включается)
        """
        self.beliefs = DiscreteDistribution()
        for p in self.legalPositions:
            self.beliefs[p] = 1.0
        self.beliefs.normalize()
    
    ########### ########### ###########
    ########### Задание 6   ###########
    ########### ########### ###########

    def observeUpdate(self, observation: int, gameState: busters.GameState):
        """
        Обновляет степени уверенности агента в отношении позиций призраков
            на основе наблюдания observation и позиции Пакмана.
        observation – это зашумленное манхеттенское расстояние до
            отслеживаемого призрака.

        self.allPositions - список возможных позиций призрака, включающий 
            позицию тюрьмы. Вам необходимо рассматривать только те позиции, 
            которые есть в self.allPositions.

        Модель обновления не является полностью стационарной: она может 
            зависисеть от текущей позиции Пакмана. Это не проблема, если текущая
            позиция Пакмана известна
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        # текущие координаты Пакмана
        pacmanPosition = gameState.getPacmanPosition()

        # позиция тюрьмы
        jailPosition = self.getJailPosition()

        # перебор клеток где может быть призрак
        for possibleGhostPos in self.allPositions:
            # вероятность наблюдения
            prob = self.getObservationProb(observation, pacmanPosition, possibleGhostPos, jailPosition)

            # обновление вероятности позиции призрака
            self.beliefs[possibleGhostPos] *= prob

        "*** КОНЕЦ ВАШЕГО КОДА ***"

        # нормализация распределения вероятностей
        self.beliefs.normalize()
    
    ########### ########### ###########
    ########### Задание 7   ###########
    ########### ########### ###########

    def elapseTime(self, gameState: busters.GameState):
        """
        Предсказывает степени уверенности агента в отношении позиций призраков
            в ответ на один шаг призрака, совершаемый из текущего состояния
                
        Модель перехода не обязательно стационарна: она может зависеть
            от текущей позиции Пакмана. Однако, это не проблема, т.к. 
            позиция Пакмана известна.
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # новое распределение
        newBeliefs = DiscreteDistribution()

        # перебор каждой возможной позиции призрака
        for oldPos in self.allPositions:
            # вероятность что призрак был именно тут
            oldProb = self.beliefs[oldPos]

            # список новых позиций и шансы перехода в них
            newPosDist = self.getPositionDistribution(gameState, oldPos)

            # перебор вариантов куда призрак мог шагнуть дальше и расчёт вероятностей
            for newPos in newPosDist.keys():
                newBeliefs[newPos] += oldProb * newPosDist[newPos]

        # нормализация распределения и сохранение
        newBeliefs.normalize()
        self.beliefs = newBeliefs

        "*** КОНЕЦ ВАШЕГО КОДА ***"
        

    def getBeliefDistribution(self):
        return self.beliefs


class ParticleFilter(InferenceModule):
    """
    Фильтр частиц для приближенного отслеживания одного призрака
    """
    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles
    
    ########### ########### ###########
    ########### Задание 9   ###########
    ########### ########### ###########

    def initializeUniformly(self, gameState: busters.GameState):
        """
        Инициализирует список частиц self.particles. Частицы должны быть
            равномерно (не случайно) распределены по допустимым позициям. 
        Использует self.numParticles для хранения числа частиц, 
            а self.legalPositions для хранения допустимых позиций частиц. 
        """

        # список частиц
        self.particles = []

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # определение числа частиц
        particle_num = self.numParticles

        # определение допустимых позиций частиц
        legal = self.legalPositions;

        # расширение списка частиц
        for i in range(int(particle_num / len(legal))):
            self.particles.extend(legal)

        "*** КОНЕЦ ВАШЕГО КОДА ***"
        

    def getBeliefDistribution(self):
        """
        Метод преобразует список частиц в соответствующее 
            распределение степеней уверенности. Метод должен возвращать 
            нормализованное распределение типа DiscreteDistribution.
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # дискретное распределение
        beliefDist = DiscreteDistribution()

        # подсчёт числа частиц в каждой позиции
        for pos in self.particles:
            beliefDist[pos] = beliefDist[pos] + 1

        # нормализация
        beliefDist.normalize()

        "*** КОНЕЦ ВАШЕГО КОДА ***"

        return beliefDist
        
    
    ########### ########### ###########
    ########### ЗАДАНИЕ 10  ###########
    ########### ########### ###########

    def observeUpdate(self, observation: int, gameState: busters.GameState):
        """
        Обновление списка частиц с учетом весов наблюдений. 
        Наблюдение - это зашумленное манхеттенское расстояние
            до отслеживаемого призрака.
        Имеется специальный случай, который необходимо учесть. Когда все 
            частицы получают нулевой вес, список частиц слудует повторно
            инициализировать, вызвав initializeUniformly.
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # позиции Пакмана и тюрьмы
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()

        # дискретное распределение
        weightsDist = DiscreteDistribution()

        # поиск суммы весов для каждой позиции
        for pos in self.particles:
            observationProb = self.getObservationProb(observation, pacmanPosition, pos, jailPosition)
            weightsDist[pos] += observationProb

        # ОСОБЫЙ СЛУЧАЙ - у всех частиц нулевой вес
        if weightsDist.total() == 0:
            # повторная инициализация
            self.initializeUniformly(gameState)
            return

        # нормализация и сохранение
        weightsDist.normalize()
        self.particles = [weightsDist.sample() for _ in range(int(self.numParticles))]

        "*** КОНЕЦ ВАШЕГО КОДА ***"
        
    
    ########### ########### ###########
    ########### Задание 11  ###########
    ########### ########### ###########

    def elapseTime(self, gameState):
        """
        Выполняет выборку следующего состояния каждой частицы на основе
            её текущего состояния и состояния игры
        """

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
       
        elapseDist = DiscreteDistribution()

        # распределение новых позиций частиц
        for pos in self.particles:
            newPosDist = self.getPositionDistribution(gameState, pos)
        
            # сумма вероятностей нахождения частицы в каждой новой позиции
            for newPos, prob in newPosDist.items():
                elapseDist[newPos] += prob

        # нормализация и формирование нового списка частиц
        elapseDist.normalize()
        self.particles = [elapseDist.sample() for _ in range(int(self.numParticles))]

        "*** КОНЕЦ ВАШЕГО КОДА ***"
        

