import telebot
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from app.work_with_inline import callback_handler
from app.add_user_in_game import *
from app.config import API_KEY
from app.generate_game_key import generate_game_key
from app.game_logic import *
from app.work_with_keyboard import *

bot = telebot.TeleBot(API_KEY)
active_games = {}


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/start'))
def start(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="👋 Привет! Это бот *Крестики-Нолики*!\n\n"
             "📌 Доступные команды:\n"
             "/create — создать новую игру\n"
             "/join — присоединиться к игре по коду\n"
             "/help — помощь по командам",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/help'))
def help(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="🆘 Помощь:\n\n"
             "/create — создаёт новую игру и выдаёт уникальный код\n"
             "/join — подключение к существующей игре по коду\n\n"
             "Передай другу код игры, чтобы он подключился к тебе!",
    )


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/create'))
def create(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username if message.from_user.username is not None else 'Анонимный игрок'

    if is_user_in_game(user_id, active_games):
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже участвуете в другой игре."
        )
        return

    game_key = generate_game_key()
    active_games[game_key] = {
        "players_id": [user_id],
        "players_name": [user_name],
        "board": start_game(),
        "turn": user_id,
        "symbols": {user_id: '❌'},
        "messages": {}
    }

    print(f'[+] {user_name} создал игру {game_key}')

    bot.send_message(
        chat_id=message.chat.id,
        text=f"✅ Игра создана!\n"
             f"🔑 Код: *{game_key}*\n"
             f"Отправь этот код другу, чтобы он присоединился!",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/join'))
def join(message: Message) -> None:
    user_id = message.from_user.id

    if is_user_in_game(user_id, active_games):
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже участвуете в другой игре."
        )
        return

    if active_games:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for game_key in active_games.keys():
            btn = KeyboardButton(text=game_key)
            keyboard.add(btn)

        bot.send_message(
            chat_id=message.chat.id,
            text="🎮 Выберете игру:",
            reply_markup=keyboard
        )
        bot.register_next_step_handler(message, lambda msg: add_user(msg, bot, active_games))

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="📭 Сейчас нет активных игр"
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    callback_handler(
        call,
        bot,
        active_games,
        create_board_keyboard,
        check_winner,
        check_draw
    )

def main():
    bot.polling(none_stop=True)
