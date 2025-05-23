from typing import Any, Dict
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import pytest
from requests import ConnectionError, HTTPError, Timeout, RequestException

from src.external_api import get_transaction_amount, get_api_key, get_exchange_rate


# Блок тестирования вывода валюты в рублях функции def get_transaction_amount()
@pytest.fixture
def transaction_rub() -> Dict[str, Any]:
    """

    :return:
    """
    return {
        "id": 200634844,
        "operationAmount": {"amount": "42210.20", "currency": {"name": "руб.", "code": "RUB"}}
    }


@pytest.fixture()
def transaction_usd() -> Dict[str, Any]:
    """

    :return:
    """
    return {
        "id": 879660146,
        "operationAmount": {"amount": "92130.50", "currency": {"name": "USD", "code": "USD"}}
    }


@pytest.fixture
def transaction_eur() -> Dict[str, Any]:
    """

    :return:
    """
    return {
        "id": 596914981,
        "operationAmount": {"amount": "65169.27", "currency": {"name": "EUR", "code": "EUR"}}
    }


@pytest.mark.parametrize("transaction, expected", [
    ({"operationAmount": {"amount": "81513.74", "currency": {"name": "руб.", "code": "RUB"}}}, 81513.74),
    ({"operationAmount": {"amount": "0", "currency": {"code": "RUB"}}}, 0.0),
])
def test_transaction_rub(transaction: Dict[str, Any], expected: float) -> None:
    """

    :param transaction:
    :param expected:
    :return:
    """
    result = get_transaction_amount(transaction)
    assert result == expected


@patch("src.external_api.get_api_key", return_value="testkey")
@patch("src.external_api.get_exchange_rate")
@pytest.mark.parametrize("transaction, rate, expected", [
    ({"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}, 90.0, 9000.00),
    ({"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}, 100.0, 5000.00),
    ({"operationAmount": {"amount": "1.00", "currency": {"code": "USD"}}}, 75.5, 75.5),
    ({"operationAmount": {"amount": "0.00", "currency": {"code": "EUR"}}}, 100.0, 0.0),
])
def test_foreign_currency_transaction(
        mock_get_exchange_rate: Mock,
        mock_get_api_key: Mock,
        transaction: Dict[str, Any],
        rate: float,
        expected: float,
) -> None:
    """

    :param mock_get_exchange_rate:
    :param transaction:
    :param rate:
    :param expected:
    :return:
    """
    mock_get_exchange_rate.return_value = rate
    result = get_transaction_amount(transaction)
    assert result == expected


@patch("src.external_api.get_api_key", return_value="testkey")
@patch("src.external_api.get_exchange_rate")
def test_api_exceptions(
        mock_get_exchange_rate: Mock,
        mock_get_api_key: Mock,
        transaction_usd: Dict[str, Any]
) -> None:
    """

    :param mock_get_exchange_rate:
    :param mock_get_api_key:
    :param transaction_usd:
    :return:
    """
    from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

    for exc in [ConnectionError, HTTPError, Timeout, RequestException]:
        mock_get_exchange_rate.side_effect = exc("mocked error")
        assert get_transaction_amount(transaction_usd) == 0.0


def test_currency_unsupported() -> None:
    """

    :return:
    """
    transaction = {"operationAmount": {"amount": "10.00", "currency": {"code": "XYZ"}}}
    with pytest.raises(ValueError):
        get_transaction_amount(transaction)


@patch("src.external_api.open")
@patch("json.load")
def test_read_from_file(
        mock_json_load: Mock,
        mock_open: Mock,
        transaction_rub: Dict[str, Any]
) -> None:
    """

    :param mock_json_load:
    :param mock_open:
    :param transaction_rub:
    :return:
    """
    mock_json_load.return_value = transaction_rub
    result = get_transaction_amount("fake_file.json")   # type: ignore
    assert result == 42210.20


# Блок тестирования запроса API функции def get_api_key()
@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_get_api_key_found(mock_load_dotenv: Mock, mock_getenv: Mock) -> None:
    """

    :param mock_load_dotenv:
    :param mock_getenv:
    :return:
    """
    mock_getenv.return_value = "TEST_KEY"
    assert get_api_key() == "TEST_KEY"
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_with("EXCHANGE_RATES_API_KEY", "")


@patch("src.external_api.os.getenv")
@patch("src.external_api.load_dotenv")
def test_get_api_key_not_found(mock_load_dotenv: Mock, mock_getenv: Mock) -> None:
    """

    :param mock_load_dotenv:
    :param mock_getenv:
    :return:
    """
    mock_getenv.return_value = ""
    with pytest.raises(ValueError, match="Ключ EXCHANGE_RATES_API_KEY не найдет в .env файле."):
        get_api_key()
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_with("EXCHANGE_RATES_API_KEY", "")


# Блок тестирования курса валюты функции def get_exchange_rate()
@patch("requests.get")
def test_get_exchange_rate_success(mock_get: Mock) -> None:
    """

    :param mock_get:
    :return:
    """
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"rates": {"RUB": 99.99}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD", "RUB", "some_key")
    assert rate == 99.99


@patch("requests.get")
def test_get_exchange_rate_not_found(mock_get: Mock) -> None:
    """

    :param mock_get:
    :return:
    """
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"rates": {"EUR": 1.12}}
    mock_get.return_value = mock_response

    with pytest.raises(KeyError):
        get_exchange_rate("USD", "RUB", "some_key")


@patch("requests.get")
@pytest.mark.parametrize("exc", [
    ConnectionError("ConnectionError"),
    HTTPError("HTTPError"),
    Timeout("Timeout"),
    RequestException("RequestException")
])
def test_get_exchange_rate_not_requests_exceptions(mock_get: Mock, exc: Exception):
    """

    :param mock_get:
    :param exc:
    :return:
    """
    mock_get.side_effect = exc
    with pytest.raises(type(exc)):
        get_exchange_rate("USD", "RUB", "some_key")
