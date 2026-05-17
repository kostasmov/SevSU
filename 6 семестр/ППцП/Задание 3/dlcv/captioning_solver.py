from __future__ import print_function, division
from builtins import range
from builtins import object
import numpy as np

from dlcv import optim
from dlcv.coco_utils import sample_coco_minibatch


class CaptioningSolver(object):
    """
    CaptioningSolver инкапсулирует всю логику, необходимую для обучения
    модели нейросети для формирования подписей к изображениям. 
    CaptioningSolver выполняет стохастический градиентный спуск, используя различные
    правила обновления, определенные в optim.py.

    Решатель принимает как данные обучения, так и вадидационные данные, а также метки,
    поэтому он может периодически проверять точность классификации как данных обучения, так и
    валидационных данных, чтобы не допустить переобучения.
    
    Чтобы обучить модель, вы сначала создадите экземпляр CaptioningSolver,
    передав модель, набор данных и различные параметры (скорость обучения, 
    размера пакета и т. д.) конструктору. Затем вы вызовете метод train(),
    чтобы запустить процедуру оптимизации и обучения модели.

    После того как метод train() выполнится, model.params будет содержать наилучшие 
    параметры, которые подверждены проверкой на валидационном множестве в ходе обучения.
    Кроме того, переменная  solver.loss_history будет содержать список всех потерь, вычисляемых
    во время обучения, а переменные solver.train_acc_history и solver.val_acc_history будут
    списками, содержащими точность обучения модели и валижационную точность на каждой эпохе.

    Пример использования класса может выглядеть примерно так:

    data = load_coco_data()
    model = MyAwesomeModel(hidden_dim=100)
    solver = CaptioningSolver(model, data,
                    update_rule='sgd',
                    optim_config={
                      'learning_rate': 1e-3,
                    },
                    lr_decay=0.95,
                    num_epochs=10, batch_size=100,
                    print_every=100)
    solver.train()


    CaptioningSolver работает с объектом модели, который должен соответствовать 
    следующему API:

    - model.params должен быть словарем, сопоставляющим имена строковых параметров 
      с массивами numpy, содержащими значения параметров.

    - model.loss(features, captions) должна быть функцией, вычисляющей
      потери во время обучения и градиенты, её входные и выходные данные:

      Входы:
      - features: массив признаков изображений, форма (N, D)
      - captions: массив заголовков для этих изобажений, форма (N, T), где
        каждый элемент имеет значение в диапазоне (0, V].

      Вазвращает:
      - loss: скалярные потери
      - grads: словарь с теми же ключами, которые имеются в  self.params; связывает имена
        параметров с градиентами функции потерь по отношению к этим парметрам.
    """

    def __init__(self, model, data, **kwargs):
        """
        Конструктор класса CaptioningSolver.

        Входные аргументы:
        - model: объектная модель с API, описанным вышеe
        - data: словарь с обучающими и валидационными данными, возвращаемый load_coco_data

        Необязательные аргументы:
        - update_rule: Строка, задающая имя правила обновления в optim.py.
          По умолчанию — "sgd".
        - optim_config: 
          Словарь, содержащий гиперпараметры, которые будут переданы в выбранное 
          правило обновления. Для каждого правила обновления требуются разные 
          гиперпараметры (см. optim.py), но для всех правил обновления требуется
          параметр "learning_rate", поэтому он всегда должен присутствовать.
        - lr_decay: Коэффициент снижения скорости обучения; после каждой эпохи 
          скорость обучения умножается на это значение.
        - batch_size: Размер мини-блока, используемый при вычичлении потерь и градиентов во время
           обучения.
        - num_epochs: Количество эпох обучения.
        - print_every: Целое число; потери обучения будут печататься через каждые print_every итераций.
        - verbose: Логическое значение; если установлено значение false, то во время обучения печать не будет осуществляться.
        """
        self.model = model
        self.data = data

        # Unpack keyword arguments
        self.update_rule = kwargs.pop('update_rule', 'sgd')
        self.optim_config = kwargs.pop('optim_config', {})
        self.lr_decay = kwargs.pop('lr_decay', 1.0)
        self.batch_size = kwargs.pop('batch_size', 100)
        self.num_epochs = kwargs.pop('num_epochs', 10)

        self.print_every = kwargs.pop('print_every', 10)
        self.verbose = kwargs.pop('verbose', True)

        # Throw an error if there are extra keyword arguments
        if len(kwargs) > 0:
            extra = ', '.join('"%s"' % k for k in list(kwargs.keys()))
            raise ValueError('Unrecognized arguments %s' % extra)

        # Make sure the update rule exists, then replace the string
        # name with the actual function
        if not hasattr(optim, self.update_rule):
            raise ValueError('Invalid update_rule "%s"' % self.update_rule)
        self.update_rule = getattr(optim, self.update_rule)

        self._reset()


    def _reset(self):
        """
        Настраивает некоторые переменные  для оптимизации. Не вызывайте этот
        метод вручную.
        """
        # Set up some variables for book-keeping
        self.epoch = 0
        self.best_val_acc = 0
        self.best_params = {}
        self.loss_history = []
        self.train_acc_history = []
        self.val_acc_history = []

        # Make a deep copy of the optim_config for each parameter
        self.optim_configs = {}
        for p in self.model.params:
            d = {k: v for k, v in self.optim_config.items()}
            self.optim_configs[p] = d


    def _step(self):
        """
        Выполняет шаг обновления градиента. Он вызывается функцией train() и не должен вызываться вручную.
        """
        # Make a minibatch of training data
        minibatch = sample_coco_minibatch(self.data,
                      batch_size=self.batch_size,
                      split='train')
        captions, features, urls = minibatch

        # Compute loss and gradient
        loss, grads = self.model.loss(features, captions)
        self.loss_history.append(loss)

        # Perform a parameter update
        for p, w in self.model.params.items():
            dw = grads[p]
            config = self.optim_configs[p]
            next_w, next_config = self.update_rule(w, dw, config)
            self.model.params[p] = next_w
            self.optim_configs[p] = next_config


    def check_accuracy(self, X, y, num_samples=None, batch_size=100):
        """
        Проверяет точность модели по предоставленным данным.

        Входы:
        - X: Массив данных, форма (N, d_1, ..., d_k)
        - y: AМассив меток, форма (N,)
        - num_samples: Если не None,то делает подвыборку данных и тестирует  модель
           на точках данных из num_samples.
        - batch_size: Разбивает X and y на мини-блоки размера batch_size.

        Возвращает:
        - acc: Скаляр, указывающий долю примеров, которые были правильно
          классифицированы моделью.
        """
        return 0.0

        # Maybe subsample the data
        N = X.shape[0]
        if num_samples is not None and N > num_samples:
            mask = np.random.choice(N, num_samples)
            N = num_samples
            X = X[mask]
            y = y[mask]

        # Compute predictions in batches
        num_batches = N / batch_size
        if N % batch_size != 0:
            num_batches += 1
        y_pred = []
        for i in range(num_batches):
            start = i * batch_size
            end = (i + 1) * batch_size
            scores = self.model.loss(X[start:end])
            y_pred.append(np.argmax(scores, axis=1))
        y_pred = np.hstack(y_pred)
        acc = np.mean(y_pred == y)

        return acc


    def train(self):
        """
        Выполняет оптимизацию и обучение модели.
        """
        num_train = self.data['train_captions'].shape[0]
        iterations_per_epoch = max(num_train // self.batch_size, 1)
        num_iterations = self.num_epochs * iterations_per_epoch

        for t in range(num_iterations):
            self._step()

            # Maybe print training loss
            if self.verbose and t % self.print_every == 0:
                print('(Итерация %d / %d) потери: %f' % (
                       t + 1, num_iterations, self.loss_history[-1]))

            # At the end of every epoch, increment the epoch counter and decay the
            # learning rate.
            epoch_end = (t + 1) % iterations_per_epoch == 0
            if epoch_end:
                self.epoch += 1
                for k in self.optim_configs:
                    self.optim_configs[k]['learning_rate'] *= self.lr_decay

