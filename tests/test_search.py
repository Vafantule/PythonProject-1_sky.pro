from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pytest

from src.search import transaction_search, count_transactions_by_category


# Блок тестирования поиска с помощью регулярных выражений.
@pytest.mark.parametrize("search_string, expected", [
    ("организации", [939719570, 594226727]),
    ("usd", [939719570, 142264268, 895315941]),
    ("руб.", [873106923, 594226727]),
    ("CANCELED", [594226727]),
    ("2019-03-23", [873106923]),
    ("Visa Classic", [895315941]),
    ("11776614605963066702", [939719570]),
    ("", [939719570, 142264268, 873106923, 895315941, 594226727]),
    ("нет совпадений", []),
    ("56883.54", [895315941]),
])
def test_transaction_search_any_field_parametrized(
        transactions: List[Dict[str, Any]],
        search_string: str,
        expected: List[int]
) -> None:
    result = transaction_search(transactions, search_string)
    result_ids = [transaction["id"] for transaction in result]
    assert result_ids == expected


def test_transaction_search_any_field_case_insensitive(transactions: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions, "usd")
    assert set(transaction["id"] for transaction in result) == {939719570, 142264268, 895315941}


def test_transaction_search_any_field_partial_match(transactions: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions, "организац")
    assert set(transaction["id"] for transaction in result) == {939719570, 594226727}


def test_transaction_search_any_field_empty_transactions() -> None:
    result = transaction_search([], "any")
    assert result == []


def test_transaction_search_any_field_nested_dict(transactions: List[Dict[str, Any]]) -> None:
    result = transaction_search(transactions, "RUB")
    assert set(transaction["id"] for transaction in result) == {873106923, 594226727}


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
