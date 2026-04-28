from bot.db import Base
from bot.models.chat import Chat
from openai import OpenAI
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    active_chat = Column(String, nullable=True)
    chats = relationship(
        "Chat", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def new_chat(self, philosopher: str) -> None:
        chat = self._find_chat(philosopher)
        if chat:
            raise ValueError("Chat already exists")

        new_chat = Chat(user_name=self.name, philosopher=philosopher)
        self.chats.append(new_chat)

    async def generate_response(
        self, openai_client: OpenAI, philosopher: str, text: str
    ) -> str:
        chat = self._find_chat(philosopher)
        if not chat:
            raise ValueError("Chat session does not exist.")
        return await chat.generate_response(openai_client, text)

    def _find_chat(self, philosopher: str) -> Chat | None:
        for chat in self.chats:
            if chat.philosopher == philosopher:
                return chat
        return None
