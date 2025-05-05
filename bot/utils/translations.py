translations = {
    "uz": {
        "about_bank": "🏦 Bank haqida",
        "services_json": "📄 Xizmatlar",
        "support": "🤖 Chatbot",
        "faq": "❓ Tez-tez so‘raladigan savollar",
        "back": "⬅️ Orqaga",
        "choose_category": "📚 FAQ turini tanlang:",
        "choose_question": "📚 Savolni tanlang:",
        "not_found": "❌ Bu savol topilmadi.",
    },
    "ru": {
        "about_bank": "🏦 О банке",
        "services_json": "📄 Услуги",
        "support": "🤖 Чат-бот",
        "faq": "❓ Часто задаваемые вопросы",
        "back": "⬅️ Назад",
        "choose_category": "📚 Выберите категорию FAQ:",
        "choose_question": "📚 Выберите вопрос:",
        "not_found": "❌ Этот вопрос не найден.",
    },
    "en": {
        "about_bank": "🏦 About the Bank",
        "services_json": "📄 Services",
        "support": "🤖 Chatbot",
        "faq": "❓ Frequently Asked Questions",
        "back": "⬅️ Back",
        "choose_category": "📚 Choose an FAQ category:",
        "choose_question": "📚 Choose a question:",
        "not_found": "❌ This question was not found.",
    }
}

def get_text(key: str, lang: str = "ru") -> str:
    return translations.get(lang, translations["ru"]).get(key, key)