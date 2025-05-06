import  pytest
from src.widget import get_date, mask_account_card
# from src.masks import get_mask_account, get_mask_card_number


## Блок тестирования 'get_date'
def test_get_date_valid_format():
    """
    Тестирование функции get_date с корректным форматом входных данных.
    """
    input_data = "2023-10-05T14:48:00.123456"
    expected_output = "05.10.2023"

    result = get_date(input_data)
    assert result == expected_output, f"Ожидалось {expected_output}, но получено {result}"


def test_get_date_invalid_format():
    """
    Тестирование функции get_date с некорректным форматом входных данных.
    Проверяем, что возникает ValueError при неправильном формате.
    """
    invalid_input = "2023/10/05 14:48:00"

    with pytest.raises(ValueError):
        get_date(invalid_input)


def test_get_date_edge_cases():
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
