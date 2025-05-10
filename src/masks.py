import re


def get_mask_card_number(user_card_number_input: str) -> str:
    # Удаление возможных пробелов
    # user_card_number = user_card_number_input.split()[-1][:16]
    # user_card_number = str(user_card_number_input)

    # Проверка на пустые строки
    # if not user_card_number.strip():
    #     raise ValueError("Не введен номер карты")

    # Проверка, что номер карты состоит только из цифр
    # if not user_card_number.isdigit():
    #     raise ValueError("Номер карты должен содержать только цифры")

    # Подстановка "*" вместо цифр, кроме первых_6, последних_4
    # private_card_number = (
    #     user_card_number[:6]
    #     + (len(user_card_number[6:-4]) * "*")
    #     + user_card_number[-4:]
    # )
    #
    # # Группировка строки по 4 секции?
    #
    # chunks, chunks_size = (
    #     len(private_card_number),
    #     len(private_card_number) // 4
    # )
    #
    # return " ".join(
    #         [
    #             private_card_number[index : index + chunks_size] \
    #             for index in range(0, chunks, chunks_size)
    #         ]
    #     )


    """
    Функция скрытия части вводимого номера карты.
    :param user_card_number_input: Вводимый номер карты.
    :return: Вывод отформатированной строки номера карты.
    """
    if re.match(r"\d{16}$", user_card_number_input):
        return (f"{user_card_number_input[0:4]} "
                f"{user_card_number_input[4:6]}** **** "
                f"{user_card_number_input[12:16]}")
    else:
        return "Номер карты не корректный. Просьба вводить только !! 16 !! цифр."


# if __name__ == "__main__":
    print(get_mask_card_number(input("Ввод номера карты: ")))


def get_mask_account(user_account_number_input: str) -> str:
        # Удаление возможных пробелов
    # user_account_number = user_account_number_input[:20].replace(' ', '')
    #
    # # Подстановка "*" вместо цифр, кроме последних_4
    # private_account_number = "*" * len(user_account_number[-2:]) + user_account_number[-4:]
    # return private_account_number

    """
    Функция отображения последних 4 символов номера счета.
    :param user_account_number_input: Вводимый номер счета.
    :return: Вывод отформатированной строки номера счета.
    """

    if re.match(r"\d{20}$", user_account_number_input):
        return f"**{user_account_number_input[-4:]}"
    else:
        return "Номер счета не корректный. Просьба вводить только !! 20 !! цифр."


# if __name__ == "__main__":
    print(get_mask_account(input("Ввод номера счета: ")))
