import telebot
from telebot import types
import math
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot("5358581757:AAHcBfyCoSGBxWwtgicNEdJ1f8swzC4-cvQ")
valuta_categories = ["Доллар-Продажа", "Доллар-Покупка",
                     "Евро-Продажа", "Евро-Покупка",
                     "Рубль-Продажа", "Рубль-Покупка",
                     "Тенге-Продажа", "Тенге-Покупка"]


# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    # Добавляем кнопки
    buttons_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for valuta_category in valuta_categories:
        item_category = types.KeyboardButton(text=valuta_category)
        buttons_category.add(item_category)

    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}!")
    bot.send_message(message.chat.id, 'Выбери категорию обмена:', reply_markup=buttons_category)

    # Получение сообщений о категории обмена
    @bot.message_handler(content_types=["text"])
    def category_text(message):
        if message.text.strip() in valuta_categories:
            valuta_category = message.text
            bot.send_message(message.chat.id, "Введите порог курса", reply_markup=types.ReplyKeyboardRemove())

            # Получение сообщения о пороге по валюте
            @bot.message_handler(content_types=["text"])
            def valuta_porog(message):
                porog_number_str = message.text
                try:
                    porog_number = float(porog_number_str)
                    bot.send_message(message.chat.id, f"Ваши данные приняты:\n{valuta_category} {porog_number}")

                    #Получение данных о банках удовлетворяющих условию
                    url = "https://valuta.kg/"

                    try:
                        response = requests.get(url)
                        print('Test---')
                    except Exception:
                        print("Не получилось подключиться к сайту https://valuta.kg/", Exception)

                    soup = BeautifulSoup(response.content, 'html.parser') #lxml html.parser
                    index=0
                    tableBankValute = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

                    for tr in soup.findAll('table')[4].findAll('tr'):
                        for a in tr.findAll('a'):
                            tableBankValute[index].append(a.text)
                        for div in tr.findAll('div', class_='td-rate__calc'):
                            tableBankValute[index].append(div.attrs.get('data-rate'))
                        index = index+1


                    if(valuta_category == "Доллар-Продажа"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[1]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[1]}")

                    if(valuta_category == "Доллар-Покупка"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[2]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[2]}")

                    if(valuta_category == "Евро-Продажа"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[3]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[3]}")

                    if(valuta_category == "Евро-Покупка"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[4]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[4]}")

                    if(valuta_category == "Рубль-Продажа"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[5]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[5]}")

                    if(valuta_category == "Рубль-Покупка"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[6]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[6]}")

                    if(valuta_category == "Тенге-Продажа"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[7]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[7]}")

                    if(valuta_category == "Тенге-Покупка"):
                        for onlyBankValute in tableBankValute:
                            if(len(onlyBankValute)>0):
                                if(float(onlyBankValute[8]) <= porog_number):
                                    bot.send_message(message.chat.id, f"{onlyBankValute[0]} {onlyBankValute[8]}")

                    bot.send_message(message.chat.id, "Парсинг сайта выполнен, можно перезапустить бота нажав /start")
                    print('Парсинг Банков выполнен')

                except:
                    bot.send_message(message.chat.id, "Введите число")
                    bot.register_next_step_handler(message, valuta_porog)

            bot.register_next_step_handler(message, valuta_porog)
        else:
            bot.send_message(message.chat.id, "Введите корректные данные или запустите бот нажав /start")
            print('конец корректных данных')
    bot.register_next_step_handler(message, category_text)
    print('конец Start')

# Получение любого сообщения
@bot.message_handler(content_types=["text"])
def any_message(message):
    bot.send_message(message.chat.id, "Введите корректные данные или запустите бот нажав /start")
    print("конец AnyMessage")



# Запускаем бота
bot.polling(none_stop=True, interval=0)









