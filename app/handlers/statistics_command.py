from app.database.players import PlayerDB
from app.bot_instance import bot
from telebot.types import Message
from app.messages.message_text import STATS_TEXT, NO_STATS

players = PlayerDB()


def statistics(message: Message) -> None:
    """
    Отправляет статистику игрока по ID.
    Если статистики нет — сообщает об этом.
    """
    user_id = message.from_user.id
    stats = players.get_player_stats(user_id)

    if stats is None:
        bot.send_message(message.chat.id, NO_STATS)
        return

    user_id, username, games_played, wins, losses, draws, elo_rating = stats

    response = STATS_TEXT.format(
        username=username,
        games_played=games_played,
        wins=wins,
        losses=losses,
        draws=draws,
        elo_rating=elo_rating
    )
    bot.send_message(message.chat.id, response)
