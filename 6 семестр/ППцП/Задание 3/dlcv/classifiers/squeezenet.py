import tensorflow as tf

NUM_CLASSES = 1000

class Fire(tf.keras.Model):
    """
     Сверточный модуль "сжатия-расширения"содержит три группы гиперпараметров:
     s1x1  - кол-во фильтров (внутренних карт активностей)  слоя сжатия (squeeze_planes);
     e1x1 и e3x3 – кол-во фильтров в слое расширения (expand1x1_planes, expand3x3_planes).
     При этом  устанавливается s1x1 < (e1x1 + e3x3).
     Поэтому слой сжатия помогает ограничить количество входных каналов для фильтров слоя расширения
     
     Например слой  Fire(64, 16, 64, 64, ) имеет:
     64 – входных канала (оно же число входных плоскостей активности(карт));
     16 – фильтров  в слое сжатия (оно же число внутренних плоскостей активности(карт) или каналов);
     64 – фильтра 1х1 в слое расширения (expand);
     64 – фильтра 3х3 в слое расширения (expand).
     Т.о. число входных каналов для слоя расширения сократилось в 64/16=4 раза,
     Число выходных плоскостей (карт) активностей или каналов 64+64=128.
     Поэтому следующий слой Fire  будет иметь 128 плоскостей на входе, т.е Fire(128,…)
    """
     
    def __init__(self, inplanes, squeeze_planes, expand1x1_planes, expand3x3_planes,name=None):
        #Конструктор, определяющий слои модуля Fire.
        # inplanes, squeeze_planes, expand1x1_planes, expand3x3_planes – соответственно число
        # плоскостей активности на входе, фильтров (плоскостей) сжатия s1x1 и расширения e1x1, e3x3
        super(Fire, self).__init__(name='%s/fire'%name)
        self.inplanes = inplanes
        # Сверточный слой сжатия, применяет фильтр 1х1 (бутылочное горлышо)
        self.squeeze = tf.keras.layers.Conv2D(squeeze_planes, input_shape=(inplanes,), kernel_size=1, strides=(1,1), padding="VALID", activation='relu',name='squeeze')
        # Сверточные слои расширения
        # слой с фильтрами 1х1
        self.expand1x1 = tf.keras.layers.Conv2D(expand1x1_planes, kernel_size=1, padding="VALID", strides=(1,1), activation='relu',name='e11')
        # слой с фильтрами 3х3
        self.expand3x3 = tf.keras.layers.Conv2D(expand3x3_planes, kernel_size=3, padding="SAME", strides=(1,1), activation='relu',name='e33')

    def call(self, x):
        # Определяет схему связи слоев сжатия и расширения 
        x = self.squeeze(x)
        return tf.concat([
            self.expand1x1(x),
            self.expand3x3(x)
        ], axis=3)


class SqueezeNet(tf.keras.Model):
    """
    SqueezeNet: обеспечение точности при малом числе параметров.
    Принципы проектирования архитектуры:
    1. Замена фильтров с размером 3х3 на фильтры с размером 1х1 (в 9 раз меньше параметров);
    2. Сокращение числа входных каналов для фильтров 3х3 за счет введения squeeze-слоёв (слоёв сжатия);
    3. Позднее прореживание (пулинг) , благодаря чему активационные карты ранних слоев имеют большие размеры.
    Большие активационные карты обеспечивают повышение точности классификации.
    
    SqueezeNet начинается с отдельного сверточного слоя (layer0) со strides=2, за которым следуют 8 модулей Fire 
    (layer3,4,6,7,9,10,11,12), в конце сверточный слой с num_classes фильтрами размером 1х1 и глобальный
    усредняющий пулинг. Таким образом, затратный полносвязный слой на выходе не применяется.
    Число фильтров в Fire-модулях увеличивается  от начала к концу сети. 
    SqueezeNet выполняет maxpool с шагом 2 после слоев layer0, layer4, layer7 и layer12.
    Эти относительно поздние размещения пулинга соответствуют принципу 3.
    
    """
    def __init__(self, num_classes=NUM_CLASSES):
        super(SqueezeNet, self).__init__()
        self.num_classes = num_classes

        self.net = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(64, kernel_size=(3, 3), strides=(2,2), padding="VALID", activation='relu', input_shape=(224, 224, 3), name='features/layer0'),
            tf.keras.layers.MaxPool2D(pool_size=3, strides=2, name='features/layer2'),
            Fire(64, 16, 64, 64, name='features/layer3'),
            Fire(128, 16, 64, 64, name='features/layer4'),
            tf.keras.layers.MaxPool2D(pool_size=3, strides=2, name='features/layer5'),
            Fire(128, 32, 128, 128, name='features/layer6'),
            Fire(256, 32, 128, 128, name='features/layer7'),
            tf.keras.layers.MaxPool2D(pool_size=3, strides=2, name='features/layer8'),
            Fire(256, 48, 192, 192, name='features/layer9'),
            Fire(384, 48, 192, 192, name='features/layer10'),
            Fire(384, 64, 256, 256, name='features/layer11'),
            Fire(512, 64, 256, 256, name='features/layer12'),
            tf.keras.layers.Conv2D(self.num_classes, kernel_size=1, padding="VALID",  activation='relu', name='classifier/layer1'),
            tf.keras.layers.AveragePooling2D(pool_size=13, strides=13, padding="VALID", name='classifier/layer3')
            ])

    def call(self, x, save_path=None):
        x = self.net(x)
        scores = tf.reshape(x, (-1, self.num_classes))
        return scores
