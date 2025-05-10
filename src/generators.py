from typing import Any, Dict, List, Generator, Iterator, Optional

transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Generator[dict[str, Any], Any, None]:
    """
    Отбор данных по отобранной валюте. Функция.
    :param transactions: Данные для отбора.
    :param currency_code: Код валюты для отбора транзакций.
    :yield:
    """
    if not isinstance(transactions, list):
        raise ValueError("Ошибка. Необходимо предоставить список словарей.")
    if not all(isinstance(transaction, dict) for transaction in transactions):
        raise ValueError("Транзакции должны быть представлены в виде словаря.")

    for transaction in transactions:
        currency = transaction.setdefault("operationAmount").get("currency").get("code")
        if currency == currency_code:
            yield transaction


# Получить итератор для транзакций в валюте.
usd_transactions = filter_by_currency(transactions, "USD")
# while True:
# try:
#     for _ in range(6):
#         print(next(usd_transactions))
# except StopIteration:
#     print("Окончание итерации.")
    # break


def transaction_descriptions(transactions: List[Dict[str, Optional[Any]]]) -> Iterator[str]:
    """
    Вывод описания операций по транзакциям. Функция.
    :param transactions: Данные для отбора.
    :return:
    :param transactions:
    :return:
    """
    if not isinstance(transactions, list):
        raise TypeError("Просьба предоставить корректный тип данных.")
    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue
        description = transaction.setdefault("description", "Нет необходимого словаря.")
        if isinstance(description, str) and description:
            yield description
        else:
            yield "Нет необходимого словаря."


descriptions = transaction_descriptions(transactions)
# while True:
try:
    for _ in range(9):
        print(next(descriptions))
except StopIteration:
    print("Окончание итерации.")
    # break


def luna_check(card_number: str) -> bool:
    """
    Проверка номера карты по алгоритму Ханса Луна. Функция.
    :param card_number: Номер карты для анализа.
    :return: Итоговый результат.
    """
    # Номер карты в цифры.
    digits = [int(digit) for digit in card_number]
    checksum = 0
    # Формула Луна.
    reverse_digits = digits[::-1]
    for index, digit in enumerate(reverse_digits):
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def card_number_generator(start: int, end: int) -> Generator[str, Any, None]:
    """
    Генерация номера банковской карты 16 символов. Функция.
    :param start: Начальное значение номера карты.
    :param end: Конечное значение номера карты.
    :return: Отформатированный вывод номера карты.
    """
    if start < 0:
        raise ValueError("Начальное число не может быть меньше или равно 0.")

    if start > end:
        raise ValueError("Начальный номер должен быть меньше или равен конечному.")

    if not (0 <= start <= 9999999999999999 and 0 <= end <= 9999999999999999):
        raise ValueError("Номера карт должны быть в диапазоне от 0 до 9999999999999999.")

    for number in range(start, end + 1):
        card_number = f"{number:016}"
    # if luna_check(card_number):
        formatted_card_number = (f"{card_number[0:4]} {card_number[4:8]} "
                                 f"{card_number[8:12]} {card_number[12:16]}")
        yield formatted_card_number


# Вывод номера карты в выбранном диапазоне.
# for card_number in card_number_generator(1, 7):
#     print(card_number)
