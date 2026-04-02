class NumberArray {
    constructor(values) {
        this.values = values;
    }

    sum() {
        let total = 0;
        for (let i = 0; i < this.values.length; i++) {
            total += this.values[i];
        }
        return total;
    }
}

let arr = new NumberArray([55, 81, -34, 12, 7, 0, 4, 2003, -2, 6]);

console.log("Сумма элементов массива:", arr.sum());
