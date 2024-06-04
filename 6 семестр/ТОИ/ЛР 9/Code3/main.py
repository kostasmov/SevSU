def boyer_moore_search(pattern, text):
    m = len(pattern)
    n = len(text)

    shift_table = [m] * 256
    for i in range(m - 1):
        shift_table[ord(pattern[i])] = m - 1 - i

    i = m - 1
    j = m - 1

    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            i = i + shift_table[ord(text[i])]
            j = m - 1

    return -1

word_to_search = input("Введите слово для поиска: ")

with open('text.txt', 'r', encoding='utf-8') as file:
    contents = file.read()
    index = boyer_moore_search(word_to_search, contents)
    if index != -1:
        print(f"Слово '{word_to_search}' найдено на позиции {index}")
    else:
        print(f"Слово '{word_to_search}' не найдено")
