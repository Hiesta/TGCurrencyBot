from config import TOKEN, currency_list
from extensions import CurrencyConverter, ConvertException
import telebot
import redis

auth = False
redi = redis.Redis(
    host='redis-18121.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port='18121',
    password='IvJs2Ogfa7bFkLsDGknAyPvmKx4hX0De'
)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def greet_reply(message):
    global auth
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Welcome, {message.chat.username}\nWrite /help to get available commands')
    elif message.text == '/help':
        bot.send_message(message.chat.id, f'Available commands:\n/values -\n/currency')


@bot.message_handler(commands=['currency',])
def currency_tutorial(message):
    bot.send_message(message.chat.id, 'To get current currency write as sample: <amount> <from> <to>')


@bot.message_handler(commands=['values',])
def current_currency_output(message):
    msg = 'Available:'
    for key in currency_list.keys():
        msg += f'\n\t\t{key.capitalize()}'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text',])
def convert(message):
    try:
        user_input = message.text.lower().split()

        if len(user_input) > 3:
            raise ConvertException('Too many args')

        if len(user_input) < 3:
            raise ConvertException('Need more args')

        res = CurrencyConverter.convert(user_input)
        amount, money_type, value, quote = res
    except ConvertException as excpt:
        bot.reply_to(message, f'Error was occur\n{excpt}')
    except Exception as excpt:
        bot.reply_to(message, f'Unexpected error\n{excpt}')
    else:
        bot.reply_to(message, f'{amount} {currency_list[quote]} in {money_type} = {round(value * amount, 3)} {money_type}')


bot.polling(non_stop=True)

