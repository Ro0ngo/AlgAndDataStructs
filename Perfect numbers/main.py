import numpy as np
from scipy.sparse import lil_matrix
from tabulate import tabulate


def get_positive_integer(prompt="Введите положительное целое число n: "):
    while True:
        try:
            num = int(input(prompt))
            if num > 0:
                return num
            else:
                print("Ошибка: число должно быть больше нуля. Попробуйте снова.")
        except ValueError:
            print("Ошибка: введено некорректное значение. Пожалуйста, введите целое число.")


def print_matrix(data):
    print(tabulate(data, tablefmt="grid"))


if __name__ == '__main__':
    while True:
        show_table = input("Хотите увидеть матрицу? (да/нет): ").strip().lower()
        if show_table in ['да', 'yes', 'y', 'нет', 'no', 'n']:
            break
        else:
            print("Ошибка: пожалуйста, введите 'да' или 'нет'.")

    n = get_positive_integer()
    rows = n // 2

    if show_table in ['да', 'yes', 'y']:
        matrix = np.zeros((rows, n), dtype=np.int32)
        perfect_num = np.zeros(n, dtype=np.int32)
    else:
        matrix = lil_matrix((rows, n), dtype=np.int32)
        perfect_num = np.zeros(n, dtype=np.int32)

    for i in range(rows):
        for j in range(i, n, i + 1):
            matrix[i, j] = i + 1
            if j != i:
                perfect_num[j] += i + 1

    print("Совершенные числа:")
    for i in range(1, n):
        if perfect_num[i] == i + 1:
            print(int(perfect_num[i]))

    if show_table in ['да', 'yes', 'y']:
        print_matrix(matrix)
