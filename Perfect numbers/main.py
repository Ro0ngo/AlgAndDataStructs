import numpy as np
from scipy.sparse import lil_matrix


def get_positive_integer():
    while True:
        try:
            num = int(input("Введите положительное целое число n: "))
            if num > 0:
                return num
            else:
                print("Ошибка: число должно быть больше нуля. Попробуйте снова.")
        except ValueError:
            print("Ошибка: введено некорректное значение. Пожалуйста, введите целое число.")


def print_matrix(data):
    dense_data = data.toarray()
    max_width = max(len(str(item)) for row in dense_data for item in row)
    for row in dense_data:
        print(" | ".join(f"{str(item).rjust(max_width)}" for item in row))


if __name__ == '__main__':
    n = get_positive_integer()
    rows = n // 2

    matrix = lil_matrix((rows, n), dtype=np.int32)
    perfect_num = np.zeros(n, dtype=np.int32)

    for i in range(rows):
        for j in range(i, n, i + 1):
            matrix[i, j] = i + 1
            if j != i:
                perfect_num[j] += i + 1

    matrix_csr = matrix.tocsr()

    print("Совершенные числа:")
    for i in range(1, n):
        if perfect_num[i] == i + 1:
            print(int(perfect_num[i]))

    # print("Матрица:")
    # print_matrix(matrix_csr)
