import telebot
from telebot.types import Message
from app.config import API_KEY
from app.generate_game_key import generate_game_key
from app.game_logic import start_game

bot = telebot.TeleBot(API_KEY)
active_games = {}


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/start'))
def start(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="👋 Привет! Это бот *Крестики-Нолики*!\n\n"
             "📌 Доступные команды:\n"
             "/create — создать новую игру\n"
             "/join — присоединиться к игре по коду\n"
             "/help — помощь по командам",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/help'))
def help(message: Message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="🆘 Помощь:\n\n"
             "/create — создаёт новую игру и выдаёт уникальный код\n"
             "/join — подключение к существующей игре по коду\n\n"
             "Передай другу код игры, чтобы он подключился к тебе!",
    )


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/create'))
def create(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username
    game_key = generate_game_key()
    if user_id not in active_games:
        print(f'[+] {user_name} создал игру')
        active_games[user_id] = game_key
        bot.send_message(
            chat_id=message.chat.id,
            text=f"✅ Игра создана!\n"
                 f"🔑 Код: *{game_key}*\n"
                 f"Отправь этот код другу, чтобы он присоединился!",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже создали игру или участвуете в другой."
        )


def add_user(message: Message) -> None:
    user_id = message.from_user.id
    user_name_join = message.from_user.username
    game_key_entered = message.text.strip()

    if user_id in active_games:
        bot.send_message(chat_id=message.chat.id, text="⚠️ Вы уже участвуете в игре.")
        return

    active_games[user_id] = game_key_entered
    opponent_found = False

    for key, value in active_games.items():
        if value.upper() == game_key_entered.upper() and key != user_id:
            opponent_found = True

            bot.send_message(chat_id=key, text=f"👤 @{user_name_join} присоединился к вашей игре!")

            board_str = '\n\n'.join('    '.join(row) for row in start_game())

            bot.send_message(chat_id=key, text=board_str)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"✅ Вы успешно подключились к игре *{game_key_entered.upper()}*",
                parse_mode="Markdown"
            )
            bot.send_message(chat_id=message.chat.id, text=board_str)
            print(f'[+] @{user_name_join} присоединился к игре {game_key_entered}')
            break

    if not opponent_found:
        del active_games[user_id]
        bot.send_message(chat_id=message.chat.id,
                         text="❌ Игра с таким ключом не найдена или вы пытаетесь подключиться к своей игре.")


@bot.message_handler(func=lambda m: m.text and m.text.lower().startswith('/join'))
def join(message: Message) -> None:
    user_id = message.from_user.id
    if user_id not in active_games:
        if active_games:
            games_list = "\n".join(game for game in active_games.values())
            bot.send_message(
                chat_id=message.chat.id,
                text=f"🎮 Активные игры:\n{games_list}\n\nВведите код игры, к которой хотите присоединиться:"
            )
            bot.register_next_step_handler(message, add_user)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="📭 Сейчас нет активных игр"
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="⚠️ Вы уже создали игру или играете"
        )


def main():
    bot.polling(none_stop=True)
