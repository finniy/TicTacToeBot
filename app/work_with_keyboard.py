from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_board_keyboard(board, game_key):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for i, row in enumerate(board):
        row_buttons = []
        for j, char in enumerate(row):
            text = char
            callback_data = f"{game_key}_{i}_{j}"
            btn = InlineKeyboardButton(text=text, callback_data=callback_data)
            row_buttons.append(btn)
        keyboard.add(*row_buttons)
    return keyboard

