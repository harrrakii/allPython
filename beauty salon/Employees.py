from base import Base
from validator import integer, string, date


class Employee:
    def __init__(self, id: int, login: str, db: Base):
        self.__id = id
        self.__login = login
        self.__db = db

    def confirm(self):
        while True:
            try:
                records = self.__db.read("records", ["*"], {
                    "employee_id": self.__id,
                    "confirmation": False
                }, all=True)
                if records:
                    for id, record in enumerate(records):
                        user = self.__db.read("users", ["login"], {"id": record[1]})[-1]
                        print(f"#{id + 1}\n"
                              f"К вам записан - {user}\n"
                              f"На дату: {record[5]}\n"
                              f"Оплата: {record[4]*0.8}\n"
                              f"Статус: Не подтвержденa\n"
                              f"---------------------------")
                    print("Выберите запись для действий: ")
                    record = integer("Ваш выбор: ", [i + 1 for i in range(len(records))]) - 1
                    answer = integer("1 - подтвердить\n"
                                     "2 - отменить\n"
                                     "3 - выйти\n"
                                     "Ваш выбор: ", [1, 2])
                    if answer == 1:
                        self.__db.update_data("records", {"confirmation": True},
                                            {"id": records[record][0]})
                        print("Запись успешна подтверждена!")
                    elif answer == 2:
                        self.__db.delete("records", {"id": records[record][0]})
                        print("Запись успешна удалена!")
                    else:
                        break
                else:
                    raise ValueError
            except:
                print('Нет записей требующие подтверждения')
                break

    def modify(self):
        while True:
            try:
                records = self.__db.read("records", ["*"], {
                    "employee_id": self.__id,
                    "confirmation": True
                }, all=True)
                if records:
                    for id, record in enumerate(records):
                        user = self.__db.read("users", ["login"], {"id": record[1]})
                        print(f"#{id + 1}\n"
                              f"К вам записан - {user}\n"
                              f"На дату: {record[5]}\n"
                              f"Оплата: {record[4] * 0.8}\n"
                              f"Статус: Подтверждена\n"
                              f"---------------------------")
                    print("Выберите запись для действия: ")
                    record = integer("Ваш выбор: ", [i + 1 for i in range(len(records))]) - 1
                    print("1 - перенести дату\n"
                          "2 - отменить\n"
                          "3 - выйти")
                    answer = integer("Ваш выбор: ", [1, 2])
                    if answer == 1:
                        record_date = date("На какое число перенсти: ")
                        self.__db.update_data("records", {"record_date": record_date},
                        {"id": records[record][0]})
                        print("Запись успешна перенесена!")
                    elif answer == 2:
                        self.__db.delete("records", {"id": records[record][0]})
                        print("Запись отменена")
                    else:
                        break
                else:
                    raise ValueError
            except:
                print('У вас нет записей')
                break



