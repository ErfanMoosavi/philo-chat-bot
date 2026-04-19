from bot.config import config


class Formatter:
    @staticmethod
    def format_greeting() -> str:
        return "<b>Welcome to PhiloChat!</b> 🏛️\n\nType /chat to begin.\n\nDeveloper: @ErfanMoosavi84"

    @staticmethod
    def format_philosopher_list() -> str:
        philosophers = "<b>Our Philosophers:</b>\n\n"
        for i, philosopher in enumerate(config.philosophers):
            philosophers += f"{i + 1}. <b>{philosopher}</b>\n"
        return philosophers

    @staticmethod
    def format_ai_message(message: str) -> str:
        parts = message.split("*")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(part)
            else:
                result.append(f"<b>{part}</b>")
        return "".join(result)
