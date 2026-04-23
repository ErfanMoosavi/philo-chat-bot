from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot API
    bot_api_key: str

    # Bot settings
    summarization_threshold: int = 8000
    limit: int = 10
    window: int = 60

    # OpenAI
    base_url: str
    openai_api_key: str
    llm_model: str
    temp: float = 0.3
    max_tokens: int = 41215

    # DB
    sqlalchemy_url: str = "sqlite:///./data/philo_chat.db"

    # Philosophers
    philosophers: list[str] = [
        "Nietzsche",
        "Schopenhauer",
        "Machiavelli",
        "Albert Camus",
        "Socrates",
        "Epicurus",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Config()
