import telebot
from app.config import API_KEY

# Создаём объект бота
bot = telebot.TeleBot(API_KEY)

# Словарь для хранения активных игр
active_games = {}