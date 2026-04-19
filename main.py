import logging

from bot.config import settings
from telebot import TeleBot

bot = TeleBot(token=settings.bot_api_key)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@bot.message_handler(commands=["start"])
def greet(message):
    bot.send_message(
        message.chat.id,
        "Welcome to Philo Chat!\nCommands? Use /help and see what's possible",
    )


@bot.message_handler(commands=["help"])
def help(message):
    help_menu = ""
    for command, desc in settings.commands:
        help_menu += f"{command}: {desc}\n"
    bot.reply_to(message, help_menu)


bot.polling()
