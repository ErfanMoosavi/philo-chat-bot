import logging

from bot.config import config
from bot.db import Base
from bot.utils import format_response
from openai import OpenAI
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import flag_modified

logger = logging.getLogger(__name__)


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    philosopher = Column(String, index=True)
    messages = Column(JSON, default=list)
    user = relationship("User", back_populates="chats")

    def __init__(self, user_name: str, philosopher: str, **kwargs):
        super().__init__(**kwargs)
        self.philosopher = philosopher
        self.messages = [
            {
                "role": "system",
                "content": config.prompt.format(
                    philosopher=philosopher, user_name=user_name
                ),
            }
        ]

    async def generate_response(self, openai_client: OpenAI, text: str) -> str:
        logger.debug(f"User message received: '{text}'")

        if len(self.messages) > 10:
            self.messages = [self.messages[0]]

        self.messages.append({"role": "user", "content": text})
        flag_modified(self, "messages")

        logger.info("Running chat completion...")
        completion = await openai_client.chat.completions.create(
            model=config.llm_model,
            messages=self.messages,
            temperature=config.temp,
            max_tokens=config.max_tokens,
        )
        response = completion.choices[0].message.content.strip()
        logger.info("Completion was successful")

        self.messages.append({"role": "assistant", "content": response})
        flag_modified(self, "messages")

        return format_response(response)
