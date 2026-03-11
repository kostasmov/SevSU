// Сумма элементов массива
function sumArray(array) {
    let sum = 0;
    for (let i = 0; i < array.length; i++) {
        sum += array[i];
    }
    return sum;
}

// Одномерный массив (10 элементов)
let array = [55, 81, -34, 12, 7, 0, 4, 2003, -2, 6];

console.log("Сумма элементов массива:", sumArray(array));