// Сумма элементов массива
const sumArray = array =>
    array.reduce((sum, value) => sum + value, 0);

// Исходный массив
const array = [55, 81, -34, 12, 7, 0, 4, 2003, -2, 6];

console.log("Сумма элементов массива:", sumArray(array));