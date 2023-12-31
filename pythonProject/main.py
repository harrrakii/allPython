import keyboard
import csv
import json
from datetime import datetime
import os
work = True
name1 = "Максим"
steps = {
'1' : f"Вы - секретный агент ЦРУ. Ваша главная задача - вычислить и ликвидировать русского шпиона по имени {name1}\n"
    "Сейчас вы находитесь в Лос-Анджелесе и ожидаете предписаний от начальства\n"
    "Для продолжения нажимайте пробел",

'2': "Так: Вам поступило сообщение от начальника об его прибытии на ваши родные земли.\n"
     "Что будем делать?\n"
     "[1] Посмотреть данные о всех последних рейсах.\n"  # к шагу 3 
     "[2] Пойти пить кофе в Starbucks.", # к шагу 4 + правильный выбор

'3' : "После просмотра всех рейсов вы не заметили ничего подозрительного.\n" 
    "На ваш телефон пришла новая наводка.\n" 
    "Вам описали внешний вид шпиона.\n" 
    "После осмотра особых примет подозреваемого, вы должны решить, что делать дальше: \n"
    "[1]Пробить по внешности \n"# (к шагу 5) +1
    "[2]Закрыть весь аэропорт для поиска шпиона ",#(к шагу 6)

'4' :"Вы направились в Starbucks, который находится в аэропорту\n" 
    "Вдруг, вы замечаете человека на кассе, очень похожего под описание шпиона\n" 
    "Вы очень долго не могли решить как правильно поступить в этой ситуации\n"
     "Пришло время сделать окончательный выбор\n" 
    "[1] Подойти и начать разговор\n"  # к шагу 7 +1
    "[2] Незаметно следить" ,# к шагу 8  ,

'5' :
    "Вы попробовали пробить через ГлазБога, но ничего не нашли.\n" 
    "После долгих раздумий вам пришла великолепная идея в голову:\n" 
    "Вы решили обратиться к своей подружке, которая способна найти любого через социальные сети.\n" 
    "После пробива, ваша подруга случайно нашла всю его семью.\n"
    "Теперь необходимо решить, насколько грязно мы будем играть...\n"
    "[1] Приехать к его семье и шантажировать шпиона.\n"  # к шагу 9 + правильный выбор
    "[2] Искать только шпиона, не трогая его семью.",  # к шагу 4 +1

'6' : "Вы закрыли весь аэропорт.\n" 
    "Но скоро народ начал бунтовать.\n" 
    "Это очень сильно не понравилось вашему начальству.\n" 
    "Вас уволили с работы и сослали в Сибирь.\n" 
    "Вы умерли в холодных краях великой России.\n"
    "The end...", # плохой конец

'7' : "Вы подошли к незнакомцу и начали разговор.\n"
    "По ходу диалога, незнакомец рассказал, что он обычный семьянин.\n" 
    "Но вел он себя довольно подозрительно.\n" 
    "Каков ваш вердикт?\n" 
    "[1] Верим\n"# к шагу 10
    "[2] Не верим", # к шагу 11 + правильный выбор

'8' : "Вы начали слежку...\n" 
    "Но в какой-то момент вас отвлек турок, торгующий мороженым.\n" 
    "Вы потеряли след...\n" 
    f"Чертов русский, {name1}, смог подговорить турка...\n" 
    "The end...", # плохой конец

'9' : "Вы сели на первый возможный рейс и отправились прямиком в РФ.\n" 
    "После прилета сразу направились к семье русского шпиона.\n" 
    "Там вы взяли их в плен и отправили русскому сообщение, в котором говорится, что его семья у вас.\n" 
    "Вы предупредили, что русский должен сдаться.\n" 
    "В противном случае каждый час вы будете убивать по одному члену его семьи.\n" 
    "Вскоре шпион сдался и раскрыл свою личность.\n" 
    "The end...",

'10' : "Вы поверили незнакомцу.\n" 
     "Как выяснилось позже, таким образом вы упустили шпиона.\n" 
     "Начальству это не понравилось и вас уволили.\n" 
     "Вопрос о вашем увольнении давно был открыт.\n" 
     "Это была последняя капля\n" 
     "Спасибо что не отправили в Сибирь...\n" 
     "The end...", # плохой конец

'11' : "Вы решили сделать вид, что поверили этому клоуну.\n" 
    f"Но на выходе с аэропорта, {name1}а связали.\n" 
    "Причиной стал кофе, который он забыл оплатить.\n" 
    "[1] Казнить шпиона.\n"  # к шагу 12
    "[2] Предложить сделку." ,# к шагу 13 + правильный выбор

'12' : "Вы уничтожили шпиона...\n" 
    "The end...",

'13' : "Вы предложили шпиону работать на вас.\n" 
    "Он согласился и вы раскрыл русскую сеть шпионажа в Америке.\n" 
    "The end...",
}
choices = {
    '2': {'1': '3', '2+': '4'},
    '3': {'1+': '5', '2': '6'},
    '4': {'1+': '7', '2': '8'},
    '5': {'1+': '9', '2+': '4'},
    '7': {'1': '10', '2+': '11'},
    '11': {'1': '12', '2+': '13'}
}
def print_step(step_id, coin):
    if step_id in ['6', '8', '9', '10', '12', '13']:
        print(steps[step_id])
        print('Вы заработали монет: ', coin)
        work = exit()
        return work
    for key in steps.keys():
        if key == step_id:
            print(steps[key])
            return True


