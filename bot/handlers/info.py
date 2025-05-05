from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from database.get_from_db import get_faq_categories, get_all_faqs, get_user_language
from aiogram import Router, types, F
from bot.keyboards.buttons import faq_back, service_buttons, service_back
from bot.utils.translations import get_text
from bot.json_func import get_keys_of_service, deposit_info, get_about_info, clean_references
from pathlib import Path
from config import assistant_id
from uuid import uuid4
import aiohttp
import openai
import time
import os

router = Router()


async def download_image(url: str, folder: str = 'media') -> str:
    Path(folder).mkdir(parents=True, exist_ok=True)
    ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
    filename = f"{uuid4().hex}{ext}"
    filepath = os.path.join(folder, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    f.write(await response.read())
                return filepath
            else:
                raise Exception(f"Failed to download image. Status: {response.status}")


@router.message(F.text.in_(["🏦 О банке", "🏦 Bank haqida", "🏦 About the Bank"]))
async def about_bank(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    about_info, image = get_about_info(lang)
    await message.answer_photo(photo=image, caption=about_info)


@router.message(F.text.in_(["🤖 Чат-бот", "🤖 Chatbot"]))
async def support(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer('''Здравствуйте!
Я — ИИ-ассистент банка Ipak Yoli.
Готов помочь вам с любыми вопросами по банковским услугам.
Пожалуйста, напишите ваш вопрос.''')


@router.message(F.text.in_(["📄 Услуги", "📄 Xizmatlar", "📄 Services"]))
async def services(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer('Выберите услугу: ', reply_markup=service_buttons())


@router.callback_query(lambda c: c.data and c.data.startswith("services"))
async def service_sub(callback_query: types.CallbackQuery):
    category = callback_query.data.split("_")[1]
    names = get_keys_of_service(category)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in names:
        idx = names.index(i)
        btn = InlineKeyboardButton(text=i, callback_data=f'product_{idx}_{category}')
        markup.inline_keyboard.append([btn])
    markup.inline_keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'product_back_none')])
    await callback_query.message.edit_text(f'Выберите интересующую вас услугу:', reply_markup=markup)


@router.callback_query(lambda c: c.data and c.data.startswith("product"))
async def service_btn(callback_query: types.CallbackQuery):
    idx = callback_query.data.split("_")[1]
    category = callback_query.data.split("_")[2]

    if idx == 'back':
        await callback_query.message.edit_text('Выберите услугу: ', reply_markup=service_buttons())
    else:
        product_info = deposit_info(category, idx)

        # Ограничение длины caption
        caption = f'{product_info[0]}\n\n{product_info[1]}'
        if len(caption) > 1024:
            caption = caption[:1020] + '...'

        # Скачиваем фото и отправляем
        photo_path = await download_image(product_info[-1])
        photo_file = FSInputFile(photo_path)

        await callback_query.message.delete()
        await callback_query.message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=service_back(product_info[-2], category)
        )


@router.callback_query(lambda c: c.data and c.data.startswith("serback"))
async def service_sub_back(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    category = callback_query.data.split("_")[1]
    names = get_keys_of_service(category)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in names:
        idx = names.index(i)
        btn = InlineKeyboardButton(text=i, callback_data=f'product_{idx}_{category}')
        markup.inline_keyboard.append([btn])
    markup.inline_keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'product_back_none')])
    await callback_query.message.answer(f'Выберите интересующую вас услугу:', reply_markup=markup)


@router.message(F.text.in_(["❓ Часто задаваемые вопросы", "❓ Tez-tez so‘raladigan savollar", "❓ Frequently Asked Questions"]))
async def faq_command(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    categories = await get_faq_categories(language=lang)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat, callback_data=f"faq_category:{cat}")]
            for cat in categories
        ]
    )
    await message.answer(get_text("choose_category", lang), reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("faq_category:"))
async def faq_category_callback(callback_query: types.CallbackQuery):
    category = callback_query.data.split(":")[1]
    lang = await get_user_language(callback_query.from_user.id)
    faqs = await get_all_faqs(language=lang)
    filtered_faqs = [faq for faq in faqs if faq.category == category]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat.question, callback_data=f"faq_question:{cat.id}")]
            for cat in filtered_faqs
        ]
    )
    keyboard.inline_keyboard.append([InlineKeyboardButton(text=get_text("back", lang), callback_data=f'main_faq')])

    await callback_query.message.edit_text(get_text("choose_question", lang), reply_markup=keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("faq_question:"))
async def faq_question_callback(callback_query: types.CallbackQuery):
    question_id = int(callback_query.data.split(":")[1])
    lang = await get_user_language(callback_query.from_user.id)
    faqs = await get_all_faqs(language=lang)
    selected_faq = next((faq for faq in faqs if faq.id == question_id), None)

    MAX_LENGTH = 4000  # чуть меньше лимита, с запасом

    text = f"❓{selected_faq.question}\n\n💬 {selected_faq.answer}"
    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH - 3] + "..."

    if selected_faq:
        await callback_query.message.edit_text(text, reply_markup=faq_back(selected_faq.category, lang))
    else:
        await callback_query.answer(get_text("not_found", lang))


@router.callback_query(lambda c: c.data and c.data.startswith("back_faq_"))
async def faq_back_callback(callback_query: types.CallbackQuery):
    category = callback_query.data.replace("back_faq_", "")
    lang = await get_user_language(callback_query.from_user.id)
    faqs = await get_all_faqs(language=lang)
    filtered_faqs = [faq for faq in faqs if faq.category == category]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=faq.question, callback_data=f"faq_question:{faq.id}")]
            for faq in filtered_faqs
        ]
    )

    keyboard.inline_keyboard.append([InlineKeyboardButton(text=get_text("back", lang), callback_data=f'main_faq')])

    await callback_query.message.edit_text(
        text=get_text("choose_question", lang),
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith("main_faq"))
async def main_menu_faq(callback_query: types.CallbackQuery):
    lang = await get_user_language(callback_query.from_user.id)
    categories = await get_faq_categories(language=lang)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cat, callback_data=f"faq_category:{cat}")]
            for cat in categories
        ]
    )
    await callback_query.message.edit_text(get_text("choose_category", lang), reply_markup=keyboard)


@router.message(F.text)
async def handle_message(message: types.Message):
    user_input = message.text

    thread = openai.beta.threads.create()

    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            await message.reply("❌ Ошибка выполнения.")
            return
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    reply = messages.data[0].content[0].text.value
    result = clean_references(reply)
    await message.reply(result)