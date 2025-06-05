from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from src.search import count_transactions_by_category, transaction_search


# Блок тестирования поиска с помощью регулярных выражений.

@pytest.mark.parametrize(
    "search_string,expected",
    [
        ("Franc", [3976154.0]),
        ("CDF", [3976154.0]),
        ("Cedi", [2396779.0]),
        ("GHS", [2396779.0]),
        ("Yuan", [3469012.0, 3310022.0, 476353.0, 151337.0, 1590900.0]),
        ("CNY", [3469012.0, 3310022.0, 476353.0, 151337.0, 1590900.0]),
        ("Peso", [134341.0]),
        ("COP", [134341.0]),
        ("CANCELED", [3976154.0, 2396779.0, 3469012.0, 3310022.0, 476353.0, 151337.0, 1590900.0, 134341.0]),
        ("2022-10-31", [2396779.0]),
        ("Visa", [2396779.0, 3310022.0, 476353.0, 151337.0, 134341.0]),
        ("Discover", [3976154.0]),
        ("Mastercard", [2396779.0, 3310022.0, 476353.0, 1590900.0]),
        ("American Express", [3469012.0, 1590900.0, 134341.0]),
        ("Перевод организации", [151337.0]),
        ("Перевод с карты на карту", [3976154.0, 2396779.0, 3469012.0, 3310022.0, 476353.0, 1590900.0, 134341.0]),
        ("", [3976154.0, 2396779.0, 3469012.0, 3310022.0, 476353.0, 151337.0, 1590900.0, 134341.0]),
        ("нет совпадений", []),
        ("9712913133684625", [3469012.0]),
        ("30324.0", [151337.0]),
    ]
)
def test_transaction_search(
        transactions_for_search: List[Dict[str, Any]],
        search_string: str,
        expected: List[float]
) -> None:
    result = transaction_search(transactions_for_search, search_string)
    result_ids = [transaction["id"] for transaction in result]
    assert result_ids == expected


def test_transaction_search_any_field_case_insensitive(transactions_for_search: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions_for_search, "Franc")
    assert set(transaction["id"] for transaction in result) == {3976154.0}


def test_transaction_search_any_field_partial_match(transactions_for_search: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions_for_search, "Mastercard")
    assert set(transaction["id"] for transaction in result) == {2396779.0, 3310022.0, 476353.0, 1590900.0}


def test_transaction_search_any_field_empty_transactions() -> None:
    result = transaction_search([], "any")
    assert result == []


def test_transaction_search_any_field_nested_dict(transactions_for_search: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions_for_search, "6047704891392748")
    assert set(transaction["id"] for transaction in result) == {3976154.0}


def test_transaction_search_any_with_patch() -> None:
    with patch("src.search.re.compile") as mock_compile:
        mock_pattern = Mock()
        mock_pattern.search.side_effect = lambda value: value == "special"
        mock_compile.return_value = mock_pattern
        fake_transactions = [
            {'id': 10, 'description': 'special', 'amount': 0},
            {'id': 20, 'description': 'other', 'amount': 0},
        ]
        result = transaction_search(fake_transactions, "special")
        assert result == [fake_transactions[0]]
        mock_compile.assert_called()


# Блок тестирования подсчета категорий.

@pytest.mark.parametrize(
    "categories, expected",
    [
        (
            ["Перевод с карты на карту", "Перевод организации"],
            {
                "Перевод с карты на карту": 7,
                "Перевод организации": 1,
            }
        ),
        (
            ["Franc", "Cedi", "Yuan Renminbi", "Peso"],
            {
                "Franc": 1,
                "Cedi": 1,
                "Yuan Renminbi": 5,
                "Peso": 1,
            }
        ),
        (
            ["CANCELED", "Visa 2858643810193921", "Счет 73049787529893930779"],
            {
                "CANCELED": 8,                         # Все транзакции имеют state CANCELED
                "Visa 2858643810193921": 1,            # from
                "Счет 73049787529893930779": 1,        # to
            }
        ),
    ]
)
def test_count_transactions_by_category(
        transactions_for_search: List[Dict[str, str]],
        categories: List[str],
        expected: Dict[str, int]
) -> None:
    result = count_transactions_by_category(transactions_for_search, categories)
    assert result == expected


def test_count_transactions_by_category_empty(transactions_for_search: List[Dict[str, str]]) -> None:
    caterories: List[str] = []
    expected: Dict[str, int] = {}
    result = count_transactions_by_category(transactions_for_search, caterories)
    assert result == expected


def test_count_transactions_by_category_no_matches(transactions_for_search: List[Dict[str, str]]) -> None:
    categories = ["Совпадений не найдено"]
    expected = {"Совпадений не найдено": 0}
    result = count_transactions_by_category(transactions_for_search, categories)
    assert result == expected


def test_count_transactions_by_category_no_case_insensitive(transactions_for_search: List[Dict[str, str]]) -> None:
    categories = ["franc", "yuan renminbi", "peso"]
    result = count_transactions_by_category(transactions_for_search, categories)
    assert result["franc"] == 1
    assert result["yuan renminbi"] == 5
    assert result["peso"] == 1
