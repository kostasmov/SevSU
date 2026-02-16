# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Пожалуйста, просмотрите предварительно learningAgents.py *

         ValueIterationAgent принимает марковский процесс принятия решений
         (см. mdp.py) при инициализации и выполняет итерацию по значениям
         для заданного количества итераций с использованием 
         коэффициента дисконтирования.
        
    """
   
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Ваш агент итераций по значениям должен принимать mdp при
          вызове конструктора, запустите его с указанным количеством итераций,
          а затем действуйте в соответствии с полученной политикой.

           Некоторые полезные методы mdp, которые вы будете использовать:
              mdp.getStates() - возвращает список состояний MDP
              mdp.getPossibleActions(state) - возвращает кортеж возможных действий в состоянии
              mdp.getTransitionStatesAndProbs(state, action)- возвращает список из пар (nextState, prob) - s' и вероятности переходов T(s,a,s')
              mdp.getReward(state, action, nextState) - вовращает награду R(s,a,s')
              mdp.isTerminal(state)- проверяет, является ли состояние терминальным
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # Counter - словарь ценностей состояний, по умолчанию содержит 0
        self.runValueIteration()

    def runValueIteration(self):
        # Напишите код, реализующий итерации по значениям 
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        #для заданного числа итераций
        for i in range(self.iterations):
            #создать копию словаря с ценностями состояний
            updatedValues = self.values.copy()
            #для всех состояний mdp
            for state in self.mdp.getStates():
                #если состояние является терминальным, то переходим к следующему состоянию
                if self.mdp.isTerminal(state):
                    continue
                else:
                    #для нетерминальных состояний
                    #создаем временный список q-ценностей
                    q_state = []
                    #для всех возможных действий в состоянии state
                    for action in self.mdp.getPossibleActions(state):
                        #вычисляем q-ценность пары (state, action)
                        #и добавляем её в список q-state
                        q_state.append(self.getQValue(state, action))
                    #находим максимальную q-ценность, т.е. ценность состояния state
                    #и запоминаем ценность состояния state в словаре 
                    updatedValues[state] = max(q_state)
            #Обновляем значения ценностей состояний объекта на итерации i     
            self.values = updatedValues

    def getValue(self, state):
        """
          Возвращает ценность состояния (вычисляется в  __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Вычисляет Q-ценность в состоянии по
          значению ценности состояния, сохраненному в self.values.
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        Qvalue = 0
        #для пары (state, action) извлекаем из MDP  следующие состояния s' и вероятности перехода prob=T(s,a,s')
        for nextstate, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # вычисляем q-ценность (s,a) с учетом уравнения Беллмана по ценностям всех следующих состояний V(s')
            Qvalue+= prob*(self.mdp.getReward(state, action, nextstate)+self.discount*self.getValue(nextstate))
        return Qvalue
        
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          Определяет политику - лучшее действие в  состоянии
          в соответствии с ценностями, хранящимися в  self.values.

          Обратите внимание, что если нет никаких допустимых действий,
          как в случае  терминального состояния, необходимо вернуть None.
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        #создаем словарь политик
        policy = util.Counter()
        
        #извлекаем действия доступные в состоянии
        temp=self.mdp.getPossibleActions(state)
        # если доступных действий нет, то выход
        if len(temp)==0:
            return None
        #для всех доступных действий в состоянии
        for action in temp:
            #вычислить q-ценность и запомнить в элементе словаря с ключем action
            policy[action] = self.getQValue(state, action)
        #вернуть действие, обеспечивающие максимум q-ценности,т.е. политику
        return policy.argMax()
     
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Возвращает политику в состоянии (без исследования)"
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
         AsynchronousValueIterationAgent принимает марковский процесс принятия решений
         (см. mdp.py) при инициализации и выполняет итерацию по значениям
         для заданного количества итераций с использованием 
         коэффициента дисконтирования.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Ваш агент итераций по значениям должен принимать mdp при
          вызове конструктора, запустите его с указанным количеством итераций,
          а затем действуйте в соответствии с полученной политикой.
          Каждая итерация обновляет значение только одного состояния,
          которое циклически выбирается из списка состояний. 
          Если выбранное состояние является конечным, на этой итерации ничего
          не происходит.


          Некоторые полезные методы mdp, которые вы будете использовать:    
              mdp.getStates() - возвращает список состояний MDP
              mdp.getPossibleActions(state) - возвращает кортеж возможных действий в состоянии
              mdp.getTransitionStatesAndProbs(state, action)- возвращает список из пар (nextState, prob) - s' и вероятности переходов T(s,a,s')
              mdp.getReward(state, action, nextState) - вовращает награду R(s,a,s')
              mdp.isTerminal(state)- проверяет, является ли состояние терминальным
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Напишите код, реализующий асинхронные итерации по значениям 
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        #формируем список состояний MDP
        states = self.mdp.getStates()
        num_states = len(states)
        #для заданного числа итераций
        for i in range(self.iterations):
            #на каждой итерации выбираем из states одно очередное состояние
            #по индексу, который лежит в диапазоне от 0 до num_states
            state = states[i % num_states]
            # если нетерминальное состояние
            if not self.mdp.isTerminal(state):
                #присваиваем начальное значение max_val = -бесконечность
                max_val = float("-inf")
                #для всех возможных действий в состоянии state
                for action in self.mdp.getPossibleActions(state):
                    #вычисляем q-ценность пары (state, action)
                    q_value = self.computeQValueFromValues(state, action)
                    #находим максимальное значение q-ценности (т.е ценности состояния)
                    if q_value > max_val:
                        max_val = q_value
                #сохраняем ценность состояния в словаре self.values
                self.values[state] = max_val
        
        
        
        
        

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        
        Агент PrioritizedSweepingValueIterationAgent принимает марковский
        процесс принятия решения (см. Mdp.py) при инициализации и выполняет 
        итерации по значениям  с разверткой приоритетных состояний при 
        заданном числе  итераций с использованием предоставленных параметров.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Ваш агент итерации по развертке приоритетных значений должен 
          принимать на вход МДП при создании, выполнять заданое количество итераций, 
          а затем действовать в соответствии с полученной политикой.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
       
        # инициализация словаря с элементами в виде
        # состояние-ключ:множество его состояний-предшественников
        predecessors = {}
        
        # для каждого состояния state
        # формируем множество всех его предшествующих состояний
        for state in self.mdp.getStates():
            # если состояние не терминальное
            if not self.mdp.isTerminal(state):
                #  для всех действий из состояния state 
                for action in self.mdp.getPossibleActions(state):
                    # для все следующих состояний nextState после (state,action)
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        # если след. состояние уже есть в словаре predecessors
                        if nextState in predecessors:
                            # то добавляем в множество с ключем nextState его предшественника state
                            predecessors[nextState].add(state)
                        else:
                            # иначе множеству с ключем nextState присваиваем начальное значение {state}
                            predecessors[nextState] = {state}
                            
        # создаем приоритетную очередь                   
        pq = util.PriorityQueue()
        # для каждого состояния state
        for state in self.mdp.getStates():
            # если состояние не терминальное
            if not self.mdp.isTerminal(state):
                values = []
                 #  для всех действий из состояния state 
                for action in self.mdp.getPossibleActions(state):
                    # вычисляем q-ценность пары  (state, action)
                    q_value = self.computeQValueFromValues(state, action)
                    # складируем q-ценности в списке values
                    values.append(q_value)
                # находим абсолютное значение разницы между текущим значением ценности state
                #  в self.values и наивысшим значением Q для всех возможных действий из state
                diff = abs(max(values) - self.values[state])
                # обновляем приоритет state в очереди
                pq.update(state, - diff)
        
        # для заданного числа итераций
        for i in range(self.iterations):
            # если очередь пустая - выход
            if pq.isEmpty():
                break
            # извлекаем очередное состояние с миним. приотетом из очереди
            temp_state = pq.pop()
            # если состояние не терминальное
            if not self.mdp.isTerminal(temp_state):
                values = []
                 #  для всех действий из состояния tempstate 
                for action in self.mdp.getPossibleActions(temp_state):
                    # вычисляем q-ценность пары  (temp_state, action)
                    q_value = self.computeQValueFromValues(temp_state, action)
                     # складируем q-ценности в списке values
                    values.append(q_value)
                # обновляем ценность состояния temp_state в словаре self.values
                self.values[temp_state] = max(values)
            
            # для всех p - предшествуюших состояний temp_state
            for p in predecessors[temp_state]:
                 # если состояние не терминальное
                if not self.mdp.isTerminal(p):
                    values = []
                    #  для всех действий из состояния p 
                    for action in self.mdp.getPossibleActions(p):
                        # вычисляем q-ценность пары  (p, action)
                        q_value = self.computeQValueFromValues(p, action)
                         # складируем q-ценности в списке values
                        values.append(q_value)
                    # находим абсолютное значение разницы между текущим значением ценности p
                    #  в self.values и наивысшим значением Q для всех возможных действий из p
                    diff = abs(max(values) - self.values[p])
                    # если разность превышает порог theta
                    if diff > self.theta:
                        # обновляем приоритет p в очереди
                        pq.update(p, -diff)


