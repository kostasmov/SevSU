// Импорт библиотек
const tf = require('@tensorflow/tfjs-node');
const mnist = require('mnist');
const fs = require('fs');
const { createCanvas } = require('canvas');

// Загрузка данных MNIST
const set = mnist.set(0, 10);
const testSet = set.test;

// Подготовка данных
const prepareData = (data) => {
    const images = data.map(item => item.input);
    return tf.tensor2d(images, [images.length, 784]);
};

// Загрузка и предсказание
(async () => {
    const model = await tf.loadLayersModel('file://./mnist-model/model.json');
    const testImages = prepareData(testSet);
    const predictions = model.predict(testImages).argMax(-1).arraySync();

    // Визуализация результатов
    const canvas = createCanvas(280, 280);
    const ctx = canvas.getContext('2d');
    for (let i = 0; i < 10; i++) {
        const imageData = tf.tensor2d(testSet[i].input, [28, 28]).mul(255).toInt().arraySync();
        const predictedLabel = predictions[i];
        const trueLabel = testSet[i].output.indexOf(1);
        ctx.clearRect(0, 0, 280, 280);
        for (let y = 0; y < 28; y++) {
            for (let x = 0; x < 28; x++) {
                const color = imageData[y][x];
                ctx.fillStyle = `rgb(${color}, ${color}, ${color})`;
                ctx.fillRect(x * 10, y * 10, 10, 10);
            }
        }
        ctx.fillStyle = 'red';
        ctx.font = '20px Arial';
        ctx.fillText(`Predicted: ${predictedLabel}`, 10, 260);
        ctx.fillText(`True: ${trueLabel}`, 150, 260);
        fs.writeFileSync(`output${i + 1}.png`, canvas.toBuffer('image/png'));
    }
})();