def take_choices(step_id, coin):
    find = False
    for key in choices.keys():
        if step_id == key:
            find = True
    if not find:
        step_id = str(int(step_id) + 1)
    else:
        input_id = True
        while (input_id):
            try:
                input_id = input("Ваш выбор: ").strip()
                if input_id == '2' or input_id == '1':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Введите 1 или 2')
        for key in choices[step_id].keys():
            if key[0] == input_id:
                if len(key) == 2:
                    coin = coins(coin)
                    step_id = choices[step_id][input_id + '+'][0]
                else:
                    step_id = choices[step_id][input_id]
    return step_id, coin


def menu():
    print('[1]Начать новую игру.\n[2]Выйти из игры.')
    while True:
         try:
            key = input()
            match key:
                case '1':
                    play(step_id='1', coin=0)
                    break# запуск функции с игрой.
                case '2':
                    exit()
                    break


         except ValueError:
            print('Неизвестная комманда.')


def exit():
    work = False
    print('Вы завершили игру')
    return work


def play(step_id, coin):
    work = print_step(step_id, coin)
    step_id_and_coin = take_choices(step_id, coin)
    step_id = step_id_and_coin[0]
    coin = step_id_and_coin[1]
    return step_id, work, coin


def main():
    step_id = '2'
    work = True
    coin = 0
    while (work):
        keyboard.wait('space')
        game = play(step_id, coin)
        step_id = game[0]
        work = game[1]
        coin = game[2]
    return coin

def coins(coin):
    coin += 1
    print('+ 1 монета')
    return coin

def deleteSave(sTime, eTime, data, allTime):
    print("Хотите ли вы удалить сохранение?")
    c = input().lower()
    if c == "да":
        for key, value in data.items():
            print(f"{key}, {value}")
        k = int(input("Выберите номер сохранения: "))
        data.pop(k)
        with open('data.csv', 'w', newline='') as file:
            file.truncate(0)
            writer = csv.writer(file)
            for row in data.keys():
                writer.writerow(data[row])
        for key in data.keys():
            dictT = {'sTime': data[key][0],
                     'eTime': data[key][1],
                     'allTime': data[key][2],-
                     'coin': data[key][3]}
            data[key] = dictT
        with open('data.json', 'w') as file:
            file.truncate(0)
            json.dump(data, file, indent=4)
    else:
        print('The end')

if __name__ == "__main__":
    sTime = datetime.now()
    menu()
    coin = main()
    eTime = datetime.now()
    allTime = eTime - sTime
    data = {1: {
            'sTime': str(sTime),
            'eTime': str(eTime),
            'allTime': str(allTime),
            'coin': coin} }
    if os.path.exists('data.json'):
        with open('data.json', 'r') as file:
            data = json.load(file)
        data[len(data.keys()) + 1] = {'sTime': str(sTime),
                                  'eTime': str(eTime),
                                  'allTime': str(allTime),
                                  'coin': coin}
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    else:
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    if os.path.exists('data.csv'):
        with open('data.csv', 'r') as file:
            data.clear()
            reader = csv.reader(file)
            for row in reader:
                data[len(data.keys()) + 1] = row
        data[len(data.keys()) + 1] = [str(sTime), str(eTime), str(allTime), coin]
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for key in data.keys():
                writer.writerow(data[key])
    else:
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for key in data.keys():
                writer.writerow(list(data[key].values()))
    deleteSave(sTime, eTime, data, allTime)









