import logging

from openai import OpenAI

from bot.core.user import User

logger = logging.getLogger(__name__)


class PhiloChat:
    def __init__(self):
        self.users: dict[int, User] = {}

    def get_or_create_user(self, user_id: int, user_name: str) -> User:
        if user_id not in self.users:
            self.users[user_id] = User(name=user_name)
            logger.info(f"User '{user_id}' created")
        else:
            logger.info("User already exists")
        return self.users[user_id]

    def start_or_resume_chat(
        self, user_id: int, user_name: str, philosopher: str
    ) -> bool:
        user = self.get_or_create_user(user_id, user_name)
        user.active_chat = philosopher

        try:
            user.new_chat(philosopher)
            logger.info(f"Created new chat with '{philosopher}' for user '{user_id}'")
            return True
        except ValueError:
            logger.info(
                f"Chat with '{philosopher}' already exists, resuming conversation..."
            )
            return False

    def generate_response(
        self, openai_client: OpenAI, user_id: int, philosopher: str, text: str
    ) -> str:
        user = self.users.get(user_id)
        if not user:
            return "Session expired. Please type /start again."
        return user.generate_response(openai_client, philosopher, text)

    def _find_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)
