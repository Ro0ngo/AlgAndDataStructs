from tabulate import tabulate


def is_valid(x, y, board):
    """Проверяет, является ли ход валидным."""
    length = len(board)
    return 0 <= x < length and 0 <= y < length and board[x][y] == -1


def get_degree(x, y, board, x_move, y_move):
    """Вычисляет степень клетки (количество валидных ходов из нее)."""
    degree = 0
    for i in range(8):
        next_x = x + x_move[i]
        next_y = y + y_move[i]
        if is_valid(next_x, next_y, board):
            degree += 1
    return degree


def solve_knights_tour(board, x, y, movei, x_move, y_move, use_warnsdorff=False):
    """Решает задачу о туре коня с или без оптимизации по принципу Ворнсдорфа."""
    length = len(board)
    if movei == length ** 2:
        return True

    moves = []

    for i in range(8):
        next_x = x + x_move[i]
        next_y = y + y_move[i]
        if is_valid(next_x, next_y, board):
            degree = get_degree(next_x, next_y, board, x_move, y_move)
            moves.append((next_x, next_y, degree))

    if use_warnsdorff:
        moves.sort(key=lambda move: move[2])

    for next_x, next_y, _ in moves:
        board[next_x][next_y] = movei

        if solve_knights_tour(board, next_x, next_y, movei + 1, x_move, y_move, use_warnsdorff):
            return True

        board[next_x][next_y] = -1

    return False


def print_board(board):
    """Выводит шахматную доску в красивом формате с использованием tabulate."""
    formatted_board = [[cell if cell != -1 else '' for cell in row] for row in board]
    print(tabulate(formatted_board, tablefmt="grid"))


def knights_tour(start_x, start_y, board_size, use_warnsdorff=True):
    """Запускает решение задачи о туре коня с заданной начальной позицией и размером доски."""

    if not (0 <= start_x < board_size) or not (0 <= start_y < board_size):
        print("Ошибка: начальные координаты должны быть в пределах размера доски.")
        return

    board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
    board[start_x][start_y] = 0

    # Возможные ходы коня
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]

    if not solve_knights_tour(board, start_x, start_y, 1, x_move, y_move, use_warnsdorff):
        print("Решения нет")
    else:
        print_board(board)


def main():
    while True:
        mode = input("Выберите режим (1: Обычный; 2: Оптимизированный (алгоритм Ворнсдорфа)): ")
        if mode in ['1', '2']:
            break
        else:
            print("Ошибка: выберите '1' или '2'.")

    while True:
        try:
            board_size = int(input("Введите размер доски (например: 5 для 5x5): "))
            if board_size < 3:
                raise ValueError("Размер доски должен быть не менее 3.")
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            start_x = int(input(f"Введите начальную координату X (0 до {board_size - 1}): "))
            start_y = int(input(f"Введите начальную координату Y (0 до {board_size - 1}): "))
            if not (0 <= start_x < board_size and 0 <= start_y < board_size):
                raise ValueError("Координаты должны быть в пределах размера доски.")
            break
        except ValueError as e:
            print(e)

    use_warnsdorff = mode == '2'

    knights_tour(start_x, start_y, board_size, use_warnsdorff)


if __name__ == "__main__":
    main()
