
import model
from qlearningAgents import PacmanQAgent
from backend import ReplayMemory
import layout
import copy
import torch
import numpy as np


class PacmanDeepQAgent(PacmanQAgent):
    def __init__(self, layout_input="smallGrid", target_update_rate=300, doubleQ=False, **args):
        PacmanQAgent.__init__(self, **args)
        self.model = None
        self.target_model = None
        self.target_update_rate = target_update_rate
        self.update_amount = 0
        self.epsilon_explore = 1.0
        self.epsilon0 = 0.05 #0.4
        self.epsilon = self.epsilon0
        self.discount = 0.8  #0.9
        self.update_frequency = 1
        self.counts = None
        self.replay_memory = ReplayMemory(50000)
        self.min_transitions_before_training = 10000
        self.td_error_clipping = None
        
        self.alpha1=0.2 # скорость Q-обучения

        # Инициализация сетей DQN:
        if isinstance(layout_input, str):
            layout_instantiated = layout.getLayout(layout_input)
        else:
            layout_instantiated = layout_input
        self.state_dim = self.get_state_dim(layout_instantiated)
        self.initialize_q_networks(self.state_dim)

        self.doubleQ = doubleQ   # Флаг режима двойного Q-обучения 
        if self.doubleQ:
            self.target_update_rate = -1

    def get_state_dim(self, layout):
        """
        Метод определяет размер вектора состояния
        """
        pac_ft_size = 2
        ghost_ft_size = 2 * layout.getNumGhosts()
        food_capsule_ft_size = layout.width * layout.height
        return pac_ft_size + ghost_ft_size + food_capsule_ft_size

    def get_features(self, state):
        """
        Метод извлекает описание вектора состояния (признаки состояния)
        """
        pacman_state = np.array(state.getPacmanPosition())
        ghost_state = np.array(state.getGhostPositions())
        capsules = state.getCapsules()
        food_locations = np.array(state.getFood().data).astype(np.float32)
        for x, y in capsules:
            food_locations[x][y] = 2
        return np.concatenate((pacman_state, ghost_state.flatten(), food_locations.flatten()))

    def initialize_q_networks(self, state_dim, action_dim=5):
        """
        Выполняет инициализацию двух одинаковых экземпляров нейросетей 
        """
        self.model = model.DeepQNetwork(state_dim, action_dim)         # предсказательная сеть
        self.target_model = model.DeepQNetwork(state_dim, action_dim)  # целевая сеть

    def getQValue(self, state, action):
        """
           Метод возвращает значение Q(state,action), предсказанное self.model 
        """
        feats = self.get_features(state)
        legalActions = self.getLegalActions(state)
        action_index = legalActions.index(action)
        state = torch.tensor(np.array([feats]).astype("float64"), dtype=torch.double)
        return self.model.run(state).data[0][action_index]


    def shape_reward(self, reward):
        """
        Масштабирование наград
        """
        if reward > 100:
            reward = 10
        elif reward > 0 and reward < 10:
            reward = 2
        elif reward == -1:
            reward = 0
        elif reward < -100:
            reward = -10
        return reward


    def compute_q_targets(self, minibatch, network = None, target_network=None, doubleQ=True):
        """Вычисляет целевые Q-ценности  = r+ max_a'{Q(s',a')} для
        алгоритмов двойного Q-обучения или DDQN        
        Вход:
            minibatch (List[Transition]): миниблок из переходов (s,a,s',r, done);
            network : нейросеть предсказания;
            target_network : целевая нейросеть;
        Возвращает:
             целевые значения Qt(s,a) ценности (float)
        """
        # определяем 2 сети: network=model и target_network=target_model,
        # если не передали их через входные параметры
        if network is None:
            network = self.model
        if target_network is None:
            target_network = self.target_model
        
        #извлекаем из миниблока состояния   batch_size x state_dim  
        states = np.vstack([x.state for x in minibatch])
        #print('states=',states.shape, states[0])
        states = torch.tensor(states, dtype=torch.double)
        
        #извлекаем из миниблока действия (a) и награды (r) для состояния (s): batch_size x 1 
        actions = np.array([x.action for x in minibatch])
        rewards = np.array([x.reward for x in minibatch])
        
        # извлекаем из миниблока новые состояния(s') и метки завершений (done)
        next_states = np.vstack([x.next_state for x in minibatch])
        next_states = torch.tensor(next_states)
        done = np.array([x.done for x in minibatch])
        
        # вычисляем предсказание Qp(s) с помощью сети network: batch_size x num_actions
        Q_predict = network.run(states).data.detach().numpy() 
        # Копируем Qp(s) в Qt(s) 
        Q_target = np.copy(Q_predict)
      
        # вычисляем бонус для состояний, которые реже посещались (функция разведки)
        state_indices = states.int().detach().numpy()
        state_indices = (state_indices[:, 0], state_indices[:, 1]) # кортежи позиций (x,y) Пакмана
        exploration_bonus = 1 / (2 * np.sqrt((self.counts[state_indices] / 100)))

        replace_indices = np.arange(actions.shape[0]) #диапазон номеров строк миниблока
        # находим индексы лучших действий a* для Qp(s',a')
        action_indices = np.argmax(network.run(next_states).data, axis=1) # batch_size x 1
        # вычисляем целевые значения q-ценностей = r+bonus+(1-done)*gamma*Qt(s',a*) с помощью целевой сети
        target = rewards + exploration_bonus + (1 - done) * self.discount * target_network.run(next_states).data[replace_indices, action_indices].detach().numpy()
        
        # обновляем Qt-значения
        Q_target[replace_indices, actions] = target
        
        # 1. вариант классического Q-обновления
        # Qt(s,a)=Qp+alpha*(target-Qp(s,a))
        #Q_target = Q_predict + self.alpha1*(Q_target - Q_predict) #new batch_size x num_actions
       
        # 2. вариант Q-обновления с операцией клиппирования
        # Qt(s,a)=Qp+clip(target-Qp(s,a))
        # Если self.td_error_clipping==None, то передается просто Q_target
        if self.td_error_clipping is not None:
            Q_target = Q_predict + np.clip(Q_target - Q_predict, -self.td_error_clipping, self.td_error_clipping)
            

        return Q_target

    def update(self, state, action, nextState, reward):
        """
        
        Метод реализует модификации либо алгоритма двойного Q-обучения (doubleQ=True), 
        либо алгоритма двойного обучения глубокой нейросети (DDQN) (doubleQ=False) 
        Переменные:
            minibatch (List[Transition]): миниблок из переходов (s,a,s',r, done);
            self.model: нейросеть предсказания;
            self.target_model : целевая нейросеть;
            self.doubleQ : флаг режима двойного Q-обучения (Если doubleQ=False, то режим DDQN)                                                     
        Возвращает:
             выполняет один шаг обучения нейросетей, в ходе которого настраивает их параметры 
        """
              
        # находим индексы действий (a) в состоянии (s)
        legalActions = self.getLegalActions(state)
        action_index = legalActions.index(action)
        # определяем является ли s' проигрышным/выигрышным состоянием
        done = nextState.isLose() or nextState.isWin()
        # масштабируем награды
        reward = self.shape_reward(reward)
        
        # инициaлизируем счетчик числа посещений позиций (x,y)
        if self.counts is None:
            x, y = np.array(state.getFood().data).shape
            self.counts = np.ones((x, y))
        
        # извлекаем признаки описания состояний s и s'
        state = self.get_features(state)
        nextState = self.get_features(nextState)
        # для состояния s увеличиваем счетчик посещений на +1
        self.counts[int(state[0])][int(state[1])] += 1
        
        #формируем выборку (s,a,r,s', done)
        transition = (state, action_index, reward, nextState, done)
        # записываем выборку в память воспроизведения опыта
        self.replay_memory.push(*transition)
        
        # управляем параметром epsilon:
        # если объем памяти воспроизведения опыта < заданного объема для начала обучения (10000)
        if len(self.replay_memory) < self.min_transitions_before_training:
            # то выполняем разведку epsilon=1 (выбираем случайное действие)
            self.epsilon = self.epsilon_explore
        else:
            # иначе epsilon= epsilon0*(1-update_amount/20000), после 20000 обновлений epsilon=0
            self.epsilon = max(self.epsilon0 * (1 - self.update_amount / 20000), 0)

        # если объем памяти воспроизведения опыта > заданного объема для начала обучения (10000) и
        # число обновлений кратно update_frequency 
        if len(self.replay_memory) > self.min_transitions_before_training and self.update_amount % self.update_frequency == 0:
            # извлекаем из памяти опыта миниблок из выборок (s,a,s',r,done)  размером batch_size
            minibatch = self.replay_memory.pop(self.model.batch_size)
            states = np.vstack([x.state for x in minibatch])
            states = torch.tensor(states.astype("float64"), dtype=torch.double)
            # вычисляем  целевое значение Qt1(s,a)
            Q_target1 = self.compute_q_targets(minibatch, self.model, self.target_model, doubleQ=self.doubleQ)
            Q_target1 = torch.tensor(Q_target1.astype("float64"), dtype=torch.double)
   
            # если задан алгоритм двойного Q-обучения (doubleQ=True), то вычисляем Qt2(s,a) для второй сети
            if self.doubleQ:
                Q_target2 = self.compute_q_targets(minibatch, self.target_model, self.model, doubleQ=self.doubleQ)
                Q_target2 = torch.tensor(Q_target2.astype("float64"), dtype=torch.double)
                
            # обучаем сеть model 
            self.model.gradient_update(states, Q_target1)
            # обучаем сеть target_model 
            if self.doubleQ:
                self.target_model.gradient_update(states, Q_target2)
        
        # Если выбран алгоритм двойного DQN и если число обновлений кратно 300
        if self.target_update_rate > 0 and self.update_amount % self.target_update_rate == 0:
            # то просто копируем параметры сети model в сеть target_model
            self.target_model.load_state_dict(self.model.state_dict())
            #self.target_model = copy.deepcopy(self.model)
            
        self.update_amount += 1

    def final(self, state):
        """Called at the end of each game."""
        PacmanQAgent.final(self, state)
