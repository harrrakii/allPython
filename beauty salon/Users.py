from validator import string, integer, date
from base import Base


class User:
    def __init__(self, db: Base):
        self.__id = ""
        self.__login = ""
        self.__db = db

    def log_in(self):
        users = self.__db.read("users", ["*"], all=True)
        employees = self.__db.read("employees", ["*"], all=True)
        user_logins = [user[1] for user in users]
        employees_logins = [employee[1] for employee in employees]
        while True:
            login = string("Введите ваш логин: ", 20)
            if login in user_logins:
                user = users[user_logins.index(login)]
                password = string("Введите ваш пароль: ")
                if password == user[2]:
                    self.__id = user[0]
                    self.__login = login
                    return False
                else:
                    print("Пароль не верен попробуйте снова")
            elif login in employees_logins:
                employee = employees[employees_logins.index(login)]
                password = string("Введите ваш пароль: ")
                if password == employee[2]:
                    self.__id = employee[0]
                    self.__login = login
                    return True
                else:
                    print("Пароль не верен попробуйте снова")
            else:
                print("такого пользователя не существует(")

    def sign_up(self):
        while True:
            login = string("Придумайте логин: ", 20)
            users = self.__db.read("users", ["login"], all=True)
            employyes = self.__db.read("employees", ["login"], all=True)
            logins = [user[0] for user in users] + [employee[0] for employee in employyes]
            if login in logins:
                print("Логин занят")
            else:
                password = string("Придумайте пароль: ", 20)
                self.__db.insert("users", {"login": login, "password": password})
                user = self.__db.read("users", ["id"])
                self.__id = user[-1]
                self.__login = login
                break

    def new_record(self):
        salons = self.__db.read("salons", ['*'], all=True)
        employees = self.__db.read("employees", ["*"], all=True)
        print('Какой салон: ')
        for id, salon in enumerate(salons):
            print(f"{id + 1}: {salon[1]} по адресу: {salon[2]}")
        salon = salons[integer("Выберите салон по номеру: ", [i + 1 for i in range(len(salons))]) - 1]
        print("К кому: ")
        for id, employee in enumerate(employees):
            print(f"{id + 1}: {employee[3]}: стаж - {employee[5]}: стоимость: {employee[4]}")
        employee = employees[integer("Выберите специалиста: ", [i + 1 for i in range(len(employees))]) - 1]
        record_date = date("На какое число Вас записать: ")
        print("Подтвердите запись:\n"
              f"Вы записаны к {employee[3]}\n"
              f"В салон: {salon[1]}\n"
              f"На дату: {record_date}")
        print("1 - подтвердить\n"
              "2 - отменить")
        answer = integer("Ваш выбор: ", [1, 2])
        if answer == 1:
            self.__db.insert("records", {
                "salon_id": salon[0],
                "employee_id": employee[0],
                "user_id": self.__id,
                "record_date": record_date,
                "price": employee[4],
                "confirmation": False
            })
            print(f"Успешная запись! Ждем Вас с 10-19 {record_date}")
            print(f"Как только запись будет подтверждена, она появится в Вашем списке записей!")
        else:
            print("Хорошо, в следующий раз")

    def modify_record(self):
        while True:
            try:
                records = self.__db.read("records", ["*"], {"user_id": self.__id,
                                                    "confirmation": True}, all=True)
                if records:
                    print("Все записи: ")
                    for id, record in enumerate(records):
                        salon = self.__db.read("salons", ["title"], {"id": record[3]})[-1]
                        employee = self.__db.read("employees", ["*"], {"id": record[2]})
                        print(f"#{id + 1}\n"
                              f"Стилист: {employee[3]}\n"
                              f"Салон: {salon}\n"
                              f"На дату: {record[5]}\n"
                              f"Стоимость: {record[4]}\n"
                              f"-----------------------")
                    record = integer("Номер записи: ", [i + 1 for i in range(len(records))]) - 1
                    print("1 - отменить\n"
                          "2 - перенести на другую дату\n"
                          "3 - поменять салон\n"
                          "4 - назад")
                    answer = integer("Ваш выбор: ", [1, 2, 3, 4])
                    if answer == 1:
                        self.__db.delete("records", {"id": records[record][0]})
                        print("Запись отменена")
                    elif answer == 2:
                        record_date = date("На какое число Вас записать: ")
                        self.__db.update_data("records", {"record_date": record_date},
                        {"id": records[record][0]})
                        print("Запись успешна перенесена!")
                    elif answer == 3:
                        salons = self.__db.read("salons", ['*'], all=True)
                        for id, salon in enumerate(salons):
                            print(f"{id + 1}: {salon[1]} по адресу: {salon[2]}")
                        salon = salons[integer("Выберите салон по номеру: ", [i + 1 for i in range(len(salons))]) - 1]
                        print(salon)
                        self.__db.update_data("records", {"salon_id": salon[0]}, {
                            "id": records[record][0]
                        })
                        print("Салон успешно изменен!")
                    else:
                        break
                else:
                    raise ValueError
            except Exception as e:
                print(e)
                print("У вас нет записей")
                break

    def get_id(self):
        return self.__id

    def get_login(self):
        return self.__login



