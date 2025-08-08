from telebot.types import CallbackQuery

def callback_handler(call: CallbackQuery, bot, active_games: dict, create_board_keyboard, check_winner, check_draw):
    data = call.data

    if '_' in data:
        try:
            game_key, row, col = data.split('_')
            row, col = int(row), int(col)
        except Exception:
            bot.answer_callback_query(call.id, "Некорректные данные.")
            return

        if game_key not in active_games:
            bot.answer_callback_query(call.id, "Игра не найдена.")
            return

        game = active_games[game_key]
        user_id = call.from_user.id

        if game['turn'] != user_id:
            bot.answer_callback_query(call.id, "Сейчас ходит другой игрок.")
            return

        if game['board'][row][col] != '⬜️':
            bot.answer_callback_query(call.id, "Эта клетка уже занята.")
            return

        symbol = game['symbols'][user_id]
        game['board'][row][col] = symbol

        if check_winner(game['board'], symbol):
            for pid in game['players_id']:
                bot.send_message(pid, f"🎉 Победил игрок {user_id}!")
            del active_games[game_key]
            bot.answer_callback_query(call.id)
            return

        if check_draw(game['board']):
            for pid in game['players_id']:
                bot.send_message(pid, "🤝 Ничья!")
            del active_games[game_key]
            bot.answer_callback_query(call.id)
            return

        players = game['players_id']
        game['turn'] = players[1] if game['turn'] == players[0] else players[0]

        keyboard = create_board_keyboard(game['board'], game_key)
        for player_id in players:
            try:
                message_id = game['messages'].get(player_id)
                if message_id:
                    bot.edit_message_reply_markup(chat_id=player_id, message_id=message_id, reply_markup=keyboard)
            except Exception:
                pass
    else:
        game_key = data
        chat_id = call.message.chat.id
        bot.send_message(chat_id=chat_id, text=game_key)
        bot.answer_callback_query(call.id)

    bot.answer_callback_query(call.id)