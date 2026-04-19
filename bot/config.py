from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Bot API
    bot_api_key: str

    # LLM API settings
    base_url: str
    openai_api_key: str
    llm_model: str

    # Commands
    commands: list[tuple[str, str]] = [
        ("/choose_philosopher", "Select the philosopher you want to chat with"),
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
