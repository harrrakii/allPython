from datetime import datetime


def string(query: str, length=None):
    while True:
        answer = input(query).strip()
        if answer != 0:
            if length:
                if len(answer) > length:
                    print(f"Ограничение на {length} символов")
                else:
                    return answer
            else:
                return answer
        else:
            print("Ответ не может быть пустым")


def integer(query: str, choices=None):
    while True:
        try:
            answer = int(input(query).strip())
            if choices:
                if answer not in choices:
                    print("Такого действия не существует")
                    continue
            if answer > 0:
                return answer
            else:
                print("Число должно быть положительным")
        except ValueError:
            print("Нужно ввести именно число")


def date(query: str):
    while True:
        try:
            d = input(query).strip()
            answer = datetime.strptime(d, "%d.%m.%Y")
            return answer.strftime("%d.%m.%Y")
        except ValueError as e:
            print("Введите дату в формате: дд.мм.гггг")