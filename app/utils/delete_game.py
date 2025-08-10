from app.bot_instance import active_games
from app.logger import logger


def auto_delete_game(game_key: str) -> None:
    """Удаляет игру, если в ней до сих пор один игрок."""
    game = active_games.get(game_key)
    if game and len(game["players_id"]) == 1:
        del active_games[game_key]
        logger.info(f"Игра {game_key} удалена из-за отсутствия второго игрока")
