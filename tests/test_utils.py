import json
import pytest
from typing import List, Dict, Any
from unittest.mock import patch, mock_open
from src.utils import load_transactions


@pytest.fixture
def valid_transactions() -> List[Dict[str, Any]]:
    """
    Возвращает корректные тестовые транзакции. Фикстура.
    :return:
    """
    return [
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {"amount": "97853.86", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на счет",
            "from": "Maestro 1308795367077170",
            "to": "Счет 96527012349577388612"
        },
        {
            "id": 207126257,
            "state": "EXECUTED",
            "date": "2019-07-15T11:47:40.496961",
            "operationAmount": {"amount": "92688.46", "currency": {"name": "USD", "code": "USD"}},
            "description": "Открытие вклада",
            "from": "Visa 1308795367077170",
            "to": "Счет 35737585785074382265"
        }
    ]


@pytest.fixture
def invalid_transactions() -> List[Any]:
    """
    Возвращает некорректные тестовые транзакции. Фикстура.
    :return:
    """
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2022-01-01T12:00:00",
            "operationAmount": {"amount": "100", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Test 1",
            "from": "Card 1",
            "to": "Account 1"
        },
        {
            "id": 2,
            "date": "2022-02-01T12:00:00",  # Нет 'state'
            "operationAmount": {"amount": "200", "currency": {"name": "USD", "code": "USD"}},
            "description": "Test 2",
            "from": "Card 2",
            "to": "Account 2"
        },
        "not_a_dict",  # Не словарь
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2022-03-01T12:00:00",
            "operationAmount": {"amount": "300", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Test 3",
            "to": "Account 3"  # Нет 'from'
        }
    ]


@pytest.mark.parametrize(
    "mock_data, required_keys, expected",
    [
        # Корректные транзакции
        ("valid_data", ["id", "state", "date", "operationAmount", "description", "from", "to"], 2),
        # Частично некорректные транзакции
        ("invalid_data", ["id", "state", "date", "operationAmount", "description", "from", "to"], 1),
        # Отсутствуют обязательные ключи
        ("invalid_data", ["не_существует"], 0),
        # Обязательные ключи=None
        ("invalid_data", None, 3),
    ]
)
def test_load_transactions(
        mock_data: List[Any],
        required_keys: List[str],
        expected: int,
        valid_transactions: List[str],
        invalid_transactions: List[str]
) -> None:
    """
    Проверка загрузки корректных транзакций. Тестирование.
    :param mock_data: Ключ для выбора тестовых данных.
    :param required_keys: Список обязательных ключей.
    :param expected: Ожидаемое количество валидных транзакций.
    :assert:
    """
    data = valid_transactions if mock_data == "valid_data" else invalid_transactions
    test_file = json.dumps(data, ensure_ascii=False)
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=test_file))
    ):
        result = load_transactions("fake.json", required_keys=required_keys)
        assert isinstance(result, list)
        assert len(result) == expected


def test_load_transactions_empty_file() -> None:
    """
    Проверка, возвращаемого пустого списка, при пустом входном файле. Тестирование.
    :assert:
    """
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="[]"))
    ):
        result = load_transactions("fake.json", required_keys=["id"])
        assert result == []


def test_load_transactions_not_found_file() -> None:
    """
    Проверка, возвращаемого пустого списка, при отсутствии входного файла. Тестирование.
    :assert:
    """
    with patch("os.path.exists", return_value=False):
        result = load_transactions("nonexistent.json")
        assert result == []


def test_load_transactions_json_invalid() -> None:
    """
    Проверка, возвращаемого пустого списка, при не корректных данных в файле. Тестирование.
    :assert:
    """
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data="не json"))
    ):
        result = load_transactions("fake.json")
        assert result == []


def test_load_transactions_json_not_list() -> None:
    """
    Проверка, что при JSON не-списке возбуждается TypeError. Тестирование.
    :return:
    """
    with (
        patch("os.path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=json.dumps({"a": 1})))
    ):
        with pytest.raises(TypeError):
            load_transactions("fake.json")
