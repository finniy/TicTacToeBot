from telebot.types import BotCommand
from telebot.types import CallbackQuery
from telebot.types import Message

from app.bot_instance import bot
from app.handlers.add_user_in_game import add_user
from app.handlers.create_game import create
from app.handlers.join_game import join
from app.handlers.work_with_inline import callback_handler
from app.messages.message_text import START_TEXT, HELP_TEXT, GITHUB_LINK_TEXT

# Настройка списка команд для меню бота в Telegram
commands = [
    BotCommand("start", "Приветственное сообщение"),
    BotCommand("help", "Список команд и инструкция"),
    BotCommand("create", "Создать новую игру"),
    BotCommand("join", "Присоединиться к игре"),
    BotCommand("github", "Ссылка на GitHub проекта")
]


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/start'))
def start(message: Message) -> None:
    # Обрабатывает команду /start — отправляет приветственное сообщение
    bot.send_message(message.chat.id, START_TEXT, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/help'))
def help(message: Message) -> None:
    # Обрабатывает команду /help — отправляет список команд и инструкцию
    bot.send_message(message.chat.id, HELP_TEXT, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/github'))
def send_my_github(message: Message) -> None:
    # Обрабатывает команду /github — отправляет ссылку на исходный код бота
    bot.send_message(message.chat.id, GITHUB_LINK_TEXT)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/create'))
def handle_create(message: Message) -> None:
    # Обрабатывает команду /create — создаёт новую игру
    create(message)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/join'))
def handle_join(message: Message) -> None:
    # Обрабатывает команду /join — показывает список игр и подключает игрока
    join(message, add_user)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    # Обрабатывает нажатия на inline-кнопки
    callback_handler(call)


def main():
    # Запускает бота в режиме постоянного опроса Telegram API
    bot.set_my_commands(commands)
    bot.polling(none_stop=True)
