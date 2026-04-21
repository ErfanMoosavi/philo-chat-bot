import time
from collections import defaultdict
from functools import wraps

from telebot import TeleBot

user_message_log = defaultdict(list)


def rate_limit(bot: TeleBot, limit: int, window: int):
    def decorator(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time.time()

            user_message_log[user_id] = [
                t for t in user_message_log[user_id] if current_time - t < window
            ]

            if len(user_message_log[user_id]) >= limit:
                bot.reply_to(
                    message,
                    "📜 <b>The mind is overwhelmed.</b> Even the greatest thinkers need a moment of silence to let the dust of thought settle. Give me a minute to find my clarity again.",
                )
                return

            user_message_log[user_id].append(current_time)
            return func(message, *args, **kwargs)

        return wrapped

    return decorator
