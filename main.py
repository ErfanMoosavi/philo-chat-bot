import asyncio
import logging
import os

from bot.config import config
from bot.db import AsyncSessionLocal, init_db
from bot.philo_chat import PhiloChat
from bot.utils import rate_limit
from openai import AsyncOpenAI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

philo_chat = PhiloChat()
bot = AsyncTeleBot(token=config.bot_api_key, parse_mode="HTML")
openai_client = AsyncOpenAI(base_url=config.base_url, api_key=config.openai_api_key)


@bot.message_handler(commands=["start"])
async def start(message):
    async with AsyncSessionLocal() as session:
        await philo_chat.get_or_create_user(
            session, message.from_user.id, message.from_user.first_name
        )

        greetings = "<b>🤔 Who are you? Feel free to ask Nietzsche - or Schopenhauer?</b>\n\nType /chat to begin.\n\n👨🏻‍💻 Developer: @ErfanMoosavi84"
        await bot.send_message(message.chat.id, greetings)


@bot.message_handler(commands=["chat"])
async def request_chat_selection(message):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for philosopher in config.philosophers:
        buttons.append(
            InlineKeyboardButton(text=philosopher, callback_data=f"chat_{philosopher}")
        )
    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i : i + 2])

    await bot.send_message(
        message.chat.id,
        "<b>🏛️ Who do you want to chat with?</b>",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("chat_"))
async def handle_philosopher_selection(call):
    philosopher = call.data.split("_")[1]
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    async with AsyncSessionLocal() as session:
        is_new_chat = await philo_chat.start_or_resume_chat(
            session, user_id, user_name, philosopher
        )

    await bot.answer_callback_query(call.id)

    image_path = f"avatars/{philosopher.lower().replace(' ', '_')}.jpg"

    if is_new_chat:
        caption = f"⚡You are now chatting with <b>{philosopher}</b>"
    else:
        caption = f"⚡Resuming your chat with <b>{philosopher}</b>"

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                await bot.send_photo(
                    call.message.chat.id,
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                )
        else:
            await bot.send_message(call.message.chat.id, caption, parse_mode="HTML")

    except Exception:
        await bot.send_message(call.message.chat.id, caption, parse_mode="HTML")


@bot.message_handler(commands=["reset_chat"])
async def reset_chat(message):
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        result_message = await philo_chat.reset_chat(session, user_id)

    await bot.reply_to(message, result_message)


@bot.message_handler(commands=["reset_all_chats"])
async def reset_all_chats(message):
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        result_message = await philo_chat.reset_all_chats(session, user_id)

    await bot.reply_to(message, result_message)


@bot.message_handler(func=lambda message: True)
@rate_limit(bot=bot, limit=config.limit, window=config.window)
async def generate_response(message):
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:
        user = await philo_chat._find_user(session, user_id)

        if not user or not user.active_chat:
            await bot.reply_to(message, "<b>❌ Start a chat first using /chat</b>")
            return

        await bot.send_chat_action(message.chat.id, "typing")

        response = await philo_chat.generate_response(
            session, openai_client, user_id, user.active_chat, message.text
        )

    await bot.reply_to(message, response)


async def main() -> None:
    await init_db()

    await bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("chat", "Begin your conversation"),
            BotCommand("reset_chat", "Clear current conversation history"),
            BotCommand("reset_all_chats", "Clear all your conversation histories"),
        ]
    )
    await bot.polling()


if __name__ == "__main__":
    asyncio.run(main())
