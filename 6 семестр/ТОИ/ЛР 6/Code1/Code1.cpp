#include <iostream>
#include <queue>
#include <unordered_map>
#include <windows.h>
using namespace std;

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

HuffmanNode* buildHuffmanTreePrefix(const unordered_map<char, string>& prefixCodes) {
    priority_queue<HuffmanNode*, vector<HuffmanNode*>, CompareNodes> pq;

    for (const auto& pair : prefixCodes) {
        HuffmanNode* node = new HuffmanNode(pair.first, pair.second.length());
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

void generatePrefixCodes(HuffmanNode* root, const string& codePrefix, unordered_map<char, string>& prefixCodes) {
    if (root == nullptr) return;

    if (root->data != '\0') prefixCodes[root->data] = codePrefix;

    generatePrefixCodes(root->left, codePrefix + "0", prefixCodes);
    generatePrefixCodes(root->right, codePrefix + "1", prefixCodes);
}

string compressUsingPrefixCodes(const string& data, const unordered_map<char, string>& prefixCodes) {
    string compressedData;
    for (char c : data) compressedData += prefixCodes.at(c);
    return compressedData;
}

string decompressUsingPrefixCodes(const string& compressedData, HuffmanNode* root) {
    string decompressedData;
    HuffmanNode* current = root;

    for (char c : compressedData) {
        current = (c == '0') ? current->left : current->right;

        if (current->left == nullptr && current->right == nullptr) {
            decompressedData += current->data;
            current = root;
        }
    }

    return decompressedData;
}

int main() {
    SetConsoleOutputCP(1251);

    string data = "AAAAABBBBBCCCCCDDDDDDEEEEE";

    unordered_map<char, string> prefixCodes = {
        {'A', "0"},
        {'B', "10"},
        {'C', "110"},
        {'D', "1110"},
        {'E', "1111"}
    };

    cout << "Исходные данные: " << data << endl;

    string compressedData = compressUsingPrefixCodes(data, prefixCodes);
    cout << "Сжатые данные: " << compressedData << endl;

    HuffmanNode* root = buildHuffmanTreePrefix(prefixCodes);
    string decompressedData = decompressUsingPrefixCodes(compressedData, root);
    cout << "Декомпрессированные данные: " << decompressedData << endl;

    return 0;
}
