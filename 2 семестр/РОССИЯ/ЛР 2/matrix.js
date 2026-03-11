// Удаление из матрицы строк с отрицательными элементами
const filterPositiveRows = matrix =>
    matrix.filter(row => !row.some(x => x < 0));

// Исходная матрица
const matrix = [
    [33, 101, 69, 300],
    [911, -1, 993, 0],
    [66, 228, 2007, 555],
    [-13, 77, 1984, 404]
];

console.log("Матрица без строк с отрицательными элементами:");
console.log(filterPositiveRows(matrix));