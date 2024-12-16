from typing import List
from tqdm import tqdm
from tabulate import tabulate


def solve_n_queens(n: int) -> List[List[int]]:
    solutions = set()
    board = [-1] * n
    columns = set()
    diag1 = set()
    diag2 = set()

    def add_solution():
        solution = tuple(board)
        solutions.add(solution)
        if n % 2 == 0 or board[0] != n // 2:
            mirrored = tuple(n - 1 - pos for pos in board)
            solutions.add(mirrored)

    def backtrack(row: int):
        if row == n:
            add_solution()
            return

        for column in range(n):
            if column in columns or (row - column) in diag1 or (row + column) in diag2:
                continue
            board[row] = column
            columns.add(column)
            diag1.add(row - column)
            diag2.add(row + column)
            backtrack(row + 1)
            columns.remove(column)
            diag1.remove(row - column)
            diag2.remove(row + column)
            board[row] = -1

    middle = n // 2

    for col in tqdm(range(middle, n), desc="Поиск решений", unit="столбец"):
        board[0] = col
        columns.add(col)
        diag1.add(0 - col)
        diag2.add(0 + col)
        backtrack(1)
        columns.remove(col)
        diag1.remove(0 - col)
        diag2.remove(0 + col)

    return list(solutions)


def print_solutions(solutions: List[List[int]], n: int) -> None:
    if not solutions:
        print("Решений не найдено!")
        return

    for idx, solution in enumerate(solutions, start=1):
        print(f"Решение {idx}:")

        table = []

        for row in range(n):
            line = ['Q' if col == solution[row] else ' ' for col in range(n)]
            table.append(line)

        print(tabulate(table, headers=[f"{i + 1}" for i in range(n)], tablefmt="grid"))

        print("\n")


def main():
    try:
        n = int(input("Введите размер доски (N): "))
        if n <= 0:
            raise ValueError("Размер доски должен быть положительным целым числом.")
    except ValueError as e:
        print(f"Некорректный ввод: {e}")
        return

    solutions = solve_n_queens(n)
    print(f"Количество уникальных решений для {n}-ферзей: {len(solutions)}\n")
    print_solutions(solutions, n)


if __name__ == "__main__":
    main()
