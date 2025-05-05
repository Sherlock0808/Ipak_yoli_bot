# Ipak_yoli_bot
Тестовый бот для Ipak Yoli bank
Ipak Yoli Bot
Данный проект представляет собой Telegram-бота, который использует ИИ-ассистента для ответа на вопросы клиентов банка Ipak Yoli. Бот интегрирован с OpenAI для обработки запросов и предоставления информации по банковским услугам.

🛠 Установка и настройка
1. Клонировать репозиторий
Сначала клонируйте репозиторий на локальную машину:

bash
Copy
Edit
git clone https://github.com/Sherlock0808/Ipak_yoli_bot.git
cd Ipak_yoli_bot
2. Установить зависимости
Убедитесь, что у вас установлен Python 3.7+, затем создайте виртуальное окружение и активируйте его:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
venv\Scripts\activate     # для Windows
После активации окружения установите все необходимые зависимости:

bash
Copy
Edit
pip install -r requirements.txt
3. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие строки:

plaintext
Copy
Edit
BOT_TOKEN=<your_token>
OPENAI_API_KEY=<your_open_api_key>
ASSISTANT_ID=<your_id>
Замените <your_token>, <your_open_api_key>, и <your_id> на реальные значения:

BOT_TOKEN: Ваш токен для Telegram-бота (получите его у BotFather).

OPENAI_API_KEY: Ваш API ключ для доступа к OpenAI (получите его на OpenAI).

ASSISTANT_ID: Уникальный идентификатор вашего ИИ-ассистента.

4. Запуск бота
После настройки всех переменных, запустите бота командой:

bash
Copy
Edit
python bot.py
Бот будет слушать запросы и отвечать на них через Telegram.

🔧 Используемые технологии
Python 3.7+

aiogram — библиотека для работы с Telegram API.

OpenAI GPT-4 — ИИ для обработки запросов.

dotenv — для работы с переменными окружения.

📄 Лицензия
Этот проект распространяется под лицензией MIT. Для подробностей смотрите файл LICENSE.
