import sqlite3
import threading
import os


class GameDB:
    def __init__(self):
        """
        Инициализирует соединение с базой и создает таблицу игр, если её нет.
        """
        root_dir = os.path.abspath(os.getcwd())
        self.db_path = os.path.join(root_dir, 'database.db')
        self.lock = threading.Lock()
        self.create_table()

    def get_connection(self):
        """
        Возвращает новое соединение с базой данных.
        """
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def create_table(self):
        """
        Создает таблицу games в базе, если она ещё не существует.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_key TEXT UNIQUE,
                    player1 TEXT,
                    player2 TEXT,
                    result TEXT
                )
            ''')
            conn.commit()

    def add_game(self, game_key: str, player1: str, player2: str, result: str):
        """
        Добавляет новую запись об игре с её результатом.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO games (game_key, player1, player2, result)
                    VALUES (?, ?, ?, ?)
                ''', (game_key, player1, player2, result))
                conn.commit()

    def get_game(self, game_key: str):
        """
        Получает информацию об игре по её уникальному ключу.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM games WHERE game_key = ?', (game_key,))
                return cursor.fetchone()
