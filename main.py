import logging

from bot.config import config
from bot.core.philo_chat import PhiloChat
from openai import OpenAI
from telebot import TeleBot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

bot = TeleBot(token=config.bot_api_key, parse_mode="HTML")
philo_chat = PhiloChat()
openai_client = OpenAI(base_url=config.base_url, api_key=config.openai_api_key)

bot.set_my_commands(
    [
        types.BotCommand("start", "Philosophize"),
        types.BotCommand("chat", "Begin your conversation"),
    ]
)


@bot.message_handler(commands=["start"])
def start(message):
    philo_chat.get_or_create_user(message.from_user.id, message.from_user.first_name)
    greetings = "<b>🤔Who are you? Feel free to ask Nietzsche - or Schopenhauer?</b>\n\nType /chat to begin.\n\n🧬Developer: @ErfanMoosavi84"
    bot.send_message(message.chat.id, greetings)


@bot.message_handler(commands=["chat"])
def request_chat_selection(message):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = []
    for philosopher in config.philosophers:
        buttons.append(
            InlineKeyboardButton(text=philosopher, callback_data=f"chat_{philosopher}")
        )

    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i : i + 2])

    bot.send_message(
        message.chat.id,
        "<b>🏛️Who do you want to chat with?</b>",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("chat_"))
def handle_philosopher_selection(call):
    philosopher = call.data.split("_")[1]
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    is_new_chat = philo_chat.start_or_resume_chat(user_id, user_name, philosopher)

    bot.answer_callback_query(call.id)

    if is_new_chat:
        bot.edit_message_text(
            f"⚡You are now chatting with <b>{philosopher}</b>!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    else:
        bot.edit_message_text(
            f"⚡Resuming your chat with <b>{philosopher}</b>.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    user = philo_chat._find_user(user_id)

    if not user or not getattr(user, "active_chat", None):
        bot.reply_to(message, "🧠Start a chat first using /chat")
        return

    bot.send_chat_action(message.chat.id, "typing")
    response = philo_chat.generate_response(
        openai_client, user_id, user.active_chat, message.text
    )
    bot.reply_to(message, response)


if __name__ == "__main__":
    bot.polling()
