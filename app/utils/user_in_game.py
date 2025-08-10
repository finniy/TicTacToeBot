from app.bot_instance import active_games


# Проверяем, участвует ли пользователь в любой игре
def is_user_in_all_game(user_id: int) -> bool:
    for game in active_games.values():
        if user_id in game["players_id"]:  # если пользователь в списке игроков
            return True
    return False


# Проверяем, участвует ли пользователь в чужой игре
def is_user_in_another_game(user_id: int) -> bool:
    for game in active_games.values():
        if user_id in game["players_id"] and len(game["players_id"]) == 2:  # если пользователь в чужой игре
            return True
    return False


# Проверяем, участвует ли пользователь в своей игре
def is_user_in_his_game(user_id: int) -> bool:
    for game in active_games.values():
        if user_id in game["players_id"] and len(game["players_id"]) == 1:  # если пользователь в своей игре
            return True
    return False
