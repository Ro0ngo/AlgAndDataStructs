import json
import random


def generate_numbers(n):
    """ Генерируем все возможные n-значные числа, не начинающиеся с 0. """
    numbers = []
    if n < 1:
        return numbers
    for i in range(10 ** (n - 1), 10 ** n):
        numbers.append(str(i))
    return numbers


def calculate_bulls_and_cows(secret, guess):
    """ Подсчет коров и быков. """
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(min(secret.count(digit), guess.count(digit)) for digit in set(guess)) - bulls
    return bulls, cows


def filter_numbers(possible_numbers, guess, bulls, cows):
    """ Фильтр чисел. """
    return [
        number for number in possible_numbers
        if calculate_bulls_and_cows(number, guess) == (bulls, cows)
    ]


def choose_best_guess(possible_numbers):
    """ Выбор лучшего числа для отгадывания на основе возможных чисел. """
    best_guess = None
    best_score = float('inf')

    for guess in possible_numbers:
        response_counts = {}

        for number in possible_numbers:
            response = calculate_bulls_and_cows(number, guess)
            response_counts[response] = response_counts.get(response, 0) + 1

        worst_case_size = max(response_counts.values())

        if worst_case_size < best_score:
            best_score = worst_case_size
            best_guess = guess

    return best_guess


def best_num(num):
    with open("best_moves.json", "r") as file:
        data = json.load(file)

    return data.get(num)


def main():
    while True:
        n = input("Введите длину числа (n): ")
        if n.isdigit() and int(n) > 0:
            n = int(n)
            break
        else:
            print("Пожалуйста, введите положительное целое число.")

    possible_numbers = generate_numbers(n)

    attempts = 0
    game_mode = input("Выберите режим (1 - стратегический, 2 - случайный): ")
    while game_mode not in ['1', '2']:
        game_mode = input("Пожалуйста, выберите режим (1 - стратегический, 2 - случайный): ")

    while True:
        attempts += 1

        if attempts == 1 and n >= 3:
            guess = best_num(str(n)) if game_mode == '1' else random.choice(possible_numbers)
        else:
            guess = choose_best_guess(possible_numbers) if game_mode == '1' else random.choice(possible_numbers)

        print(f"Попытка {attempts}: {guess}")
        print(f"Возможные числа осталось: {len(possible_numbers)}")

        while True:
            try:
                bulls = int(input("Введите количество быков: "))
                cows = int(input("Введите количество коров: "))
                if bulls < 0 or cows < 0:
                    raise ValueError("Количество быков и коров не может быть отрицательным.")
                break
            except ValueError:
                print("Пожалуйста, введите неотрицательные целые числа.")

        if bulls == n:
            print(f"Поздравляем! Вы угадали число {guess} за {attempts} попыток!")
            break

        possible_numbers = filter_numbers(possible_numbers, guess, bulls, cows)

        if not possible_numbers:
            print("Нет подходящих чисел. Попробуйте еще раз.")
            break

    play_again = input("Хотите сыграть еще раз? (да/нет): ")
    if play_again.lower() == 'да':
        main()


if __name__ == '__main__':
    main()
