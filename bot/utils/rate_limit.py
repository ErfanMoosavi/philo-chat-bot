import time
from collections import defaultdict
from functools import wraps

user_message_log = defaultdict(list)


def rate_limit(bot, limit, window):
    def decorator(func):
        @wraps(func)
        async def wrapped(message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time.time()

            user_message_log[user_id] = [
                t for t in user_message_log[user_id] if current_time - t < window
            ]

            if len(user_message_log[user_id]) >= limit:
                await bot.reply_to(message, "📜 <b>The mind is overwhelmed...</b>")
                return

            user_message_log[user_id].append(current_time)
            return await func(message, *args, **kwargs)

        return wrapped

    return decorator
