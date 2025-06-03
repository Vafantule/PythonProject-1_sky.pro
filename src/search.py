import re
from typing import Any, Dict, List


def transaction_search(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Поиск банковских операций по строке поиска среди всех значений всех ключей в каждом словаре. Функция.
    :param transactions: Список транзакций для обработки.
    :param search_string: Строка для поиска.
    :return: Найденная транзакция по строке поиска.
    """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [
        transaction for transaction in transactions
        if any(pattern.search(str(value)) for value in transaction.values())
    ]


# if __name__ == "__main__":
#     transactions = [
#         {'id': 3976154.0, 'state': 'CANCELED', 'date': '2021-04-20T21:42:09Z', 'amount': 29376.0,
#         'currency_name': 'Franc', 'currency_code': 'CDF', 'from': 'Discover 8636221246947113',
#         'to': 'Discover 6047704891392748', 'description': 'Перевод с карты на карту'},
#         {'id': 2396779.0, 'state': 'CANCELED', 'date': '2022-10-31T10:13:09Z', 'amount': 23032.0,
#         'currency_name': 'Cedi', 'currency_code': 'GHS', 'from': 'Visa 2641084763468257',
#         'to': 'Mastercard 4387921060349959', 'description': 'Перевод с карты на карту'},
#         {'id': 3469012.0, 'state': 'CANCELED', 'date': '2020-12-09T10:23:16Z', 'amount': 12054.0,
#         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'American Express 4199438264025417',
#         'to': 'American Express 9712913133684625', 'description': 'Перевод с карты на карту'},
#         {'id': 3310022.0, 'state': 'CANCELED', 'date': '2023-02-02T13:47:42Z', 'amount': 16038.0,
#         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa4627120922876722',
#         'to': 'Mastercard 1972621796388911', 'description': 'Перевод с карты на карту'},
#         {'id': 476353.0, 'state': 'CANCELED', 'date': '2022-05-30T13:46:38Z', 'amount': 14168.0,
#         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa 8422480077696066',
#         'to': 'Mastercard 1458590505547240', 'description': 'Перевод с карты на карту'},
#         {'id': 151337.0, 'state': 'CANCELED', 'date': '2020-10-28T07:47:54Z', 'amount': 30324.0,
#         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa 2858643810193921',
#         'to': 'Счет 73049787529893930779', 'description': 'Перевод организации'},
#         {'id': 1590900.0, 'state': 'CANCELED', 'date': '2020-02-19T08:06:07Z', 'amount': 26493.0,
#         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'American Express 3307595602334148',
#         'to': 'Mastercard 2435250807815654', 'description': 'Перевод с карты на карту'},
#         {'id': 134341.0, 'state': 'CANCELED', 'date': '2022-03-03T08:41:08Z', 'amount': 13642.0,
#         'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Visa 9770850749183268',
#         'to': 'American Express 0522499169905654', 'description': 'Перевод с карты на карту'},
#     ]
#
#     result = transaction_search(transactions, '2641084763468257')
#     print(result)
