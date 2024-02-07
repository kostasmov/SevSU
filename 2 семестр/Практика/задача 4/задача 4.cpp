#include <iostream>
#include <string>
using namespace std;

//возвращает строку с меньшим из чисел
string min(string A, string B) {
    if ((A[0] == '-') && (B[0] != '-'))
        return A;
    if ((A[0] != '-') && (B[0] == '-'))
        return B;
    string A1 = A, B1 = B;
    if ((A[0] == '-') && (B[0] == '-'))
        A1 = B, B1 = A;
    if (A.length() > B.length())
        return B1;
    if (A.length() < B.length())
        return A1;
    for (int i = 0; i < (int)A.length(); i++) {
        if (A[i] > B[i]) return B1;
        if (A[i] < B[i]) return A1;
    }
    return A;
}

//главная функция
int main() {
    string a, b, c, Answer;
    cin >> a >> b >> c;
    Answer = min(a, b);
    Answer = min(Answer, c);
    cout << Answer;
}
