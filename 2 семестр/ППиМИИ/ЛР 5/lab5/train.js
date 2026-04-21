const tf = require('@tensorflow/tfjs-node');
const mnist = require('mnist');

// Загрузка данных MNIST
const set = mnist.set(8000, 2000);
const trainingSet = set.training;
const testSet = set.test;

// Подготовка данных
const prepareData = (data) => {
    const images = data.map(item => item.input);
    const labels = data.map(item => item.output);
    return {
        images: tf.tensor2d(images, [images.length, 784]),
        labels: tf.tensor2d(labels, [labels.length, 10])
    };
};

const trainData = prepareData(trainingSet);
const testData = prepareData(testSet);

// Определение модели
const model = tf.sequential();

model.add(tf.layers.dense({ units: 128, activation: 'relu', inputShape: [784] }));
model.add(tf.layers.dense({ units: 64, activation: 'relu' }));
model.add(tf.layers.dense({ units: 10, activation: 'softmax' }));

//model.add(tf.layers.dense({ units: 10, activation: 'softmax', inputShape: [784] }));

// Компиляция модели
model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
});

// Обучение модели
(async () => {
    await model.fit(trainData.images, trainData.labels, {
        epochs: 20,
        //epochs: 1,
        validationData: [testData.images, testData.labels],
        callbacks: {
            onEpochEnd: (epoch, logs) => {
                console.log(`Epoch ${epoch + 1}: loss = ${logs.loss.toFixed(4)}, 
                            accuracy = ${logs.acc.toFixed(4)}`);
            }
        }
    });

    // Сохранение модели
    await model.save('file://./mnist-model');
})();