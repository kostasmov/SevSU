from torch import no_grad, stack
from torch.utils.data import DataLoader
from torch.nn import Module

"""
Функции, которые вам следует использовать.
Пожалуйста, не импортируйте любые другие функции или модули Torch.
Ваш код не пройдет проверку, если autograder обнаружит какое-либо измененение
строк импорта
"""

from torch.nn import Parameter, Linear
from torch import optim, tensor, tensordot, empty, ones
from torch.nn.functional import cross_entropy, relu, mse_loss
from torch import movedim


class PerceptronModel(Module):
    def __init__(self, dimensions):
        """
        Инициализирует новый экземпляр класса PerceptronModel.

        Персептрон классифицирует точки данных как принадлежащие определенному
            классу (+1) или нет (-1). `dimensions` — это размерность данных.
        Например, dimensions=2 будет означать, что персептрон должен классифицировать
            2D-точки.

        Чтобы автогрейдер (autograder) мог идентфицировать веса, инициализируйте
            их как объект pytorch Parameter следующим образом:

        Parameter(weight_vector),

        где weight_vector — это тензор pytorch размерности 'dimensions'.

        Подсказка: можно использовать ones(dim) для создания тензора размерности dim.
        """

        super(PerceptronModel, self).__init__()
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        # инициализация весов персептрона
        self.w = Parameter(ones(1, dimensions))

    def get_weights(self):
        """
        Возвращает экземпляр Parameter с текущими весами персептрона.
        """
        return self.w

    def run(self, x):
        """
        Вычисляет оценку n=x*w, назначенную персептроном точке данных x.

        Входные данные:
            x: вектор с формой (1 x dimensions)
        Возвращает: одно число (оценку)

        Здесь может быть полезна функция pytorch `tensordot`.
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        # вычисление скалярного произведения вектора весов и вектора входа
        return tensordot(x, self.w, dims=([1], [1]))


    def get_prediction(self, x):
        """
        Вычисляет прогнозируемый класс пинадлежности одной точки данных `x`.

        Возвращает: 1 или -1
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
    
        return 1 if self.run(x).item() >= 0 else -1 

    def train(self, dataset):
        """
        Обучение персептрона до сходимости.
        
        Выполняйте итерации по данным с помощью DataLoader, чтобы
            извлекать порции данных, на которых нужно обучаться.

        Каждая выборка  данных dataloader имеет вид {'x': features, 'label': label}, где 
            label — истинная метка данных, которую нужно предсказать на основе признаков x.
        """        

        with no_grad():
            dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
            
            "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
            
            with no_grad():
                converged = False       # флаг сходимости
                while not converged:
                    converged = True
                    for batch in dataloader:    # перебор точек
                        x, y = batch['x'], batch['label']

                        # классификация точки x
                        pred = self.get_prediction(x) 

                        # сравнение с истиной
                        if pred != y.item():
                            self.w += x * y     # если предсказание неверное - корректируем веса
                            converged = False   # обучение продолжается
             

class RegressionModel(Module):
    """
    Модель нейронной сети для аппроксимации функции, которая отображает 
        действительные числа в действительные числа. Сеть должна быть достаточно
        большой, чтобы иметь возможность аппроксимировать sin(x) на интервале
        [-2pi, 2pi] с разумной точностью.
    """
   
    def __init__(self):
        # Здесь инициализируйте параметры вашей модели нейросети
       
        super(RegressionModel,self).__init__()
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        self.fc1 = Linear(1, 200)
        self.fc2 = Linear(200, 200)
        self.fc3 = Linear(200, 1)
        


    def forward(self, x):
        """
        Запускает модель для блока (batch) входных данных.

        Входные данные:
            x: блок данных с формой (batch_size x 1)
        Возвращает:
            блок с формой (batch_size x 1), содержащий прогнозируемые значения y    
        """
               
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        return self.fc3(x)

    
    def get_loss(self, x, y):
        """
        Вычисляет среднеквадратические потери для блока входных данных.

        Входные данные:
            x: блок данных с формой (batch_size x 1)
            y: блок данных с формой (batch_size x 1), содержащий истинные значения y,
            которые будут использоваться для обучения
        Возвращает: тензор размером 1, содержащий потери
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        return mse_loss(self.forward(x), y)
  

    def train(self, dataset):
        """
        Обучение модели.

        Чтобы получить блок данных, создайте объект DataLoader и передайте ему `dataset`, а также требуемый размер блока.
        Просмотрите класс PerceptronModel как руководство по использованию DataLoader

        Каждая выборка dataloader будет иметь вид {'x': features, 'label': label}, где label
        — это истинное значение (метка), которое должна предсказать модель нейросети.

        Входные данные:
            dataset:  набор данных PyTorch, содержащий данные для обучения 
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
       
        dataloader = DataLoader(dataset, batch_size=10, shuffle=True)
        optimizer = optim.Adam(self.parameters(), lr=0.01)

        for epoch in range(100):
            for batch in dataloader:
                x, y = batch['x'], batch['label']
                optimizer.zero_grad()
                loss = self.get_loss(x, y)
                loss.backward()
                optimizer.step()
        

   
