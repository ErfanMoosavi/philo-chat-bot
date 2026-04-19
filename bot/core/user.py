from openai import OpenAI

from bot.core.chat import Chat


class User:
    def __init__(self, name: str):
        self.name = name
        self.chats: dict[str, Chat] = {}
        self.active_chat: str | None = None

    def new_chat(self, philosopher: str) -> None:
        chat = self._find_chat(philosopher)
        if chat:
            raise ValueError("Chat already exists")

        self.chats[philosopher] = Chat(user_name=self.name, philosopher=philosopher)

    def generate_response(
        self, openai_client: OpenAI, philosopher: str, text: str
    ) -> str:
        chat = self._find_chat(philosopher)
        if not chat:
            raise ValueError("Chat session does not exist.")
        return chat.generate_response(openai_client, text)

    def _find_chat(self, philosopher: str) -> Chat | None:
        return self.chats.get(philosopher)
