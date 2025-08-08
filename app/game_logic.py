def start_game() -> list:
    # Создание пустого поля
    matrix = []
    for _ in range(3):
        row = ['⬜️'] * 3
        matrix.append(row)
    return matrix


def make_move(board: list, row: int, col: int, player_symbol: str) -> bool | list:
    if board[row][col] == '⬜️':
        board[row][col] = player_symbol
        return board
    return False


def check_winner(board: list, player_symbol: str) -> bool:
    # Проверка победы игрока (3 в ряд по горизонтали, вертикали, диагонали)
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
    # Проверка ничьи — нет пустых клеток и нет победителя
    for row in board:
        if '⬜️' in row:
            return False
    return True
