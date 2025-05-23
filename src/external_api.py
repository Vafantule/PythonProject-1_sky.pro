import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout


def get_api_key() -> str:
    """
    Загрузка API ключа из .env файла. Функция.
    :return:
    """
    load_dotenv()
    api_key = os.getenv("EXCHANGE_RATES_API_KEY", "")
    if not api_key:
        raise ValueError("Ключ EXCHANGE_RATES_API_KEY не найдет в .env файле.")
    return api_key


def get_exchange_rate(from_currency: str, to_currency: str, api_key: str) -> float:
    """
    Получение курса валюты с использованием Exchange Rates Data API. Функция.
    :param from_currency: Исходная валюта для конвертации.
    :param to_currency: Итоговая валюта для конвертации.
    :param api_key: API ключ для подключения к сайту.
    :return: Итоговый результат конвертации.
    """
    url = (
        f"https://api.apilayer.com/exchangerates_data/latest"
        f"?base={from_currency}&symbols={to_currency}"
    )
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"][to_currency]
        return float(rate)
    except ConnectionError as error:
        print(f"Ошибка подключения: {error}")
        raise
    except HTTPError as error:
        print(f"HTTP ошибка: {error}")
        raise
    except Timeout as error:
        print(f"Ошибка тайм-аута: {error}")
        raise
    except RequestException as error:
        print(f"Ошибка запроса: {error}")
        raise
    except Exception as error:
        print(f"Непредвиденная ошибка: {error}")
        raise


def get_transaction_amount(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    Если валюта не RUB, конвертирует через Exchange Rates Data API. Функция.
    :param transaction: Словарь с транзакцией либо путь к файлу с данными для обработки.
    :return:
    """
    # Возможное чтение данных из файла json.
    if isinstance(transaction, str):
        with open(transaction, "r", encoding="ut-8") as file:
            transaction = json.load(file)

    amount_str: str = transaction["operationAmount"]["amount"]
    currency_code: str = transaction["operationAmount"]["currency"]["code"].lower()
    amount: float = float(amount_str)

    if currency_code == "rub":
        return amount
    elif currency_code in ("usd", "eur"):
        api_key = get_api_key()
        try:
            rate = get_exchange_rate(currency_code.upper(), "RUB", api_key)
            return round(amount * rate, 2)
        except (ConnectionError, HTTPError, Timeout, RequestException):
            print("Ошибка получения курса валюты.")
            return 0.0
    else:
        raise ValueError(f"Не задана валюта: {currency_code}")


if __name__ == "__main__":
    # Чтение всех транзакций из файла
    # with open("data/operations.json", "r", encoding="utf-8") as f:
    #     operations = json.load(f)
    # for operation in operations:
    #     try:
    #         rub_amount = get_transaction_amount(operation)
    #         print(f"ID: {operation['id']}, сумма в RUB: {rub_amount}")
    #     except Exception as error:
    #         print(f"Ошибка при обработке транзакции {operation.get('id')}: {error}")

    rub_amount = get_transaction_amount({
        "id": 879660146,
        "state": "EXECUTED",
        "date": "2018-07-22T07:42:32.953324",
        "operationAmount": {
          "amount": "92130.50",
          "currency": {
            "name": "rub",
            "code": "usd"
          }
        },
        "description": "Перевод организации",
        "from": "Счет 19628854383215954147",
        "to": "Счет 90887717138446397473"
      })
    print(f"Сумма операции в валюте: {rub_amount}")
