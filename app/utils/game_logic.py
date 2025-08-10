def start_game() -> list:
    """Создаёт и возвращает пустое игровое поле 3x3."""
    matrix = []
    for _ in range(3):
        row = ['⬜️'] * 3
        matrix.append(row)
    return matrix


def make_move(board: list, row: int, col: int, player_symbol: str) -> bool | list:
    """Выполняет ход игрока, если клетка свободна; возвращает обновлённое поле или False."""
    if board[row][col] == '⬜️':
        board[row][col] = player_symbol
        return board
    return False


def check_winner(board: list, player_symbol: str) -> bool:
    """Проверяет, есть ли у игрока победа (3 в ряд по горизонтали, вертикали или диагонали)."""
    lines = []

    # строки и столбцы
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # столбцы

    # диагонали
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if all(elem == player_symbol for elem in line):
            return True
    return False


def check_draw(board: list) -> bool:
    """Проверяет, что ничья — нет пустых клеток на поле."""
    for row in board:
        if '⬜️' in row:
            return False
    return True
