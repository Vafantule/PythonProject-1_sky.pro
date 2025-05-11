import re


def get_mask_card_number(user_card_number_input: str) -> str:
    """
    Функция скрытия части вводимого номера карты.
    :param user_card_number_input: Вводимый номер карты.
    :return: Вывод отформатированной строки номера карты.
    """
    # Преобразуем число в строку и удаляем пробелы.
    # card_str = str(user_card_number_input).replace(" ", "")
    card_str = re.sub(r'\D', '', str(user_card_number_input))

    # Проверка, что строка состоит только из цифр и длина с выбросом исключения
    if not ((12 <= len(card_str) <= 19) and card_str.isdigit()):
        raise ValueError("Ошибка: Длина номера карты должна быть от 12 до 19 символов.")

    # Для 12 символов: XXX X** *** XXX
    if len(card_str) == 12:
        masked = f"{card_str[:3]}{card_str[3]}**{card_str[-3:]}"
        formatted = f"{masked[:3]} {masked[3:6]} *** {masked[-3:]}"
    else:
        # Для 13–19 символов: XXXX XX** **** XXXX
        stars_count = len(card_str) - 10  # Звездочки для середины
        masked = card_str[:6] + "*" * stars_count + card_str[-4:]
        formatted = f"{masked[:4]} {masked[4:6]}** {'*' * (stars_count - 2)} {masked[-4:]}"

    return formatted


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
