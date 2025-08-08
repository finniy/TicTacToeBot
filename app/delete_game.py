from telebot.types import Message

from app.bot_instance import bot, active_games
from app.message_text import *


def delete(message: Message):
    user_id = message.from_user.id

    # Найти игру, созданную этим пользователем
    game_key_to_remove = None
    for game_key, game in active_games.items():
        if game['players_id'][0] == user_id:  # создатель — первый в списке
            game_key_to_remove = game_key
            break

    if not game_key_to_remove:
        bot.send_message(
            chat_id=message.chat.id,
            text=NO_DELETE_GAME
        )
        return

    # Удаляем игру
    del active_games[game_key_to_remove]
    bot.send_message(
        chat_id=message.chat.id,
        text=YOUR_GAME_DELETED.format(game_key_to_remove)
    )
    print(f'[+] Игра {game_key_to_remove} удалена создателем {user_id}')
