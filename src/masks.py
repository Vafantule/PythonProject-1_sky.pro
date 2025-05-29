import logging
import os.path
import re


def get_logger(for_test: bool = False) -> logging.Logger:
    """

    :return:
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    upper_dir = os.path.dirname(current_dir)
    log_dir = os.path.join(upper_dir, "logs")

    if for_test:
        log_filename = os.path.join(log_dir, f"test_{module_name}.log")
        logger_name = f"test_{module_name}_log"
    else:
        log_filename = os.path.join(log_dir, f"{module_name}.log")
        logger_name = f"{module_name}_log"

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_filename, "w", encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def get_mask_card_number(user_card_number_input: str, for_test: bool = False) -> str:
    """
    Функция скрытия части вводимого номера карты.
    :param for_test:
    :param user_card_number_input: Вводимый номер карты.
    :return: Вывод отформатированной строки номера карты.
    """
    log = get_logger(for_test=for_test)
    try:
        # Преобразуем число в строку и удаляем пробелы.
        # card_str = str(user_card_number_input).replace(" ", "")
        card_str = re.sub(r'\D', '', str(user_card_number_input))

        # Проверка, что строка состоит только из цифр и длина с выбросом исключения
        if not ((12 <= len(card_str) <= 19) and card_str.isdigit()):
            log.error(f"Ошибка: Длина номера карты должна быть от 12 до 19 символов. "
                      f"Введено: {user_card_number_input}")
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

        log.info(f"Вводные данные: {user_card_number_input} Вывод: {formatted}")
        return formatted

    except Exception as error:
        log.exception(f"Исключение при обработке номера карты: {error}")
        raise


# if __name__ == "__main__":
    print(get_mask_card_number(input("Ввод номера карты: ")))


# Функция для маскировки номера счета
def get_mask_account(user_account_number_input: str, for_test: bool = False) -> str:
    """
    Функция отображения '**' + последние 4 символов номера счета.
    :param for_test:
    :param user_account_number_input: Вводимый номер счета.
    :return: Вывод отформатированной строки номера счета.
    """
    log = get_logger(for_test=for_test)
    # Удаляем все нецифровые символы
    digits = ""
    for char in user_account_number_input:
        if char.isdigit():
            digits += char

    # Проверяем длину
    if len(digits) != 20:
        log.error(f"Ошибка: Номер счета должен содержать ровно 20 цифр. "
                 f"Введено: {user_account_number_input}")
        raise ValueError(
            f"Номер счета должен содержать ровно 20 цифр, но содержит: {len(digits)}. "
            f"Входное значение: {digits if digits else 'пустая строка'}")

    # Создаем маску: ** + последние 4 цифры
    masked = "**" + digits[-4:]
    log.info(f"Вводные данные: {user_account_number_input} Вывод: {masked}")
    return masked


# if __name__ == "__main__":
    print(get_mask_account(input("Ввод номера счета: ")))
