
"""
Модули и функции, которые вам следует использовать.
Пожалуйста, избегайте импорта любых других функций или модулей Torch.
Ваш код не пройдет автооценивание, если будут обнаружены изменения импортов
"""

from torch.nn import Module
from torch.nn import  Linear
from torch import tensor, double, optim
from torch.nn.functional import relu, mse_loss

class DeepQNetwork(Module):
    """
    Модель глубокой нейросети для
    аппроксимации функции ценности Q(s,a) .
    
    state_dim - размер входного вектора состояний
    action_dim - кол-во действий
    self.learning_rate - скорость обучения нейросети
    self.numTrainingGames - кол-во обучающих игр
    self.batch_size - размер миниблока
    """
    
    def __init__(self, state_dim, action_dim):
        self.num_actions = action_dim 
        self.state_size = state_dim 
        super(DeepQNetwork, self).__init__()
        
        # Незабудьте определить self.learning_rate,
        # self.numTrainingGames и self.batch_size!
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        self.learning_rate = 0.000025
        self.numTrainingGames = 2100
        self.batch_size =25 
        
        # кол-во нейронов скрытых слоев
        H1=414
        H2=250
        H3=40
        # слои нейросети
        self.layer1=Linear(self.state_size,H1)
        self.layer2=Linear(H1,H2)
        self.layer3=Linear(H2,H3)
        self.layer4=Linear(H3,self.num_actions)
        # оптимизатор
        #self.optimizer=optim.SGD(self.parameters(),lr=self.learning_rate)
        self.optimizer = optim.Adam(self.parameters(),lr=self.learning_rate)
       
        "*КОНЕЦ ВАШЕГО КОДА"""
        self.double()
 
    def forward(self, states):
        """
        Метод реализует прямое распространение состояний по сети.
        Сеть принимает состояния states и возвращает для каждого
        состояния Q-значения для всех num_actions действий,которые
        могут быть выполнены.
        
        Входные данные:
            states- тензор состояний размером (batch_size x state_dim) 
        Выходные данные:
            Тензор оценок Q-значений  размером (batch_size x num_actions)        
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        x=relu(self.layer1(states))
        x=relu(self.layer2(x))
        x=relu(self.layer3(x))
        x=self.layer4(x)
        return x
    
    def run(self, states):
        # Метод необходим для совместимости кода с другими модулями
        return self.forward(states)
    
    def get_loss(self, states, Q_target):
        """
        Возвращает средний квадрат ошибок между  предсказанными
        значениями Q-ценностей нейросетью и целевым значением Q_target.
        Входные данные:
            states- тензор состояний размером (batch_size x state_dim) 
            Q_target: тензор целевых значений Q-ценностей
            размером (batch_size x num_actions) или None
        Выходные данные:
            Средний квадрат ошибок между предсказаниями Q и Q_target
        """
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        q_pred=self.forward(states)
        mse= mse_loss(q_pred,Q_target)
        #print('mse=', mse.detach().numpy())
        return mse

    def gradient_update(self, states, Q_target):
        """
        Обновляет параметры нейросети на одном шаге оценки 
        градиента с помощью optimizer.step().
        Просмотрите ЛР по машинному обучению, чтобы вспомнить
        как это сделать.Но обратите внимание, что здесь вместо
        того,чтобы перебирать весь набор данных, вы должны 
        выполнить только один шаг обучения нейросети.
        Входные данные:
            states- тензор состояний размером (batch_size x state_dim) 
            Q_target: тензор целевых значений Q-ценностей
            размером (batch_size x num_actions) или None
        Выходные данные:
            None
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
   
        loss=self.get_loss(states, Q_target)
        self.optimizer.zero_grad
        loss.backward()
        self.optimizer.step()
       
        
        
        