import random
import string

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot_instance import active_games


# Проверяем, участвует ли пользователь в активной игре
def is_user_in_game(user_id: int) -> bool:
    for game in active_games.values():
        if user_id in game["players_id"]:  # если пользователь в списке игроков
            return True
    return False


# Генерируем уникальный ключ игры из заглавных букв и цифр
def generate_game_key(length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))


# Создаем клавиатуру с кнопками игрового поля
def create_board_keyboard(board, game_key):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for i, row in enumerate(board):
        row_buttons = []
        for j, char in enumerate(row):
            text = char
            callback_data = f"{game_key}_{i}_{j}"  # данные для обработки нажатия кнопки
            btn = InlineKeyboardButton(text=text, callback_data=callback_data)
            row_buttons.append(btn)
        keyboard.add(*row_buttons)
    return keyboard
