from telebot.types import CallbackQuery

from app.message_text import *


def callback_handler(call: CallbackQuery, bot, active_games: dict, create_board_keyboard, check_winner, check_draw):
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

    # Проверяем, выиграл ли текущий игрок после этого хода
    if check_winner(game['board'], symbol):
        for pid in game['players_id']:
            if pid == user_id:
                bot.send_message(pid, YOU_WIN)
            else:
                bot.send_message(pid, YOU_LOSE)
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
            pass  # игнорируем ошибки, например, если сообщение удалено
