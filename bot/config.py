from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Bot API
    bot_api_key: str

    # LLM API config
    base_url: str
    openai_api_key: str
    llm_model: str

    # Commands
    commands: list[tuple[str, str]] = [
        ("/philosophers", "Get the list of philosophers")
    ]

    # Philosophers
    philosophers: list[str] = ["Nietzsche", "Schopenhauer", "Socrates", "Machiavelli"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


config = Config()
