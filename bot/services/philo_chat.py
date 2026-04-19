from bot.config import config


class PhiloChat:
    @staticmethod
    def get_greetings() -> str:
        return config.greetings

    @staticmethod
    def get_philosophers() -> str:
        philosophers = "Here are our dear philosophers that you can chat with!\n\n"
        for i, philosopher in enumerate(config.philosophers):
            philosophers += f"{i + 1}- {philosopher}\n"
        return philosophers

    @staticmethod
    def get_help_menu() -> str:
        help_menu = ""
        for command, desc in config.commands:
            help_menu += f"{command}: {desc}\n"
        return help_menu
