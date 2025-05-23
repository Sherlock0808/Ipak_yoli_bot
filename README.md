Ipak Yoli Bot
Данный проект представляет собой Telegram-бота, который использует ИИ-ассистента для ответа на вопросы клиентов банка Ipak Yoli. Бот интегрирован с OpenAI для обработки запросов и предоставления информации по банковским услугам.

🛠 Установка и настройка
1. Клонировать репозиторий
Сначала клонируйте репозиторий на локальную машину:
    ```bash
     git clone https://github.com/Sherlock0808/Ipak_yoli_bot.git
     cd Ipak_yoli_bot

2. Установить зависимости
Убедитесь, что у вас установлен Python 3.7+, затем создайте виртуальное окружение и активируйте его:
    ```bash
      python -m venv venv
      source venv/bin/activate  # для Linux/MacOS
      venv\Scripts\activate     # для Windows

    
После активации окружения установите все необходимые зависимости:

    pip install -r requirements.txt
    
3. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие строки:
   ```bash
    BOT_TOKEN=<your_token>
    OPENAI_API_KEY=<your_open_api_key>
    ASSISTANT_ID=<your_id>

Замените <your_token>, <your_open_api_key>, и <your_id> на реальные значения:

BOT_TOKEN: Ваш токен для Telegram-бота (получите его у BotFather).

OPENAI_API_KEY: Ваш API ключ для доступа к OpenAI (получите его на OpenAI).

ASSISTANT_ID: Уникальный идентификатор вашего ИИ-ассистента.

4. Запуск бота
После настройки всех переменных, запустите бота командой:
   ```bash
   cd bot
   python main.py
   
## 🔧 Используемые технологии

- **aiogram** (v3.20.0.post0) — библиотека для работы с Telegram API, позволяющая создавать асинхронных ботов.
- **openai** (v1.77.0) — API для работы с моделями OpenAI (например, GPT-4), используемое для обработки запросов ИИ-ассистента.
- **SQLAlchemy** (v2.0.40) — ORM (Object-Relational Mapping) для работы с базами данных, используется для взаимодействия с базой данных SQLite.
- **python-dotenv** (v1.1.0) — библиотека для загрузки переменных окружения из файла `.env`.
- **pydantic** (v2.11.4) — библиотека для валидации данных и работы с типами данных.

📄 Лицензия
Этот проект распространяется под лицензией MIT. Для подробностей смотрите файл LICENSE.

