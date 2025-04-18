# import re


def get_mask_card_number(user_card_number_input: str) -> str:
    """Функция скрытия части вводимого номера карты."""
    # Удаление возможных пробелов
    user_card_number = (user_card_number_input[:16].replace(" ", ""))

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

# print(get_mask_card_number(input("Ввод номера карты: ")))


def get_mask_account(user_account_number_input: str) -> str:
    """Функция отображения последних 4 символов номера счета."""
    # Удаление возможных пробелов
    user_account_number = user_account_number_input[:20].replace(' ', '')

    # Подстановка "*" вместо цифр, кроме последних_4
    private_account_number = "*" * len(user_account_number[-2:]) + user_account_number[-4:]
    return private_account_number

# print(get_mask_account(input("Ввод номера счета: ")))
