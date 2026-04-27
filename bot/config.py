from pydantic_settings import BaseSettings, SettingsConfigDict


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
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "philo-bot"
    postgres_host: str = "db"
    postgres_port: int = 5432

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Philosophers
    philosophers: list[str] = [
        "Nietzsche",
        "Schopenhauer",
        "Khayyam",
        "Machiavelli",
        "Albert Camus",
        "Socrates",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


config = Config()
