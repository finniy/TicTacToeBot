from telebot.types import BotCommand
from telebot.types import CallbackQuery
from telebot.types import Message

from app.bot_instance import bot
from app.handlers.add_user_in_game import add_user
from app.handlers.create_game import create
from app.handlers.join_game import join
from app.handlers.work_with_inline import callback_handler
from app.messages.message_text import START_TEXT, HELP_TEXT, GITHUB_LINK_TEXT
from app.database.players import PlayerDB
from app.handlers.statistics_command import statistics
from app.handlers.rating_command import rating

# Настройка списка команд для меню бота в Telegram
commands = [
    BotCommand("start", "👋 Приветственное сообщение"),
    BotCommand("help", "📚 Список команд и инструкция"),
    BotCommand("create", "🎮 Создать новую игру"),
    BotCommand("join", "🤝 Присоединиться к игре"),
    BotCommand("github", "🔗 Ссылка на GitHub проекта"),
    BotCommand("statistics", "📊 Показать статистику игрока"),
    BotCommand("rating", "🏅 Показать топ-10 игроков по рейтингу")
]
players = PlayerDB()


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/start'))
def start(message: Message) -> None:
    """Приветствует пользователя и добавляет/обновляет его в базе."""
    user_id = message.from_user.id
    user_name = message.from_user.username if message.from_user.username else 'Анонимный игрок'

    players.add_or_update_player(user_id, user_name)
    bot.send_message(message.chat.id, START_TEXT, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/help'))
def help(message: Message) -> None:
    """Обрабатывает /help — показывает инструкции и список команд."""
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/github'))
def send_my_github(message: Message) -> None:
    """Обрабатывает /github — отправляет ссылку на GitHub проекта."""
    bot.send_message(message.chat.id, GITHUB_LINK_TEXT)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/create'))
def handler_create(message: Message) -> None:
    """Обрабатывает /create — создаёт новую игру."""
    create(message)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/join'))
def handler_join(message: Message) -> None:
    """Обрабатывает /join — показывает список игр и подключает игрока."""
    join(message, add_user)


@bot.message_handler(func=lambda message: message.text and message.text.lower() == '/statistics')
def handler_statistics(message: Message) -> None:
    """Отправляет статистику игрока."""
    statistics(message)


@bot.message_handler(func=lambda message: message.text and message.text.lower() == '/rating')
def handler_rating(message: Message) -> None:
    """Отправляет топ-10 игроков по рейтингу."""
    rating(message)


@bot.callback_query_handler(func=lambda call: True)
def handler_callback(call: CallbackQuery):
    """Обрабатывает нажатия на inline-кнопки."""
    callback_handler(call)


def main():
    """Запускает бота и устанавливает команды меню Telegram."""
    bot.set_my_commands(commands)
    bot.polling(none_stop=True)
