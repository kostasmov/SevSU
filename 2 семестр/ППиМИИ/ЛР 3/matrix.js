class NumberMatrix {
    constructor(values) {
        this.matrix = values;
    }

    getOnlyPositive() {
        // return this.matrix.filter(row => !row.some(x => x < 0))
        return this.matrix.filter(row => !this.hasNegative(row))
    }

    hasNegative(row) {
        var hasNegative = false;

        for (var i = 0; i < row.length; i++) {
            if (row[i] < 0) {
                hasNegative = true;
                break;
            }
        }

        return hasNegative;
    }
}

let matrix = new NumberMatrix([
    [33, 101, 69, 300],
    [911, -1, 993, 0],
    [66, 228, 2007, 555],
    [-13, 77, 1984, 404]
]);

console.log("Матрица без строк с отрицательными элементами: ");
console.log(matrix.getOnlyPositive());