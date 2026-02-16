# qlearningAgents.py
# ------------------
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



#########################################
from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from backend import ReplayMemory

import model
import backend
import gridworld


import random,util,math
import numpy as np
import copy


class QLearningAgent(ReinforcementAgent):
    """
      Агент с Q-обучением

      Функции, которые необходимо дополнить:   
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      
      Переменные, к которым у вас есть доступ
        - self.epsilon (вероятность исследования)
        - self.alpha (скорость обучения)
        - self.discount (коэффициент дисконтирования)

       Фукнции, которые Вам следует использовать
        - self.getLegalActions(state)
          возвращает допустимые действия в состоянии state
          
    """
    def __init__(self, **args):
        "Инициализация  Q-ценностей"
        ReinforcementAgent.__init__(self, **args)

        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        self.values = util.Counter() # Counter - словарь q ценностей, по умолчанию содержит 0
        "*** КОНЕЦ ВАШЕГО КОДА ***"
        self.qVals = {}
        self.eval = False

    def getQValue(self, state, action):
        """
          Возвращает Q(state,action)
          Должен вернуть 0.0, если состояние никогда не встречалось
          или  Q-ценность  в ином случае
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        return self.values[(state, action)]
        #util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Возвращает ценность состояния state путем вычисления
          max_action Q(state,action), где  
          максимум ищется по всем допустимым действиям.
          Если нет допустимых действий,
          что имеет место в терминальных состояних,
          метод должен вернуть значение 0.0
          
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        # если состояние не имеет допустимых действий, возвращаем 0
        if len(self.getLegalActions(state)) == 0:
            return 0

        Qvalue_state = []
        # для всех допустимых действий
        for action in self.getLegalActions(state):
            # извлекаем q-ценности состояний и добавляем их в список
            Qvalue_state.append(self.getQValue(state, action))
        # возвращаем ценность состояния state
        return max(Qvalue_state)
        
        #util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
         Вычисляет лучшее действие, которое нужно предпринять в состоянии.
         Обратите внимание, если нет допустимых действий, что имеет место
         в терминальных состояниях, метод должен вернуть None.
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
          # если состояние не имеет допустимых действий, возвращаем None
        if len(self.getLegalActions(state)) == 0:
            return None
        # вычисляем максимальную q-ценность для state
        bestQ = self.computeValueFromQValues(state)
        bestActions = []
        # для всех допустимых действий 
        for action in self.getLegalActions(state):
            #находим лучшие действия и помещаем их в список bestActions
            if bestQ == self.getQValue(state, action):
                bestActions.append(action)
        # выбираем случайное действие среди лучших из bestActions
        return random.choice(bestActions)
        #util.raiseNotDefined()

    def getAction(self, state):
        """
          Возвращает действие, которое нужно предпринять в текущем состоянии.
          С вероятностью self.epsilon предпринимается случайное действие
          и в противном случае предпринимается наилучшее  действие.
          Обратите внимание, что если нет никаких допустимых действий,
          что имеет место в терминальном состоянии, вы должны 
          вернуть в качестве действия None.

           ПОДСКАЗКА: вы можете использовать util.flipCoin(prob)
           ПОДСКАЗКА: для случайного выбора из списка используйте random.choice (list) 
          
        """
        # Получаем список допустимых действий
        legalActions = self.getLegalActions(state)
        action = None
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # подбрасываем монетку
        if util.flipCoin(self.epsilon):
            #  с вероятностью epsilon выбираем случайное действие
            action = random.choice(legalActions)
        else:
            # иначе выбираем лучшее действие
            action = self.computeActionFromQValues(state)
        
        #util.raiseNotDefined()

        return action

   
    def update(self, state, action, nextState, reward: float):    
        """
                   
          Выполняет шаг обновления q-ценностей
          в соответствии с алгоритмом q-обучения при 
          переходе:
          state => action => nextState =>reward.
          
          ПРИМЕЧАНИЕ: вы никогда не должны вызывать этот метод 
        
        """
      
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        # q-обучение q(s,a)=(1-alpha)*q(s,a)+alpha*(r+gamma*max_a'(q(s',a'))
        self.values[(state, action)] = (1 - self.alpha)* self.values[(state,action)]\
                                       + self.alpha*(reward + self.discount * self.getValue(nextState))
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       Агент Q-обучения с аппроксимацией
       
       Вам нужно только переопределить getQValue
        и update.  Все другие функции QLearningAgent 
       должны работать без изменнения.
       Также, при желании, допишите метод final(self, state),
       чтобы отображать итоговые значения весов признаков и
       такие параметры как: alpha, epsilon, gamma,
       число эпизодов обучения.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights # веса признаков

    def getQValue(self, state, action):
        """
          Должен возвращать Q(state,action) = w * featureVector
          где * оператор матричного умножения
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        # извлекаем признаки q-состояния
        self.features = self.featExtractor.getFeatures(state, action)
        total = 0
        # для каждого из признаков
        for i in self.features:
            # суммируем взвешенные  признаки 
            total += self.features[i] * self.weights[i]
        # возращаем сумму признаков взвешенных с весами weights
        return total
        #util.raiseNotDefined()

  
    def update(self, state, action, nextState, reward: float):
        """
           Обновляет веса признаков на основе данных переходов (s,a,s',r)
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        # diff=(r+gamma*V(s'))-q(s,a))
        diff = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        # извлекаем признаки q-состояния
        features = self.featExtractor.getFeatures(state, action)
        # для каждого из признаков fi(s,a)
        for i in features:
            # обновляем его вес
            # w <-- w + alpha*diff*fi(s,a)
            self.weights[i] = self.weights[i] + self.alpha * diff * features[i]
        #util.raiseNotDefined()

    def final(self, state):
        "Вызывается в конце игры"

        # вызов метода final супер-класса
        PacmanQAgent.final(self, state)

        # проверяем, завершилось ли обучение?
        if self.episodesSoFar == self.numTraining:
            # здесь, если захотите, вы можете распечатать веса при отладке
           
            "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
            print("Итоги Q-обучения с аппроксимацией")
            print("Скорость обучения(alpha) : {0}".format(self.alpha))
            print("Дисконтирование(gamma) : {0}".format(self.discount))
            print("Вероятность исследования (epsilon) : {0}".format(self.epsilon))
            print("Эпизодов обучения : {0}".format(self.numTraining))
            print("=======Веса признаков=======")
            for i in self.features:
                print("{0} : {1}".format(i, self.weights[i]))
            
            pass
