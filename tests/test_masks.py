import pytest

from src.masks import get_mask_account, get_mask_card_number

# Блок тестирования номера карты.

# Тест с использованием фикстуры
def test_valid_card_numbers_with_fixture(valid_card_numbers):
    for input_number, expected in valid_card_numbers:
        assert get_mask_card_number(input_number) == expected


# Тест для корректных номеров с параметризацией
@pytest.mark.parametrize("input_number, expected", [
    ("123456789012", "123 4** *** 012"),  # 12 символов
    ("7000792289606361", "7000 79** **** 6361"),  # 16 символов
    ("1234567890123456789", "1234 56** ******* 6789"),  # 19 символов
    ("123-456-789 012", "123 4** *** 012"),  # С пробелами и дефисами
    ("7000-7922-abc-6361", "700 0** *** 361"),  # С буквами
    ("1234!5678@9012#3456$789", "1234 56** ******* 6789"),  # Со спецсимволами
])
def test_valid_card_numbers(input_number, expected):
    assert get_mask_card_number(input_number) == expected


# Тест для некорректных номеров с параметризацией
@pytest.mark.parametrize("input_number", [
    "123456789",  # Слишком короткий (9 символов)
    "12345678901234567890",  # Слишком длинный (20 символов)
    "abc-xyz",  # Только буквы (0 символов после очистки)
    "",  # Пустая строка
])
def test_invalid_card_numbers(input_number):
    with pytest.raises(ValueError, match="Ошибка: Длина номера карты должна быть от 12 до 19 символов."):
        get_mask_card_number(input_number)


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
