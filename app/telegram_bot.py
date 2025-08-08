import telebot
from telebot.types import Message
from telebot.types import BotCommand

from app.config import API_KEY
from app.create_game import create
from app.join_game import join
from app.delete_game import delete
from app.work_with_inline import callback_handler

from app.add_user_in_game import *
from app.game_logic import *
from app.message_text import *
from app.utils import create_board_keyboard

bot = telebot.TeleBot(API_KEY)

# Настройка списка команд для меню бота в Telegram
commands = [
    BotCommand("start", "Приветственное сообщение"),
    BotCommand("help", "Список команд и инструкция"),
    BotCommand("create", "Создать новую игру"),
    BotCommand("join", "Присоединиться к игре"),
    BotCommand("delete", "Удалить свою игру"),
    BotCommand("github", "Ссылка на GitHub проекта")
]
# Словарь для хранения всех активных игр
active_games = {}


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


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/delete'))
def handle_delete(message):
    # Обрабатывает команду /leave — позволяет игроку удалить свою игру
    delete(message, bot, active_games)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/create'))
def handle_create(message: Message) -> None:
    # Обрабатывает команду /create — создаёт новую игру
    create(message, bot, active_games)


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/join'))
def handle_join(message):
    # Обрабатывает команду /join — показывает список игр и подключает игрока
    join(message, bot, active_games, add_user)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Обрабатывает нажатия на inline-кнопки
    callback_handler(
        call,
        bot,
        active_games,
        create_board_keyboard,
        check_winner,
        check_draw
    )


def main():
    # Запускает бота в режиме постоянного опроса Telegram API
    bot.set_my_commands(commands)
    bot.polling(none_stop=True)
