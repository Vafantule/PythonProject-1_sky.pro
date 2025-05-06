import pytest

from src.masks import get_mask_account, get_mask_card_number

# Блок тестирования номера карты.
incorrect_number_card = "Номер карты не корректный. Просьба вводить только !! 16 !! цифр."


def test_get_mask_card_number(card_number: str) -> None:
    assert get_mask_card_number(card_number) == "4608 83** **** 5199"


@pytest.mark.parametrize("card, expected", [
    ("", incorrect_number_card),
    ("80123456", incorrect_number_card),
    ("59994142284263530123", incorrect_number_card),
    ("8990-9221-1366-5229", incorrect_number_card),
    ("Карта 6831982476737658", incorrect_number_card),
    ("номер карты", incorrect_number_card),
])
def test_get_mask_card_wrong_number(card: str, expected: str) -> None:
    assert get_mask_card_number(card) == expected


# Блок тестирования номера счета.
incorrect_number_account = "Номер счета не корректный. Просьба вводить только !! 20 !! цифр."


def test_get_mask_account(account_number: str) -> None:
    assert get_mask_account(account_number) == "**0123"


@pytest.mark.parametrize("account, expected", [
    ("", incorrect_number_account),
    ("0123456", incorrect_number_account),
    ("0159994142284263530123", incorrect_number_account),
    ("8990-9221-1366-5229", incorrect_number_account),
    ("номер карты", incorrect_number_account),
    ("Счет 7I5830O73472675895", incorrect_number_account),
])
def test_get_mask_wrong_account(account: str, expected: str) -> None:
    assert get_mask_account(account) == expected
