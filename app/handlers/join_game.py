from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.bot_instance import bot, active_games
from app.handlers.add_user_in_game import is_user_in_game
from app.messages.message_text import YOU_IN_ANOTHER_GAME, TAKE_GAME


def join(message: Message, add_user):
    user_id = message.from_user.id

    if is_user_in_game(user_id):  # проверяем, есть ли пользователь в игре
        bot.send_message(
            chat_id=message.chat.id,
            text=YOU_IN_ANOTHER_GAME
        )
        return

    if active_games:  # если есть активные игры
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)  # создаем клавиатуру
        for game_key in active_games.keys():
            btn = KeyboardButton(text=game_key)  # создаем кнопку для каждой игры
            keyboard.add(btn)

        bot.send_message(
            chat_id=message.chat.id,
            text=TAKE_GAME,
            reply_markup=keyboard  # отправляем клавиатуру с играми
        )
        bot.register_next_step_handler(message, add_user)  # следующий обработчик

    else:  # если активных игр нет
        bot.send_message(
            chat_id=message.chat.id,
            text=NO_ACTIVE_GAME
        )
