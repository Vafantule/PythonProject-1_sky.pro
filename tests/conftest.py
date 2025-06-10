

import pytest


@pytest.fixture
def empty_string() -> str:
    return ""


# Фикстура для предоставления тестовых данных
@pytest.fixture
def valid_card_numbers() -> list:
    return [
        ("123456789012", "123 4** *** 012"),  # 12 символов
        ("7000792289606361", "7000 79** **** 6361"),  # 16 символов
        ("1234567890123456789", "1234 56** ******* 6789"),  # 19 символов
    ]


# Фикстура для корректных входных данных
@pytest.fixture
def valid_account_numbers() -> list:
    return [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("99999999999999999999", "**9999"),
        ("00000000000000000001", "**0001"),  # Строка с ведущими нулями
    ]


# Блок фикстур для тестов 'transaction_descriptions'
@pytest.fixture
def description_sample() -> list:
    return [
        {"description": "Перевод организации"},
        {"description": ""},
        {},
        {"description": "Перевод с карты на карту"},
        {"description": 123},
        {"description": None},
        {"description": ["что-то для теста"]},
        "не словарь",
        42,
        ["список"],
    ]


# Блок фикстур для тестов 'card_number_generator'
@pytest.fixture
def small_range() -> tuple[int, int]:
    return 1, 10


@pytest.fixture
def large_range() -> tuple[int, int]:
    return 1, 1000


@pytest.fixture
def empty_range() -> tuple[int, int]:
    return 100, 99


@pytest.fixture
def transactions() -> list:
    return [
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


@pytest.fixture
def transactions_for_search() -> list:
    return [
        {'id': 3976154.0, 'state': 'CANCELED', 'date': '2021-04-20T21:42:09Z', 'amount': 29376.0,
         'currency_name': 'Franc', 'currency_code': 'CDF', 'from': 'Discover 8636221246947113',
         'to': 'Discover 6047704891392748', 'description': 'Перевод с карты на карту'},
        {'id': 2396779.0, 'state': 'CANCELED', 'date': '2022-10-31T10:13:09Z', 'amount': 23032.0,
         'currency_name': 'Cedi', 'currency_code': 'GHS', 'from': 'Visa 2641084763468257',
         'to': 'Mastercard 4387921060349959', 'description': 'Перевод с карты на карту'},
        {'id': 3469012.0, 'state': 'CANCELED', 'date': '2020-12-09T10:23:16Z', 'amount': 12054.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'American Express 4199438264025417',
         'to': 'American Express 9712913133684625', 'description': 'Перевод с карты на карту'},
        {'id': 3310022.0, 'state': 'CANCELED', 'date': '2023-02-02T13:47:42Z', 'amount': 16038.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa4627120922876722',
         'to': 'Mastercard 1972621796388911', 'description': 'Перевод с карты на карту'},
        {'id': 476353.0, 'state': 'CANCELED', 'date': '2022-05-30T13:46:38Z', 'amount': 14168.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa 8422480077696066',
         'to': 'Mastercard 1458590505547240', 'description': 'Перевод с карты на карту'},
        {'id': 151337.0, 'state': 'CANCELED', 'date': '2020-10-28T07:47:54Z', 'amount': 30324.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'Visa 2858643810193921',
         'to': 'Счет 73049787529893930779', 'description': 'Перевод организации'},
        {'id': 1590900.0, 'state': 'CANCELED', 'date': '2020-02-19T08:06:07Z', 'amount': 26493.0,
         'currency_name': 'Yuan Renminbi', 'currency_code': 'CNY', 'from': 'American Express 3307595602334148',
         'to': 'Mastercard 2435250807815654', 'description': 'Перевод с карты на карту'},
        {'id': 134341.0, 'state': 'CANCELED', 'date': '2022-03-03T08:41:08Z', 'amount': 13642.0,
         'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Visa 9770850749183268',
         'to': 'American Express 0522499169905654', 'description': 'Перевод с карты на карту'},
    ]
