from typing import Dict, List, Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number


# Блок тестирования номера карты.

# Тест с использованием фикстуры.
def test_valid_card_numbers_with_fixture(valid_card_numbers: List[Tuple[str, str]]) -> None:
    for input_number, expected in valid_card_numbers:
        assert get_mask_card_number(input_number, for_test=True) == expected


# Тест для корректных номеров с параметризацией
@pytest.mark.parametrize("input_number, expected", [
    ("123456789012", "123 4** *** 012"),  # 12 символов
    ("7000792289606361", "7000 79** **** 6361"),  # 16 символов
    ("1234567890123456789", "1234 56** ******* 6789"),  # 19 символов
    ("123-456-789 012", "123 4** *** 012"),  # С пробелами и дефисами
    ("7000-7922-abc-6361", "700 0** *** 361"),  # С буквами
    ("1234!5678@9012#3456$789", "1234 56** ******* 6789"),  # Со спецсимволами
])
def test_valid_card_numbers(input_number: str, expected: str) -> None:
    assert get_mask_card_number(input_number, for_test=True) == expected


# Тест для некорректных номеров с параметризацией
@pytest.mark.parametrize("input_number", [
    "123456789",  # Слишком короткий (9 символов)
    "12345678901234567890",  # Слишком длинный (20 символов)
    "abc-xyz",  # Только буквы (0 символов после очистки)
    "",  # Пустая строка
])
def test_invalid_card_numbers(input_number: str) -> None:
    with pytest.raises(ValueError,
                       match="Ошибка: Длина номера карты должна быть от 12 до 19 символов."):
        get_mask_card_number(input_number, for_test=True)


# Блок тестирования номера счета.

# Единая фикстура для всех тестовых данных с аннотацией
@pytest.fixture
def test_account_number() -> Dict[str, List[Tuple[str, str]]]:
    return {
        "invalid_lengths": [
            ("123.45", "Номер счета должен содержать ровно 20 цифр, но содержит: 5. "
                       "Входное значение: 12345"),
            ("123", "Номер счета должен содержать ровно 20 цифр, но содержит: 3. "
                    "Входное значение: 123"),
            ("123456789012345678901", "Номер счета должен содержать ровно 20 цифр, но содержит: 21. "
                                      "Входное значение: 123456789012345678901"),
            ("0123456789", "Номер счета должен содержать ровно 20 цифр, но содержит: 10. "
                           "Входное значение: 0123456789"),  # Тест из ошибки
            ("abc", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
                    "Входное значение: пустая строка"),
            ("...", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
                    "Входное значение: пустая строка"),
            ("", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
                 "Входное значение: пустая строка"),
            ("   ", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
                    "Входное значение: пустая строка"),
        ],
        "additional_scenarios": [
            ("-73654108430135874305", "**4305"),  # Отрицательное число как строка
            ("123abc01245678901234567890", "Номер счета должен содержать ровно 20 цифр, но содержит: 23. "
                                           "Входное значение: 12301245678901234567890"),  # Строка с цифрами и буквами
            ("100000000000000000000", "Номер счета должен содержать ровно 20 цифр, но содержит: 21. "
                                      "Входное значение: 100000000000000000000"),  # Очень большая строка
        ]
    }


# Тесты для корректного ввода
@pytest.mark.parametrize("input_number, expected", [
    ("73654108430135874305", "**4305"),
    ("12345678901234567890", "**7890"),
    ("99999999999999999999", "**9999"),
    ("00000000000000000001", "**0001"),
])
def test_valid_input(input_number: str, expected: str,
                     valid_account_numbers: List[Tuple[str, str]]) -> None:
    result: str = get_mask_account(input_number, for_test=True)
    assert result == expected
    # Проверяем, что данные из фикстуры соответствуют
    assert (input_number, expected) in valid_account_numbers


# Тесты для неверной длины
@pytest.mark.parametrize("input_value, error_message", [
    ("123.45", "Номер счета должен содержать ровно 20 цифр, но содержит: 5. "
               "Входное значение: 12345"),
    ("123", "Номер счета должен содержать ровно 20 цифр, но содержит: 3. "
            "Входное значение: 123"),
    ("123456789012345678901", "Номер счета должен содержать ровно 20 цифр, но содержит: 21. "
                              "Входное значение: 123456789012345678901"),
    ("0123456789", "Номер счета должен содержать ровно 20 цифр, но содержит: 10. "
                   "Входное значение: 0123456789"),
    ("abc", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
            "Входное значение: пустая строка"),
    ("...", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
            "Входное значение: пустая строка"),
    ("", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
         "Входное значение: пустая строка"),
    ("   ", "Номер счета должен содержать ровно 20 цифр, но содержит: 0. "
            "Входное значение: пустая строка"),
])
def test_invalid_length(input_value: str, error_message: str,
                        test_account_number: Dict[str, List[Tuple[str, str]]]) -> None:
    with pytest.raises(ValueError, match=error_message):
        get_mask_account(input_value, for_test=True)
    # Проверяем, что данные из фикстуры соответствуют
    assert (input_value, error_message) in test_account_number["invalid_lengths"]


# Тесты для дополнительных сценариев
@pytest.mark.parametrize("input_value, expected", [
    ("-73654108430135874305", "**4305"),
    ("123abc01245678901234567890", "Номер счета должен содержать ровно 20 цифр, но содержит: 23. "
                                   "Входное значение: 12301245678901234567890"),
    ("100000000000000000000", "Номер счета должен содержать ровно 20 цифр, но содержит: 21. "
                              "Входное значение: 100000000000000000000"),
], ids=["negative_number", "string_with_digits", "very_large_number"])
def test_additional_scenarios(input_value: str, expected: str,
                              test_account_number: Dict[str, List[Tuple[str, str]]]) -> None:
    if expected.startswith("Номер счета должен содержать ровно 20 цифр"):
        with pytest.raises(ValueError, match=expected):
            get_mask_account(input_value, for_test=True)
    else:
        result: str = get_mask_account(input_value, for_test=True)
        assert result == expected
    # Проверяем, что данные из фикстуры соответствуют
    assert (input_value, expected) in test_account_number["additional_scenarios"]
