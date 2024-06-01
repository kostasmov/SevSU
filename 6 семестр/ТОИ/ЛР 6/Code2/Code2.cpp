#include <iostream>
#include <queue>
#include <unordered_map>
#include <string>
#include <windows.h>

struct HuffmanNode {
    char data;
    int frequency;
    HuffmanNode* left;
    HuffmanNode* right;

    HuffmanNode(char data, int frequency) : data(data), frequency(frequency), left(nullptr), right(nullptr) {}
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
    std::unordered_map<char, double> probabilities = {
        {'A', 0.4},
        {'B', 0.2},
        {'C', 0.1},
        {'D', 0.1},
        {'E', 0.1},
        {'F', 0.05},
        {'G', 0.05}
    };

    std::cout << "Исходные вероятности символов:\n";
    for (const auto& pair : probabilities) {
        std::cout << "Символ: " << pair.first << ", Вероятность: " << pair.second << "\n";
    }

    HuffmanNode* root = buildHuffmanTree(probabilities);

    std::unordered_map<char, std::string> prefixCodes;
    generatePrefixCodes(root, "", prefixCodes);

    std::cout << "\nПрефиксные коды для каждого символа:\n";
    for (const auto& pair : prefixCodes) {
        std::cout << "Символ: " << pair.first << ", Код: " << pair.second << "\n";
    }

    return 0;
}
