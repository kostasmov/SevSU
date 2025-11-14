import csv

# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
table = None
separators = ',=+-<>()'


def read_table(filename):
    """Чтение таблицы переходов из файла"""
    global table

    try:
        with open(filename, "r") as file:
            reader = csv.reader(file, delimiter=';')

            n, m = map(int, next(reader))
            table = []

            for _ in range(n):
                row = list(map(int, next(reader)))
                table.append(row)

    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
        exit(0)


def scan_file(filename):
    """Сканирование программы из файла"""
    global table, separators
    flag = False

    try:
        with open(filename, "r") as file:
            N_sost = 0          # текущее состояние КА (столбец таблицы состояний)
            N_str = 0           # код лексемы (строка таблицы состояний)
            word = ""           # текущее слово
            c = file.read(1)    # текущая литера на входе КА

            while True:
                if c == '\n':   # абзац не учитывается
                    c = file.read(1)
                    continue

                if c.isalpha():     # Это буква?
                    match c.upper():
                        case 'A':
                            N_str = 0
                        case 'B':
                            N_str = 1
                        case 'C':
                            N_str = 2
                        case 'D':
                            N_str = 3
                        case 'E':
                            N_str = 4
                        case 'F':
                            N_str = 5
                        case 'O':
                            N_str = 6
                        case 'U':
                            N_str = 7
                        case 'N':
                            N_str = 8
                        case 'T':
                            N_str = 9
                        case 'I':
                            N_str = 10
                        case 'L':
                            N_str = 11
                        case 'X':
                            N_str = 12
                        case letter if letter in 'GHJKMPQRSVWYZ':
                            N_str = 13
                        case _:
                            N_str = 27
                elif c.isdigit():   # Это цифра?
                    match int(c):
                        case 0:
                            N_str = 14
                        case num if 1 <= num <= 9:
                            N_str = 15
                else:               # Это ни буква, ни цифра?
                    match c:
                        case '(':
                            N_str = 16
                        case ')':
                            N_str = 17
                        case '=':
                            N_str = 18
                        case '+':
                            N_str = 19
                        case '-':
                            N_str = 20
                        case '*':
                            N_str = 21
                        case '/':
                            N_str = 22
                        case '<':
                            N_str = 23
                        case '>':
                            N_str = 24
                        case '#':
                            N_str = 25
                        case ' ':
                            N_str = 26
                        case _:
                            N_str = 27

                if not word and not c: break    # проверка конца файла

                N_sost = table[N_str][N_sost]   # новое состояние по таблице переходов

                if N_sost:                      # запоминание лекс. единицы
                    word += c if c else '.'

                #print(f"Литера - '{c}', слово - '{word}'")

                # обработка состояний
                if 100 <= N_sost < 500:     # ключевое слово
                    handle_keyword_state(N_sost, word[:-1])
                    flag = True
                elif 500 <= N_sost < 700:   # разделитель
                    handle_separator_state(N_sost)
                    if N_sost == 508:
                        flag = True
                elif N_sost >= 700:         # ошибка
                    if len(word) != 1:
                        word = word[:-1]
                    handle_error_state(N_sost, word)
                    if N_sost > 701:
                        flag = True

                # обнуление состояния
                if N_sost >= 100:
                    N_sost = 0
                    word = ''

                if not c: break;  # конец файла

                if not flag:
                    c = file.read(1)
                else:
                    flag = False

    except Exception as e:
        print(f"Ошибка при обработке файла {filename}: {e}")
        exit(0)


def handle_keyword_state(state, keyword):
    """Обработка состояния ключевых слов"""
    keywords = {
        100: "Служебное слово",
        200: "Служебное слово",
        300: "Идентификатор",
        400: "Константа"
    }
    print(f"{keywords.get(state, 'Неизвестное ключевое слово')} '{keyword}'. Cостояние {state}")


def handle_separator_state(state):
    """Обработка состояний разделителей"""
    separators = {
        501: "Разделитель '('",
        502: "Разделитель ')'",
        503: "Разделитель '='",
        504: "Разделитель '+'",
        505: "Разделитель '-'",
        506: "Разделитель '*'",
        507: "Разделитель '/'",
        508: "Разделитель '<'",
        509: "Разделитель '>'",
        510: "Разделитель '#'",
        600: "Разделитель '<>'",
    }
    print(f"{separators.get(state, 'Неизвестный разделитель')}. Cостояние - {state}")


def handle_error_state(state, word):
    """Обработка ошибок"""
    errors = {
        701: "Некорректный фрагмент цепочки",
        702: "Ошибка в служебном слове",
        703: "Ошибка в написании имени переменной",
        704: "Ошибочная константа",
        705: "Ошибка записи разделителя"
    }
    print(f"{errors.get(state, 'Неизвестная входная литера')} '{word}'. Cостояние - {state}")


# ОСНОВНОЙ КОД
try:
    read_table("transitions.csv")
    scan_file("data.txt")
except Exception as e:
    print(f"\nОшибка: {e}")
