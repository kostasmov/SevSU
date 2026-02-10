// Двумерный массив (матрица 4x4 = 16 элементов)
let matrix = [
    [33, 101, 69, 300],
    [911, -1, 993, 0],
    [66, 228, 2007, 555],
    [-13, 77, 1984, 404]
];

// Удаление из матрицы строк с отрицательными элементами
let positiveMatrix = [];
for (let i = 0; i < matrix.length; i++) {   // обход строк
    let hasNegative = false;
    for (let j = 0; j < matrix[i].length; j++) {    // обход элементов строки
        if (matrix[i][j] < 0) {
            hasNegative = true;
            break;
        }
    }
    if (!hasNegative) {
        positiveMatrix.push(matrix[i]);
    }
}

console.log("Матрица без строк с отрицательными элементами:");
console.log(positiveMatrix);
