from base import Base
from Users import User
from Employees import Employee
from validator import integer, string


def main(worker: bool):
    while True:
        if worker:
            id = base.read("employees", ["id"], {"login": user.get_login()})[0]
            employee = Employee(id, user.get_login(), base)
            print("1 - просмотреть все записи\n"
                  "2 - подтвердить записи\n"
                  "3 - выйти")
            choice = integer("Ваш выбор: ", [1, 2, 3])
            if choice == 1:
                employee.modify()
            elif choice == 2:
                employee.confirm()
            else:
                break
        else:
            print("1 - записаться в салон\n"
                  "2 - просмотреть все записи\n"
                  "3 - выйти\n")
            choice = integer("Ваш выбор: ", [1, 2, 3])
            if choice == 1:
                user.new_record()
            elif choice == 2:
                user.modify_record()
            else:
                break


if __name__ == "__main__":
    base = Base()
    # print(base.read("users", ["*"], {"login": "z"}, all=True))
    user = User(base)
    while True:
        print("1 - log in\n"
              "2 - sign up\n"
              "3 - exit")
        answer = integer("Ваш выбор: ", [1, 2, 3])
        if answer == 1:
            worker = user.log_in()
            main(worker)
        elif answer == 2:
            user.sign_up()
            main(False)
        else:
            break

