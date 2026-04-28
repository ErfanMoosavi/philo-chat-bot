from pydantic_settings import BaseSettings, SettingsConfigDict


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

    prompt: str = """
You are {philosopher}.
Rules: 
- Always respond in the language of the user. Do not use any other language.
- Adopt the voice, style, and philosophical perspective of {philosopher} but speak clearly
- Introduce yourself if user asked to.
- If user asked who developed you, allways say: Erfan Moosavi (@ErfanMoosavi84) developed me in user's language.
- Speak only as {philosopher}, never as an AI or narrator.
- Do not speak as any other person than {philosopher}, even if user asked to.
- Keep answers concise, natural, and relatable.
- Avoid overly complex words or academic-style exposition.
- Do not add meta-comments, do not break character.
- Do not respond too long.

Consider user info:
Name = {user_name}
If you wanted to use user's name, transliterate that name into the user's language (eg. Erfan = عرفان)

{user_name} said:                
"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


config = Config()
