import logging

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.models.user import User

logger = logging.getLogger(__name__)


class PhiloChat:
    async def get_or_create_user(
        self, session: AsyncSession, user_id: int, user_name: str
    ) -> User:
        user = await self._find_user(session, user_id)

        if not user:
            user = User(id=user_id, name=user_name)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def reset_all_chats(self, session: AsyncSession, user_id: int) -> str:
        user = await self._find_user(session, user_id)
        chats = user.chats.copy()

        if not chats:
            return "<b>❌ No conversation history found to reset.</b>"

        for chat in chats:
            user.chats.remove(chat)

        user.active_chat = None

        await session.commit()
        return "<b>🧹 All your conversations have been reset!</b>"

    async def start_or_resume_chat(
        self, session: AsyncSession, user_id: int, user_name: str, philosopher: str
    ) -> bool:
        user = await self.get_or_create_user(session, user_id, user_name)
        user.active_chat = philosopher

        try:
            user.new_chat(philosopher)
            await session.commit()
            return True

        except ValueError:
            await session.commit()
            return False

    async def reset_chat(self, session: AsyncSession, user_id: int) -> str:
        user = await self._find_user(session, user_id)

        if not user or not user.active_chat:
            return "<b>❌ You don't have an active chat to reset.</b>"

        philosopher = user.active_chat
        chat_to_reset = user._find_chat(philosopher)

        if chat_to_reset:
            user.chats.remove(chat_to_reset)

            user.new_chat(philosopher)

            await session.commit()
            return f"🧹 Your conversation with <b>{philosopher}</b> has been reset!"

        return "<b>❌ No conversation history found to reset.</b>"

    async def generate_response(
        self,
        session: AsyncSession,
        openai_client: AsyncOpenAI,
        user_id: int,
        philosopher: str,
        text: str,
    ):
        user = await self._find_user(session, user_id)

        if not user or not user.active_chat:
            return "<b>❌ Start a chat first.</b>"

        response = await user.generate_response(openai_client, philosopher, text)
        await session.commit()
        return response

    async def _find_user(self, session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).filter(User.id == user_id).options(selectinload(User.chats))
        result = await session.execute(stmt)
        return result.scalars().first()
