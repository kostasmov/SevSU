from __future__ import print_function, division
from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
import os
import pickle as pickle

import numpy as np

from dlcv import optim


class Solver(object):
    """
    Решатель (solver) инкапсулирует всю логику, необходимую для обучения моделей классификации.
    Solver выполняет стохастический градиентный спуск, используя различные правила обновления,
    определенные в optim.py.

    Решатель принимает данные и метки как для обучения, так и для валидации, поэтому он может 
    периодически проверять точность классификации как на обучающих, так и на валидационных данных,
    чтобы не допустить переобучения.

    Чтобы обучить модель, вы сначала создадите экземпляр (объект) Solver, передав модель, набор данных и 
    различные параметры (скорость обучения, размер пакета и т. д.) конструктору. Затем вы вызовете
    метод train(), чтобы запустить процедуру оптимизации и обучить модель.

    После возврата результатов метода train(),  model.params будет содержать параметры, которые показали
    наилучшие результаты на валидационном множестве данных в ходе обучения. Кроме того, переменная экземпляра
    solver.loss_history будет содержать список всех потерь, вычисляемых в ходе обучения, а переменные экземпляра
    solver.train_acc_history и solver.val_acc_history будут содержать списки точности модели на данных обучения и
    и валидации для каждой эпохи.

    Пример использования класса может выглядеть так:
        
    data = {
      'X_train': # обучающие данные
      'y_train': # обучающие метки
      'X_val': # валидационные данные
      'y_val': # валидационные метки
    }
    model = MyAwesomeModel(hidden_size=100, reg=10)
    solver = Solver(model, data,
                    update_rule='sgd',
                    optim_config={
                      'learning_rate': 1e-3,
                    },
                    lr_decay=0.95,
                    num_epochs=10, batch_size=100,
                    print_every=100)
    solver.train()
    
   Решатель работает с объектом модели и предполагает следующий API:
     - model.params - словарь, отображающий имена параметров-строк в
       массивы numpy, содержащие значения параметров.
     - model.loss(X, y) - функция, которая вычисляет потери и градиенты в ходе обучения,
       и рейтинги в ходе тестирования, её входные и выходные данные:
      
      Входы:
      - X: миниблок входных данных формы (N, d_1, ..., d_k)
      - y: массив меток формы (N,), задающий метки для X, в котором y[i]
        метка для X[i].

      Возращает:
      Если y равен None, то выполняет прямое распространение для этапа тестирования и возвращает:
      - scores: массив формы (N, C), содержащий рейтинги классов из X, где 
        scores[i, c]  соответсвует рейтингу класса c для примера X[i].

      Если y не равен None, то выполняет обучение с использованием прямого и обратного путей
      и возвращает кортеж из:
      - loss: потери
      - grads: словарь с такими же ключами как в словаре  self.params, отображающий имена параметров
        на градиенты функции потерь по отношению к этим параметрам 
    """

    def __init__(self, model, data, **kwargs):
        """
        Создает новый экземпляр (объект) класса Solver.

        Требуемые аргументы:
        - model: объект модели нейросети, соотвествующий API описанному выше
        - data: словарь обучающих и валидационных данных, содержащий
          'X_train': массив обучающих изображений, форма (N_train, d_1, ..., d_k)
          'X_val': массив валидационных изображений, форма (N_val, d_1, ..., d_k)
          'y_train': массив обучающих меток, форма (N_train,)
          'y_val': массив меток для валидации, форма (N_val,)

        Опциональные (необязательные) аргументы:
        - update_rule: строка с именем правила обучения из optim.py.
          Значение по умолчанию - 'sgd'.
        - optim_config: словарь содержащий гиперпараметры, которые будут передаваться 
          выбранному правилу обучения (обновления). Каждое правило обновления требует 
          различные гиперпараметры (см. optim.py), но все правила обновления используют
          параметр скорости обучения 'learning_rate', который должен всегда присутствовать.
        - lr_decay: коэффициент затухания скорости обучения; после каждой эпохи обучения 
          learning rate умножается на значение этого коэффициента.
        - batch_size: размер минимблока (минибэтча), используемого при вычислении потерь и
          градиентов в ходе обучения.
        - num_epochs: число эпох обучения.
        - print_every: целое число; определяет, через сколько итераций будут печаться потери обучения.
        - verbose: логическое значение; если false, то в ходе обучения не будут выводиться промежуточные значения
          некоторых переменных.
        - num_train_samples: число обучающих выборок, используемых для проверки точности обучения; по умолчанию 1000;
          если  None, то используется все обучающее множество.
        - num_val_samples: число валидационных выборок, , используемых для проверки вадидационной точности; по умолчанию
          равно None, что предполагает использование всего валидационного множества.
        - checkpoint_name: Если не None, то сохраняет контрольные точки модели для каждой эпохи.
        """

        self.model = model
        self.X_train = data['X_train']
        self.y_train = data['y_train']
        self.X_val = data['X_val']
        self.y_val = data['y_val']

        # Распаковка ключевых аргументов
        self.update_rule = kwargs.pop('update_rule', 'sgd')
        self.optim_config = kwargs.pop('optim_config', {})
        self.lr_decay = kwargs.pop('lr_decay', 1.0)
        self.batch_size = kwargs.pop('batch_size', 100)
        self.num_epochs = kwargs.pop('num_epochs', 10)
        self.num_train_samples = kwargs.pop('num_train_samples', 1000)
        self.num_val_samples = kwargs.pop('num_val_samples', None)

        self.checkpoint_name = kwargs.pop('checkpoint_name', None)
        self.print_every = kwargs.pop('print_every', 10)
        self.verbose = kwargs.pop('verbose', True)

        # Формирование ошибки, если имеются лишние ключевые аргументы
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
        Установка (инициализация) некоторых переменных. Не вызывайте метод вручную.
        """

        # Инициализация некоторых переменных 
        self.epoch = 0
        self.best_val_acc = 0
        self.best_params = {}
        self.loss_history = []
        self.train_acc_history = []
        self.val_acc_history = []

        # Созданиие глубокой копии optim_config для каждого параметра
        self.optim_configs = {}
        for p in self.model.params:
            d = {k: v for k, v in self.optim_config.items()}
            self.optim_configs[p] = d


    def _step(self):
        """
        Шаг обновления градиеннта. Метод вызывается в train(). Не вызывайте его вручную.
        """

        # Создание миниблока обучающих данных
        num_train = self.X_train.shape[0]
        batch_mask = np.random.choice(num_train, self.batch_size)
        X_batch = self.X_train[batch_mask]
        y_batch = self.y_train[batch_mask]

        # Вычисление потерь и градиента
        loss, grads = self.model.loss(X_batch, y_batch)
        self.loss_history.append(loss)

        # Выполнение обновления параметров
        for p, w in self.model.params.items():
            dw = grads[p]
            config = self.optim_configs[p]
            next_w, next_config = self.update_rule(w, dw, config)
            self.model.params[p] = next_w
            self.optim_configs[p] = next_config


    def _save_checkpoint(self):
        if self.checkpoint_name is None: return
        checkpoint = {
          'model': self.model,
          'update_rule': self.update_rule,
          'lr_decay': self.lr_decay,
          'optim_config': self.optim_config,
          'batch_size': self.batch_size,
          'num_train_samples': self.num_train_samples,
          'num_val_samples': self.num_val_samples,
          'epoch': self.epoch,
          'loss_history': self.loss_history,
          'train_acc_history': self.train_acc_history,
          'val_acc_history': self.val_acc_history,
        }
        filename = '%s_epoch_%d.pkl' % (self.checkpoint_name, self.epoch)
        if self.verbose:
            print('Saving checkpoint to "%s"' % filename)
        with open(filename, 'wb') as f:
            pickle.dump(checkpoint, f)


    def check_accuracy(self, X, y, num_samples=None, batch_size=100):
        """
        Проверка точности модели на предоставленных данных

        Входы:
        - X: массив данных, форма (N, d_1, ..., d_k)
        - y: массив меток, форма (N,)
        - num_samples: Если не None, выбрать подмножество данных и протестировать модель 
          только на  num_samples выборках  данных.
        - batch_size: Разбиваем  X и y на блоки (batches) размера  batch_size, чтобы не допустить использование
          слишком больших объемов памяти.

        Возращает:
        - acc: доля примеров, которые были правильно классифицированы моделью
        """

        # Возможна выборка подмножества данных
        N = X.shape[0]
        if num_samples is not None and N > num_samples:
            mask = np.random.choice(N, num_samples)
            N = num_samples
            X = X[mask]
            y = y[mask]

        # Вычисление предсказаний на миниблоке
        num_batches = N // batch_size
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
        Выполняет оптимизацию для обучения модели
        """
        num_train = self.X_train.shape[0]
        iterations_per_epoch = max(num_train // self.batch_size, 1)
        num_iterations = self.num_epochs * iterations_per_epoch

        for t in range(num_iterations):
            self._step()

            # Печать потерь обучения
            if self.verbose and t % self.print_every == 0:
                print('(Итерация %d / %d) потери: %f' % (
                       t + 1, num_iterations, self.loss_history[-1]))

            # В конце каждой эпохи, увеличение счетчика эпох и
            # уменьшение скорости обучения
            epoch_end = (t + 1) % iterations_per_epoch == 0
            if epoch_end:
                self.epoch += 1
                for k in self.optim_configs:
                    self.optim_configs[k]['learning_rate'] *= self.lr_decay

            # Проверка точности обучения и валидации на первой итерации,на
            # последней итерации и в конце каждой эпохи
            first_it = (t == 0)
            last_it = (t == num_iterations - 1)
            if first_it or last_it or epoch_end:
                train_acc = self.check_accuracy(self.X_train, self.y_train,
                    num_samples=self.num_train_samples)
                val_acc = self.check_accuracy(self.X_val, self.y_val,
                    num_samples=self.num_val_samples)
                self.train_acc_history.append(train_acc)
                self.val_acc_history.append(val_acc)
                self._save_checkpoint()

                if self.verbose:
                    print('(Эпоха %d / %d) точность обучения: %f; валидационная точность: %f' % (
                           self.epoch, self.num_epochs, train_acc, val_acc))

                # Отслеживание и сохранение лучшей модели
                if val_acc > self.best_val_acc:
                    self.best_val_acc = val_acc
                    self.best_params = {}
                    for k, v in self.model.params.items():
                        self.best_params[k] = v.copy()

        # В конце обучения подстановка лучщих парметров в модель
        self.model.params = self.best_params
