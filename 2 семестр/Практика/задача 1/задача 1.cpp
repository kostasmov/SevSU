#include <iostream>
#include <string>
const long unsigned int ERROR = -1;
using namespace std;

int main()
{
	string Str;
	getline(cin, Str);
	char StrArr[] = { '.', ':', ';', '!', '?', ',' };
	int pos, count;
	for (int i = 0; i < 6; i++) {
		pos = 0, count = 0;
		while (Str.find(StrArr[i], pos) != -1) {
			count++;
			pos = Str.find(StrArr[i], pos) + 1;
		}
		cout << StrArr[i] << " = " << count << "\n";
	}
	return 0;
}