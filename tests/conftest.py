import builtins
import os
import tempfile
from typing import Any, Callable, Generator
from unittest.mock import MagicMock, patch

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
def temp_file() -> Generator[str, Any, None]:
    """
    Создание и удаление временных файлов для тестирования функций.
    :return:
    """
    temp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    temp.close()

    temp_dir = os.path.dirname(temp.name)
    for file in os.listdir(temp_dir):
        if file.startswith("mylog_") and file.endswith(".txt"):
            os.remove(os.path.join(temp_dir, file))

    yield temp.name

    if os.path.exists(temp.name):
        os.remove(temp.name)
    for file in os.listdir(temp_dir):
        if file.startswith("mylog_") and file.endswith(".txt"):
            os.remove(os.path.join(temp_dir, file))


@pytest.fixture
def mock_file_error(temp_file: str) -> Callable[[type, bool], MagicMock]:
    """
    Имитация ошибки записи в файл для temp_file
    :param temp_file: Временный файл.
    :return:
    """
    def create_mock(error_type: type, all_files: bool = False) -> MagicMock:
        """
        Создание имитации ошибки.
        :param all_files:
        :param error_type: Тип ошибки.
        :return:
        """
        real_open = builtins.open

        def mock_open(*args: Any, **kwargs: Any) -> Any:
            # if args and args[0] == temp_file:
            if args:
                if args[0] == temp_file or (all_files and 'mylog_' in
                                            args[0] and args[0].endswith('.txt')):
                    raise error_type("Ложная ошибка")
            return real_open(*args, **kwargs)
        return patch("builtins.open", side_effect=mock_open)
    return create_mock