class DigitClassificationModel(Module):
    """
    Модель классификации рукописных цифр с использованием набора данных MNIST.

    Каждая рукописная цифра представляет собой изображение в оттенках серого 
     размером 28x28 пикселей, которое преобразовано в 784-мерный вектор для целей 
     этой модели нейросети. Каждый элемент вектора представляет собой число с
     плавающей точкой от 0 до 1.

    Цель состоит в том, чтобы отнести каждую цифру к одному из 10 классов (число от 0 до 9).

    (См. RegressionModel для получения дополнительной информации об API различных
     методов класса. Рекомендуется  реализовать RegressionModel перед
     работой над этим заданием.)
    """
    
    def __init__(self):
        # Здесь инициализируйте параметры вашей модели нейросети
        super().__init__()
        input_size = 28 * 28
        output_size = 10
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        self.fc1 = Linear(input_size, 256)
        self.fc2 = Linear(256, 128)
        self.fc3 = Linear(128, output_size)
    

    def run(self, x):
        """
        Запускает модель для блока входных данных.

        Ваша модель должна формировать предсказание в виде тензора с формой
        (batch_size x 10), который содержит оценки предсказания. Более высокие оценки
        соответствуют большей вероятности принадлежности изображения к 
        определенному классу.

        Входные данные:
            x: тензор с формой (batch_size x 784)
        Выходные данные:
            тензор с формой (batch_size x 10), содержащий предсказанные оценки
            (также называемые логитами)
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        return self.fc3(x)
    
    
    def get_loss(self, x, y):
        """
        Вычисляет потери для блока входных данных.

        Истинные метки `y` представляются в виде тензора с формой
        (batch_size x 10). Каждая строка тензора — это one-hot вектор, кодирующий
        правильный класс изображения цифры (0-9).

        Входные данные:
            x: тензор с формой (batch_size x 784)
            y: тензор с формой (batch_size x 10)
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
        
        logits = self.run(x)
        return cross_entropy(logits, y)
       

    def train(self, dataset):
        """
        Обучение модели.
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
        optimizer = optim.Adam(self.parameters(), lr=0.001)

        for epoch in range(10):
            for batch in dataloader:
                x, y = batch['x'], batch['label']
                optimizer.zero_grad()
                loss = self.get_loss(x, y)
                loss.backward()
                optimizer.step()



ы

        
        
        
def Convolve(input: tensor, weight: tensor):
    """
    Реализуйте двумерную свертку с заданными входами и весами.
    НЕ импортируйте никакие методы pytorch, которые напрямую реализуют свертку.
    Ваша реализация свертка должна быть выполнена только с помощью  уже 
    импортированных функций.

    Есть несколько способов реализовать свертку. Одним из возможных решений 
    является использование  'tensordot'.
    Если вы хотите индексировать тензор, вы можете сделать это следующим образом:

        tensor[y:y+height, x:x+width]

    Это вызов возвращает подтензор, первый элемент которого — tensor[y,x] 
    Подтензор имеет высоту 'height, и ширину 'width'
    """
    input_tensor_dimensions = input.shape
    weight_dimensions = weight.shape
    Output_Tensor = tensor(())
   
    "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

    
    
    "*** КОНЕЦ ВАШЕГО КОДА ***"
    return Output_Tensor



class DigitConvolutionalModel(Module):
    """
    Модель для классификации рукописных цифр с использованием набора данных MNIST.

    Этот класс представляет собой  модель нейросети со сверточным слоем.
    Если Convolve() реализована правильно, эта модель должна быстро достичь  
    заданной точности на наборе данных MNIST .

    """
    

    def __init__(self):
        
        # Здесь инициализируйте параметры вашей модели нейросети
        super().__init__()
        output_size = 10

        self.convolution_weights = Parameter(ones((3, 3)))
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"


    def run(self, x):
        """
       
        Вызов сверточного слоя и преобразование его выхода  в "плоский "вектор 
        уже реализованы.
        Здесь вам следует рассматривать выход сверточного слоя x как обычный блок данных, 
        размером bz x 676, который далее обрабатывается полносвязными слоями, аналогичеыми
        классу DigitClassificationModel.
             
        """
        x = x.reshape(len(x), 28, 28)
        x = stack(list(map(lambda sample: Convolve(sample, self.convolution_weights), x)))
        x = x.flatten(start_dim=1)
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

 

    def get_loss(self, x, y):
        """
        Вычисляет потери для блока входных данных.

        Истинные метки `y` представляются в виде тензора с формой
        (batch_size x 10). Каждая строка тензора — это one-hot вектор, кодирующий
        правильный класс изображения цифры (0-9).

        Входные данные:
            x: тензор с формой (batch_size x 784)
            y: тензор с формой (batch_size x 10)
        Возвращает: тензор потерь
        """
        
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"

        

    def train(self, dataset):
        """
        Обучение модели.
        """
       
        "*** ВСТАВЬТЕ ВАШ КОД СЮДА ***"
 
