import { from } from "rxjs";
import { filter, toArray } from "rxjs/operators";

// Исходный двумерный массив (матрица 4x4)
const matrix = [
    [33, 101, 69, 300],
    [911, -1, 993, 0],
    [66, 228, 2007, 555],
    [-13, 77, 1984, 404]
];

// Создание потока данных из строк матрицы
from(matrix)
    .pipe(
        // фильтр строк без отрицательных элементов
        filter(row => !row.some(value => value < 0)),
        toArray()
    )
    // точка запуска потока
    .subscribe(positiveMatrix => {
        console.log("Матрица без строк с отрицательными элементами:");
        console.log(positiveMatrix);
    });

