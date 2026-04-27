import logging

from bot.config import config
from bot.db import Base
from bot.utils import format_response, summarize
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

        did_summarize = await self.maybe_summarize(openai_client)
        if did_summarize:
            logger.info(
                f"Chat with {self.philosopher} summarized. Summary:\n{self.messages}"
            )

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

    async def maybe_summarize(self, openai_client: OpenAI) -> bool:
        system_msg = self.messages[0]
        history_str = " ".join([m["content"] for m in self.messages[1:]])

        if len(history_str) <= config.summarization_threshold:
            return False

        summary_text = await summarize(openai_client, history_str)
        self.messages = [
            system_msg,
            {
                "role": "system",
                "content": f"Conversation memory summary:\n{summary_text}",
            },
        ]
        flag_modified(self, "messages")
        return True
