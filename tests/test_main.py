from typing import Any, Dict, List
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from src.main import lower_keys, main, print_transaction


@pytest.mark.parametrize("input_odj, expected", [
    ({"A": 1, "B": 2}, {"a": 1, "b": 2}),
    ({"A": {"B": 2}}, {"a": {"b": 2}}),
    ([{"A": 1}, {"B": 2}], [{"a": 1}, {"b": 2}]),
    ({"A": [{"B": 2}]}, {"a": [{"b": 2}]}),
    ("строка", "строка"),
    (99, 99)
])
def test_lower_keys(input_odj: Any, expected: Any) -> None:
    """

    :param input_odj:
    :param expected:
    """
    assert lower_keys(input_odj) == expected


@pytest.mark.parametrize(
    "transaction,expected",
    [
        (
            {
                "date": "2024-06-05T12:00:00",
                "description": "Описание для теста",
                "operation_amount": {"amount": 100, "currency": {"name": "RUB"}},
                "from": "1234567890123456",
                "to": "9876543210987654"
            },
            [
                "05.06.2024 Описание для теста",
                "123456******3456 -> 987654******7654",
                "Сумма: 100 RUB"
            ]
        ),
        (
            {
                "date": "2024-06-05T12:00:00",
                "description": "Описание отсутствует",
                "operation_amount": {"amount": 55, "currency": {"name": "USD"}},
                "from": "1234567890123456"
            },
            [
                "05.06.2024 Описание отсутствует",
                "123456******3456",
                "Сумма: 55 USD"
            ]
        ),
        (
            {
                "date": "2024-06-05T12:00:00",
                "description": "from/to отсутствуют",
                "amount": 42,
                "currency": "EUR"
            },
            [
                "05.06.2024 from/to отсутствуют",
                "Сумма: 42 EUR"
            ]
        ),
    ]
)
def test_print_transaction(transaction: Dict[str, Any], expected: List[str], capsys: CaptureFixture[str]
) -> None:
    with patch("src.main.mask_account_card",
               side_effect=lambda element: element[:6] + "******" + element[-4:]
               if len(element) >= 10 else ""):
        print_transaction(transaction)
        captured = capsys.readouterr()
        for line in expected:
            assert line in captured.out


def test_main_json() -> None:
    test_transactions = [
        {
            "date": "2024-06-05T12:00:00",
            "description": "описание",
            "operation_amount": {"amount": 1, "currency": {"name": "RUB"}},
            "from": "1234567890123456",
            "to": "9876543210987654",
            "state": "executed"
        }
    ]
    input_sequence = iter([
        "1",
        "executed",
        "нет",
        "нет",
        "нет"
    ])
    with (patch("builtins.input", side_effect=lambda _: next(input_sequence)),
          patch("src.main.load_transactions", return_value=test_transactions),
          patch("src.main.filter_by_state", side_effect=lambda transactions, state: transactions),
          patch("src.main.sort_by_date", side_effect=lambda transactions, reverse: transactions),
          patch("src.main.filter_by_currency", side_effect=lambda transactions, currency: transactions),
          patch("src.main.mask_account_card",
                side_effect=lambda element:
                element[:6] + "******" + element[-4:]if len(element) >= 10 else ""),
          patch("src.main.print_transaction") as mock_print_transaction,
          patch("builtins.print") as mock_print):
        main()
        mock_print_transaction.assert_called()
        found = any("Всего банковских операций в выборке: 1" in str(call) for call in mock_print.call_args_list)
        assert found
