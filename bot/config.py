from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot API
    bot_api_key: str

    # Bot settings
    limit: int = 10
    window: int = 60

    # OpenAI
    base_url: str
    openai_api_key: str
    llm_model: str
    temp: float = 0.3

    # DB
    sqlalchemy_url: str = "sqlite:///./data/philo_chat.db"

    # Commands
    commands: list[tuple[str, str]] = [
        ("/philosophers", "Get the list of philosophers")
    ]

    # Philosophers
    philosophers: list[str] = [
        "Nietzsche",
        "Schopenhauer",
        "Socrates",
        "Machiavelli",
        "Albert Camus",
        "Gorgias",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Config()
