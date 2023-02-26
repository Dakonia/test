import telebot
import requests
import json


TOKEN = "5867220432:AAGxTVBo_RI2xjrRzgGl5R5Ojwla4ZYuTLE"

bot = telebot.TeleBot(TOKEN)
keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следушем формате: \n\n<Название валюты> \
<В какую валюту перевести> \
<Колличество переводимой валюты> \n\nУвидеть список всех доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text= 'Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text, key,))
    bot.reply_to(message,text)

#@bot.message_handler(content_types=['text',])
class ConvertionException(Exception):
    pass
class Converter:
    @staticmethod
    def get_price(quote:str, base: str, amount:str):

        if quote==base:
            raise ConvertionException(f'Не удалось перевести одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        try:
            amount = str(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}. Введите целое число.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/6f3fb2412d2bf36d47f4a77b/pair/{quote_ticker}/{base_ticker}/{amount}')

        resp= json.loads(r.content)
        total_base = json.loads(r.content)['conversion_result']
        return total_base

@bot.message_handler(content_types=['text', ])
def conver(message: telebot.types.Message):

        values = message.text.split(' ')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
