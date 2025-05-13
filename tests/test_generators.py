import pytest
# import re

from typing import Any, Dict, List, Optional, Iterator

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Блок тестирование функции отбора по валюте.
@pytest.mark.parametrize("currency_code, expected", [
    ("USD", 3),
    ("RUB", 2),
    ("EUR", 0)
])
def test_filter_by_currency(transactions: List[Dict[str, Any]],
                            currency_code: str,
                            expected: str) -> None:
    assert len(list(filter_by_currency(transactions, currency_code))) == expected
    for transaction in list(filter_by_currency(transactions, currency_code)):
        assert transaction.setdefault("operationAmount",
                                      {}).setdefault("currency",
                                                     {}).setdefault("code") == currency_code


def test_filter_by_currency_empty_list() -> None:
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_no_currency(transactions: List[Dict[str, Any]]) -> None:
    assert list(filter_by_currency(transactions, "EUR")) == []


# Блок тестирование функции вывода описания операций.
def test_transaction_descriptions(description_sample: List[Dict[str, Optional[Any]]]) -> None:
    """
    Тестирование функции с заданными фикстурами.
    :param description_sample:
    :assert:
    """
    result = list(transaction_descriptions(description_sample))
    expected = [
        "Перевод организации",
        "Нет необходимого словаря.",
        "Нет необходимого словаря.",
        "Перевод с карты на карту",
        "Нет необходимого словаря.",
        "Нет необходимого словаря.",
        "Нет необходимого словаря.",
    ]
    assert result == expected


@pytest.mark.parametrize("description, expected", [
    ([{"description": "Тест"}], ["Тест"]),
    ([{"description": ""}], ["Нет необходимого словаря."]),
    ([{}], ["Нет необходимого словаря."]),
    ([], []),
    ([{"description": 123}], ["Нет необходимого словаря."]),
    ([{"description": None}], ["Нет необходимого словаря."]),
    ([{"description": ["test"]}], ["Нет необходимого словаря."]),
    ([{"description": "Первый"}, "not a dict",
        {"description": ""}], ["Первый", "Нет необходимого словаря."]),
    (
        [
            {"description": "Начало"},
            {"description": ""},
            {},
            {"description": 123},
            {"description": None},
            "not a dict",
            {"description": "Окончание"},
        ],
        [
            "Начало",
            "Нет необходимого словаря.",
            "Нет необходимого словаря.",
            "Нет необходимого словаря.",
            "Нет необходимого словаря.",
            "Окончание",
        ],
    ),
])
def test_transaction_descriptions_with_parameterize(description: List[Dict[str, Optional[Any]]],
                                                    expected: List[str]) -> None:
    """
    Тестирование функции с параметризацией.
    :param description: Вводный словарь для тестирования.
    :param expected: Ожидаемый результат.
    :assert:
    """
    assert list(transaction_descriptions(description)) == expected


def test_transaction_descriptions_iterator_type(description_sample: List[Dict[str, Optional[Any]]]) -> None:
    """
    Тестирование функции на соответствие типов.
    :param description_sample: Фикстуры.
    :assert:
    """
    assert isinstance(transaction_descriptions(description_sample), Iterator)


# Блок тестирование функции генерации номера карты.
@pytest.mark.parametrize("start, end, expected", [
    (1, 4, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004"
    ]),
    (9999999999999998, 9999999999999999, [
        "9999 9999 9999 9998", "9999 9999 9999 9999"]),
])
def test_card_number_generator(start: int, end: int, expected: int) -> None:
    """
    Тестирование генератора на правильное формирование номера. Функция теста.
    :param start: Начальное значение.
    :param end: Конечное значение.
    :param expected: Ожидаемый номер карты.
    :assert:
    """
    result = list(card_number_generator(start, end))
    assert result == expected, f"Ожидались номера {expected}, получено {result}"


def test_card_number_generator_format(small_range: tuple[int, int]) -> None:
    """
    Тестирование, что итоговый номер карты имеет корректный формат. Функция теста.
    :param small_range: Диапазон карт.
    :assert:
    """
    start, end = small_range
    for card_number in card_number_generator(start, end):
        assert len(card_number) == 19   # Общая длина номера.
        assert card_number.count(" ") == 3
        assert card_number.replace(" ", "").isdigit()


def test_card_number_generator_edge_cases() -> None:
    """
    Тестирование генератора проверки начального либо конечного номера. Функция теста.
    :assert:
    """
    # Минимальный диапазон
    result = list(card_number_generator(0, 0))
    assert result == ["0000 0000 0000 0000"], "Ошибка при генерации минимального номера"

    # Максимальный диапазон
    result = list(card_number_generator(9999999999999999, 9999999999999999))
    assert result == ["9999 9999 9999 9999"], "Ошибка при генерации максимального номера"

    # Одно значение
    result = list(card_number_generator(1, 1))
    assert result == ["0000 0000 0000 0001"], "Ошибка при генерации одного номера"


def test_card_number_generator_negative_start() -> None:
    """
    Тестирование генератора, при значении start меньше 0. Функция теста.
    :return: Возврат сообщения с ошибкой.
    """
    with pytest.raises(ValueError, match="Начальное число не может быть меньше или равно 0"):
        list(card_number_generator(-1, 10))


def test_card_number_generator_start_greater_than_end() -> None:
    """
    Тестирование генератора, при значении start меньше end. Функция теста.
    :return: Возврат сообщения с ошибкой.
    """
    with pytest.raises(ValueError, match="Начальный номер должен быть меньше или равен конечному"):
        list(card_number_generator(10, 5))


def test_card_number_generator_maximum() -> None:
    """
    Тестирование генератора, на выходящий за границы индекс. Функция теста.
    :return: Возврат сообщения с ошибкой.
    """
    with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 0 до 9999999999999999"):
        list(card_number_generator(10000000000000000, 10000000000000001))


@pytest.mark.parametrize("start, end", [
    (0, 5),
    (1000, 1005),
    (9999999999999990, 9999999999999995),
])
def test_complete_generation(start: int, end: int) -> None:
    """
    Тестирование генерации номеров в диапазоне. Функция теста.
    :param start: Начальное значение.
    :param end: Конечное значение.
    :assert:
    """
    result = list(card_number_generator(start, end))
    expected_count = end - start + 1
    assert len(result) == expected_count, f"Ожидалось {expected_count} номеров, получено {len(result)}"


def test_card_number_generator_range(large_range: tuple[int, int]) -> None:
    """
    Тестирование производительности с большим набором номеров карт. Функция теста.
    :param large_range: Диапазон карт.
    :assert:
    """
    start, end = large_range
    count = sum(1 for _ in card_number_generator(start, end) if _ and sum(1 for _ in range(1000)))
    assert count == 1000
