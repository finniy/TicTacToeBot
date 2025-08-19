# ❌⭕ Telegram-бот — для игры Крестики-Нолики

**Крестики Нолики Бот** — это Telegram-бот, который позволяет играть в классическую игру крестики-нолики вдвоём прямо в
чате. Удобное управление через кнопки, система рейтинга Эло, статистика игроков.

---

## 🚀 Возможности

- 🎮 Создание и присоединение к игре по уникальному коду
- 🟦 Ход в игру через интерактивные кнопки
- 🏅 Система рейтинга Эло для оценки и ранжирования игроков
- 📊 Просмотр своей статистики и топ-10 игроков
- 🤖 Удобный и понятный интерфейс в Telegram

---

## 🛠️ Стек технологий

![Python](https://img.shields.io/badge/-Python-05122A?style=flat&logo=python)
![sqlite3](https://img.shields.io/badge/-sqlite3-05122A?style=flat&logo=sqlite)
![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-05122A?style=flat&logo=telegram)
![logger](https://img.shields.io/badge/%E2%9A%A0-logger-05122A?style=flat&logo=logging)
![python-dotenv](https://img.shields.io/badge/%F0%9F%8C%BF-python--dotenv-05122A?style=flat)

---

## 📦 Установка

1. Клонируйте репозиторий

```bash
git clone https://github.com/finniy/TicTacToeBot.git
cd TicTacToeBot
```

2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости

```bash
pip install -r requirements.txt
```

4. Укажите токен бота в `.env`

```bash
API_KEY=YOUR_TELEGRAM_BOT_TOKEN
```

5. Запустите бота

```bash
python main.py
```

---

## 📂 Структура проекта

``` 
TicTacToeBot/
├── app/
│ ├── bot_instance.py
│ ├── config.py
│ ├── logger.py
│ ├── telegram_bot.py
│ ├── database/
│ │ ├── init.py
│ │ ├── game.py
│ │ ├── players.py
│ ├── handlers/
│ │ ├── init.py
│ │ ├── create_game.py
│ │ ├── join_game.py
│ │ ├── rating_command.py
│ │ ├── statistics_command.py
│ │ ├── work_with_inline.py
│ ├── messages/
│ │ ├── init.py
│ │ └── message_text.py
│ └── utils/
│ ├── init.py
│ ├── game_logic.py
│ ├── user_in_game.py
│ └── delete_game.py
├── images/
│   ├── Photo1.png
│   └── Photo2.png
├── .env
├── .env.template
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## 💬 Использование

1. Запустите бота в Telegram.
2. Используйте команды:

    - `/start` — приветственное сообщение и регистрация игрока
    - `/create` — создать новую игру в Крестики-Нолики
    - `/join` — присоединиться к существующей игре
    - `/statistics` — показать вашу игровую статистику
    - `/rating` — показать топ-10 игроков по рейтингу Эло
    - `/help` — помощь и список команд
    - `/github` — ссылка на исходный код проекта

---

## ⚙️ О системе рейтинга

Используется система рейтинга Эло ⭐, которая автоматически корректирует рейтинг игроков после каждой партии в
зависимости от результата и уровня соперника.

---

## 📸 Примеры работы бота

<img src="images/Photo1.png" width="600" style="display: block; margin: auto;">

<img src="images/Photo2.png" width="600" style="display: block; margin: auto;">


## 📄 Лицензия

Проект распространяется под лицензией MIT. Свободно используй, дорабатывай и распространяй с указанием авторства.

---

## 👤 Автор

🚀 **[Перейти к боту в Telegram](https://t.me/XOpy_bot)**

- GitHub: [@finniy](https://github.com/finniy)
- Telegram: [@fjnnjk](https://t.me/fjnnjk)

💌 Не забудьте поставить звезду ⭐ на GitHub, если вам понравился бот! 😉
