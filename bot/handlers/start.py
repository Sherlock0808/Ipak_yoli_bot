from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from keyboards.buttons import main_menu, language_keyboard
from database.db import async_session, add_user
from database.models import User
from database.get_from_db import get_user_language
from sqlalchemy import select

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    async with async_session() as session:  # Открываем сессию
        await add_user(
            session,
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            language=message.from_user.language_code
        )
    lang = await get_user_language(message.from_user.id)
    if lang == 'en':
        text = '👋 Welcome to the Bank!\nI am your virtual assistant.'
    elif lang == 'uz':
        text = '👋 Bankimizga xush kelibsiz!\nMen sizning virtual yordamchingizman.'
    else:
        text = "👋 Добро пожаловать в Банк!\nЯ ваш виртуальный помощник."
    await message.answer(text, reply_markup=main_menu(lang))


@router.message(Command("language"))
async def change_language(message: types.Message):
    await message.answer("🌐 Выберите язык:", reply_markup=language_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith("set_language:"))
async def set_language(callback_query: types.CallbackQuery):
    lang = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.language = lang

        await session.commit()

    if lang == 'en':
        text = f'✅ Language successfully changed to {lang}\nClick /start'
    elif lang == 'uz':
        text = f'✅ Til {lang}-ga muvaffaqiyatli oʻzgartirildi\n /Start tugmasini bosing'
    else:
        text = f"✅ Язык успешно изменён на {lang}\nНажмите /start"
    await callback_query.message.edit_text(text)