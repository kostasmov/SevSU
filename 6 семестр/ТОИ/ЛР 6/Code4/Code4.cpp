#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <fstream>
#include <windows.h>
using namespace std;

struct FanoNode {
    char symbol;
    double probability;
    FanoNode* left;
    FanoNode* right;

    FanoNode(char sym, double prob) : symbol(sym), probability(prob), left(nullptr), right(nullptr) {}
};

struct FanoNodeComparator {
    bool operator()(const FanoNode* a, const FanoNode* b) const {
        return a->probability < b->probability;
    }
};

FanoNode* buildFanoTree(const unordered_map<char, double>& probabilities) {
    priority_queue<FanoNode*, vector<FanoNode*>, FanoNodeComparator> pq;

    for (const auto& entry : probabilities) {
        FanoNode* node = new FanoNode(entry.first, entry.second * 1000);
        pq.push(node);
    }

    while (pq.size() > 1) {
        FanoNode* left = pq.top(); pq.pop();
        FanoNode* right = pq.top(); pq.pop();

        FanoNode* parent = new FanoNode('\0', left->probability + right->probability);
        parent->left = left;
        parent->right = right;

        pq.push(parent);
    }

    return pq.top();
}

void generateFanoCodes(FanoNode* root, string code, unordered_map<char, string>& codes) {
    if (!root)
        return;

    if (root->symbol != '\0') {
        codes[root->symbol] = code;
        return;
    }

    generateFanoCodes(root->left, code + "0", codes);
    generateFanoCodes(root->right, code + "1", codes);
}

void encodeFile(const string& inputFilename, const string& outputFilename) {
    unordered_map<char, double> probabilities;
    ifstream inputFile(inputFilename);
    char ch;
    int totalSymbols = 0;
    while (inputFile.get(ch)) {
        probabilities[ch]++;
        totalSymbols++;
    }
    inputFile.close();

    for (auto& entry : probabilities) {
        entry.second /= totalSymbols;
    }

    FanoNode* root = buildFanoTree(probabilities);

    unordered_map<char, string> codes;
    generateFanoCodes(root, "", codes);

    cout << "Префиксные коды:\n";
    for (const auto& pair : codes) {
        cout << pair.first << ": " << pair.second << "\n";
    }

    ofstream outputFile(outputFilename);
    inputFile.open(inputFilename);
    while (inputFile.get(ch)) {
        outputFile << codes[ch];
    }
    inputFile.close();
    outputFile.close();
}

int main() {
    SetConsoleOutputCP(1251);
    string inputFilename = "input.txt";
    string outputFilename = "output.txt";
    encodeFile(inputFilename, outputFilename);
    return 0;
}
