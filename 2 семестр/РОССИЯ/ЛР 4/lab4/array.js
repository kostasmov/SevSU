import { from } from "rxjs";
import { reduce } from "rxjs/operators";

// Исходный одномерный массив (10 элементов)
const arr = [55, 81, -34, 12, 7, 0, 4, 2003, -2, 6];

// Создание потока данных из элементов массива
from(arr)
    .pipe(
        // подсчёт суммы элементов потока
        reduce((sum, x) => sum + x, 0)
    )
    // точка запуска потока
    .subscribe(sum => {
        console.log("Сумма элементов массива:", sum);
    });
