from app.database.players import PlayerDB
from app.bot_instance import bot
from telebot.types import Message
from app.messages.message_text import PLAYERS_EMPTY, RATING_HEADER, RATING_LINE

players = PlayerDB()


def rating(message: Message) -> None:
    """
    Отправляет топ-10 игроков по рейтингу ELO.
    Если рейтинг пуст, информирует об этом.
    """
    top_players = players.get_top_players(10)

    if not top_players:
        bot.send_message(message.chat.id, PLAYERS_EMPTY)
        return

    response = RATING_HEADER
    for i, player in enumerate(top_players, start=1):
        user_id, username, games_played, wins, losses, draws, elo_rating = player
        response += RATING_LINE.format(
            pos=i,
            username=username,
            elo=elo_rating,
            wins=wins,
            losses=losses,
            draws=draws
        )

    bot.send_message(message.chat.id, response)