#include <iostream>
using namespace std;

typedef struct fraction {
    int numerator;
    int denominator;
} fraction;

int compare(fraction a, fraction b) {
    int n1 = a.numerator * b.denominator;
    int n2 = b.numerator * a.denominator;
    if (n1 > n2) return 1;
    else if (n1 < n2) return -1;
    return 0;
}

int main()
{
    fraction d1, d2;
    cin >> d1.numerator >> d1.denominator;
    cin >> d2.numerator >> d2.denominator;
    cout << compare(d1, d2);
}