from bot.config import config
from bot.dependencies import get_philo_chat
from telebot import TeleBot

bot = TeleBot(token=config.bot_api_key)


@bot.message_handler(commands=["start"])
def greet(message):
    greetings = get_philo_chat().get_greetings()
    bot.send_message(message.chat.id, greetings)


@bot.message_handler(commands=["help"])
def help(message):
    help_menu = get_philo_chat().get_help_menu()
    bot.reply_to(message, help_menu)


@bot.message_handler(commands=["philosophers"])
def get_philosophers(message):
    philosophers = get_philo_chat().get_philosophers()
    bot.reply_to(message, philosophers)


bot.polling()
