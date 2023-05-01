import telebot
import traceback
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

#пропишем приветствие и инструкцию
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет!\n Чтобы начать работу, введите команду боту в следующем формате:\n \
<имя валюты, цену которой хотите узнать>\n \
<имя валюты, в которую хотите перевести>\n \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

#пропишем какие валюты доступны для выбора
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#пропишем цену одной валюты в единицах другой валюты
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        base, quote, amount = values
        answer = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()