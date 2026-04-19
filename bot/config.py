from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot API
    bot_api_key: str

    # LLM API config
    base_url: str
    openai_api_key: str
    llm_model: str

    # Greetings
    greetings: str = (
        "Welcome to Philo Chat!\nCommands? Use /help and see what's possible"
    )

    # Commands
    commands: list[tuple[str, str]] = [
        ("/philosophers", "Get the list of philosophers")
    ]

    # Philosophers
    philosophers: list[str] = ["Nietzsche", "Schopenhauer"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Config()
