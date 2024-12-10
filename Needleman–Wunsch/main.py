first_word = input("Введите первое слово: ").upper()
second_word = input("Введите второе слово: ").upper()

matrix = [[0] * (len(first_word) + 1) for _ in range(len(second_word) + 1)]

for i in range(1, len(second_word) + 1):
    for j in range(1, len(first_word) + 1):
        if second_word[i - 1] == first_word[j - 1]:
            matrix[i][j] = matrix[i - 1][j - 1] + 1
        else:
            matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])

count_match = matrix[len(second_word)][len(first_word)]
print(f"Количество совпадений: {count_match}")

line_matches = ""
i, j = len(second_word), len(first_word)
while i > 0 and j > 0:
    if second_word[i - 1] == first_word[j - 1]:
        line_matches = second_word[i - 1] + line_matches
        i -= 1
        j -= 1
    elif matrix[i - 1][j] > matrix[i][j - 1]:
        i -= 1
    else:
        j -= 1

print(f"Строка совпадений: {line_matches}")

print("\nМатрица совпадений:")
for row in matrix[1:]:
    print(" ".join(map(str, row[1:])))
