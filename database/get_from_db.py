from sqlalchemy import select, distinct
from database.models import FAQ, User
from database.db import async_session


async def get_all_faqs(language: str):
    async with async_session() as session:
        result = await session.execute(
            select(FAQ).where(FAQ.is_active == True, FAQ.lang == language)
        )
        return result.scalars().all()


async def get_faq_categories(language: str):
    async with async_session() as session:
        result = await session.execute(
            select(distinct(FAQ.category)).where(FAQ.is_active == True, FAQ.lang == language)
        )
        categories = result.scalars().all()
        return categories


async def get_user_language(user_id: int) -> str:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        return user.language if user and user.language else "ru"
