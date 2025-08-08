from telebot.types import Message
from app.work_with_keyboard import *


def is_user_in_game(user_id: int, active_games: dict) -> bool:
    for game in active_games.values():
        if user_id in game["players_id"]:
            return True
    return False


def add_user(message: Message, bot, active_games: dict) -> None:
    user_id = message.from_user.id
    game_key_entered = message.text.strip().upper()
    joiner_user_name = message.from_user.username if message.from_user.username else 'Анонимный игрок'

    if is_user_in_game(user_id, active_games):
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже участвуете в другой игре."
        )
        return

    if game_key_entered not in active_games:
        bot.send_message(
            chat_id=message.chat.id,
            text="❌ Игра с таким ключом не найдена."
        )
        return

    if user_id in active_games[game_key_entered]['players_id']:
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже в этой игре."
        )
        return

    active_games[game_key_entered]['players_id'].append(user_id)
    active_games[game_key_entered]['players_name'].append(joiner_user_name)
    active_games[game_key_entered]['symbols'][user_id] = '⭕'

    creator_id = active_games[game_key_entered]['players_id'][0]
    creator_name = active_games[game_key_entered]['players_name'][0] or 'Анонимный игрок'

    keyboard = create_board_keyboard(active_games[game_key_entered]['board'], game_key_entered)

    msg1 = bot.send_message(
        chat_id=creator_id,
        text=f"✅ Игра началась!\n\nПротивник:\n*{joiner_user_name}*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    msg2 = bot.send_message(
        chat_id=user_id,
        text=f"✅ Игра началась!\n\nПротивник:\n*{creator_name}*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    active_games[game_key_entered]['messages'] = {
        creator_id: msg1.message_id,
        user_id: msg2.message_id,
    }

    print(f'[+] {joiner_user_name} присоединился к игре {game_key_entered}')
    print(f'[+] Началась игра {game_key_entered}')
