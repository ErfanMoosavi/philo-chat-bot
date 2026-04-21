import logging

from openai import OpenAI
from sqlalchemy.orm import Session

from bot.models.user import User

logger = logging.getLogger(__name__)


class PhiloChat:
    def get_or_create_user(
        self, session: Session, user_id: int, user_name: str
    ) -> User:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, name=user_name)
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"User '{user_id}' created")
        else:
            logger.info("User already exists")
        return user

    def start_or_resume_chat(
        self, session: Session, user_id: int, user_name: str, philosopher: str
    ) -> bool:
        user = self.get_or_create_user(session, user_id, user_name)
        user.active_chat = philosopher

        try:
            user.new_chat(philosopher)
            session.commit()
            logger.info(f"Created new chat with '{philosopher}' for user '{user_id}'")
            return True
        except ValueError:
            session.commit()
            logger.info(f"Chat with '{philosopher}' already exists, resuming...")
            return False

    def reset_chat(self, session: Session, user_id: int) -> str:
        user = self._find_user(session, user_id)

        if not user or not user.active_chat:
            return "❌You don't have an active chat to reset."

        philosopher = user.active_chat
        chat_to_reset = user._find_chat(philosopher)

        if chat_to_reset:
            user.chats.remove(chat_to_reset)

            user.new_chat(philosopher)

            session.commit()
            return f"🧹Your conversation with <b>{philosopher}</b> has been reset!"

        return "❌No conversation history found to reset."

    def generate_response(
        self,
        session: Session,
        openai_client: OpenAI,
        user_id: int,
        philosopher: str,
        text: str,
    ) -> str:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return "❌Session expired. Please type /start again."

        try:
            response = user.generate_response(openai_client, philosopher, text)
        except Exception as e:
            logger.error(str(e))
            response = "I'm pondering on my thoughts, I'll come back soon."

        session.commit()
        return response

    def _find_user(self, session: Session, user_id: int) -> User | None:
        return session.query(User).filter(User.id == user_id).first()
