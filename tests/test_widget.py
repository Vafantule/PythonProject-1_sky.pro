import pytest

from src.widget import get_date, mask_account_card

# from src.masks import get_mask_account, get_mask_card_number


# Блок тестирования 'mask_account_card'
wrong_card_account_number = "Номер некорректный"
# @pytest.fixture
# def mask_card():
#     return [
#         ("Счет 64686473678894779589", "Счет **9589"),
#         ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
#         ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
#         ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353")
#     ]


@pytest.mark.parametrize("value, expected", [
    ("Счет 64686473678894779589", "Счет **9589"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
])
def test_mask_account_card(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected


def test_mask_account_card_empty() -> None:
    with pytest.raises(TypeError):
        mask_account_card()


@pytest.mark.parametrize("value, expected", [
    ("", wrong_card_account_number),
    ("Карта 9876543210", wrong_card_account_number),
    ("Счет 9876543210", wrong_card_account_number),
    ("64686473678894779589", wrong_card_account_number),
    ("4658300734726758", wrong_card_account_number),
    ("Не цифровые символы", wrong_card_account_number),
    ("Visa Gold 5999 414228426353", wrong_card_account_number),
    ("Счет 6468647367889477 9589", wrong_card_account_number),
])
def test_mask_account_card_wrong(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected


# Блок тестирования 'get_date'
def test_get_date_valid_format() -> None:
    """
    Тестирование функции get_date с корректным форматом входных данных.
    """
    input_data = "2023-10-05T14:48:00.123456"
    expected_output = "05.10.2023"

    result = get_date(input_data)
    assert result == expected_output, f"Ожидалось {expected_output}, но получено {result}"


def test_get_date_invalid_format() -> None:
    """
    Тестирование функции get_date с некорректным форматом входных данных.
    Проверяем, что возникает ValueError при неправильном формате.
    """
    invalid_input = "2023/10/05 14:48:00"

    with pytest.raises(ValueError):
        get_date(invalid_input)


def test_get_date_edge_cases() -> None:
    """
    Тестирование граничных случаев, таких как начало и конец года.
    """
    # Начало года
    input_data_1 = "2023-01-01T00:00:00.000000"
    expected_output_1 = "01.01.2023"

    # Конец года
    input_data_2 = "2023-12-31T23:59:59.999999"
    expected_output_2 = "31.12.2023"

    assert get_date(input_data_1) == expected_output_1
    assert get_date(input_data_2) == expected_output_2
