from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from bs4 import BeautifulSoup
import requests

# функция sms() будет вызвана пользователем при отправке команды  start
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # вывод при отправке команды /start
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать']], resize_keyboard=True) #добавляем кнопку
    bot.message.reply_text('Здравствуйте, {}!  \n'
                           'Поговорите со мной!'.format(bot.message.chat.first_name), reply_markup=my_keyboard) # отправим ответ

def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random') #отправляем запрос к странице
    page = BeautifulSoup(receive.text, "html.parser") #подключаем html парсер, подключаем текст страницы
    find = page.select('.anekdot_text') # из страницы html получаем  class="anekdot_text"
    for text in find:
        page = (text.getText().strip()) # из class="anekdot_text"  получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page) # отправлячем  один анекдот, последний

# функция parrot() отвечает тем же сообщением которое ему прислали
def parrot(bot, update):
    print(bot.message.text) # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text) # отправляем обратно текст который пользователь ввел

# Создаем и объявляем функцию  main,  которая соединяется с платформой Telegram
def main():
    # создадим переменную my_bot, с помощью которой будем  взаимодействовать с ботом
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) #  dispather  принимает сообщение от Телеграмма входящее,
    #  addheandler передает в CommandHeandler подписанный на реагирование опредленных событий выполняет следующие действия (когда нажмут старт будет выхвана функция sms()
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) # обработчик текстового сообщения

    my_bot.start_polling() #проверяет о наличии сообщений с платформы Telegram
    my_bot.idle() # бот будет работать пока его не остановят

main()