def kmp_search(pattern, text):
    def compute_prefix_function(pattern):
        pi = [0]
        j = 0
        for i in range(1, len(pattern)):
            while j > 0 and pattern[j] != pattern[i]:
                j = pi[j-1]
            if pattern[j] == pattern[i]:
                j += 1
            pi.append(j)
        return pi

    pi = compute_prefix_function(pattern)
    q = 0
    for i in range(len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q-1]
        if pattern[q] == text[i]:
            q += 1
        if q == len(pattern):
            return i - (q - 1)
    return -1

word_to_search = input("Введите слово для поиска: ")

with open('text.txt', 'r', encoding='utf-8') as file:
    contents = file.read()
    index = kmp_search(word_to_search, contents)
    if index != -1:
        print(f"Слово '{word_to_search}' найдено на позиции {index}")
    else:
        print(f"Слово '{word_to_search}' не найдено")
