#include <iostream>
#include <unordered_map>
#include <queue>
#include <string>
#include <iomanip>
#include <locale>
#include <windows.h>

struct HuffmanNode {
    char data;
    double frequency;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(char data, double frequency) : data(data), frequency(frequency), left(nullptr), right(nullptr) {}
};

struct CompareNodes {
    bool operator()(HuffmanNode* lhs, HuffmanNode* rhs) {
        return lhs->frequency > rhs->frequency;
    }
};

HuffmanNode* buildHuffmanTree(const std::unordered_map<char, double>& probabilities) {
    std::priority_queue<HuffmanNode*, std::vector<HuffmanNode*>, CompareNodes> pq;

    for (const auto& pair : probabilities) {
        HuffmanNode* node = new HuffmanNode(pair.first, pair.second * 1000);
        pq.push(node);
    }

    while (pq.size() > 1) {
        HuffmanNode* left = pq.top(); pq.pop();
        HuffmanNode* right = pq.top(); pq.pop();

        HuffmanNode* parent = new HuffmanNode('\0', left->frequency + right->frequency);
        parent->left = left;
        parent->right = right;

        pq.push(parent);
    }

    return pq.top();
}

void generatePrefixCodes(HuffmanNode* root, const std::string& codePrefix, std::unordered_map<char, std::string>& prefixCodes) {
    if (root == nullptr) return;

    if (root->data != '\0') prefixCodes[root->data] = codePrefix;

    generatePrefixCodes(root->left, codePrefix + "0", prefixCodes);
    generatePrefixCodes(root->right, codePrefix + "1", prefixCodes);
}

int main() {
    SetConsoleOutputCP(1251);
    std::string inputString = "Мовенко Константин Михайлович, 11.10.2023, город Севастополь";

    std::unordered_map<char, int> charFrequencies;
    for (char c : inputString) {
        charFrequencies[c]++;
    }

    std::unordered_map<char, double> probabilities;
    for (const auto& pair : charFrequencies) {
        char c = pair.first;
        int frequency = pair.second;
        double probability = static_cast<double>(frequency) / inputString.length();
        probabilities[c] = probability;
    }

    HuffmanNode* root = buildHuffmanTree(probabilities);

    std::unordered_map<char, std::string> prefixCodes;
    generatePrefixCodes(root, "", prefixCodes);

    std::string encodedString;
    for (char c : inputString) {
        encodedString += prefixCodes[c];
    }

    std::cout << "Префиксные коды:\n";
    for (const auto& pair : prefixCodes) {
        std::cout << "'" << pair.first << "': " << pair.second << "\n";
    }

    std::cout << "Закодированная строка: " << encodedString << "\n";

    int originalBits = inputString.length() * 8;
    int encodedBits = encodedString.length();

    double compressionRatio = static_cast<double>(originalBits) / encodedBits;

    std::cout << "Коэффициент сжатия: " << std::fixed << std::setprecision(2) << compressionRatio << "\n";

    return 0;
}
