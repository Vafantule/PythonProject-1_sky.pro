def get_mask_card_number():
    """Функция скрытия части вводимого номера карты."""
    # Ввод номера карты
    user_card_number_input = input("Ввод номера карты: ")[:16]
    # Удаление возможных пробелов
    user_card_number = user_card_number_input.replace(
        " ", ""
    )

    # Подстановка "*" вместо цифр, кроме первых_6, последних_4
    private_card_number = (
        user_card_number[:6]
        + (len(user_card_number[6:-4]) * "*")
        + user_card_number[-4:]
    )

    # Группировка строки по 4 секции?
    chunks, chunks_size = (
        len(private_card_number),
        len(private_card_number) // 4,
    )

    return " ".join(
        [
            private_card_number[i : i + chunks_size]
            for i in range(0, chunks, chunks_size)
        ]
    )

print(get_mask_card_number())


def get_mask_account(user_account_number_input):
    """Функция отображения последних 4 символов номера счета."""
    # Удаление возможных пробелов
    user_account_number = user_account_number_input.replace(
        " ", ""
    )

    # Подстановка "*" вместо цифр, кроме последних_4
    private_account_number = (
        "*" * len(user_account_number[:-4])
    ) + user_account_number[-4:]

    # Обрезка до последних 6 символов
    result = private_account_number[-6:]
    return result

print(get_mask_account(input("Ввод номера счета: ")[:20]))

# print(get_mask_account())
# print(get_mask_account.__doc__)