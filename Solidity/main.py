import string
from time import sleep
from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import address_contract, abi

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=address_contract, abi=abi)

def check_password(password):
    if len(password) < 12:
        print("Пароль должен быть больше 12 символов")
        return False

    if not any(char.islower() for char in password):
        print("Пароль должен содержать строчные буквы")
        return False

    if not any(char.isupper() for char in password):
        print("Пароль должен содержать прописные буквы")
        return False

    if not any(char.isdigit() for char in password):
        print("Пароль должен содержать цифры")
        return False

    special_chars = string.punctuation
    if not any(char in special_chars for char in password):
        print("Пароль должен содержать специальные символы")
        return False

    common_passwords = ["password123", "qwerty123", "123", "password", "qwerty"]
    if password.lower() in common_passwords:
        print("Избегайте использования простых шаблонов паролей")
        return False

    return True

def register():
    while True:
        password = input("Введите пароль: ")

        if check_password(password):
            try:
                account = w3.geth.personal.new_account(password)
                print(f"Ваш публичный ключ: {account}")
                break
            except Exception as e:
                print(f"Ошибка создания аккаунта: {e}")
        else:
            print("Попробуйте еще раз.")

def login():
    while True:
        try:
            public_key = input("Введите ваш публичный ключ: ")
            password = input("Введите пароль: ")

            w3.geth.personal.unlock_account(public_key, password)
            print("\nАвторизация прошла успешно!\n")
            return public_key

        except Exception as e:
            print(f"\nОшибка авторизации: {e}\n")
            return ''

def create_estate(account):
    try:
        size = int(input("Размер недвижимости: "))
        if size <= 0:
            print("Размер недвижимости должен быть положительным числом.")
            return

        address = input("Адрес недвижимости: ")
        if not address:
            print("Введите адрес недвижимости.")
            return

        print("Выберите тип недвижимости:")
        print("1. Дом (House)")
        print("2. Квартира (Flat)")
        print("3. Лофт (Loft)")
        type_estate = int(input("Тип недвижимости: "))
        if type_estate < 1 or type_estate > 3:
            print("Неверный тип недвижимости.")
            return
        
        tx_hash = contract.functions.createEstate(size, address, type_estate - 1).transact({
            'from': account
        })
        
        print(f"Операция выполнена успешно. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_ad(account):
    try:
        price = int(input("Введите цену недвижимости в WEI: "))
        if price <= 0:
            print("Цена недвижимости должна быть положительным числом.")
            return
        
        get_estate(account) 
        id_estate = int(input("Введите ID недвижимости, для которой создается объявление: "))
        if id_estate < 0:
            print("ID недвижимости должен быть положительным числом.")
            return
        
        print("Выберите статус объявления:")
        print("1. Открытое объявление")
        print("2. Закрытое объявление")
        ad_status_input = input("Выберите статус объявления: ")

        if not ad_status_input:
            print("Статус объявления не может быть пустым.")
            return

        ad_status = int(ad_status_input)
        if ad_status < 1 or ad_status > 2:
            print("Неверный статус объявления.")
            return
        
        tx_hash = contract.functions.createAd(price, id_estate, ad_status - 1).transact({
            'from': account
        })
        
        print(f"Операция выполнена успешно. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def change_estate_status(account):
    try:
        estate_id = int(input("Введите ID недвижимости, которую хотите изменить: "))
        if estate_id < 0:
            print("ID недвижимости должен быть положительным числом.")
            return
        
        tx_hash = contract.functions.changeStatusEstate(estate_id).transact({
            'from': account
        })
        
        print(f"Статус недвижимости успешно изменен. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def change_ad_status(account):
    try:
        ad_id = int(input("Введите ID объявления, которое хотите изменить: "))
        if ad_id < 0:
            print("ID объявления должен быть положительным числом.")
            return
        
        tx_hash = contract.functions.changeStatusAd(ad_id).transact({
            'from': account
        })
        
        print(f"Статус объявления успешно изменен. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def buy_estate(account):
    try:
        estate_id = int(input("Введите ID недвижимости, которую хотите купить: "))
        if estate_id < 0:
            print("ID недвижимости должен быть положительным числом.")
            return
        
        tx_hash = contract.functions.buyEstate(estate_id).transact({
            'from': account
        })
        
        print(f"Операция покупки недвижимости выполнена успешно. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")

def withdraw(data):
    account = data['account']
    try:
        value = int(input("Введите количество WEI для вывода: "))
        if value <= 0:
            print("Количество WEI должно быть положительным числом.")
            return

        tx_hash = w3.eth.sendTransaction({
            'to': account,
            'from': w3.eth.accounts[0],
            'value': value
        })
        
        print(f"Операция выполнена успешно. Хэш операции: {tx_hash.hex()}")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка вывода средств: {e}")

def get_estate(account):
    try:
        events = contract.events.CreatedEstates().process()
        for i in events:
            print(i['args'])
    except Exception as e:
        print(f"Ошибка отображения недвижимости: {e}")

def get_ad(account):
    try:
        events = contract.events.CreatedAd().process()
        for i in events:
            print(i['args'])
    except Exception as e:
        print(f"Ошибка отображения объявления: {e}")

def get_balance(account):
    try:
        balance = w3.eth.get_balance(account)
        print(f"Баланс аккаунта {account}: {w3.fromWei(balance, 'ether')} ETH")
    except Exception as e:
        print(f"Ошибка получения баланса: {e}")

def menu(account):
    while True:
        print("\n1. Создать недвижимость")
        print("2. Создать объявление")
        print("3. Изменить статус недвижимости")
        print("4. Изменить статус объявления")
        print("5. Купить недвижимость")
        print("6. Вывести средства")
        print("7. Показать доступные недвижимости")
        print("8. Показать доступные объявления")
        print("9. Показать баланс аккаунта")
        print("0. Выход")

        try:
            choice = int(input("\nВыберите действие: "))
            if choice == 1:
                create_estate(account)
            elif choice == 2:
                create_ad(account)
            elif choice == 3:
                change_estate_status(account)
            elif choice == 4:
                change_ad_status(account)
            elif choice == 5:
                buy_estate(account)
            elif choice == 6:
                withdraw({'account': account})
            elif choice == 7:
                get_estate(account)
            elif choice == 8:
                get_ad(account)
            elif choice == 9:
                get_balance(account)
            elif choice == 0:
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
        except ValueError:
            print("Ошибка: введите число.")
        except Exception as e:
            print(f"Ошибка выполнения операции: {e}")

def main():
    print("Добро пожаловать в программу для управления недвижимостью и объявлениями.")
    print("Выберите действие:")
    print("1. Регистрация")
    print("2. Вход")

    try:
        choice = int(input("Ваш выбор: "))
        if choice == 1:
            register()
        elif choice == 2:
            account = login()
            if account:
                menu(account)
            else:
                print("Ошибка входа. Попробуйте еще раз.")
        else:
            print("Неверный выбор. Попробуйте еще раз.")
    except ValueError:
        print("Ошибка: введите число.")
    except Exception as e:
        print(f"Ошибка выполнения операции: {e}")

if __name__ == "__main__":
    main()
