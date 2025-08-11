import sqlite3
import threading


class PlayerDB:
    def __init__(self, db_path='database.db'):
        """
        Инициализирует подключение к базе и создает таблицу игроков.
        """
        self.db_path = db_path
        self.lock = threading.Lock()
        self.create_table()

    def get_connection(self):
        """
        Возвращает новое соединение с базой данных.
        """
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def create_table(self):
        """
        Создает таблицу игроков, если её ещё нет.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0,
                    rating INTEGER DEFAULT 1000
                )
            ''')
            conn.commit()

    def add_or_update_player(self, user_id: int, username: str):
        """
        Добавляет игрока или обновляет его имя пользователя.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
                if cursor.fetchone() is None:
                    cursor.execute(
                        'INSERT INTO players (user_id, username, rating) VALUES (?, ?, ?)',
                        (user_id, username, 1000)
                    )
                else:
                    cursor.execute('UPDATE players SET username = ? WHERE user_id = ?', (username, user_id))
                conn.commit()

    def update_stats(self, user_id: int, won=False, lost=False, draw=False):
        """
        Обновляет статистику игр (выигрыши, поражения, ничьи) и общее число игр.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Получаем текущий рейтинг игрока
                cursor.execute('SELECT rating FROM players WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                current_rating = row[0] if row else 1000

                # Обновляем статистику игр
                cursor.execute('UPDATE players SET games_played = games_played + 1 WHERE user_id = ?', (user_id,))
                if won:
                    cursor.execute('UPDATE players SET wins = wins + 1 WHERE user_id = ?', (user_id,))
                elif lost:
                    cursor.execute('UPDATE players SET losses = losses + 1 WHERE user_id = ?', (user_id,))
                elif draw:
                    cursor.execute('UPDATE players SET draws = draws + 1 WHERE user_id = ?', (user_id,))

                conn.commit()

    def get_player_stats(self, user_id: int):
        """
        Возвращает статистику игрока по user_id.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
                return cursor.fetchone()

    def calculate_elo(self, winner_rating, loser_rating, draw=False, k=32):
        """
        Вычисляет новые рейтинги ELO с учётом результата (победа/ничья).
        """
        expected_win = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
        if draw:
            score_winner = 0.5
            score_loser = 0.5
        else:
            score_winner = 1
            score_loser = 0
        new_winner_rating = winner_rating + k * (score_winner - expected_win)
        new_loser_rating = loser_rating + k * (score_loser - (1 - expected_win))
        return round(new_winner_rating), round(new_loser_rating)

    def update_elo_game(self, winner_id=None, loser_id=None, draw=False):
        """
        Обновляет рейтинги игроков после игры с учётом результата.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Получаем рейтинги игроков
                cursor.execute('SELECT rating FROM players WHERE user_id = ?', (winner_id,))
                winner_rating_row = cursor.fetchone()
                winner_rating = winner_rating_row[0] if winner_rating_row else 1000

                cursor.execute('SELECT rating FROM players WHERE user_id = ?', (loser_id,))
                loser_rating_row = cursor.fetchone()
                loser_rating = loser_rating_row[0] if loser_rating_row else 1000

                if draw:
                    new_winner_rating, new_loser_rating = self.calculate_elo(winner_rating, loser_rating, draw=True)
                else:
                    new_winner_rating, new_loser_rating = self.calculate_elo(winner_rating, loser_rating, draw=False)

                # Обновляем рейтинги в БД
                cursor.execute('UPDATE players SET rating = ? WHERE user_id = ?', (new_winner_rating, winner_id))
                cursor.execute('UPDATE players SET rating = ? WHERE user_id = ?', (new_loser_rating, loser_id))
                conn.commit()

    def get_top_players(self, limit=10):
        """
        Возвращает топ игроков по рейтингу, ограничение задаётся параметром limit.
        """
        with self.lock:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id, username, games_played, wins, losses, draws, rating
                    FROM players
                    ORDER BY rating DESC
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
