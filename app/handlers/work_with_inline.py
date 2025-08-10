from telebot.types import CallbackQuery

from app.bot_instance import bot, active_games
from app.utils.utils import create_board_keyboard
from app.utils.game_logic import check_winner, check_draw
from app.messages.message_text import WORST_DATA, GAME_NOT_FOUNDED, ANOTHER_MOVE, NOT_FREE_PLACE, YOU_WIN, YOU_LOSE, \
    ALL_WIN


def callback_handler(call: CallbackQuery):
    """
    Обрабатывает нажатия на inline-кнопки игрового поля:
    обновляет состояние игры, проверяет победу или ничью, переключает ход и оповещает игроков.
    """
    data = call.data  # данные из нажатой inline-кнопки

    try:
        game_key, row, col = data.split('_')
        row, col = int(row), int(col)
    except Exception:
        bot.answer_callback_query(call.id, WORST_DATA)
        return

    if game_key not in active_games:  # проверяем, что игра существует и активна
        bot.answer_callback_query(call.id, GAME_NOT_FOUNDED)
        return

    game = active_games[game_key]
    user_id = call.from_user.id

    if game['turn'] != user_id:  # если сейчас ходит другой игрок — отменяем действие
        bot.answer_callback_query(call.id, ANOTHER_MOVE)
        return

    if game['board'][row][col] != '⬜️':  # если клетка уже занята — нельзя ходить
        bot.answer_callback_query(call.id, NOT_FREE_PLACE)
        return

    symbol = game['symbols'][user_id]  # символ (крестик или нолик) текущего игрока
    game['board'][row][col] = symbol

    # Меняем очередь хода на другого игрока
    players = game['players_id']
    game['turn'] = players[1] if game['turn'] == players[0] else players[0]

    # Создаем обновленную клавиатуру с игровым полем
    keyboard = create_board_keyboard(game['board'], game_key)

    # Обновляем у каждого игрока сообщение с игрой, чтобы отобразить ход
    for player_id in players:
        try:
            message_id = game['messages'].get(player_id)
            if message_id:
                bot.edit_message_reply_markup(chat_id=player_id, message_id=message_id, reply_markup=keyboard)
        except Exception:
            pass

    # Проверяем, выиграл ли текущий игрок после этого хода
    if check_winner(game['board'], symbol):
        # Находим индекс игрока с победным символом
        winner_index = None
        for idx, pid in enumerate(game['players_id']):
            if game['symbols'][pid] == symbol:
                winner_index = idx
                break

        winner_name = game['players_name'][winner_index] if winner_index is not None else 'Анонимный игрок'

        for pid in game['players_id']:
            if pid == user_id:
                bot.send_message(pid, YOU_WIN)
            else:
                bot.send_message(pid, YOU_LOSE.format(winner_name))
        del active_games[game_key]
        bot.answer_callback_query(call.id)
        return

    # Проверяем, есть ли ничья (все клетки заняты, но победителя нет)
    if check_draw(game['board']):
        for pid in game['players_id']:
            bot.send_message(pid, ALL_WIN)  # сообщаем о ничьей
        del active_games[game_key]
        bot.answer_callback_query(call.id)
        return
