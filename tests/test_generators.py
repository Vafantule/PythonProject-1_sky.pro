import pytest

from typing import Any, Dict, List
from src.generators import filter_by_currency, card_number_generator


# Блок тестирование функции отбора по валюте.
@pytest.mark.parametrize("currency_code, expected", [
    ("USD", 3),
    ("RUB", 2),
    ("EUR", 0)
])
def test_filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str, expected: str) -> None:
    assert len(list(filter_by_currency(transactions, currency_code))) == expected
    for transaction in list(filter_by_currency(transactions, currency_code)):
        assert transaction.setdefault("operationAmount").get("currency").get("code") == currency_code


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_no_currency(transactions: List[Dict[str, Any]]) -> None:
    assert list(filter_by_currency(transactions, "EUR")) == []



# Блок тестирование функции генерации номера карты.
@pytest.mark.parametrize("start, end, expected", [
    (1, 4, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004"
    ])
])
def test_card_number_generator(start: int, end: int, expected: int) -> None:
    assert list(card_number_generator(start, end)) == expected


def test_card_number_generator_empty(empty_range: int) -> None:
    """
    Тестирование пустого диапазона номера карт. Функция теста.
    :param empty_range: Пустой диапазон карт.
    :assert:
    """
    start, end = empty_range
    assert list(card_number_generator(start, end)) == []


def test_card_number_generator_format(small_range: int) -> None:
    """
    Тестирование, что итоговый номер карты имеет корректный формат. Функция теста.
    :param small_range: Диапазон карт.
    :assert:
    """
    start, end = small_range
    for card_number in card_number_generator(start, end):
        assert len(card_number) == 19
        assert card_number.count(" ") == 3
        assert card_number.replace(" ", "").isdigit()


def test_card_number_generator_range(large_range: int) -> None:
    """
    Тестирование производительности с большим набором номеров карт. Функция теста.
    :param large_range: Диапазон карт.
    :assert:
    """
    start, end = large_range
    count = sum(1 for _ in card_number_generator(start, end) if _ and sum(1 for _ in range(1000)))
    assert count == 1000
