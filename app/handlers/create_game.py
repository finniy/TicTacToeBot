import threading
from telebot.types import Message

from app.logger import logger
from app.bot_instance import bot, active_games
from app.utils.delete_game import auto_delete_game
from app.utils.utils import generate_game_key
from app.utils.game_logic import start_game
from app.utils.user_in_game import is_user_in_all_game
from app.messages.message_text import YOU_IN_ANOTHER_GAME, YOU_CREATE_GAME


# Функция для создания новой игры
def create(message: Message) -> None:
    """
    Создаёт новую игру с уникальным кодом, добавляет её в активные игры,
    отправляет сообщение создателю и запускает таймер автоудаления игры через 3 минуты,
    если к ней не присоединится второй игрок.
    """
    user_id = message.from_user.id
    user_name = message.from_user.username if message.from_user.username else 'Анонимный игрок'

    # Проверяем, не находится ли игрок уже в другой игре
    if is_user_in_all_game(user_id):
        bot.send_message(chat_id=message.chat.id, text=YOU_IN_ANOTHER_GAME)
        return

    # Генерируем уникальный код игры
    game_key = generate_game_key()

    # Создаём запись об игре в словаре active_games
    active_games[game_key] = {
        "players_id": [user_id],
        "players_name": [user_name],
        "board": start_game(),
        "turn": user_id,
        "symbols": {user_id: '❌'},
        "messages": {}
    }

    bot.send_message(chat_id=message.chat.id, text=YOU_CREATE_GAME.format(game_key), parse_mode='Markdown')
    logger.info(f'{user_name} создал игру {game_key}')

    # Запускаем таймер удаления через 3 минут (180 сек)
    threading.Timer(180, auto_delete_game, args=(game_key,)).start()
