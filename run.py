import telebot

from config import TOKEN, keys
from extensions import RequestAPI, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "\nЧто бы начать работу введити команду боту в слудующем формате:\n<имя валюты> " \
           "<в какую валюту перевести> <кол-во валюты>\n\n" \
           "Что бы увидить список всех доступных валют /values\n\n" \
           "Пример ввода если вы хотите ввести число дестичной дроби: 0.5"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
       text = '\n   '.join((text, key))
    bot.reply_to(massage, text)


@bot.message_handler(content_types=['text'])
def messages(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много прараметров.')

        base, quote, amount = values
        response = RequestAPI.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(massage, f'Пользовательская ошибка\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Неудалось обработать команду\n{e}')

    else:
        text = f"{amount} {base} = {response} {quote}"
        bot.reply_to(massage, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

