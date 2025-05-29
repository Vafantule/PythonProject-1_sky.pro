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


# Функция для маскировки номера счета
def get_mask_account(user_account_number_input: str) -> str:
    """
    Функция отображения '**' + последние 4 символов номера счета.
    :param user_account_number_input: Вводимый номер счета.
    :return: Вывод отформатированной строки номера счета.
    """
    # Удаляем все нецифровые символы
    digits = ""
    for char in user_account_number_input:
        if char.isdigit():
            digits += char

    # Проверяем длину
    if len(digits) != 20:
        raise ValueError(
            f"Номер счета должен содержать ровно 20 цифр, но содержит: {len(digits)}. "
            f"Входное значение: {digits if digits else 'пустая строка'}")

    # Создаем маску: ** + последние 4 цифры
    masked = "**" + digits[-4:]
    return masked


# if __name__ == "__main__":
    print(get_mask_account(input("Ввод номера счета: ")))
