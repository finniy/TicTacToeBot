from telebot.types import Message

from app.bot_instance import bot, active_games
from app.utils import is_user_in_game, create_board_keyboard
from app.message_text import *


# Добавление пользователя в игру
def add_user(message: Message) -> None:
    user_id = message.from_user.id  # ID присоединившегося пользователя
    game_key_entered = message.text.strip().upper()  # Код игры, введённый пользователем
    joiner_user_name = message.from_user.username if message.from_user.username else 'Анонимный игрок'

    # Если пользователь уже играет — отказ
    if is_user_in_game(user_id):
        bot.send_message(
            chat_id=message.chat.id,
            text=YOU_IN_ANOTHER_GAME
        )
        return

    # Проверка, существует ли игра с введённым ключом
    if game_key_entered not in active_games:
        bot.send_message(
            chat_id=message.chat.id,
            text=GAME_NOT_FOUNDED
        )
        return

    # Проверка, что игрок не в этой же игре
    if user_id in active_games[game_key_entered]['players_id']:
        bot.send_message(
            chat_id=message.chat.id,
            text=YOU_IN_THIS_GAME
        )
        return

    # Добавляем игрока в список участников
    active_games[game_key_entered]['players_id'].append(user_id)
    active_games[game_key_entered]['players_name'].append(joiner_user_name)
    active_games[game_key_entered]['symbols'][user_id] = '⭕'  # Второму игроку ставим нолики

    # Данные о создателе игры
    creator_id = active_games[game_key_entered]['players_id'][0]
    creator_name = active_games[game_key_entered]['players_name'][0] or 'Анонимный игрок'

    # Создаём игровое поле (inline-кнопки)
    keyboard = create_board_keyboard(active_games[game_key_entered]['board'], game_key_entered)

    # Сообщение создателю игры
    msg1 = bot.send_message(
        chat_id=creator_id,
        text=FIRST_MOVE.format(joiner_user_name),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    # Сообщение присоединившемуся игроку
    msg2 = bot.send_message(
        chat_id=user_id,
        text=SECOND_MOVE.format(creator_name),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    # Сохраняем ID сообщений, чтобы потом обновлять их при ходе
    active_games[game_key_entered]['messages'] = {
        creator_id: msg1.message_id,
        user_id: msg2.message_id,
    }

    # Логи в консоль
    print(f'[+] {joiner_user_name} присоединился к игре {game_key_entered}')
    print(f'[+] Началась игра {game_key_entered}')
