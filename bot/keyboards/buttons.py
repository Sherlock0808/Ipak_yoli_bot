from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.translations import translations
from bot.json_func import get_keys_of_service


def main_menu(lang: str = 'ru'):
    t = translations.get(lang, translations["ru"])
    markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=t["services_json"]), KeyboardButton(text=t["support"])],
        [KeyboardButton(text=t["faq"]), KeyboardButton(text=t["about_bank"])]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел ⤵",
    one_time_keyboard=True)
    return markup


def faq_back(faq_category, lang):
    t = translations.get(lang, translations["ru"])
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    btn = [InlineKeyboardButton(text=t["back"], callback_data=f'back_faq_{faq_category}')]
    markup.inline_keyboard.append(btn)
    return markup


def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 Oʻzbekcha", callback_data="set_language:uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_language:en")]
    ])

def service_buttons():
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    categories = ['Вклады', 'Кредиты', 'Карты']
    for i in categories:
        btn = InlineKeyboardButton(text=i, callback_data=f'services_{i}')
        markup.inline_keyboard.append([btn])
    return markup


def define_service_info(category):
    names = get_keys_of_service(category)
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    for i in names:
        btn = InlineKeyboardButton(text=i, callback_data=f'product_{i}')
        markup.inline_keyboard.append([btn])
    markup.inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data=f'product_back')])
    return markup

def service_back(link, category):
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    markup.inline_keyboard.append([InlineKeyboardButton(text='Узнать подробнее...', url=link)])
    markup.inline_keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'serback_{category}')])
    return markup
