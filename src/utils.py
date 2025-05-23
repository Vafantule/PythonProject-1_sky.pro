import json
import os.path
from typing import Any, Dict, List, Optional


def load_transactions(
        path: str,
        required_keys: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Получение списка финансовых транзакций из файла JSON. Функция.
    :param path: Путь до файла с данными.
    :param required_keys: Ключи списка транзакций.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return []

            if not data:
                return []

            if not isinstance(data, list):
                raise TypeError("Объект JSON не список")

            transactions_valid = []
            for element in data:
                if not isinstance(element, dict):
                    continue
                if required_keys:
                    if required_keys is not None:
                        if not all(key in element for key in required_keys):
                            continue
                transactions_valid.append(element)

            return transactions_valid

    except (TypeError, KeyError, ValueError) as error:
        raise error


# if __name__ == "__main__":
    keys = ["id", "state", "date", "operationAmount", "description", "from", "to"]
    transactions = load_transactions("data/operations.json", required_keys=keys)
    for transaction in transactions:
        print(json.dumps(transaction, indent=2, ensure_ascii=False))
