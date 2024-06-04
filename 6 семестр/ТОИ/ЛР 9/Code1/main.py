def direct_search(text, pattern):
    len_text = len(text)
    len_pattern = len(pattern)
    positions = []

    for i in range(len_text - len_pattern + 1):
        match = True
        for j in range(len_pattern):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)

    return positions

with open('text.txt', 'r') as file:
    text = file.read()

pattern = input("Введите слово для поиска: ")
positions = direct_search(text, pattern)

if positions:
    print(f'Слово "{pattern}" найдено на следующих позициях: {positions}')
else:
    print(f'Слово "{pattern}" не найдено в тексте.')
