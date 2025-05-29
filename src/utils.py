import json
import logging
import os
import os.path
from typing import Any, Dict, List, Optional


LOG_DIR = "logs"


def get_logger(name: Optional[str] = None, log_file: Optional[str] = None) -> logging.Logger:
    """
    Ленивая инициализация логгера. Функция.
    :param name: Имя файла с логами.
    :param log_file: Файл для записи логов.
    :return:
    """
    if name is None:
        name = __name__
    logger = logging.getLogger(LOG_DIR)
    if not logger.handlers:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        if log_file is None:
            try:
                current_file = os.path.abspath(__file__)
                # dir_name = os.path.basename(os.path.dirname(curl_file))
                module_name = os.path.splitext(os.path.basename(current_file))[0]
                log_name = f"{module_name}.log"
            except Exception:
                log_name = f"{name}.log"
            log_file = os.path.join(LOG_DIR, log_name)
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logger


def load_transactions(
        path: str,
        required_keys: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None
) -> List[Dict[str, Any]]:
    """
    Получение списка финансовых транзакций из файла JSON. Функция.
    :param logger:
    :param path: Путь до файла с данными.
    :param required_keys: Ключи списка транзакций.
    :return: Список словарей с данными о финансовых транзакциях.
    """
    if logger is None:
        logger = get_logger()
    if not os.path.exists(path):
        logger.warning(f"!!! Файл для чтения данных не найден: {path} !!!")
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as error:
                logger.error(f"Ошибка JSON файла: {error}")
                return []

            if not data:
                logger.error(f"{path} не содержит данных для обработки.")
                return []

            if not isinstance(data, list):
                logger.error(f"Данные в {path} не в формате JSON.")
                raise TypeError(f"Данные в {path} не в формате JSON.")

            transactions_valid = []
            for element in data:
                if not isinstance(element, dict):
                    logger.warning("Элемент не является словарём и будет исключён из обработки.")
                    continue
                if required_keys:
                    # if required_keys is not None:
                    if not all(key in element for key in required_keys):
                        # logger.warning(f"Транзакция пропущена. Отсутствуют обязательные ключи: {element}")
                        continue
                transactions_valid.append(element)

            logger.info(f"Получен список словарей с данными "
                        f"о финансовых транзакциях из файла {path}: ")
            return transactions_valid

    except (TypeError, KeyError, ValueError) as error:
        logger.error(f"Ошибка выполнения запроса: {error}")
        raise error


# if __name__ == "__main__":
    keys = ["id", "state", "date", "operationAmount", "description", "from", "to"]
    transactions = load_transactions("data/operations.json", required_keys=keys)
    for transaction in transactions:
        # print(json.dumps(transaction, indent=2, ensure_ascii=False))
        pass
