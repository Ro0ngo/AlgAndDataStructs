import numpy as np


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
    max_width = max(len(str(item)) for row in data for item in row)
    for row in data:
        print(" | ".join(f"{str(item).rjust(max_width)}" for item in row))


n = get_positive_integer()
rows = int(n / 2)

matrix = [[0 for _ in range(n)] for _ in range(rows)]
perfect_num = np.zeros(n)

for i in range(rows):
    for j in range(i, n, i + 1):
        matrix[i][j] = i + 1
        if j != i:
            perfect_num[j] += i + 1

print("Совершенные числа:")
for i in range(1, n):
    if perfect_num[i] == i + 1:
        print(int(perfect_num[i]))

# print("Матрица:")
# print_matrix(matrix)
