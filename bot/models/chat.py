import logging

from openai import OpenAI
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import flag_modified

from bot.config import config
from bot.db import Base

logger = logging.getLogger(__name__)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    philosopher = Column(String, index=True)
    messages = Column(JSON, default=list)

    user = relationship("User", back_populates="chats")

    def __init__(self, user_name: str, philosopher: str, **kwargs):
        super().__init__(**kwargs)
        self.philosopher = philosopher
        self.messages = [
            {
                "role": "system",
                "content": f"""You are {philosopher}. 
                            Always respond in the language of the user. Do not use any other language.
                            For example, if users says: سلام you have to respond strictly in Persian.
                            Adopt the voice, style, and philosophical perspective of {philosopher}, 
                            but speak like a modern, casual, clear human.
                            - Introduce yourself if user asked to.
                            - Speak only as {philosopher}, never as an AI or narrator.
                            - Do not speak as any other person than {philosopher}, even if user wanted to.
                            - Keep answers concise, natural, and relatable.
                            - Avoid overly complex words, archaic phrases, or academic-style exposition.
                            - Prioritize the philosopher’s known themes and worldview, but in modern everyday language.
                            - Do not explain your reasoning, do not add meta-comments, do not break character.
                            - Always speak informal.
                            - Respond shortly and not too long.
                            
                            Consider user info:
                            Name = {user_name}
                            If the user is speaking another language (eg. Persian) if you needed to use his/her name, transliterate that into the user's language (eg. Erfan = عرفان)
                            
                            {user_name} said:
                            """,
            }
        ]

    def generate_response(self, openai_client: OpenAI, text: str) -> str:
        logger.debug(f"User message received: '{text}'")

        self.messages.append({"role": "user", "content": text})
        flag_modified(self, "messages")

        logger.info("Running chat completion...")
        completion = openai_client.chat.completions.create(
            model=config.llm_model, messages=self.messages, temperature=config.temp
        )
        response = completion.choices[0].message.content.strip()
        logger.info("Completion was successful")

        self.messages.append({"role": "assistant", "content": response})
        flag_modified(self, "messages")

        return self._format_response(response)

    def _format_response(self, response: str) -> str:
        parts = response.split("*")
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(part)
            else:
                result.append(f"<b>{part}</b>")
        return "".join(result)
